class Livre:
    """
    Classe représentant un livre dans une bibliothèque.
    Gère les attributs d'un livre et son état de disponibilité.
    """
    # Attribut de classe (public) - compte le nombre total de livres créés
    nombre_total = 0
    
    def __init__(self, titre, auteur, isbn):
        """
        Initialise un livre avec ses informations.
        
        Args:
            titre (str): Le titre du livre
            auteur (str): L'auteur du livre
            isbn (str): L'ISBN du livre
        """
        # Attributs d'instance (privés) - ne peuvent pas être modifiés directement de l'extérieur
        self.__titre = titre
        self.__auteur = auteur
        self.__isbn = isbn
        self.__disponible = True  # Par défaut, le livre est disponible
        Livre.nombre_total += 1  # Incrémente le compteur de livres
    
    def emprunter(self):
        """
        Emprunte le livre s'il est disponible.
        
        Returns:
            bool: True si l'emprunt a réussi, False sinon
        """
        if self.__disponible:
            self.__disponible = False
            return True
        return False
    
    def retourner(self):
        """
        Retourne le livre à la bibliothèque (le rend disponible).
        """
        self.__disponible = True
    
    def __str__(self):
        """
        Retourne une représentation textuelle du livre avec son statut.
        
        Returns:
            str: Une chaîne formatée avec titre, auteur et statut
        """
        statut = "Disponible" if self.__disponible else "Emprunté"
        return f"{self.__titre} par {self.__auteur} - {statut}"


# === TESTS DU CODE ===
print("=" * 50)
print("TEST DE LA CLASSE LIVRE")
print("=" * 50)

# Création de plusieurs instances de Livre
livre1 = Livre("Peau noir et masque blanc", "Fanon", "E129N")
livre2 = Livre("Sapiens", "Yuval Noah Harari", "ISBN123")
livre3 = Livre("Le Seigneur des Anneaux", "Tolkien", "ISBN456")

# Test 1: Affichage des livres créés
print("\n1. Affichage des livres créés:")
print(f"  - {livre1}")
print(f"  - {livre2}")
print(f"  - {livre3}")

# Test 2: Affichage du nombre total de livres
print(f"\nNombre total de livres créés: {Livre.nombre_total}")

# Test 3: Test de la méthode emprunter()
print("\n2. Test d'emprunt:")
print(f"  Avant emprunt: {livre1}")
resultat = livre1.emprunter()
print(f"  Emprunt réussi: {resultat}")
print(f"  Après emprunt: {livre1}")

# Test 4: Tentative d'emprunt du même livre (non disponible)
print("\n3. Test d'emprunt du même livre deux fois:")
resultat = livre1.emprunter()
print(f"  Deuxième emprunt réussi: {resultat}")

# Test 5: Test de la méthode retourner()
print("\n4. Test de retour:")
livre1.retourner()
print(f"  Après retour: {livre1}")
print(f"  Nouvelle tentative d'emprunt: {livre1.emprunter()}")

print("\n" + "=" * 50)