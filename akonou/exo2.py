

class Etudiant:
    
    # Attributs de classe (partagés par tous les étudiants)
    universite = "Université des Antilles"
    nombre_etudiants = 0
    
    def __init__(self, nom, prenom, numero_etudiant, filiere):
       
        self.__nom = nom
        self.__prenom = prenom
        self.__numero_etudiant = numero_etudiant
        self.__filiere = filiere
        self.__notes = {}  # Dictionnaire {matiere: [notes]}
        Etudiant.nombre_etudiants += 1
    
    def ajouter_note(self, matiere, note):
        
        if not 0 <= note <= 20:
            raise ValueError("La note doit être entre 0 et 20")
        
        if matiere not in self.__notes:
            self.__notes[matiere] = []
        
        self.__notes[matiere].append(note)
    
    def calculer_moyenne(self):
        """
        Calcule la moyenne générale de tous les résultats.
        
        Returns:
            float: La moyenne générale, 0 si aucune note
        """
        if not self.__notes:
            return 0.0
        
        toutes_les_notes = []
        for notes_matiere in self.__notes.values():
            toutes_les_notes.extend(notes_matiere)
        
        return sum(toutes_les_notes) / len(toutes_les_notes) if toutes_les_notes else 0.0
    
    def calculer_moyenne_matiere(self, matiere):
        """
        Calcule la moyenne pour une matière spécifique.
        
        Args:
            matiere (str): Le nom de la matière
            
        Returns:
            float: La moyenne de la matière, 0 si aucune note
        """
        if matiere not in self.__notes or not self.__notes[matiere]:
            return 0.0
        
        notes = self.__notes[matiere]
        return sum(notes) / len(notes)
    
    def est_admis(self, seuil=10):
        """
        Vérifie si l'étudiant est admis selon un seuil de moyenne.
        
        Args:
            seuil (float): La moyenne minimale requise (défaut: 10)
            
        Returns:
            bool: True si la moyenne >= seuil, False sinon
        """
        return self.calculer_moyenne() >= seuil
    
    def obtenir_mention(self):
        """
        Retourne la mention selon la moyenne générale.
        
        Returns:
            str: La mention (Passable, Assez bien, Bien, Très bien, ou Invalide)
        """
        moyenne = self.calculer_moyenne()
        
        if moyenne < 10:
            return "Invalide"
        elif moyenne < 12:
            return "Passable"
        elif moyenne < 14:
            return "Assez bien"
        elif moyenne < 16:
            return "Bien"
        else:
            return "Très bien"
    
    def comparer_avec(self, autre_etudiant):
        """
        Compare les moyennes avec un autre étudiant.
        
        Args:
            autre_etudiant (Etudiant): L'autre étudiant à comparer
            
        Returns:
            str: Un message de comparaison
        """
        if not isinstance(autre_etudiant, Etudiant):
            raise TypeError("L'argument doit être un Etudiant")
        
        ma_moyenne = self.calculer_moyenne()
        son_moyenne = autre_etudiant.calculer_moyenne()
        
        if ma_moyenne > son_moyenne:
            diff = ma_moyenne - son_moyenne
            return f"{self.__prenom} {self.__nom} a une meilleure moyenne (+{diff:.2f})"
        elif son_moyenne > ma_moyenne:
            diff = son_moyenne - ma_moyenne
            return f"{autre_etudiant.__prenom} {autre_etudiant.__nom} a une meilleure moyenne (+{diff:.2f})"
        else:
            return f"{self.__prenom} {self.__nom} et {autre_etudiant.__prenom} {autre_etudiant.__nom} ont la même moyenne"
    
    def __str__(self):
        """Représentation textuelle de l'étudiant."""
        moyenne = self.calculer_moyenne()
        mention = self.obtenir_mention()
        return (f"{self.__prenom} {self.__nom} ({self.__numero_etudiant}) - {self.__filiere}\n"
                f"  Moyenne: {moyenne:.2f}/20 | Mention: {mention}")
    
    def afficher_notes_detaillees(self):
        """Affiche toutes les notes par matière."""
        print(f"\n=== Notes de {self.__prenom} {self.__nom} ===")
        for matiere in sorted(self.__notes.keys()):
            notes = self.__notes[matiere]
            moyenne = self.calculer_moyenne_matiere(matiere)
            print(f"  {matiere}: {notes} (moyenne: {moyenne:.2f})")
        print()


class Promotion:
    """
    Classe représentant une promotion d'étudiants.
    Gère une liste d'étudiants et calcule des statistiques.
    """
    
    def __init__(self, nom, annee):
        """
        Initialise une promotion.
        
        Args:
            nom (str): Le nom de la promotion
            annee (int): L'année académique
        """
        self.__nom = nom
        self.__annee = annee
        self.__etudiants = []
    
    def ajouter_etudiant(self, etudiant):
        """Ajoute un étudiant à la promotion."""
        if not isinstance(etudiant, Etudiant):
            raise TypeError("L'argument doit être un Etudiant")
        self.__etudiants.append(etudiant)
    
    def calculer_moyenne_promotion(self):
        """Calcule la moyenne générale de la promotion."""
        if not self.__etudiants:
            return 0.0
        
        moyennes = [etudiant.calculer_moyenne() for etudiant in self.__etudiants]
        return sum(moyennes) / len(moyennes)
    
    def calculer_taux_reussite(self, seuil=10):
        """Calcule le taux de réussite de la promotion."""
        if not self.__etudiants:
            return 0.0
        
        reussis = sum(1 for etudiant in self.__etudiants if etudiant.est_admis(seuil))
        return (reussis / len(self.__etudiants)) * 100
    
    def obtenir_meilleur_etudiant(self):
        """Retourne l'étudiant avec la meilleure moyenne."""
        if not self.__etudiants:
            return None
        
        return max(self.__etudiants, key=lambda e: e.calculer_moyenne())
    
    def afficher_statistiques(self):
        """Affiche les statistiques de la promotion."""
        print(f"\n{'='*60}")
        print(f"STATISTIQUES DE LA PROMOTION {self.__nom} ({self.__annee})")
        print(f"{'='*60}")
        print(f"Nombre d'étudiants: {len(self.__etudiants)}")
        print(f"Moyenne de la promotion: {self.calculer_moyenne_promotion():.2f}/20")
        print(f"Taux de réussite (>=10): {self.calculer_taux_reussite():.1f}%")
        
        meilleur = self.obtenir_meilleur_etudiant()
        if meilleur:
            print(f"Meilleur étudiant: {meilleur} (moyenne: {meilleur.calculer_moyenne():.2f})")
        print(f"{'='*60}\n")


# === TESTS DU CODE ===
print("=" * 60)
print("EXERCICE 1.2")
print("=" * 60)

# Création d'étudiants
alice = Etudiant("Wisley", "Ali", "E12345", "Informatique")
bob = Etudiant("Ronaldo", "Ronaldo", "E12346", "Informatique")
carlos = Etudiant("Tevez", "Carlos", "E12347", "Informatique")

# Test 1: Affichage du nombre d'étudiants et de l'université
print(f"\nNombre d'étudiants: {Etudiant.nombre_etudiants}")
print(f"Université: {Etudiant.universite}")

# Test 2: Ajout de notes pour Alice
print("\n--- ALICE ---")
alice.ajouter_note("POO", 15)
alice.ajouter_note("Web", 14)
alice.ajouter_note("POO", 16)
alice.ajouter_note("Mobile", 13)

print(f"\nMoyenne générale d'Alice: {alice.calculer_moyenne():.2f}")
print(f"Moyenne POO d'Alice: {alice.calculer_moyenne_matiere('POO'):.2f}")
print(f"Alice admise (seuil=10)?: {alice.est_admis()}")
print(f"Mention d'Alice: {alice.obtenir_mention()}")
alice.afficher_notes_detaillees()

# Test 3: Ajout de notes pour Bob
print("--- BOB ---")
bob.ajouter_note("POO", 18)
bob.ajouter_note("Web", 17)
bob.ajouter_note("Mobile", 19)

print(f"\nMoyenne générale de Bob: {bob.calculer_moyenne():.2f}")
print(f"Mention de Bob: {bob.obtenir_mention()}")
bob.afficher_notes_detaillees()

# Test 4: Ajout de notes pour Carlos (mauvais étudiant)
print("--- CARLOS ---")
carlos.ajouter_note("POO", 8)
carlos.ajouter_note("Web", 7)
carlos.ajouter_note("Mobile", 6)

print(f"\nMoyenne générale de Carlos: {carlos.calculer_moyenne():.2f}")
print(f"Carlos admis (seuil=10)?: {carlos.est_admis()}")
print(f"Mention de Carlos: {carlos.obtenir_mention()}")

# Test 5: Comparaisons
print("\n--- COMPARAISONS ---")
print(alice.comparer_avec(bob))
print(alice.comparer_avec(carlos))

# Test 6: Affichage de tous les étudiants
print("\n--- AFFICHAGE DE TOUS LES ÉTUDIANTS ---")
print(alice)
print()
print(bob)
print()
print(carlos)

# Test 7: Création d'une promotion et statistiques
print("\n--- PROMOTION ---")
promotion = Promotion("INFO-2026", 2026)
promotion.ajouter_etudiant(alice)
promotion.ajouter_etudiant(bob)
promotion.ajouter_etudiant(carlos)

promotion.afficher_statistiques()

print("=" * 60)
