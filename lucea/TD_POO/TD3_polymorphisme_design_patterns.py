from abc import ABC, abstractmethod #importation de la classe ABC et du décorateur abstractmethod pour créer des classes abstraites et des méthodes abstraites


class Notification(ABC):
    @abstractmethod
    def envoyer(self, message, destinataire): #méthode abstraite qui doit être implémentée par les classes dérivées pour envoyer une notification à un destinataire donné
        pass


    def formater_message(self, message): #méthode concrète qui formate le message de notification en ajoutant le nom de la classe entre crochets
        return f"[{self.__class__.__name__}] {message}"
    

class NotificationEmail(Notification): #classe dérivée de Notification qui implémente la méthode envoyer pour envoyer une notification par email
    def envoyer(self, message, destinataire):
        return f"Envoi de la notification par email à {destinataire}: {self.formater_message(message)}"
    

class NotificationSMS(Notification): #classe dérivée de Notification qui implémente la méthode envoyer pour envoyer une notification par SMS
    def envoyer(self, message, destinataire):
        return f"Envoi de la notification par SMS à {destinataire}: {self.formater_message(message)}"
    

class NotificationPush(Notification): #classe dérivée de Notification qui implémente la méthode envoyer pour envoyer une notification par Push
    def envoyer(self, message, destinataire):
        return f"Envoi de la notification par Push à {destinataire}: {self.formater_message(message)}"
    

class GestionnaireNotifications: #classe qui gère les notifications en utilisant le polymorphisme pour envoyer des notifications à différents canaux de notification
    def __init__(self):
        self.notifications = []
    

    def ajouter_canal(self, notification): #méthode pour ajouter un canal de notification à la liste des notifications gérées par le gestionnaire
        self.notifications.append(notification)

    
    def notifier_tous(self, message, destinataire): #méthode pour envoyer une notification à tous les canaux de notification gérés par le gestionnaire en utilisant la méthode envoyer de chaque canal
        for notification in self.notifications:
            print(notification.envoyer(message, destinataire))


class Livre: #classe qui représente un livre avec des attributs tels que le titre, l'auteur, l'ISBN et le nombre de pages
    def __init__(self, titre, auteur, isbn, nb_pages):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.nb_pages = nb_pages


class Magazine: #classe qui représente un magazine avec des attributs tels que le titre, l'éditeur, le numéro et le mois de publication
    def __init__(self, titre, editeur, numero, mois):
        self.titre = titre
        self.editeur = editeur
        self.numero = numero
        self.mois = mois


class DVD: #classe qui représente un DVD avec des attributs tels que le titre, le réalisateur et la durée
    def __init__(self, titre, realisateur, duree):
        self.titre = titre
        self.realisateur = realisateur
        self.duree = duree


class Ebook: #classe qui représente un ebook avec des attributs tels que le titre, l'auteur, le format et la taille en Mo
    def __init__(self, titre, auteur, format, taille_mo):
        self.titre = titre
        self.auteur = auteur
        self.format = format
        self.taille_mo = taille_mo


class FabriqueDocument: #V1 classe qui implémente le design pattern de la fabrique pour créer des instances de différentes classes de documents en fonction d'un type de document donné
    @staticmethod
    def creer(type_doc, **kwargs):
        if type_doc == "livre":
            return Livre(**kwargs)
        elif type_doc == "magazine":
            return Magazine(**kwargs)
        elif type_doc == "dvd":
            return DVD(**kwargs)
        elif type_doc == "ebook":
            return Ebook(**kwargs)
        else:
            raise ValueError(f"Type de document inconnu : {type_doc}")


"""class FabriqueDocument: #V2 classe qui implémente le design pattern de la fabrique pour créer des instances de différentes classes de documents en fonction d'un type de document donné
    _types = {
        "livre": Livre,
        "magazine": Magazine,
        "dvd": DVD,
        "ebook": Ebook
    }
    
    @classmethod
    def creer(cls, type_doc, **kwargs):
        if type_doc in cls._types:
            return cls._types[type_doc](**kwargs)
        else:            
            raise ValueError(f"Type de document inconnu : {type_doc}")"""


class Observateur(ABC): #classe abstraite qui définit l'interface pour les observateurs qui souhaitent être notifiés des événements liés aux documents
    @abstractmethod
    def update(self, evenement):
        pass


class JournalEvenements(Observateur): #classe qui implémente l'interface Observateur pour enregistrer les événements liés aux documents dans un journal et les afficher à la console
    def __init__(self):
        self.journal = []
    

    def update(self, evenement):
        self.journal.append(evenement)
        print(f"[LOG] {evenement}")


class StatistiquesEmprunts(Observateur): #classe qui implémente l'interface Observateur pour suivre les statistiques d'emprunts et de retours de documents et les afficher à la console
    def __init__(self):
        self.nb_emprunts = 0
        self.nb_retours = 0

    def update(self, evenement): #méthode qui met à jour les statistiques d'emprunts et de retours en fonction de l'événement reçu et les affiche à la console
        if "a emprunté" in evenement:
            self.nb_emprunts += 1
        elif "a retourné" in evenement:
            self.nb_retours += 1
        print(f"[Stats] Emprunts: {self.nb_emprunts}, Retours: {self.nb_retours}")


class NotificateurUtilisateurs(Observateur): #classe qui implémente l'interface Observateur pour notifier les utilisateurs en attente lorsqu'un document est emprunté ou retourné et les afficher à la console
    def __init__(self):
        self.utilisateurs_en_attente = []

    def ajouter_utilisateur_en_attente(self, utilisateur): #méthode pour ajouter un utilisateur à la liste des utilisateurs en attente de notification
        self.utilisateurs_en_attente.append(utilisateur)

    def update(self, evenement): #méthode qui notifie les utilisateurs en attente de l'événement reçu et les affiche à la console, puis vide la liste des utilisateurs en attente
        for utilisateur in self.utilisateurs_en_attente:
            print(f"[Notification] {utilisateur} : {evenement}")
        self.utilisateurs_en_attente.clear()


class DocumentObservable: #classe qui représente un document observable qui peut être emprunté ou retourné, et qui notifie les observateurs des événements liés à ces actions
    def __init__(self, titre):
        self.titre = titre
        self._observateurs = []
    

    def ajouter_observateur(self, obs): #méthode pour ajouter un observateur à la liste des observateurs qui seront notifiés des événements liés au document
        self._observateurs.append(obs)
    

    def retirer_observateur(self, obs): #méthode pour retirer un observateur de la liste des observateurs qui seront notifiés des événements liés au document
        if obs in self._observateurs:
            self._observateurs.remove(obs)

    

    def notifier_observateurs(self, evenement): #méthode pour notifier tous les observateurs de l'événement reçu en appelant leur méthode update avec l'événement comme argument
        for obs in self._observateurs:
            obs.update(evenement)
    

    def emprunter(self, utilisateur): #méthode pour emprunter le document, qui génère un événement d'emprunt et notifie les observateurs de cet événement
        evenement = f"{utilisateur} a emprunté le document '{self.titre}'"
        self.notifier_observateurs(evenement)


    def retourner(self, utilisateur): #méthode pour retourner le document, qui génère un événement de retour et notifie les observateurs de cet événement
        evenement = f"{utilisateur} a retourné le document '{self.titre}'"
        self.notifier_observateurs(evenement)
