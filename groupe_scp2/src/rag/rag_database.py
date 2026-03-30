"""
RAGDatabase — Gestion de pgvector pour le RAG Kiprix.
Stocke les embeddings des produits dans PostgreSQL avec l'extension pgvector.
"""

import os
import logging
import psycopg2
from psycopg2.extras import DictCursor
from typing import List, Dict, Optional, Tuple

class RAGDatabase:
    """
    Gère la connexion pgvector et les opérations de vectorisation.
    
    Utilise l'extension pgvector de PostgreSQL pour stocker
    et rechercher des embeddings par similarité cosinus.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.host = os.environ.get('DB_HOST', 'localhost')
        self.user = os.environ.get('DB_USER', 'laravel')
        self.password = os.environ.get('DB_PASS', 'secret')
        self.dbname = os.environ.get('DB_NAME', 'kiprix_db')
        self.port = os.environ.get('DB_PORT', '5433')

    def get_connection(self):
        return psycopg2.connect(
            host=self.host, user=self.user,
            password=self.password, dbname=self.dbname, port=self.port
        )

    def init_rag_tables(self):
        """Installe pgvector et crée la table des embeddings."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Installer l'extension pgvector
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

                # Table des chunks vectorisés
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS produits_embeddings (
                        id SERIAL PRIMARY KEY,
                        produit_id INTEGER REFERENCES produits(id) ON DELETE CASCADE,
                        chunk_text TEXT NOT NULL,
                        embedding vector(768),
                        territory VARCHAR(10),
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # Index pour la recherche par similarité cosinus
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_embeddings_vector
                    ON produits_embeddings USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100);
                """)

            conn.commit()
        self.logger.info("Tables RAG initialisées avec pgvector.")

    def save_embedding(self, produit_id: int, chunk_text: str,
                       embedding: List[float], territory: str, metadata: dict):
        """Sauvegarde un embedding en base."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO produits_embeddings
                        (produit_id, chunk_text, embedding, territory, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (produit_id, chunk_text, embedding, territory,
                      psycopg2.extras.Json(metadata)))
            conn.commit()

    def similarity_search(self, query_embedding: List[float],
                          territory: Optional[str] = None,
                          top_k: int = 5) -> List[Dict]:
        """Recherche les chunks les plus proches par similarité cosinus."""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                if territory:
                    cur.execute("""
                        SELECT chunk_text, territory, metadata,
                               1 - (embedding <=> %s::vector) AS score
                        FROM produits_embeddings
                        WHERE territory = %s
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s
                    """, (query_embedding, territory, query_embedding, top_k))
                else:
                    cur.execute("""
                        SELECT chunk_text, territory, metadata,
                               1 - (embedding <=> %s::vector) AS score
                        FROM produits_embeddings
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s
                    """, (query_embedding, query_embedding, top_k))
                return [dict(row) for row in cur.fetchall()]

    def count_embeddings(self) -> int:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM produits_embeddings")
                return cur.fetchone()[0]

    def clear_embeddings(self, territory: Optional[str] = None):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                if territory:
                    cur.execute(
                        "DELETE FROM produits_embeddings WHERE territory = %s",
                        (territory,)
                    )
                else:
                    cur.execute("DELETE FROM produits_embeddings")
            conn.commit()
        self.logger.info("Embeddings supprimés.")
