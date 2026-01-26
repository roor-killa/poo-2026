class Livre:
    """
    Classe représentant un livre dans une bibliothèque.
    Démontre l'encapsulation avec attributs privés/protégés et propriétés.
    """
    
    # ═══════════════════════════════════════════════════════════
    # ATTRIBUT DE CLASSE
    # ═══════════════════════════════════════════════════════════
    # Attribut partagé par toutes les instances de Livre
    # Préfixe _ indique qu'il est "protégé" (convention Python)
    # Ne devrait pas être modifié directement hors de la classe
    _nombre_total = 0
    
    
    def __init__(self, titre, auteur, isbn):
        """
        Constructeur : initialise un nouveau livre.
        
        Args:
            titre (str): Titre du livre
            auteur (str): Nom de l'auteur
            isbn (str): Numéro ISBN unique
        """
        # ═══════════════════════════════════════════════════════════
        # ATTRIBUTS D'INSTANCE PRIVÉS (__)
        # ═══════════════════════════════════════════════════════════
        # Double underscore (__) = attribut "privé"
        # Python le renomme en _Livre__titre (name mangling)
        # Accessible uniquement via les propriétés (getters)
        self.__titre = titre        # Privé : accès lecture seule
        self.__auteur = auteur      # Privé : accès lecture seule
        
        # ═══════════════════════════════════════════════════════════
        # ATTRIBUTS D'INSTANCE PROTÉGÉS (_)
        # ═══════════════════════════════════════════════════════════
        # Simple underscore (_) = attribut "protégé"
        # Convention : ne pas modifier depuis l'extérieur
        # Mais techniquement accessible (moins strict que __)
        self._isbn = isbn           # Protégé : identifiant unique
        self._disponible = True     # Protégé : état du livre
        
        # Incrémente le compteur de classe
        # À chaque création d'un livre, on augmente le total
        Livre._nombre_total += 1
    
    
    # ═══════════════════════════════════════════════════════════
    # PROPRIÉTÉS (GETTERS) - ACCÈS EN LECTURE SEULE
    # ═══════════════════════════════════════════════════════════
    # Le décorateur @property transforme une méthode en attribut
    # Permet d'accéder comme livre.titre au lieu de livre.titre()
    # Protège les données : on peut lire mais pas modifier directement
    
    @property
    def titre(self):
        """
        Getter pour le titre du livre.
        Permet: livre.titre (lecture seule)
        Interdit: livre.titre = "Nouveau" (pas de setter)
        """
        return self.__titre
    
    @property
    def auteur(self):
        """
        Getter pour l'auteur du livre.
        Retourne l'attribut privé __auteur.
        """
        return self.__auteur
    
    @property
    def isbn(self):
        """
        Getter pour le numéro ISBN.
        Retourne l'attribut protégé _isbn.
        """
        return self._isbn
    
    @property
    def disponible(self):
        """
        Getter pour la disponibilité du livre.
        Retourne True si le livre peut être emprunté.
        """
        return self._disponible
    
    
    # ═══════════════════════════════════════════════════════════
    # MÉTHODE DE CLASSE
    # ═══════════════════════════════════════════════════════════
    # @classmethod indique que la méthode travaille sur la classe
    # Premier paramètre : cls (la classe elle-même, pas une instance)
    # Utilisé pour accéder aux attributs de classe
    
    @classmethod
    def get_nombre_total(cls):
        """
        Retourne le nombre total de livres créés.
        
        Returns:
            int: Nombre de livres instanciés depuis le début
            
        Usage:
            total = Livre.get_nombre_total()  # Appel sur la classe
        """
        return cls._nombre_total
    
    
    # ═══════════════════════════════════════════════════════════
    # MÉTHODES D'INSTANCE
    # ═══════════════════════════════════════════════════════════
    # Méthodes qui modifient l'état d'un livre spécifique
    # Premier paramètre : self (l'instance courante)
    
    def emprunter(self):
        """
        Emprunte le livre s'il est disponible.
        
        Returns:
            bool: True si l'emprunt a réussi, False sinon
            
        Comportement:
            - Si disponible : marque comme indisponible et retourne True
            - Si déjà emprunté : retourne False sans modification
        """
        # Vérifie si le livre est disponible
        if self._disponible:
            # Change l'état : livre maintenant emprunté
            self._disponible = False
            return True  # Emprunt réussi
        
        # Livre déjà emprunté
        return False  # Emprunt échoué
    
    
    def retourner(self):
        """
        Retourne le livre à la bibliothèque.
        
        Effet:
            Marque le livre comme disponible, qu'il soit déjà
            disponible ou non (opération idempotente).
        """
        # Remet le livre en état disponible
        # Fonctionne même si déjà disponible (pas de vérification)
        self._disponible = True
    
    
    # ═══════════════════════════════════════════════════════════
    # MÉTHODE MAGIQUE __str__
    # ═══════════════════════════════════════════════════════════
    # Définit comment afficher l'objet avec print() ou str()
    
    def __str__(self):
        """
        Représentation textuelle lisible du livre.
        
        Returns:
            str: Description formatée du livre avec son statut
            
        Appelé automatiquement par:
            - print(livre)
            - str(livre)
            - f"Le livre: {livre}"
        """
        # Détermine le texte du statut selon la disponibilité
        # Opérateur ternaire : valeur_si_vrai if condition else valeur_si_faux
        statut = "Disponible" if self._disponible else "Emprunté"
        
        # Construit et retourne la chaîne formatée
        # Utilise les attributs privés directement (on est dans la classe)
        return f"📖 {self.__titre} par {self.__auteur} [{statut}]"


# ═══════════════════════════════════════════════════════════
# PROGRAMME PRINCIPAL - DÉMONSTRATION
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("📚 SYSTÈME DE GESTION DE BIBLIOTHÈQUE")
    print("=" * 70)
    
    # ───────────────────────────────────────────────────────────
    # CRÉATION DES LIVRES
    # ───────────────────────────────────────────────────────────
    # Chaque instanciation appelle __init__()
    # Le compteur _nombre_total est incrémenté automatiquement
    
    print("\n📝 Création des livres...\n")
    
    livre1 = Livre("1984", "George Orwell", "1234567890")
    livre2 = Livre("Le Seigneur des Anneaux", "J.R.R. Tolkien", "0987654321")
    livre3 = Livre("Harry Potter", "J.K. Rowling", "1122334455")
    
    # Affiche le nombre total via la méthode de classe
    print(f"✅ Nombre de livres créés: {Livre.get_nombre_total()}")
    
    
    # ───────────────────────────────────────────────────────────
    # DÉMONSTRATION DES PROPRIÉTÉS
    # ───────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("🔍 ACCÈS AUX PROPRIÉTÉS (LECTURE SEULE)")
    print("=" * 70)
    
    # Utilisation des propriétés : syntaxe d'attribut, mais appelle une méthode
    print(f"\nTitre de livre1: {livre1.titre}")       # Appelle livre1.titre()
    print(f"Auteur de livre1: {livre1.auteur}")       # Appelle livre1.auteur()
    print(f"ISBN de livre1: {livre1.isbn}")           # Appelle livre1.isbn()
    print(f"Disponible: {livre1.disponible}")         # Appelle livre1.disponible()
    
    # ⚠️ TENTATIVE DE MODIFICATION (génère une erreur)
    print("\n⚠️ Test de modification d'une propriété lecture seule:")
    try:
        livre1.titre = "Nouveau titre"  # ❌ AttributeError
    except AttributeError as e:
        print(f"✅ Erreur attendue: {e}")
    
    
    # ───────────────────────────────────────────────────────────
    # EMPRUNTS DE LIVRES
    # ───────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("📤 EMPRUNTS DE LIVRES")
    print("=" * 70)
    
    # Emprunte livre1 (première fois)
    print(f"\n➤ Emprunt de '{livre1.titre}':")
    if livre1.emprunter():
        print("   ✅ Emprunt réussi")
    else:
        print("   ❌ Livre déjà emprunté")
    
    # Emprunte livre2 (première fois)
    print(f"\n➤ Emprunt de '{livre2.titre}':")
    if livre2.emprunter():
        print("   ✅ Emprunt réussi")
    else:
        print("   ❌ Livre déjà emprunté")
    
    # Tentative d'emprunter livre1 à nouveau (échec attendu)
    print(f"\n➤ Tentative de ré-emprunt de '{livre1.titre}':")
    if livre1.emprunter():
        print("   ✅ Emprunt réussi")
    else:
        print("   ❌ Livre déjà emprunté")
    
    
    # ───────────────────────────────────────────────────────────
    # AFFICHAGE DES STATUTS (utilise __str__)
    # ───────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("📊 STATUT ACTUEL DES LIVRES")
    print("=" * 70 + "\n")
    
    # print() appelle automatiquement __str__() sur chaque objet
    print(livre1)  # Affiche "... [Emprunté]"
    print(livre2)  # Affiche "... [Emprunté]"
    print(livre3)  # Affiche "... [Disponible]"
    
    
    # ───────────────────────────────────────────────────────────
    # RETOUR DE LIVRE
    # ───────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("📥 RETOUR DE LIVRE")
    print("=" * 70)
    
    print(f"\n➤ Retour de '{livre1.titre}'")
    livre1.retourner()  # Marque comme disponible
    print("   ✅ Livre retourné")
    
    
    # ───────────────────────────────────────────────────────────
    # AFFICHAGE FINAL
    # ───────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("📊 STATUT FINAL DES LIVRES")
    print("=" * 70 + "\n")
    
    print(livre1)  # Maintenant "... [Disponible]"
    print(livre2)  # Toujours "... [Emprunté]"
    print(livre3)  # Toujours "... [Disponible]"
    
    
    # ───────────────────────────────────────────────────────────
    # STATISTIQUES FINALES
    # ───────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("📈 STATISTIQUES")
    print("=" * 70)
    
    # Utilisation de la méthode de classe
    print(f"\n📚 Nombre total de livres: {Livre.get_nombre_total()}")
    
    # Compte les livres disponibles (utilise les propriétés)
    disponibles = sum(1 for livre in [livre1, livre2, livre3] if livre.disponible)
    print(f"✅ Livres disponibles: {disponibles}")
    print(f"📤 Livres empruntés: {Livre.get_nombre_total() - disponibles}")
    
    print("\n" + "=" * 70)
    print("✅ DÉMONSTRATION TERMINÉE")
    print("=" * 70)