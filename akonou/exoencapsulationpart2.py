"""
Exercice 3 - Encapsulation Part 2
Démonstration de l'encapsulation avec propriétés et validations
"""

class Livre:
    """
    Classe représentant un livre avec encapsulation complète.
    Utilise des propriétés (property) pour contrôler l'accès aux attributs privés.
    """
    
    def __init__(self, titre, auteur, isbn):
        """Initialise un livre.
        
        Args:
            titre (str): Le titre du livre
            auteur (str): L'auteur du livre
            isbn (str): L'ISBN du livre
        """
        self._titre = titre
        self._auteur = auteur
        self.__isbn = isbn  # Privé (double underscore)
        self._disponible = True
    
    # ===== PROPRIÉTÉS EN LECTURE =====
    
    @property
    def titre(self):
        """Retourne le titre du livre (lecture seule)."""
        return self._titre
    
    @property
    def auteur(self):
        """Retourne l'auteur du livre (lecture seule)."""
        return self._auteur
    
    @property
    def isbn(self):
        """Retourne l'ISBN du livre (lecture seule)."""
        return self.__isbn
    
    @property
    def disponible(self):
        """Retourne la disponibilité du livre."""
        return self._disponible
    
    # ===== PROPRIÉTÉS AVEC SETTER (LECTURE-ÉCRITURE) =====
    
    @property
    def titre_modifiable(self):
        """Permet de lire le titre (avec setter)."""
        return self._titre
    
    @titre_modifiable.setter
    def titre_modifiable(self, nouveau_titre):
        """Permet de modifier le titre avec validation."""
        if not isinstance(nouveau_titre, str):
            raise TypeError("Le titre doit être une chaîne de caractères")
        if len(nouveau_titre) == 0:
            raise ValueError("Le titre ne peut pas être vide")
        self._titre = nouveau_titre
    
    @property
    def auteur_modifiable(self):
        """Permet de lire l'auteur (avec setter)."""
        return self._auteur
    
    @auteur_modifiable.setter
    def auteur_modifiable(self, nouvel_auteur):
        """Permet de modifier l'auteur avec validation."""
        if not isinstance(nouvel_auteur, str):
            raise TypeError("L'auteur doit être une chaîne de caractères")
        if len(nouvel_auteur) == 0:
            raise ValueError("L'auteur ne peut pas être vide")
        self._auteur = nouvel_auteur
    
    # ===== MÉTHODES =====
    
    def emprunter(self):
        """Emprunte le livre s'il est disponible.
        
        Returns:
            bool: True si l'emprunt a réussi, False sinon
        """
        if self._disponible:
            self._disponible = False
            return True
        return False
    
    def retourner(self):
        """Retourne le livre à la bibliothèque."""
        self._disponible = True
    
    def afficher_info(self):
        """Affiche les informations du livre."""
        statut = "Disponible" if self._disponible else "Emprunté"
        return f"{self._titre} par {self._auteur} (ISBN: {self.__isbn}) - {statut}"
    
    def __str__(self):
        """Représentation textuelle du livre."""
        return self.afficher_info()


# === TESTS DU CODE ===
print("=" * 80)
print("EXERCICE 3 - ENCAPSULATION PART 2")
print("=" * 80)

# Test 1: Création d'un livre
print("\n1. CRÉATION D'UN LIVRE:")
print("-" * 80)

livre1 = Livre("Test titre", "Mon auteur", "12ZAZ")
print(f"✓ Livre créé: {livre1}")

# Test 2: Accès aux propriétés en lecture (AUTORISÉ)
print("\n2. ACCÈS AUX PROPRIÉTÉS EN LECTURE (Autorisé):")
print("-" * 80)

print(f"livre1.titre = {livre1.titre}")
print(f"livre1.auteur = {livre1.auteur}")
print(f"livre1.isbn = {livre1.isbn}")
print(f"livre1.disponible = {livre1.disponible}")

# Test 3: Tentative d'accès direct aux attributs protégés
print("\n3. ACCÈS AUX ATTRIBUTS PROTÉGÉS (_):")
print("-" * 80)

try:
    print(f"livre1._titre = {livre1._titre} (possible mais déconseillé)")
    print(f"  ⚠️  L'underscore indique que c'est une convention: ne pas y accéder directement")
except Exception as e:
    print(f"  ✗ Erreur: {e}")

# Test 4: Tentative d'accès direct à l'attribut privé (__)
print("\n4. ACCÈS À L'ATTRIBUT PRIVÉ (__):")
print("-" * 80)

print("Tentative 1: livre1.__isbn")
try:
    print(f"  Résultat: {livre1.__isbn}")
except AttributeError as e:
    print(f"  ✗ AttributeError: {e}")
    print(f"  ✓ L'attribut privé ne peut pas être accédé directement!")

print("\nTentative 2: livre1.isbn (via propriété)")
try:
    print(f"  Résultat: {livre1.isbn}")
    print(f"  ✓ L'accès via la propriété fonctionne!")
except Exception as e:
    print(f"  ✗ Erreur: {e}")

# Test 5: Tentative de modification directe des attributs (MAUVAISE APPROCHE)
print("\n5. TENTATIVE DE MODIFICATION DIRECTE (Mauvaise approche):")
print("-" * 80)

print("Tentative: livre1.titre = 'Nouveau titre'")
try:
    livre1.titre = "Nouveau titre"
    print(f"  ✗ Modification directe possible mais attendue: {livre1.titre}")
    print(f"  ⚠️  C'est incorrect car on ne voulait que la lecture!")
except AttributeError as e:
    print(f"  ✓ AttributeError: {e}")

# Test 6: Modification via propriété avec setter (BONNE APPROCHE)
print("\n6. MODIFICATION VIA PROPRIÉTÉ AVEC SETTER (Bonne approche):")
print("-" * 80)

print("Avant modification:")
print(f"  Titre: {livre1.titre}")

livre1.titre_modifiable = "Nouveau titre du livre"
print(f"\nAprès modification avec setter:")
print(f"  Titre: {livre1.titre_modifiable}")
print(f"  ✓ Modification validée et acceptée!")

# Test 7: Validation dans le setter
print("\n7. VALIDATION DANS LE SETTER:")
print("-" * 80)

print("Test 1: Tentative d'assigner un titre vide")
try:
    livre1.titre_modifiable = ""
except ValueError as e:
    print(f"  ✓ ValueError levée: {e}")

print("\nTest 2: Tentative d'assigner un titre non-string")
try:
    livre1.titre_modifiable = 123
except TypeError as e:
    print(f"  ✓ TypeError levée: {e}")

print("\nTest 3: Assignation d'un titre valide")
try:
    livre1.titre_modifiable = "Titre valide"
    print(f"  ✓ Titre modifié avec succès: {livre1.titre_modifiable}")
except Exception as e:
    print(f"  ✗ Erreur: {e}")

# Test 8: Modification de l'auteur
print("\n8. MODIFICATION DE L'AUTEUR:")
print("-" * 80)

print(f"Auteur actuel: {livre1.auteur}")
livre1.auteur_modifiable = "Nouvel auteur"
print(f"Nouvel auteur: {livre1.auteur_modifiable}")

# Test 9: Emprunt du livre
print("\n9. EMPRUNT DU LIVRE:")
print("-" * 80)

print(f"Avant emprunt:")
print(f"  {livre1}")
print(f"  Disponible: {livre1.disponible}")

resultat = livre1.emprunter()
print(f"\nEmprunt réussi: {resultat}")
print(f"  {livre1}")
print(f"  Disponible: {livre1.disponible}")

# Test 10: Tentative d'emprunt d'un livre déjà emprunté
print("\n10. TENTATIVE D'EMPRUNT DU MÊME LIVRE:")
print("-" * 80)

resultat2 = livre1.emprunter()
print(f"Deuxième emprunt réussi: {resultat2}")
print(f"  {livre1}")

# Test 11: Retour du livre
print("\n11. RETOUR DU LIVRE:")
print("-" * 80)

livre1.retourner()
print(f"Après retour:")
print(f"  {livre1}")
print(f"  Disponible: {livre1.disponible}")

# Test 12: Encapsulation avec plusieurs livres
print("\n12. GESTION DE PLUSIEURS LIVRES:")
print("-" * 80)

livre2 = Livre("Les Misérables", "Victor Hugo", "ISBN-001")
livre3 = Livre("1984", "George Orwell", "ISBN-002")

livres = [livre1, livre2, livre3]

print(f"\nBibliothèque avec {len(livres)} livres:")
for i, livre in enumerate(livres, 1):
    print(f"  {i}. {livre}")

print(f"\nEmprunt de tous les livres:")
for livre in livres:
    livre.emprunter()
    print(f"  ✓ {livre.titre} emprunté")

print(f"\nVérification de la disponibilité:")
for livre in livres:
    print(f"  {livre.titre}: Disponible={livre.disponible}")

# Test 13: Comparaison avant/après
print("\n13. RÉSUMÉ DE L'ENCAPSULATION:")
print("-" * 80)

print("""
✓ LECTURE (Toujours autorisée):
  - livre.titre (propriété)
  - livre.auteur (propriété)
  - livre.isbn (propriété)
  - livre.disponible (propriété)

✓ MODIFICATION (Avec validation):
  - livre.titre_modifiable = "..." (setter validé)
  - livre.auteur_modifiable = "..." (setter validé)

✗ ACCÈS DIRECT (À éviter):
  - livre._titre (convention: protégé)
  - livre.__isbn (private: impossible)

✓ OPÉRATIONS (Méthodes contrôlées):
  - livre.emprunter()
  - livre.retourner()
  - livre.afficher_info()
""")

print("=" * 80)
print("✓ TOUS LES TESTS SONT COMPLÉTÉS AVEC SUCCÈS!")
print("=" * 80)
