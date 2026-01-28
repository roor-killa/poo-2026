
class Document:
    """diamond'"""
    def __init__(self, titre):
        print(f"Document.__init__() appelé pour '{titre}'")
        self.titre = titre
    
    def afficher_info(self):
        return f"Document: {self.titre}"

class Empruntable(Document):
    """Première branche du diamond"""
    def __init__(self, titre):
        print("Empruntable.__init__() appelé")
        super().__init__(titre)  
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
        super().__init__(titre)  
        self.reservations = []
    
    def reserver(self, utilisateur):
        self.reservations.append(utilisateur)
        print(f"✓ Réservation ajoutée pour {utilisateur}")
    
    def afficher_info(self):
        info = super().afficher_info()
        nb_reservations = len(self.reservations)
        return f"{info} | Réservations: {nb_reservations}"


class LivreNumerique(Empruntable, Reservable):

    def __init__(self, titre, auteur, format_fichier):
        print(f"\n--- Création de LivreNumerique '{titre}' ---")
        super().__init__(titre)  
        self.auteur = auteur
        self.format_fichier = format_fichier
        print("--- Fin de la création ---\n")
    
    def afficher_info(self):
        info = super().afficher_info()
        return f"{info} | Auteur: {self.auteur} | Format: {self.format_fichier}"


print("=" * 70)
print("ANALYSE DU MRO (Method Resolution Order)")
print("=" * 70)

print("\nMRO de LivreNumerique:")
for i, cls in enumerate(LivreNumerique.__mro__, 1):
    print(f"  {i}. {cls.__name__}")

print("\n Signification:")
print("   Python cherche les méthodes dans cet ordre précis")
print("   Cela résout le diamond problem automatiquement!")

# 4. TEST : Création d'un objet

print("\n" + "=" * 70)
print("CRÉATION D'UN OBJET (observez l'ordre des appels)")
print("=" * 70)

livre = LivreNumerique("Python Avancé", "Guido van Rossum", "PDF")

# 5. TEST : Utilisation des méthodes

print("\n" + "=" * 70)
print("UTILISATION DES MÉTHODES")
print("=" * 70)

print("\nTest 1: Emprunt par Alice")
livre.emprunter("Alice")

print("\nTest 2: Tentative d'emprunt par Bob (doit échouer)")
livre.emprunter("Bob")

print("\nTest 3: Réservations")
livre.reserver("Charlie")
livre.reserver("David")

print(f"\nInformations complètes du livre:")
print(f"  {livre.afficher_info()}")

# ============================================
# 6. PROBLÈME POTENTIEL 
# ============================================

print("\n" + "=" * 70)
print("⚠️  PROBLÈME: Sans super() (MAUVAISE PRATIQUE)")
print("=" * 70)

class LivreNumeriqueProblematique(Empruntable, Reservable):
    """
     Mauvaise pratique : appel direct aux __init__ des parents
    """
    def __init__(self, titre, auteur, format_fichier):
        print(f"\n--- Création problématique '{titre}' ---")
        Empruntable.__init__(self, titre)  
        Reservable.__init__(self, titre)  
        # Document.__init__() sera appelé DEUX FOIS !
        self.auteur = auteur
        self.format_fichier = format_fichier
        print("--- Fin (problématique) ---\n")

print("\nCréation avec appels directs (PROBLÉMATIQUE):")
print("⚠️  Notez que Document.__init__() est appelé DEUX FOIS!")
livre_pb = LivreNumeriqueProblematique("Bad Practice", "Unknown", "EPUB")

# ============================================
# 7. ALTERNATIVE : COMPOSITION (souvent préférable)
# ============================================

print("\n" + "=" * 70)
print(" ALTERNATIVE RECOMMANDÉE: COMPOSITION")
print("=" * 70)

class GestionEmprunt:
    """Composant pour gérer les emprunts"""
    def __init__(self):
        self.emprunte_par = None
    
    def emprunter(self, utilisateur):
        if self.emprunte_par is None:
            self.emprunte_par = utilisateur
            print(f"✓ Composant: Emprunté par {utilisateur}")
            return True
        print(f"✗ Composant: Déjà emprunté par {self.emprunte_par}")
        return False

class GestionReservation:
    """Composant pour gérer les réservations"""
    def __init__(self):
        self.reservations = []
    
    def reserver(self, utilisateur):
        self.reservations.append(utilisateur)
        print(f"✓ Composant: Réservation ajoutée pour {utilisateur}")

class LivreNumeriqueComposition:

    def __init__(self, titre, auteur, format_fichier):
        print(f"\n--- Création par composition '{titre}' ---")
        self.titre = titre
        self.auteur = auteur
        self.format_fichier = format_fichier
        
        # Composition : "a-un" au lieu de "est-un"
        self.gestion_emprunt = GestionEmprunt()
        self.gestion_reservation = GestionReservation()
        print("--- Fin ---\n")
    
    def emprunter(self, utilisateur):
        return self.gestion_emprunt.emprunter(utilisateur)
    
    def reserver(self, utilisateur):
        self.gestion_reservation.reserver(utilisateur)
    
    def afficher_info(self):
        statut = f"emprunté par {self.gestion_emprunt.emprunte_par}" if self.gestion_emprunt.emprunte_par else "disponible"
        nb_reservations = len(self.gestion_reservation.reservations)
        return f"Livre: {self.titre} | Auteur: {self.auteur} | Format: {self.format_fichier} | Statut: {statut} | Réservations: {nb_reservations}"

print("Création avec composition (simple et clair):")
livre_comp = LivreNumeriqueComposition("Clean Code", "Robert Martin", "PDF")

print("\nTest de composition:")
livre_comp.emprunter("Eve")
livre_comp.reserver("Frank")
livre_comp.reserver("Grace")

print(f"\nInformations: {livre_comp.afficher_info()}")

# 8. COMPARAISON : Héritage vs Composition

print("\n" + "=" * 70)
print("COMPARAISON: HÉRITAGE MULTIPLE vs COMPOSITION")
print("=" * 70)


# ============================================
# 9. GUIDE DE DÉCISION
# ============================================

print("\n" + "=" * 70)
print("📚 QUAND UTILISER L'HÉRITAGE MULTIPLE ?")
print("=" * 70)



# ============================================
# 10. IMPLÉMENTATION DE L'EXERCICE
# ============================================

print("\n" + "=" * 70)
print("SOLUTION EXERCICE: AudioLivre avec héritage")
print("=" * 70)

class AudioLivre(Empruntable, Reservable):
    """AudioLivre avec héritage multiple - Diamond Problem"""
    
    def __init__(self, titre, auteur, narrateur, duree_minutes, format_audio):
        print(f"\n--- Création AudioLivre '{titre}' ---")
        super().__init__(titre)
        self.auteur = auteur
        self.narrateur = narrateur
        self.duree_minutes = duree_minutes
        self.format_audio = format_audio
        print("--- Fin ---\n")
    
    def afficher_info(self):
        info = super().afficher_info()
        return f"{info} | Auteur: {self.auteur} | Narrateur: {self.narrateur} | Durée: {self.duree_minutes}min | Format: {self.format_audio}"

print("MRO de AudioLivre:")
for i, cls in enumerate(AudioLivre.__mro__, 1):
    print(f"  {i}. {cls.__name__}")

print("\nCréation d'un AudioLivre:")
audio = AudioLivre("Sapiens", "Yuval Noah Harari", "François Morel", 480, "MP3")

print("\nUtilisation d'AudioLivre:")
audio.emprunter("Utilisateur1")
audio.reserver("Utilisateur2")
audio.reserver("Utilisateur3")

print(f"\nInfos: {audio.afficher_info()}")

# 11. RÉSUMÉ

print("\n" + "=" * 70)
print("📝 RÉSUMÉ DE L'HÉRITAGE MULTIPLE")
print("=" * 70)


print("\n" + "=" * 70)
print("✓ TOUS LES TESTS ET EXPLICATIONS SONT COMPLÉTÉS!")
print("=" * 70)