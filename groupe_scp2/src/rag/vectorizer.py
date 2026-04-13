"""
Vectorizer — Transforme les produits Kiprix en chunks et les vectorise.
Utilise sentence-transformers pour les embeddings (multilingue).
"""

import logging
import psycopg2
from psycopg2.extras import DictCursor
import os
from typing import List, Dict

from .rag_database import RAGDatabase


class KiprixVectorizer:
    """
    Convertit les produits de la table `produits` en embeddings
    stockés dans `produits_embeddings` via pgvector.
    """

    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.rag_db = RAGDatabase()
        self._model = None

    def _get_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self.logger.info(f"Chargement modèle : {self.EMBEDDING_MODEL}")
            self._model = SentenceTransformer(self.EMBEDDING_MODEL)
        return self._model

    def _product_to_chunk(self, product: dict) -> str:
        """Transforme un produit en texte descriptif pour l'embedding."""
        lines = [f"Produit : {product.get('name', '')}"]

        if product.get('territory_name'):
            lines.append(f"Territoire : {product['territory_name']} ({product.get('territory', '')})")

        if product.get('price_france'):
            lines.append(f"Prix en France : {product['price_france']}")

        if product.get('price_dom'):
            lines.append(f"Prix en DOM : {product['price_dom']}")

        if product.get('difference'):
            lines.append(f"Écart de prix : {product['difference']}")

        if product.get('unit_price_france') and product.get('unit_reference'):
            lines.append(
                f"Prix unitaire France : {product['unit_price_france']} {product['unit_reference']}"
            )

        if product.get('unit_price_dom') and product.get('unit_reference'):
            lines.append(
                f"Prix unitaire DOM : {product['unit_price_dom']} {product['unit_reference']}"
            )

        return "\n".join(lines)

    def _get_products_from_db(self, territory: str = None) -> List[Dict]:
        """Récupère les produits depuis PostgreSQL."""
        conn = self.rag_db.get_connection()
        try:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                if territory:
                    cur.execute(
                        "SELECT * FROM produits WHERE territory = %s", (territory,)
                    )
                else:
                    cur.execute("SELECT * FROM produits")
                return [dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def vectorize(self, territory: str = None, batch_size: int = 32) -> int:
        """
        Vectorise tous les produits et les stocke dans pgvector.
        
        Args:
            territory: Filtrer par territoire (ex: 'mq'). None = tous.
            batch_size: Nombre de produits traités par batch.
            
        Returns:
            Nombre d'embeddings créés.
        """
        self.rag_db.init_rag_tables()

        products = self._get_products_from_db(territory)
        if not products:
            self.logger.warning("Aucun produit trouvé en base.")
            return 0

        self.logger.info(f"{len(products)} produits à vectoriser...")
        model = self._get_model()

        created = 0
        for i in range(0, len(products), batch_size):
            batch = products[i:i + batch_size]
            texts = [self._product_to_chunk(p) for p in batch]
            embeddings = model.encode(texts, show_progress_bar=False)

            for product, text, embedding in zip(batch, texts, embeddings):
                self.rag_db.save_embedding(
                    produit_id=product['id'],
                    chunk_text=text,
                    embedding=embedding.tolist(),
                    territory=product.get('territory', ''),
                    metadata={
                        'name': product.get('name'),
                        'price_france': product.get('price_france'),
                        'price_dom': product.get('price_dom'),
                        'difference': product.get('difference'),
                        'territory_name': product.get('territory_name'),
                    }
                )
                created += 1

            self.logger.info(f"Batch {i//batch_size + 1} : {created}/{len(products)} embeddings créés")

        return created
