# ============================================
# DÉMONSTRATION COMPLÈTE DU DIAMOND PROBLEM
# ============================================

# ============================================
# 1. HIÉRARCHIE DE CLASSES (Le Diamond)
# ============================================

class Document:
    """Classe de base - Sommet du diamond"""
    def __init__(self, titre):
        print(f"  → Document.__init__() pour '{titre}'")
        self.titre = titre
    
    def afficher_info(self):
        return f"📄 {self.titre}"

class Empruntable(Document):
    """Branche gauche du diamond"""
    def __init__(self, titre):
        print(f"  → Empruntable.__init__()")
        super().__init__(titre)  # ✅ Utilise super() !
        self.emprunte_par = None
    
    def emprunter(self, utilisateur):
        if self.emprunte_par is None:
            self.emprunte_par = utilisateur
            return f"✓ {utilisateur} a emprunté le document"
        return f"✗ Déjà emprunté par {self.emprunte_par}"
    
    def afficher_info(self):
        info = super().afficher_info()  # ✅ Appelle le suivant dans le MRO
        statut = f"emprunté par {self.emprunte_par}" if self.emprunte_par else "disponible"
        return f"{info} | 📚 {statut}"

class Reservable(Document):
    """Branche droite du diamond"""
    def __init__(self, titre):
        print(f"  → Reservable.__init__()")
        super().__init__(titre)  # ✅ Utilise super() !
        self.reservations = []
    
    def reserver(self, utilisateur):
        self.reservations.append(utilisateur)
        return f"✓ Réservation de {utilisateur} enregistrée"
    
    def afficher_info(self):
        info = super().afficher_info()  # ✅ Appelle le suivant dans le MRO
        return f"{info} | 🔖 {len(self.reservations)} réservation(s)"

class LivreNumerique(Empruntable, Reservable):
    """Point de convergence du diamond - Héritage multiple"""
    def __init__(self, titre, auteur, format_fichier):
        print(f"\n🔷 Création de LivreNumerique: '{titre}'")
        print("Ordre des appels __init__:")
        super().__init__(titre)  # ✅ Démarre la chaîne MRO
        self.auteur = auteur
        self.format_fichier = format_fichier
        print("✅ Création terminée\n")
    
    def afficher_info(self):
        info = super().afficher_info()
        return f"{info} | ✍️ {self.auteur} | 💾 {self.format_fichier}"


# ============================================
# 2. ANALYSE DU MRO
# ============================================

print("=" * 70)
print("📊 ANALYSE DU MRO (Method Resolution Order)")
print("=" * 70)

print("\n🔍 MRO de LivreNumerique:")
for i, cls in enumerate(LivreNumerique.__mro__, 1):
    print(f"   {i}. {cls.__name__}")

print("\n💡 Explication:")
print("   Python cherche les méthodes dans CET ORDRE précis:")
print("   1. D'abord dans LivreNumerique")
print("   2. Puis dans Empruntable (premier parent)")
print("   3. Puis dans Reservable (second parent)")
print("   4. Puis dans Document (parent commun)")
print("   5. Enfin dans object (classe de base Python)")


# ============================================
# 3. TEST: Création d'objet
# ============================================

print("\n" + "=" * 70)
print("🧪 TEST 1: Création d'un objet")
print("=" * 70)

livre = LivreNumerique("Python Avancé", "Guido van Rossum", "PDF")

print("🎯 OBSERVATION IMPORTANTE:")
print("   Document.__init__() n'a été appelé QU'UNE SEULE FOIS !")
print("   C'est le MRO qui résout automatiquement le diamond problem.")


# ============================================
# 4. TEST: Utilisation des méthodes
# ============================================

print("\n" + "=" * 70)
print("🧪 TEST 2: Utilisation des méthodes héritées")
print("=" * 70)

print("\n1️⃣ Emprunt:")
print("  ", livre.emprunter("Alice"))
print("  ", livre.emprunter("Bob"))  # Déjà emprunté

print("\n2️⃣ Réservations:")
print("  ", livre.reserver("Charlie"))
print("  ", livre.reserver("David"))

print("\n3️⃣ Affichage complet:")
print("  ", livre.afficher_info())


# ============================================
# 5. COMPARAISON: AVEC vs SANS super()
# ============================================

print("\n" + "=" * 70)
print("⚠️  DANGER: Sans super() (MAUVAISE PRATIQUE)")
print("=" * 70)

class LivreProblematique(Empruntable, Reservable):
    """❌ Mauvaise pratique: appels directs"""
    def __init__(self, titre, auteur, format_fichier):
        print(f"\n❌ Création problématique: '{titre}'")
        print("Ordre des appels __init__:")
        Empruntable.__init__(self, titre)  # ❌ Appel direct
        Reservable.__init__(self, titre)   # ❌ Appel direct
        # Document.__init__() sera appelé DEUX FOIS !
        self.auteur = auteur
        self.format_fichier = format_fichier

print("\nCréation d'un livre sans super():")
livre_pb = LivreProblematique("Bad Practice", "Unknown", "EPUB")

print("\n🚨 PROBLÈME:")
print("   Document.__init__() a été appelé DEUX FOIS !")
print("   → Duplication inutile")
print("   → Peut causer des bugs si __init__ a des effets de bord")


# ============================================
# 6. SOLUTION ALTERNATIVE: COMPOSITION
# ============================================

print("\n" + "=" * 70)
print("✅ ALTERNATIVE: COMPOSITION (Souvent préférable)")
print("=" * 70)

class GestionEmprunt:
    """Composant autonome pour les emprunts"""
    def __init__(self):
        self.emprunte_par = None
    
    def emprunter(self, utilisateur):
        if self.emprunte_par is None:
            self.emprunte_par = utilisateur
            return f"✓ {utilisateur} a emprunté"
        return f"✗ Déjà emprunté par {self.emprunte_par}"

class GestionReservation:
    """Composant autonome pour les réservations"""
    def __init__(self):
        self.reservations = []
    
    def reserver(self, utilisateur):
        self.reservations.append(utilisateur)
        return f"✓ Réservation de {utilisateur}"

class LivreComposition:
    """✅ Composition: 'a-un' au lieu de 'est-un'"""
    def __init__(self, titre, auteur, format_fichier):
        self.titre = titre
        self.auteur = auteur
        self.format_fichier = format_fichier
        
        # Composition: on "contient" ces fonctionnalités
        self.emprunt = GestionEmprunt()
        self.reservation = GestionReservation()
    
    def emprunter(self, utilisateur):
        return self.emprunt.emprunter(utilisateur)
    
    def reserver(self, utilisateur):
        return self.reservation.reserver(utilisateur)

print("\nCréation avec composition:")
livre_comp = LivreComposition("Clean Code", "Robert Martin", "PDF")
print("✓ Livre créé (simple, pas de MRO à gérer)")
print("  ", livre_comp.emprunter("Eve"))
print("  ", livre_comp.reserver("Frank"))


# ============================================
# 7. GUIDE DE DÉCISION
# ============================================

print("\n" + "=" * 70)
print("📚 GUIDE: Héritage Multiple vs Composition")
print("=" * 70)

print("""
✅ UTILISEZ L'HÉRITAGE MULTIPLE QUAND:
   • Vous créez des mixins (petites classes de comportement)
   • Vraie relation "est-un" avec plusieurs concepts
   • Exemple: LoggableMixin, SerializableMixin

❌ PRÉFÉREZ LA COMPOSITION QUAND:
   • Relation "a-un" (un livre A un système d'emprunt)
   • Classes avec états complexes
   • Besoin de flexibilité (changer de stratégie)
   • Hiérarchie qui devient confuse

🎯 RÈGLES D'OR:
   1. TOUJOURS utiliser super() dans __init__
   2. Vérifier le MRO avec ClassName.__mro__
   3. Composition > Héritage multiple (en général)
   4. Documenter vos choix
""")


# ============================================
# 8. EXERCICE SOLUTION
# ============================================

print("\n" + "=" * 70)
print("🎓 EXERCICE: AudioLivre")
print("=" * 70)

class AudioLivre(Empruntable, Reservable):
    """AudioLivre avec héritage multiple correct"""
    def __init__(self, titre, narrateur, duree_minutes):
        super().__init__(titre)
        self.narrateur = narrateur
        self.duree_minutes = duree_minutes
    
    def afficher_info(self):
        info = super().afficher_info()
        return f"{info} | 🎙️ {self.narrateur} | ⏱️ {self.duree_minutes}min"

print("\nCréation d'un AudioLivre:")
audio = AudioLivre("1984", "Jean Dupont", 720)

print(f"\nMRO d'AudioLivre: {[c.__name__ for c in AudioLivre.__mro__]}")

print("\nTests:")
print("  ", audio.emprunter("Alice"))
print("  ", audio.reserver("Bob"))
print("  ", audio.afficher_info())


# ============================================
# 9. VERSION COMPOSITION (Comparaison)
# ============================================

print("\n" + "=" * 70)
print("🔄 MÊME CHOSE avec Composition")
print("=" * 70)

class AudioLivreComposition:
    """Version composition du même AudioLivre"""
    def __init__(self, titre, narrateur, duree_minutes):
        self.titre = titre
        self.narrateur = narrateur
        self.duree_minutes = duree_minutes
        self.emprunt = GestionEmprunt()
        self.reservation = GestionReservation()
    
    def emprunter(self, utilisateur):
        return self.emprunt.emprunter(utilisateur)
    
    def reserver(self, utilisateur):
        return self.reservation.reserver(utilisateur)

audio_comp = AudioLivreComposition("Le Petit Prince", "Marie Martin", 180)
print("✓ AudioLivre (composition) créé")
print("  ", audio_comp.emprunter("Charlie"))

print("\n💡 Les deux approches fonctionnent, mais la composition est:")
print("   • Plus simple à comprendre")
print("   • Plus flexible")
print("   • Évite les problèmes de MRO")

print("\n" + "=" * 70)
print("✅ Fin de la démonstration")
print("=" * 70)