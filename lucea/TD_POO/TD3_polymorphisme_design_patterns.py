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


donnees = [
    {"type": "livre", "titre": "1984", "auteur": "Orwell", "isbn": "123", "nb_pages": 328},
    {"type": "magazine", "titre": "Science", "editeur": "Nature", "numero": 42, "mois": "Janvier"},
    {"type": "dvd", "titre": "Matrix", "realisateur": "Wachowski", "duree": 136}
]

documents = []
for data in donnees:
    type_doc = data.pop("type")
    doc = FabriqueDocument.creer(type_doc, **data)
    documents.append(doc)