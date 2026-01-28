# ============================================
# 1. DÉMONSTRATION DU DIAMOND PROBLEM
# ============================================

class Document:
    """Classe de base commune - crée le 'diamond'"""
    def __init__(self, titre):
        print(f"Document.__init__() appelé pour '{titre}'")
        self.titre = titre
    
    def afficher_info(self):
        return f"Document: {self.titre}"

class Empruntable(Document):
    """Première branche du diamond"""
    def __init__(self, titre):
        print("Empruntable.__init__() appelé")
        super().__init__(titre)  # ⚠️ Important pour le MRO
        self.emprunte_par = None
    
    def emprunter(self, utilisateur):
        if self.emprunte_par is None:
            self.emprunte_par = utilisateur
            print(f"✓ Emprunté par {utilisateur}")
            return True
        print(f"✗ Déjà emprunté par {self.emprunte_par}")
        return False
    
    def afficher_info(self):
        info = super().afficher_info()
        statut = f"emprunté par {self.emprunte_par}" if self.emprunte_par else "disponible"
        return f"{info} | Statut: {statut}"

class Reservable(Document):
    """Deuxième branche du diamond"""
    def __init__(self, titre):
        print("Reservable.__init__() appelé")
        super().__init__(titre)  # ⚠️ Important pour le MRO
        self.reservations = []
    
    def reserver(self, utilisateur):
        self.reservations.append(utilisateur)
        print(f"✓ Réservation ajoutée pour {utilisateur}")
    
    def afficher_info(self):
        info = super().afficher_info()
        nb_reservations = len(self.reservations)
        return f"{info} | Réservations: {nb_reservations}"

# ============================================
# 2. CLASSE AVEC HÉRITAGE MULTIPLE (Le point du diamond)
# ============================================

class LivreNumerique(Empruntable, Reservable):
    """
    Diamond problem: LivreNumerique hérite de Empruntable et Reservable,
    qui héritent tous deux de Document.
    
    Question: Document.__init__() sera appelé combien de fois ?
    Réponse: Une seule fois, grâce au MRO !
    """
    def __init__(self, titre, auteur, format_fichier):
        print(f"\n--- Création de LivreNumerique '{titre}' ---")
        super().__init__(titre)  # ✅ Bonne pratique : utiliser super()
        self.auteur = auteur
        self.format_fichier = format_fichier
        print("--- Fin de la création ---\n")
    
    def afficher_info(self):
        info = super().afficher_info()
        return f"{info} | Auteur: {self.auteur} | Format: {self.format_fichier}"

# ============================================
# 3. DÉMONSTRATION DU MRO (Method Resolution Order)
# ============================================

print("=" * 60)
print("ANALYSE DU MRO (Method Resolution Order)")
print("=" * 60)

# Afficher le MRO
print("\nMRO de LivreNumerique:")
for i, cls in enumerate(LivreNumerique.__mro__, 1):
    print(f"  {i}. {cls.__name__}")

print("\n📌 Signification:")
print("   Python cherche les méthodes dans cet ordre précis")
print("   Cela résout le diamond problem automatiquement!")

# ============================================
# 4. TEST : Création d'un objet
# ============================================

print("\n" + "=" * 60)
print("CRÉATION D'UN OBJET (observez l'ordre des appels)")
print("=" * 60)

livre = LivreNumerique("Python Avancé", "Guido van Rossum", "PDF")

# ============================================
# 5. TEST : Utilisation des méthodes
# ============================================

print("\n" + "=" * 60)
print("UTILISATION DES MÉTHODES")
print("=" * 60)

livre.emprunter("Alice")
livre.emprunter("Bob")  # Devrait échouer
livre.reserver("Charlie")
livre.reserver("David")

print(f"\nInformations: {livre.afficher_info()}")

# ============================================
# 6. PROBLÈME POTENTIEL : Sans super()
# ============================================

print("\n" + "=" * 60)
print("⚠️  PROBLÈME: Sans super() (MAUVAISE PRATIQUE)")
print("=" * 60)

class LivreNumeriqueProblematique(Empruntable, Reservable):
    """
    ❌ Mauvaise pratique : appel direct aux __init__ des parents
    """
    def __init__(self, titre, auteur, format_fichier):
        print(f"\n--- Création problématique '{titre}' ---")
        Empruntable.__init__(self, titre)  # ❌ Appel direct
        Reservable.__init__(self, titre)   # ❌ Appel direct
        # Document.__init__() sera appelé DEUX FOIS !
        self.auteur = auteur
        self.format_fichier = format_fichier
        print("--- Fin ---\n")

print("\nCréation avec appels directs:")
livre_pb = LivreNumeriqueProblematique("Bad Practice", "Unknown", "EPUB")

# ============================================
# 7. ALTERNATIVE : COMPOSITION (souvent préférable)
# ============================================

print("\n" + "=" * 60)
print("✅ ALTERNATIVE RECOMMANDÉE: COMPOSITION")
print("=" * 60)

class GestionEmprunt:
    """Composant pour gérer les emprunts"""
    def __init__(self):
        self.emprunte_par = None
    
    def emprunter(self, utilisateur):
        if self.emprunte_par is None:
            self.emprunte_par = utilisateur
            return True
        return False

class GestionReservation:
    """Composant pour gérer les réservations"""
    def __init__(self):
        self.reservations = []
    
    def reserver(self, utilisateur):
        self.reservations.append(utilisateur)

class LivreNumeriqueComposition:
    """
    ✅ Utilise la composition au lieu de l'héritage multiple
    Plus flexible, plus maintenable, pas de MRO à gérer
    """
    def __init__(self, titre, auteur, format_fichier):
        self.titre = titre
        self.auteur = auteur
        self.format_fichier = format_fichier
        
        # Composition : "a-un" au lieu de "est-un"
        self.gestion_emprunt = GestionEmprunt()
        self.gestion_reservation = GestionReservation()
    
    def emprunter(self, utilisateur):
        return self.gestion_emprunt.emprunter(utilisateur)
    
    def reserver(self, utilisateur):
        self.gestion_reservation.reserver(utilisateur)

print("\nCréation avec composition (simple et clair):")
livre_comp = LivreNumeriqueComposition("Clean Code", "Robert Martin", "PDF")
livre_comp.emprunter("Eve")
livre_comp.reserver("Frank")

# ============================================
# 8. GUIDE DE DÉCISION
# ============================================

print("\n" + "=" * 60)
print("📚 QUAND UTILISER L'HÉRITAGE MULTIPLE ?")
print("=" * 60)

guide = """
✅ UTILISEZ l'héritage multiple quand:
   • Les classes parentes sont des mixins (petites classes de comportement)
   • Vous ajoutez des capacités indépendantes (logging, serialization)
   • Il y a une vraie relation "est-un" avec plusieurs concepts

❌ ÉVITEZ l'héritage multiple quand:
   • Vous pouvez utiliser la composition (souvent préférable)
   • Les classes parentes ont des états complexes
   • Il y a risque de conflits de méthodes
   • La hiérarchie devient difficile à comprendre

🎯 RÈGLES D'OR:
   1. Toujours utiliser super() dans les __init__
   2. Vérifier le MRO avec __mro__
   3. Préférer la composition quand c'est possible
   4. Documenter clairement les raisons de l'héritage multiple
"""

print(guide)

# ============================================
# 9. EXERCICE PRATIQUE
# ============================================

print("\n" + "=" * 60)
print("🎓 EXERCICE")
print("=" * 60)

exercice = """
Créez une classe AudioLivre qui:
1. Hérite de Document, Empruntable et Reservable
2. Ajoute les attributs: narrateur, duree_minutes
3. Surcharge afficher_info() correctement
4. Utilise super() partout

Puis:
- Affichez son MRO
- Créez une instance
- Testez toutes les méthodes
- Comparez avec une version en composition
"""
print(exercice)


#1 classe AudioLivre(Document, Empruntable, Reservable):
class AudioLivre(Empruntable, Reservable):
    def __init__(self, titre, narrateur, duree_minutes):
        print(f"\n Création de AudioLivre '{titre}'")
        super().__init__(titre)  
        self.narrateur = narrateur
        self.duree_minutes = duree_minutes
        print(" Fin de la création\n")

    def afficher_info(self):
        info = super().afficher_info()  
        return f"{info} , Narrateur: {self.narrateur} ,Durée: {self.duree_minutes} min"
    
#2 
print("\nMRO de AudioLivre:") #ce que chat gpt a generer pour afficher le MRO
for i, cls in enumerate(AudioLivre.__mro__, 1):
    print(f"{i}. {cls.__name__}")

#3 creation instance
audiolivre = AudioLivre("Le Petit Prince", "Jean Reno", 120)

#4 test emprunt
audiolivre.emprunter("Gaston")
audiolivre.reserver("Hélène")

#5 test reservation
audiolivre.reserver("Charlie")
audiolivre.reserver("David")

#6 print

print("\nInformations finales:")
print(audiolivre.afficher_info())