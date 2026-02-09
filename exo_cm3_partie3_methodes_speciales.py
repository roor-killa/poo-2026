print("=" * 70)
print("🧪 TESTS DES MÉTHODES SPÉCIALES (Magic Methods)")
print("=" * 70)

# ============================================
# 1. CLASSE DOCUMENT (pour les tests)
# ============================================

class Document:
    """Classe simple pour tester la bibliothèque"""
    def __init__(self, titre, auteur, annee):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
    
    def __str__(self):
        return f"{self.titre} ({self.auteur}, {self.annee})"
    
    def __repr__(self):
        return f"Document('{self.titre}', '{self.auteur}', {self.annee})"


# ============================================
# 2. CLASSE BIBLIOTHÈQUE (Votre code)
# ============================================

class Bibliotheque:
    """
    Bibliothèque avec méthodes spéciales pour un comportement pythonique
    """
    def __init__(self, nom):
        self.nom = nom
        self.documents = []
    
    def ajouter(self, document):
        """Ajoute un document à la bibliothèque"""
        self.documents.append(document)
    
    def __len__(self):
        """
        Surcharge de len() - permet d'utiliser len(biblio)
        Appelé quand on fait: len(biblio)
        """
        return len(self.documents)
    
    def __getitem__(self, index):
        """
        Surcharge de [] - permet l'indexation
        Appelé quand on fait: biblio[0] ou biblio[1:3]
        """
        return self.documents[index]
    
    def __contains__(self, titre):
        """
        Surcharge de 'in' - permet de vérifier l'appartenance
        Appelé quand on fait: "titre" in biblio
        """
        return any(doc.titre == titre for doc in self.documents)
    
    def __str__(self):
        """
        Surcharge de str() - affichage lisible
        Appelé quand on fait: print(biblio) ou str(biblio)
        """
        return f"Bibliothèque {self.nom} avec {len(self)} document(s)"


# ============================================
# 3. CRÉATION DES DONNÉES DE TEST
# ============================================

print("\n📚 CRÉATION DE LA BIBLIOTHÈQUE ET DES DOCUMENTS")
print("-" * 70)

# Création de la bibliothèque
biblio = Bibliotheque("Université des Antilles")
print(f"✓ Créé: {biblio}")

# Création de documents
doc1 = Document("1984", "George Orwell", 1949)
doc2 = Document("Le Petit Prince", "Antoine de Saint-Exupéry", 1943)
doc3 = Document("L'Étranger", "Albert Camus", 1942)
doc4 = Document("Les Misérables", "Victor Hugo", 1862)
doc5 = Document("Dune", "Frank Herbert", 1965)

# Ajout des documents
print("\nAjout de documents:")
for doc in [doc1, doc2, doc3, doc4, doc5]:
    biblio.ajouter(doc)
    print(f"  ✓ Ajouté: {doc}")


# ============================================
# 4. TEST DE __len__
# ============================================

print("\n" + "=" * 70)
print("TEST 1: __len__() - Utilisation de len()")
print("-" * 70)

nombre = len(biblio)  # Appelle __len__()
print(f"📊 Nombre de documents dans la bibliothèque: {nombre}")
print(f"✅ len(biblio) fonctionne grâce à __len__()")

# Test après ajout
nouveau_doc = Document("Fondation", "Isaac Asimov", 1951)
biblio.ajouter(nouveau_doc)
print(f"\nAprès ajout: {len(biblio)} documents")


# ============================================
# 5. TEST DE __getitem__
# ============================================

print("\n" + "=" * 70)
print("TEST 2: __getitem__() - Indexation et slicing")
print("-" * 70)

# Indexation simple
print("🔍 Accès par index:")
print(f"  biblio[0] = {biblio[0]}")  # Appelle __getitem__(0)
print(f"  biblio[2] = {biblio[2]}")  # Appelle __getitem__(2)
print(f"  biblio[-1] = {biblio[-1]}")  # Dernier élément

# Slicing (découpage)
print("\n🔪 Slicing:")
print(f"  biblio[1:3] = {biblio[1:3]}")  # Appelle __getitem__(slice(1,3))
print(f"  biblio[:2] = {biblio[:2]}")    # Les 2 premiers
print(f"  biblio[-2:] = {biblio[-2:]}")  # Les 2 derniers

# Itération (utilise aussi __getitem__)
print("\n🔄 Itération (grâce à __getitem__):")
print("  Documents dans la bibliothèque:")
for i, doc in enumerate(biblio, 1):
    print(f"    {i}. {doc.titre}")

print("\n✅ biblio[index] fonctionne grâce à __getitem__()")


# ============================================
# 6. TEST DE __contains__
# ============================================

print("\n" + "=" * 70)
print("TEST 3: __contains__() - Opérateur 'in'")
print("-" * 70)

# Test de présence
print("🔍 Recherche de titres:")
titres_a_chercher = [
    "1984",
    "Le Petit Prince",
    "Harry Potter",  # N'existe pas
    "Dune",
    "Narnia"  # N'existe pas
]

for titre in titres_a_chercher:
    if titre in biblio:  # Appelle __contains__(titre)
        print(f"  ✓ '{titre}' est dans la bibliothèque")
    else:
        print(f"  ✗ '{titre}' n'est PAS dans la bibliothèque")

print("\n✅ 'titre' in biblio fonctionne grâce à __contains__()")


# ============================================
# 7. TEST DE __str__
# ============================================

print("\n" + "=" * 70)
print("TEST 4: __str__() - Affichage lisible")
print("-" * 70)

# Affichage direct
print("📝 Affichage avec print():")
print(f"  {biblio}")  # Appelle __str__()

# Affichage avec str()
texte = str(biblio)  # Appelle __str__()
print(f"\n📝 Conversion en string:")
print(f"  str(biblio) = '{texte}'")

print("\n✅ print(biblio) fonctionne grâce à __str__()")


# ============================================
# 8. TESTS D'ERREURS (Edge cases)
# ============================================

print("\n" + "=" * 70)
print("TEST 5: GESTION DES ERREURS")
print("-" * 70)

print("⚠️  Test des cas limites:")

# Test index hors limites
try:
    doc = biblio[100]
    print("  ✗ Devrait échouer!")
except IndexError as e:
    print(f"  ✓ IndexError capturé: {e}")

# Test index négatif extrême
try:
    doc = biblio[-100]
    print("  ✗ Devrait échouer!")
except IndexError as e:
    print(f"  ✓ IndexError capturé: {e}")

# Test bibliothèque vide
biblio_vide = Bibliotheque("Vide")
print(f"\n📭 Bibliothèque vide:")
print(f"  len(biblio_vide) = {len(biblio_vide)}")
print(f"  '1984' in biblio_vide = {'1984' in biblio_vide}")
print(f"  str(biblio_vide) = {biblio_vide}")


# ============================================
# 9. DÉMONSTRATION DES AVANTAGES
# ============================================

print("\n" + "=" * 70)
print("🎯 DÉMONSTRATION: Comportement Pythonique")
print("-" * 70)

print("\n💡 Grâce aux méthodes spéciales, la bibliothèque se comporte")
print("   comme une collection native Python:")

# Comme une liste
print("\n1️⃣ Comme une liste:")
print(f"  - Taille: len(biblio) = {len(biblio)}")
print(f"  - Premier: biblio[0] = {biblio[0].titre}")
print(f"  - Dernier: biblio[-1] = {biblio[-1].titre}")

# Itérable
print("\n2️⃣ Itérable (dans une boucle):")
print("  Tous les auteurs:")
auteurs = [doc.auteur for doc in biblio]
print(f"  {auteurs[:3]}...")  # Premiers auteurs

# Recherche facile
print("\n3️⃣ Recherche intuitive:")
if "1984" in biblio:
    print("  '1984' est disponible!")

# Utilisation dans des fonctions Python
print("\n4️⃣ Compatible avec les fonctions Python:")
print(f"  - max() par année: {max(biblio, key=lambda d: d.annee).titre}")
print(f"  - min() par année: {min(biblio, key=lambda d: d.annee).titre}")
print(f"  - sorted(): {[d.titre for d in sorted(biblio, key=lambda d: d.annee)][:3]}...")
