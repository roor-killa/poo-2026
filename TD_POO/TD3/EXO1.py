# on importe ABC et abstractmethod pour créer une classe abstraite
from abc import ABC, abstractmethod


# -----------------------------
# Classe abstraite Notification
# -----------------------------

# Cette classe sert de modèle pour tous les types de notifications
class Notification(ABC):

    # méthode commune à toutes les notifications
    # elle ajoute le nom de la classe au message
    def formater_message(self, message):

        return f"[{self.__class__.__name__}] {message}"

    # méthode abstraite
    # chaque type de notification doit implémenter sa propre version
    @abstractmethod
    def envoyer(self, message, destinataire):
        pass


# -----------------------------
# Notification par Email
# -----------------------------

class NotificationEmail(Notification):

    def envoyer(self, message, destinataire):

        # on formate le message
        msg = self.formater_message(message)

        # simulation d'envoi
        print(f"Email envoyé à {destinataire} : {msg}")


# -----------------------------
# Notification par SMS
# -----------------------------

class NotificationSMS(Notification):

    def envoyer(self, message, destinataire):

        msg = self.formater_message(message)

        print(f"SMS envoyé à {destinataire} : {msg}")


# -----------------------------
# Notification Push (mobile)
# -----------------------------

class NotificationPush(Notification):

    def envoyer(self, message, destinataire):

        msg = self.formater_message(message)

        print(f"Notification PUSH à {destinataire} : {msg}")


# -----------------------------
# Gestionnaire de notifications
# -----------------------------

class GestionnaireNotifications:

    def __init__(self):

        # liste des canaux de notification
        self.notifications = []

    # ajouter un canal
    def ajouter_canal(self, notification):

        self.notifications.append(notification)

    # envoyer la notification sur tous les canaux
    def notifier_tous(self, message, destinataire):

        # on parcourt tous les canaux
        for notif in self.notifications:

            # polymorphisme : chaque objet utilise sa propre méthode envoyer()
            notif.envoyer(message, destinataire)


# -----------------------------
# TEST
# -----------------------------

gestionnaire = GestionnaireNotifications()

gestionnaire.ajouter_canal(NotificationEmail())
gestionnaire.ajouter_canal(NotificationSMS())
gestionnaire.ajouter_canal(NotificationPush())

gestionnaire.notifier_tous("Votre livre est disponible", "marie@example.com")