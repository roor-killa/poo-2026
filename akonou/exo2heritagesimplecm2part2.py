"""
Exercice 2 - CM2 Part 2 : Héritage et polymorphisme
Gestion d'une bibliothèque avec différents types de documents
"""

class Document:
    """Classe parent représentant un document général."""
    
    def __init__(self, titre, auteur):
        """Initialise un document.
        
        Args:
            titre (str): Le titre du document
            auteur (str): L'auteur du document
        """
        self.titre = titre
        self.auteur = auteur
        self.disponible = True
    
    def emprunter(self):
        """Emprunte le document s'il est disponible.
        
        Returns:
            bool: True si l'emprunt a réussi, False sinon
        """
        if self.disponible:
            self.disponible = False
            return True
        return False
    
    def retourner(self):
        """Retourne le document à la bibliothèque."""
        self.disponible = True
    
    def afficher_info(self):
        """Retourne les informations du document.
        
        Returns:
            str: Les informations du document
        """
        return f"{self.titre} par {self.auteur}"
    
    def obtenir_statut(self):
        """Retourne le statut de disponibilité.
        
        Returns:
            str: "Disponible" ou "Emprunté"
        """
        return "Disponible" if self.disponible else "Emprunté"


class Livre(Document):
    """Classe représentant un livre (hérite de Document)."""
    
    def __init__(self, titre, auteur, isbn, nb_pages):
        """Initialise un livre.
        
        Args:
            titre (str): Le titre du livre
            auteur (str): L'auteur du livre
            isbn (str): L'ISBN du livre
            nb_pages (int): Le nombre de pages
        """
        super().__init__(titre, auteur)
        self.isbn = isbn
        self.nb_pages = nb_pages
    
    def afficher_info(self):
        """Affiche les informations du livre (surcharge polymorphe).
        
        Returns:
            str: Les informations complètes du livre
        """
        info_base = super().afficher_info()
        return f"{info_base} - ISBN: {self.isbn} ({self.nb_pages} pages)"


class Magazine(Document):
    """Classe représentant un magazine (hérite de Document)."""
    
    def __init__(self, titre, auteur, numero, mois):
        """Initialise un magazine.
        
        Args:
            titre (str): Le titre du magazine
            auteur (str): L'éditeur/auteur du magazine
            numero (int): Le numéro du magazine
            mois (str): Le mois de publication
        """
        super().__init__(titre, auteur)
        self.numero = numero
        self.mois = mois
    
    def afficher_info(self):
        """Affiche les informations du magazine (surcharge polymorphe).
        
        Returns:
            str: Les informations complètes du magazine
        """
        info_base = super().afficher_info()
        return f"{info_base} - N°{self.numero} ({self.mois})"


# === TESTS DU CODE ===
print("=" * 70)
print("EXERCICE 2 - CM2 PART 2 : HÉRITAGE ET POLYMORPHISME")
print("=" * 70)

# Test 1: Création de documents
print("\n1. CRÉATION DE DOCUMENTS:")
print("-" * 70)

livre1 = Livre("Peau noire, masque blanc", "Frantz Fanon", "ISBN123", 250)
livre2 = Livre("Sapiens", "Yuval Noah Harari", "ISBN456", 512)
magazine1 = Magazine("Science et Vie", "Mondadori", 1234, "Janvier 2026")
magazine2 = Magazine("Géo", "Prisma Media", 567, "Février 2026")

print(f"✓ Livre 1 créé: {livre1.titre}")
print(f"✓ Livre 2 créé: {livre2.titre}")
print(f"✓ Magazine 1 créé: {magazine1.titre}")
print(f"✓ Magazine 2 créé: {magazine2.titre}")

# Test 2: Affichage des informations (polymorphisme)
print("\n2. AFFICHAGE DES INFORMATIONS (Polymorphisme):")
print("-" * 70)

print(f"\n{livre1.afficher_info()}")
print(f"  Statut: {livre1.obtenir_statut()}")

print(f"\n{livre2.afficher_info()}")
print(f"  Statut: {livre2.obtenir_statut()}")

print(f"\n{magazine1.afficher_info()}")
print(f"  Statut: {magazine1.obtenir_statut()}")

print(f"\n{magazine2.afficher_info()}")
print(f"  Statut: {magazine2.obtenir_statut()}")

# Test 3: Emprunt d'un livre
print("\n3. TEST D'EMPRUNT - LIVRE 1:")
print("-" * 70)

print(f"Avant emprunt: {livre1.afficher_info()}")
print(f"  Disponible: {livre1.disponible}")

succes = livre1.emprunter()
print(f"\nEmprunt réussi: {succes}")
print(f"  Disponible: {livre1.disponible}")

# Test 4: Tentative d'emprunt d'un document déjà emprunté
print("\n4. TENTATIVE D'EMPRUNT DU MÊME LIVRE:")
print("-" * 70)

succes2 = livre1.emprunter()
print(f"Deuxième emprunt réussi: {succes2}")
print(f"  Statut: {livre1.obtenir_statut()}")

# Test 5: Emprunt d'un magazine
print("\n5. TEST D'EMPRUNT - MAGAZINE 1:")
print("-" * 70)

print(f"Avant emprunt: {magazine1.afficher_info()}")
succes_mag = magazine1.emprunter()
print(f"Emprunt réussi: {succes_mag}")
print(f"Après emprunt: {magazine1.afficher_info()}")
print(f"  Statut: {magazine1.obtenir_statut()}")

# Test 6: Retour d'un document
print("\n6. TEST DE RETOUR:")
print("-" * 70)

print(f"Avant retour - Livre 1: {livre1.obtenir_statut()}")
livre1.retourner()
print(f"Après retour - Livre 1: {livre1.obtenir_statut()}")

print(f"\nAvant retour - Magazine 1: {magazine1.obtenir_statut()}")
magazine1.retourner()
print(f"Après retour - Magazine 1: {magazine1.obtenir_statut()}")

# Test 7: Polymorphisme en action (liste hétérogène)
print("\n7. POLYMORPHISME - GESTION D'UNE COLLECTION:")
print("-" * 70)

documents = [livre1, livre2, magazine1, magazine2]

print(f"\nNombre total de documents: {len(documents)}")
print(f"\nListe de tous les documents:")
for i, doc in enumerate(documents, 1):
    print(f"  {i}. {doc.afficher_info()}")
    print(f"     Statut: {doc.obtenir_statut()}\n")

# Test 8: Simulation d'emprunts multiples
print("\n8. SIMULATION D'EMPRUNTS MULTIPLES:")
print("-" * 70)

print("\nEmprunt de tous les documents:")
for doc in documents:
    resultat = doc.emprunter()
    statut = "✓ Succès" if resultat else "✗ Échoué"
    print(f"  {statut}: {doc.titre}")

print("\nVérification des statuts après emprunt:")
for doc in documents:
    print(f"  {doc.titre}: {doc.obtenir_statut()}")

# Test 9: Retour de tous les documents
print("\n9. RETOUR DE TOUS LES DOCUMENTS:")
print("-" * 70)

for doc in documents:
    doc.retourner()
    print(f"  ✓ {doc.titre} retourné")

print("\nVérification des statuts après retour:")
for doc in documents:
    print(f"  {doc.titre}: {doc.obtenir_statut()}")

# Test 10: Démonstration de l'héritage
print("\n10. DÉMONSTRATION DE L'HÉRITAGE:")
print("-" * 70)

print(f"\nLivre1 est une instance de Livre: {isinstance(livre1, Livre)}")
print(f"Livre1 est une instance de Document: {isinstance(livre1, Document)}")

print(f"\nMagazine1 est une instance de Magazine: {isinstance(magazine1, Magazine)}")
print(f"Magazine1 est une instance de Document: {isinstance(magazine1, Document)}")

print(f"\nMagazine1 est une instance de Livre: {isinstance(magazine1, Livre)}")

# Test 11: Affichage du type de chaque document
print("\n11. TYPE DE CHAQUE DOCUMENT:")
print("-" * 70)

for doc in documents:
    type_name = type(doc).__name__
    print(f"  {doc.titre}: {type_name}")

print("\n" + "=" * 70)
print("✓ TOUS LES TESTS SONT COMPLÉTÉS AVEC SUCCÈS!")
print("=" * 70)
