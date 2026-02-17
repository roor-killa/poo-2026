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


gestionnaire = GestionnaireNotifications()
gestionnaire.ajouter_canal(NotificationEmail())
gestionnaire.ajouter_canal(NotificationSMS())
gestionnaire.ajouter_canal(NotificationPush())

gestionnaire.notifier_tous("Votre livre est disponible", "marie@example.com")