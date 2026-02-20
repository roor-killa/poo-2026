from TD4_Mini_projet_intégratif.bibliotheque.modeles.emprunt import Emprunt # importation de la classe Emprunt depuis le module emprunt
from TD4_Mini_projet_intégratif.bibliotheque.modeles.utilisateurs import Etudiant, Enseignant, Personnel  # importation des classes d'utilisateurs spécifiques pour pouvoir typer les utilisateurs de la bibliothèque
from TD4_Mini_projet_intégratif.bibliotheque.services.notifications import GestionnaireNotifications, JournalEvenements, NotificationEmail, NotificationSMS, NotificationPush, DocumentObservable # importation des classes de gestionnaire de notifications et d'observateur pour pouvoir gérer les notifications et les événements liés aux documents dans la bibliothèque
from datetime import datetime # Importation de la classe datetime pour gérer les dates et les calculs de durée




class Bibliotheque: #classe principale représentant la bibliothèque, elle contient les méthodes pour gérer les documents, les utilisateurs, les emprunts, les retours, les recherches et les statistiques
    def __init__(self, nom): 
        self.nom = nom
        self.catalogue = []
        self.utilisateurs = []
        self.emprunts_actifs = []
        self.historique = []
        self.gestionnaire_notifications = GestionnaireNotifications()

    
    def ajouter_document(self, document): #méthode pour ajouter un document à la bibliothèque, ajoute le document au catalogue et notifie les observateurs du document de son ajout
        self.catalogue.append(document)
        return f"Document {document.titre} ajouté à la bibliothèque {self.nom}"
    
    def emprunter(self, utilisateur, document): #méthode pour emprunter un document, vérifie les conditions d'emprunt, crée un nouvel emprunt, met à jour les listes d'emprunts actifs et d'emprunts de l'utilisateur, et notifie les observateurs 
        for emprunt in self.emprunts_actifs:
            if emprunt.document == document:
                if hasattr(document, "notifier_observateurs"):
                    evenement = f"Tentative échouée : {document.titre} déjà emprunté."
                    document.notifier_observateurs(evenement)
                return f"Le document {document.titre} est déjà emprunté."
        if len(utilisateur.emprunts_actifs) < utilisateur.nombre_max_emprunts():
            nouvel_emprunt = Emprunt(utilisateur, document, datetime.now())
            self.emprunts_actifs.append(nouvel_emprunt)
            utilisateur.emprunter(document)
            evenement = f"{utilisateur.nom} a emprunté {document.titre}"
            if hasattr(document, "notifier_observateurs"):
                document.notifier_observateurs(evenement)
            self.gestionnaire_notifications.notifier_tous(evenement, utilisateur.nom)
            return evenement
        else:
            evenement = f"{utilisateur.nom} a atteint sa limite d'emprunts."
            if hasattr(document, "notifier_observateurs"):
                document.notifier_observateurs(evenement)
            return evenement
        
    
    def retourner(self, emprunt):
        # Calculer frais
        # Mettre à jour statuts
        # Notifier observateurs
        pass
    
    def rechercher_document(self, critere):
        # ...
        pass
    
    def statistiques(self):
        # Documents par type
        # Emprunts par utilisateur
        # Taux d'utilisation
        pass