# ============================================
# VOTRE CODE ORIGINAL (avec problèmes)
# ============================================

print("=" * 70)
print("❌ VERSION ORIGINALE - Problèmes à identifier")
print("=" * 70)

class Livre:
    nombre_total = 0
    
    def __init__(self, titre, auteur, isbn):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.disponible = True
        Livre.nombre_total += 1

class Empruntable:
    def __init__(self):
        self.emprunte_par = None
    
    def emprunter(self, utilisateur):
        if self.emprunte_par is None:
            self.emprunte_par = utilisateur
            return True
        return False

class Reservable:
    def __init__(self):
        self.reservations = []
    
    def reserver(self, utilisateur):
        self.reservations.append(utilisateur)

class LivreNumeriqueProblematique(Livre, Empruntable, Reservable):
    def __init__(self, titre, auteur, isbn, format_fichier):
        Livre.__init__(self, titre, auteur, isbn)  # ❌ Appel direct
        Empruntable.__init__(self)                  # ❌ Appel direct
        Reservable.__init__(self)                   # ❌ Appel direct
        self.format_fichier = format_fichier

# Test
print("\n📊 MRO de LivreNumeriqueProblematique:")
for i, cls in enumerate(LivreNumeriqueProblematique.__mro__, 1):
    print(f"   {i}. {cls.__name__}")

print("\n🧪 Test de création:")
livre1 = LivreNumeriqueProblematique("Python", "Guido", "123", "PDF")
print(f"✓ Livre créé: {livre1.titre}")
print(f"✓ Attributs: emprunte_par={livre1.emprunte_par}, reservations={livre1.reservations}")

print("\n⚠️  PROBLÈMES IDENTIFIÉS:")
print("   1. Appels directs aux __init__ au lieu de super()")
print("   2. Pas de chaîne d'appels cohérente")
print("   3. Les classes parentes n'utilisent pas super() non plus")
print("   4. Erreur: Livre.__init__ prend 3 params, vous en passez 4!")


# ============================================
# VERSION CORRIGÉE (Meilleure pratique)
# ============================================

print("\n" + "=" * 70)
print("✅ VERSION CORRIGÉE - Utilisation de super()")
print("=" * 70)

class LivreV2:
    """Classe de base - MODIFIÉE pour utiliser super()"""
    nombre_total = 0
    
    def __init__(self, titre, auteur, isbn, **kwargs):
        # **kwargs permet de passer des arguments au suivant dans le MRO
        super().__init__(**kwargs)  # ✅ Appelle le suivant dans le MRO
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.disponible = True
        LivreV2.nombre_total += 1
        print(f"  → LivreV2.__init__() pour '{titre}'")

class EmpruntableV2:
    """Classe Empruntable - MODIFIÉE pour utiliser super()"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # ✅ Continue la chaîne
        self.emprunte_par = None
        print(f"  → EmpruntableV2.__init__()")
    
    def emprunter(self, utilisateur):
        if self.emprunte_par is None:
            self.emprunte_par = utilisateur
            self.disponible = False
            return f"✓ {utilisateur} a emprunté le livre"
        return f"✗ Déjà emprunté par {self.emprunte_par}"
    
    def rendre(self):
        if self.emprunte_par:
            utilisateur = self.emprunte_par
            self.emprunte_par = None
            self.disponible = True
            return f"✓ {utilisateur} a rendu le livre"
        return "✗ Le livre n'était pas emprunté"

class ReservableV2:
    """Classe Reservable - MODIFIÉE pour utiliser super()"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # ✅ Continue la chaîne
        self.reservations = []
        print(f"  → ReservableV2.__init__()")
    
    def reserver(self, utilisateur):
        self.reservations.append(utilisateur)
        return f"✓ Réservation de {utilisateur} enregistrée"
    
    def annuler_reservation(self, utilisateur):
        if utilisateur in self.reservations:
            self.reservations.remove(utilisateur)
            return f"✓ Réservation de {utilisateur} annulée"
        return f"✗ {utilisateur} n'a pas de réservation"

class LivreNumeriqueV2(LivreV2, EmpruntableV2, ReservableV2):
    """Version corrigée avec super()"""
    def __init__(self, titre, auteur, isbn, format_fichier):
        print(f"\n🔷 Création de LivreNumeriqueV2: '{titre}'")
        # ✅ Un seul appel à super(), qui déclenche toute la chaîne MRO
        super().__init__(titre=titre, auteur=auteur, isbn=isbn)
        self.format_fichier = format_fichier
        print(f"  → LivreNumeriqueV2.__init__() - Format: {format_fichier}")
        print("✅ Création terminée\n")
    
    def afficher_info(self):
        statut = "📕 Emprunté" if self.emprunte_par else "📗 Disponible"
        reservations = f"{len(self.reservations)} réservation(s)"
        return (f"{statut} | {self.titre} par {self.auteur} "
                f"| ISBN: {self.isbn} | Format: {self.format_fichier} "
                f"| {reservations}")

# Test de la version corrigée
print("\n📊 MRO de LivreNumeriqueV2:")
for i, cls in enumerate(LivreNumeriqueV2.__mro__, 1):
    print(f"   {i}. {cls.__name__}")

print("\n🧪 Test de création (observez l'ordre des appels):")
livre2 = LivreNumeriqueV2("Clean Code", "Robert Martin", "456", "EPUB")

print("🧪 Test des fonctionnalités:")
print(livre2.afficher_info())
print(livre2.emprunter("Alice"))
print(livre2.emprunter("Bob"))  # Devrait échouer
print(livre2.reserver("Charlie"))
print(livre2.reserver("David"))
print(livre2.afficher_info())
print(livre2.rendre())
print(livre2.afficher_info())


# ============================================
# ALTERNATIVE: COMPOSITION (Recommandée)
# ============================================

print("\n" + "=" * 70)
print("🎯 ALTERNATIVE RECOMMANDÉE: COMPOSITION")
print("=" * 70)

class GestionEmprunt:
    """Composant autonome pour gérer les emprunts"""
    def __init__(self):
        self.emprunte_par = None
    
    def emprunter(self, utilisateur):
        if self.emprunte_par is None:
            self.emprunte_par = utilisateur
            return f"✓ {utilisateur} a emprunté"
        return f"✗ Déjà emprunté par {self.emprunte_par}"
    
    def rendre(self):
        if self.emprunte_par:
            utilisateur = self.emprunte_par
            self.emprunte_par = None
            return f"✓ {utilisateur} a rendu"
        return "✗ Pas emprunté"
    
    def est_emprunte(self):
        return self.emprunte_par is not None

class GestionReservation:
    """Composant autonome pour gérer les réservations"""
    def __init__(self):
        self.reservations = []
    
    def reserver(self, utilisateur):
        if utilisateur not in self.reservations:
            self.reservations.append(utilisateur)
            return f"✓ Réservation de {utilisateur}"
        return f"✗ {utilisateur} a déjà réservé"
    
    def annuler(self, utilisateur):
        if utilisateur in self.reservations:
            self.reservations.remove(utilisateur)
            return f"✓ Annulation de {utilisateur}"
        return f"✗ Pas de réservation pour {utilisateur}"
    
    def nombre(self):
        return len(self.reservations)

class LivreNumeriqueComposition:
    """Version avec composition - Plus simple et flexible"""
    nombre_total = 0
    
    def __init__(self, titre, auteur, isbn, format_fichier):
        # Attributs du livre
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.format_fichier = format_fichier
        self.disponible = True
        
        # Composition: "a-un" au lieu de "est-un"
        self.gestion_emprunt = GestionEmprunt()
        self.gestion_reservation = GestionReservation()
        
        LivreNumeriqueComposition.nombre_total += 1
        print(f"✓ Livre '{titre}' créé (composition)")
    
    # Délégation aux composants
    def emprunter(self, utilisateur):
        resultat = self.gestion_emprunt.emprunter(utilisateur)
        if "✓" in resultat:
            self.disponible = False
        return resultat
    
    def rendre(self):
        resultat = self.gestion_emprunt.rendre()
        if "✓" in resultat:
            self.disponible = True
        return resultat
    
    def reserver(self, utilisateur):
        return self.gestion_reservation.reserver(utilisateur)
    
    def annuler_reservation(self, utilisateur):
        return self.gestion_reservation.annuler(utilisateur)
    
    def afficher_info(self):
        statut = "📕 Emprunté" if not self.disponible else "📗 Disponible"
        nb_res = self.gestion_reservation.nombre()
        return (f"{statut} | {self.titre} par {self.auteur} "
                f"| ISBN: {self.isbn} | Format: {self.format_fichier} "
                f"| {nb_res} réservation(s)")

# Test de la version composition
print("\n🧪 Test de la version composition:")
livre3 = LivreNumeriqueComposition("Design Patterns", "GoF", "789", "PDF")
print(livre3.afficher_info())
print(livre3.emprunter("Eve"))
print(livre3.reserver("Frank"))
print(livre3.reserver("Grace"))
print(livre3.afficher_info())


# ============================================
# COMPARAISON FINALE
# ============================================

print("\n" + "=" * 70)
print("📊 COMPARAISON DES TROIS APPROCHES")
print("=" * 70)

comparaison = """
1️⃣ VERSION ORIGINALE (Appels directs):
   ❌ Fragile (ordre des appels important)
   ❌ Difficile à maintenir
   ❌ Pas de chaîne MRO cohérente
   ❌ Erreur dans le nombre de paramètres

2️⃣ VERSION CORRIGÉE (super() + **kwargs):
   ✅ Respecte le MRO
   ✅ Chaîne d'initialisation correcte
   ✅ Flexible pour l'extension
   ⚠️  Complexe à comprendre
   ⚠️  Nécessite **kwargs dans toutes les classes

3️⃣ VERSION COMPOSITION:
   ✅ Simple et claire
   ✅ Flexible (facile de changer les composants)
   ✅ Pas de MRO à gérer
   ✅ Testable (composants indépendants)
   ✅ RECOMMANDÉE pour la plupart des cas

🎯 RECOMMANDATION:
   Pour votre cas (Livre avec emprunts/réservations):
   → Utilisez la COMPOSITION
   → Plus maintenable et compréhensible
"""

print(comparaison)

print("\n💡 Nombre total de livres créés:")
print(f"   LivreV2: {LivreV2.nombre_total}")
print(f"   Composition: {LivreNumeriqueComposition.nombre_total}")