"""
Exercice 1.1 : Du procédural à l'objet - Gestion d'un compte bancaire
Conversion d'une approche procédurale à une approche orientée objet
"""

class CompteBancaire:
    """
    Classe représentant un compte bancaire.
    Gère le solde, l'historique des transactions et les opérations bancaires.
    """
    
    def __init__(self, numero, titulaire, solde_initial=0.0):
        """
        Initialise un compte bancaire.
        
        Args:
            numero (str): Le numéro IBAN du compte
            titulaire (str): Le nom du titulaire
            solde_initial (float): Le solde initial (par défaut 0)
        """
        self.__numero = numero
        self.__titulaire = titulaire
        self.__solde = solde_initial
        self.__historique = []
        if solde_initial > 0:
            self.__historique.append(f"Création du compte: +{solde_initial}€")
    
    def deposer(self, montant):
        """
        Effectue un dépôt sur le compte.
        
        Args:
            montant (float): Le montant à déposer
            
        Returns:
            float: Le nouveau solde après dépôt
            
        Raises:
            ValueError: Si le montant est négatif ou nul
        """
        if montant <= 0:
            raise ValueError("Le montant doit être positif")
        
        self.__solde += montant
        self.__historique.append(f"Dépôt: +{montant}€")
        return self.__solde
    
    def retirer(self, montant):
        """
        Effectue un retrait sur le compte.
        
        Args:
            montant (float): Le montant à retirer
            
        Returns:
            bool: True si le retrait a réussi, False sinon
        """
        if montant <= 0:
            raise ValueError("Le montant doit être positif")
        
        if montant > self.__solde:
            self.__historique.append(f"Tentative de retrait échouée: -{montant}€ (solde insuffisant)")
            return False
        
        self.__solde -= montant
        self.__historique.append(f"Retrait: -{montant}€")
        return True
    
    def virement(self, montant, autre_compte):
        """
        Effectue un virement vers un autre compte.
        
        Args:
            montant (float): Le montant à virer
            autre_compte (CompteBancaire): Le compte destinataire
            
        Returns:
            bool: True si le virement a réussi, False sinon
        """
        if not isinstance(autre_compte, CompteBancaire):
            raise TypeError("Le destinataire doit être un CompteBancaire")
        
        if self.retirer(montant):
            autre_compte.deposer(montant)
            self.__historique.append(f"Virement vers {autre_compte.__titulaire}: -{montant}€")
            return True
        return False
    
    def afficher_solde(self):
        """Affiche le solde actuel du compte."""
        print(f"Solde de {self.__titulaire}: {self.__solde}€")
        return self.__solde
    
    def afficher_historique(self):
        """Affiche l'historique des transactions."""
        print(f"\n=== Historique de {self.__titulaire} ({self.__numero}) ===")
        for operation in self.__historique:
            print(f"  • {operation}")
        print(f"Solde actuel: {self.__solde}€\n")
    
    def obtenir_solde(self):
        """Retourne le solde actuel sans l'afficher."""
        return self.__solde
    
    def obtenir_historique(self):
        """Retourne l'historique des transactions."""
        return self.__historique.copy()
    
    def __str__(self):
        """Représentation textuelle du compte."""
        return f"Compte {self.__numero} - {self.__titulaire} (Solde: {self.__solde}€)"


# === TESTS DU CODE ===
print("=" * 60)
print("EXERCICE 1.1 : DU PROCÉDURAL À L'OBJET - COMPTE BANCAIRE")
print("=" * 60)

# Création de deux comptes
alice = CompteBancaire("FR7630001007941234567890185", "Alice Dupont", 1000.0)
bob = CompteBancaire("FR7630001007941234567890186", "Bob Martin", 500.0)

# Test 1: Affichage des comptes
print("\n1. Affichage des comptes créés:")
print(f"  {alice}")
print(f"  {bob}")

# Test 2: Dépôt
print("\n2. Test de dépôt:")
nouveau_solde = alice.deposer(500)
print(f"  Alice dépose 500€, nouveau solde: {nouveau_solde}€")

# Test 3: Retrait valide
print("\n3. Test de retrait valide:")
succes = alice.retirer(300)
print(f"  Alice retire 300€: succès={succes}, nouveau solde={alice.obtenir_solde()}€")

# Test 4: Retrait échoué (solde insuffisant)
print("\n4. Test de retrait échoué (solde insuffisant):")
succes = alice.retirer(2000)
print(f"  Alice tente de retirer 2000€: succès={succes}, solde={alice.obtenir_solde()}€")

# Test 5: Virement
print("\n5. Test de virement:")
print(f"  Avant virement - Alice: {alice.obtenir_solde()}€, Bob: {bob.obtenir_solde()}€")
succes = alice.virement(400, bob)
print(f"  Alice vire 400€ à Bob: succès={succes}")
print(f"  Après virement - Alice: {alice.obtenir_solde()}€, Bob: {bob.obtenir_solde()}€")

# Test 6: Historique
print("\n6. Historiques complets:")
alice.afficher_historique()
bob.afficher_historique()

print("=" * 60)

# === EXPLICATIONS DES PROBLÈMES DU PROCÉDURAL ===
print("\n📋 PROBLÈMES DE L'APPROCHE PROCÉDURALE:")
print("""
1. ❌ Variables globales difficiles à gérer
   → Impossible d'avoir plusieurs comptes sans créer des dizaines de variables

2. ❌ Pas de protection des données
   → Quelqu'un peut modifier directement compte_solde = -1000 sans validation

3. ❌ Difficile de maintenir la cohérence
   → Si on oublie de mettre à jour l'historique dans une fonction, données incohérentes

4. ❌ Pas d'association logique des données et opérations
   → Les fonctions et variables ne sont pas liées conceptuellement

5. ❌ Problèmes de scalabilité (100 comptes = 400 variables!)
   → Code devient rapidement illisible et non maintenable

✅ AVANTAGES DE L'APPROCHE POO:
   • Chaque compte est une entité indépendante
   • Les attributs privés (__) sont protégés
   • Les données et méthodes sont logiquement groupées
   • Facile à étendre et maintenir
   • Scalabilité: gérer 1000 comptes = 1000 instances
""")
