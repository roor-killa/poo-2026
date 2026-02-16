from abc import ABC, abstractmethod


class Utilisateur(ABC):
    def __init__(self, nom, prenom, id_utilisateur):
        self.nom = nom
        self.prenom = prenom
        self.id_utilisateur = id_utilisateur
        self.emprunts_actifs = []
    

    def emprunter(self, document):
        if len(self.emprunts_actifs) < self.nombre_max_emprunts():
            self.emprunts_actifs.append(document)
            return "Emprunt enregistré"
        else:
            return "Nombre maximum d'emprunts atteint"
    

    def retourner(self, document):
        if document in self.emprunts_actifs:
            self.emprunts_actifs.remove(document)
            return "Retour enregistré"
        else:
            return "Document non enregistré dans les emprunts actifs"

    @abstractmethod
    def nombre_max_emprunts(self):
        pass

    
    @abstractmethod
    def duree_max_emprunt(self):
        pass


    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Etudiant(Utilisateur):
    def __init__(self, nom, prenom, id_utilisateur):
        super().__init__(nom, prenom, id_utilisateur)


    def nombre_max_emprunts(self):
        return 5
    

    def duree_max_emprunt(self):
        return 21
    

    def __str__(self):
        return f"Étudiant : {super().__str__()}"
    

class Enseignant(Utilisateur):
    def __init__(self, nom, prenom, id_utilisateur):
        super().__init__(nom, prenom, id_utilisateur)


    def nombre_max_emprunts(self):
        return 10
    

    def duree_max_emprunt(self):
        return 60
    

    def __str__(self):
        return f"Enseignant : {super().__str__()}"


class Personnel(Utilisateur):
    def __init__(self, nom, prenom, id_utilisateur):
        super().__init__(nom, prenom, id_utilisateur)

        
    def nombre_max_emprunts(self):
        return 7
    

    def duree_max_emprunt(self):
        return 30
    

    def __str__(self):
        return f"Personnel : {super().__str__()}"
    

etudiant = Etudiant("Dupont", "Marie", "E12345")
enseignant = Enseignant("Martin", "Paul", "T001")

print(etudiant.nombre_max_emprunts())  # 5
print(enseignant.duree_max_emprunt())  # 60

etudiant.emprunter("Livre Python")
print(len(etudiant.emprunts_actifs))  # 1