# EXERCICE 2.1
class CompteBancaire:
    _taux_interet = 0.02  # 2%

    def __init__(self, numero, titulaire, solde_initial=0):
        if solde_initial < 0:
            raise ValueError("Solde initial négatif interdit")

        self.__numero = numero          # privé
        self._solde = solde_initial     # protégé
        self._titulaire = None
        self.titulaire = titulaire      # passe par le setter

    @property
    def numero(self):
        """Lecture seule du numéro"""
        return self.__numero

    @property
    def solde(self):
        """Lecture seule du solde"""
        return self._solde

    @property
    def titulaire(self):
        return self._titulaire

    @titulaire.setter
    def titulaire(self, nouveau_titulaire):
        if not isinstance(nouveau_titulaire, str):
            raise TypeError("Titulaire invalide")
        if len(nouveau_titulaire) < 2:
            raise ValueError("Nom trop court")
        self._titulaire = nouveau_titulaire

    def deposer(self, montant):
        if montant <= 0:
            raise ValueError("Montant doit être positif")
        self._solde += montant

    def retirer(self, montant):
        if montant <= 0:
            raise ValueError("Montant doit être positif")
        if montant > self._solde:
            raise ValueError("Solde insuffisant")
        self._solde -= montant

    def appliquer_interets(self):
        interets = self._solde * self._taux_interet
        self.deposer(interets)
        return interets

    @classmethod
    def changer_taux_interet(cls, nouveau_taux):
        if not 0 <= nouveau_taux <= 0.10:
            raise ValueError("Taux invalide")
        cls._taux_interet = nouveau_taux

#EXERCICE 2.2
import hashlib
from datetime import datetime, date

class Personne:
    def __init__(self, nom, prenom, date_naissance, email, telephone):
        # Utiliser les setters pour valider à l'initialisation
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.email = email
        self.telephone = telephone

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, valeur):
        """Valide et nettoie le nom"""
        if not isinstance(valeur, str):
            raise TypeError("Le nom doit être une chaîne")

        valeur = valeur.strip().title()
        if len(valeur) < 2:
            raise ValueError("Nom trop court")
        if not valeur.replace(" ", "").replace("-", "").isalpha():
            raise ValueError("Nom contient des caractères invalides")

        self._nom = valeur

    @property
    def prenom(self):
        return self._prenom

    @prenom.setter
    def prenom(self, valeur):
        """Même validation que nom"""
        if not isinstance(valeur, str):
            raise TypeError("Le prénom doit être une chaîne")

        valeur = valeur.strip().title()
        if len(valeur) < 2:
            raise ValueError("Prénom trop court")
        if not valeur.replace(" ", "").replace("-", "").isalpha():
            raise ValueError("Prénom contient des caractères invalides")

        self._prenom = valeur

    @property
    def date_naissance(self):
        return self._date_naissance

    @date_naissance.setter
    def date_naissance(self, valeur):
        """Valide la date de naissance"""
        if isinstance(valeur, str):
            jour, mois, annee = map(int, valeur.split('/'))
            valeur = date(annee, mois, jour)

        if not isinstance(valeur, date):
            raise TypeError("Date invalide")

        age = self._calculer_age(valeur)
        if not 0 <= age <= 150:
            raise ValueError(f"Âge invalide: {age} ans")

        self._date_naissance = valeur

    @property
    def age(self):
        """Propriété calculée en lecture seule"""
        return self._calculer_age(self._date_naissance)

    def _calculer_age(self, date_naiss):
        aujourd_hui = date.today()
        age = aujourd_hui.year - date_naiss.year
        if (aujourd_hui.month, aujourd_hui.day) < (date_naiss.month, date_naiss.day):
            age -= 1
        return age

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valeur):
        """Valide l'email"""
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', valeur):
            raise ValueError("Email invalide")
        self._email = valeur.lower()

    @property
    def telephone(self):
        return self._telephone

    @telephone.setter
    def telephone(self, valeur):
        """Valide et formate le téléphone français"""
        import re

        if not isinstance(valeur, str):
            raise TypeError("Téléphone invalide")

        numero = re.sub(r"[ .-]", "", valeur)

        if not re.match(r"^0[1-9]\d{8}$", numero):
            raise ValueError("Numéro de téléphone français invalide")

        self._telephone = "+33" + numero[1:]

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    def __str__(self):
        return f"{self.nom_complet}, {self.age} ans ({self.email})"


class CarteBancaire:
    def __init__(self, numero, titulaire, code_pin, plafond_journalier=300):
        self._numero = numero
        self._titulaire = titulaire
        self._code_pin_hash = self._hasher_pin(code_pin)
        self._plafond_journalier = plafond_journalier
        self._tentatives_restantes = 3
        self._bloquee = False
        self._retraits_jour = {}  # date -> montant
        self._historique = []

    def _hasher_pin(self, pin):
        return hashlib.sha256(str(pin).encode()).hexdigest()

    def verifier_pin(self, pin):
        if self._bloquee:
            raise PermissionError("Carte bloquée")

        if self._hasher_pin(pin) == self._code_pin_hash:
            self._tentatives_restantes = 3
            return True
        else:
            self._tentatives_restantes -= 1
            if self._tentatives_restantes == 0:
                self._bloquee = True
                raise PermissionError("Carte bloquée après 3 échecs")
            raise ValueError("PIN incorrect")

    def retirer(self, montant, pin):
        if montant <= 0:
            raise ValueError("Montant invalide")

        self.verifier_pin(pin)

        aujourd_hui = date.today()
        deja_retire = self._retraits_jour.get(aujourd_hui, 0)

        if deja_retire + montant > self._plafond_journalier:
            raise ValueError("Plafond journalier dépassé")

        self._retraits_jour[aujourd_hui] = deja_retire + montant
        self._historique.append(
            (datetime.now(), "RETRAIT", montant)
        )

        return montant

    def debloquer(self, pin_puk):
        # Code PUK fictif pour le TD
        if pin_puk == "0000":
            self._bloquee = False
            self._tentatives_restantes = 3
        else:
            raise ValueError("PUK incorrect")

    @property
    def retraits_aujourd_hui(self):
        return self._retraits_jour.get(date.today(), 0)

    @property
    def reste_disponible_aujourd_hui(self):
        return self._plafond_journalier - self.retraits_aujourd_hui
    

# Test EXERCICE 2.1
print("EXERCICE 2.1\n")
# Création du compte
compte = CompteBancaire("FR123", "Alice", 2500)

# Lecture OK
print("Solde du compte :",compte.solde,"€")    # 2500 €
print("Numéro du compte :",compte.numero)   # "FR123"

# Modification interdite du solde
try:
    compte.solde = 5000  # Doit échouer
except AttributeError:
    print("✓ Solde protégé")

# Modification interdite du numéro
try:
    compte.numero = "HACK"  # Doit échouer
except AttributeError:
    print("✓ Numéro protégé")

# Modification validée du titulaire
compte.titulaire = "Alice Dupont"
print("✓ Titulaire modifié")

# Validation du titulaire (trop court)
try:
    compte.titulaire = "A"
except ValueError as e:
    print(f"✓ Validation: {e}")

# Test des intérêts
interets = compte.appliquer_interets()
print(f"Intérêts: {interets}€")

# Changer le taux global
CompteBancaire.changer_taux_interet(0.03)
print("✓ Taux d'intérêt modifié\n")

#Test EXERCICE 2.2
print("EXERCICE 2.3\n")
# Création de la carte
carte = CarteBancaire("1234567890123456", "Alice", 1234)

print("=== VÉRIFICATION DU CODE PIN ===")

# 3 tentatives maximum
for tentative in range(3):
    pin = input("Entrez votre code PIN : ")

    try:
        carte.verifier_pin(pin)
        print("PIN correct")
        break
    except Exception as e:
        print("PIN incorrect")

# Si la carte est bloquée
if carte._bloquee:
    print("\nCarte bloquée après 3 échecs.")

    puk = input("Entrez le code PUK pour débloquer la carte : ")

    try:
        carte.debloquer(puk)
        print("Carte débloquée")
    except Exception:
        print("PUK incorrect – carte toujours bloquée")

# Tentative de retrait après déblocage
if not carte._bloquee:
    montant = float(input("\nMontant à retirer : "))

    try:
        carte.retirer(montant, input("Entrez à nouveau le PIN : "))
        print("Retrait effectué avec succès")
    except Exception as e:
        print("Retrait refusé :", e)

# Affichage final
print("\n=== RÉCAPITULATIF ===")
print("Total retiré aujourd'hui :", carte.retraits_aujourd_hui, "€")
print("Reste disponible aujourd'hui :", carte.reste_disponible_aujourd_hui, "€")

