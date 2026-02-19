from abc import ABC, abstractmethod #importation de la classe ABC et du décorateur abstractmethod pour créer des classes abstraites et des méthodes abstraites


class Utilisateur(ABC):
    def __init__(self, nom, prenom, id_utilisateur): #constructeur de la classe Utilisateur qui prend en paramètres le nom, le prénom et l'identifiant de l'utilisateur
        self.nom = nom
        self.prenom = prenom
        self.id_utilisateur = id_utilisateur
        self.emprunts_actifs = []
    

    def emprunter(self, document): #méthode pour emprunter un document, elle vérifie si le nombre d'emprunts actifs est inférieur au nombre maximum d'emprunts autorisé, si oui, elle ajoute le document à la liste des emprunts actifs et retourne un message de confirmation, sinon elle retourne un message d'erreur
        if len(self.emprunts_actifs) < self.nombre_max_emprunts():
            self.emprunts_actifs.append(document)
            return "Emprunt enregistré"
        else:
            return "Nombre maximum d'emprunts atteint"
    

    def retourner(self, document): #méthode pour retourner un document, elle vérifie si le document est dans la liste des emprunts actifs, si oui, elle le retire de la liste et retourne un message de confirmation, sinon elle retourne un message d'erreur
        if document in self.emprunts_actifs:
            self.emprunts_actifs.remove(document)
            return "Retour enregistré"
        else:
            return "Document non enregistré dans les emprunts actifs"


    @abstractmethod
    def nombre_max_emprunts(self): #méthode abstraite pour définir le nombre maximum d'emprunts autorisé pour chaque type d'utilisateur, elle doit être implémentée dans les classes dérivées
        pass

    
    @abstractmethod
    def duree_max_emprunt(self): #méthode abstraite pour définir la durée maximale d'emprunt pour chaque type d'utilisateur, elle doit être implémentée dans les classes dérivées
        pass


    def __str__(self): #méthode pour retourner une représentation en chaîne de caractères de l'utilisateur, elle retourne le nom et le prénom de l'utilisateur
        return f"{self.nom} {self.prenom}"


class AccesSalleRecherche: #classe pour gérer l'accès à la salle de recherche, elle contient une méthode pour accéder à la salle de recherche qui retourne un message indiquant que l'utilisateur accède à la salle de recherche
    def acceder_salle_recherche(self):
        return f"{self.nom} {self.prenom} Accède à la salle de recherche"


class PrioriteReservation: #classe pour gérer la priorité de réservation, elle contient une méthode pour indiquer que l'utilisateur a une priorité de réservation élevée qui retourne un message indiquant que l'utilisateur a une priorité de réservation élevée
    def priorite_reservation(self, document):
        return f"{self.nom} {self.prenom} réserve {document} en priorité"
    

class Etudiant(Utilisateur): #classe pour représenter un étudiant, elle hérite de la classe Utilisateur, elle implémente les méthodes abstraites nombre_max_emprunts et duree_max_emprunt pour définir les règles d'emprunt spécifiques aux étudiants
    def __init__(self, nom, prenom, id_utilisateur):
        super().__init__(nom, prenom, id_utilisateur)


    def nombre_max_emprunts(self):
        return 5
    

    def duree_max_emprunt(self):
        return 21
    

    def __str__(self):
        return f"Étudiant : {super().__str__()}"


class Enseignant(Utilisateur): #classe pour représenter un enseignant, elle hérite de la classe Utilisateur, elle implémente les méthodes abstraites nombre_max_emprunts et duree_max_emprunt pour définir les règles d'emprunt spécifiques aux enseignants
    def __init__(self, nom, prenom, id_utilisateur):
        super().__init__(nom, prenom, id_utilisateur)


    def nombre_max_emprunts(self):
        return 10
    

    def duree_max_emprunt(self):
        return 60
    

    def __str__(self):
        return f"Enseignant : {super().__str__()}"


class Personnel(Utilisateur): #classe pour représenter un membre du personnel, elle hérite de la classe Utilisateur, elle implémente les méthodes abstraites nombre_max_emprunts et duree_max_emprunt pour définir les règles d'emprunt spécifiques aux membres du personnel
    def __init__(self, nom, prenom, id_utilisateur):
        super().__init__(nom, prenom, id_utilisateur)

        
    def nombre_max_emprunts(self):
        return 7
    

    def duree_max_emprunt(self):
        return 30
    

    def __str__(self):
        return f"Personnel : {super().__str__()}"