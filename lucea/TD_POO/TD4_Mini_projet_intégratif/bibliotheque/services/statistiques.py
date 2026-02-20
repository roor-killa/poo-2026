from TD4_Mini_projet_intégratif.bibliotheque.services.notifications import Observateur # importation de la classe Observateur depuis le module notifications pour pouvoir implémenter une classe d'observateur qui suit les statistiques d'emprunts et de retours de documents dans la bibliothèque


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