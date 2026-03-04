class etudiant:
    def __init__(self, nom,prenom, numetu):
        self.nom = nom
        self.prenom=prenom
        self.num_etu = numetu
        self.__notes = []

    def ajouter_note(self, __notes):
        if __notes < 0 or __notes > 20:
            print("Note invalide. La note doit être entre 0 et 20.") #ici si la note n'est pas comprise entre 0 et 20 elle n'est pas prise en compte 
        else:
            self.__notes.append(__notes)
    def calculer_moyenne(self):
        if not self.notes:
            return 0
        total = sum(self.notes)
        return total / len(self.notes)
        
    def est_admis(self, base=10):
        if self.calculer_moyenne() <base:
            return False
        else:
            return True
 


class promotion:
    def __init__(self, nom_promo=""):
        self.etudiants = []
        self.nom_promo = nom_promo

    def ajouter_etudiant(self, etudiant):
        self.etudiants.append(etudiant)
        etudiant.__class__.nombre_etudiants += 1  # Incrémente le nombre d'étudiants à chaque ajout

    def calculer_moyenne_promo(self):
        if not self.etudiants:
            return 0
        total_moyenne = sum(etudiant.calculer_moyenne() for etudiant in self.etudiants)
        return total_moyenne / len(self.etudiants)
    
    def lister_admis(self,):
        etu_admis = []
        for etudiant in self.etudiants:
            if etudiant.est_admis():
                etu_admis.append(etudiant)
        return etu_admis #ici on cree iune liste pour stocker les etudiants qui sont admis par "est_amis" on verifie si c'est true et on les affiche 
                
#q1 : Parce que sinon tous les etudiants vont partager la meme liste de notes car une liste de classe est partagée entre toutes les instances de la classe. 
#q2 :tous les objets partagent la même liste
#q3 : notes est encapsulée pour éviter les modifications donc il est privé de plus dans ajouter_notes il y a cette ligne :if __notes < 0 or __notes > 20:




    def taux_de_reussite(self, base=10):
        if not self.etudiants:
            return 0
        nombre_admis = len(self.lister_admis(base))
        return (nombre_admis / len(self.etudiants)) * 100
    
    def best_etu(self):
        if not self.etudiants:
            return None
        return max(self.etudiants, key=lambda etudiant: etudiant.calculer_moyenne())
    #key=lambda permet de definir une fonction anonyme pour extraire la moyenne de chaque etudiant pour la comparaison



#test
alice = etudiant("Alice","Dupont", "E00001", "Informatique")
bob= etudiant("Bob","Martin", "E00002", "Mathématiques")

#test attributs class
print(etudiant.nombre_etudiants)
print(alice.uni)

#test notes 
alice.ajouter_note("Mathématiques", 15)
alice.ajouter_note("Mathématiques", 20)
alice.ajouter_note("Informatique", 18)
bob.ajouter_note("Mathématiques", 9)
bob.ajouter_note("Informatique", 12)
bob.ajouter_note("Informatique", 14)
print(f"La moyenne générale d'Alice est : {alice.calculer_moyenne()}") #moy generale
print(f"La moyenne générale de Bob est : {bob.calculer_moyenne()}") #moy generale
print(f"La moyenne de Mathématiques d'Alice est : {alice.moyerne_matiere('Mathématiques')}")
print(f"La moyenne de Informatique de Bob est : {bob.moyerne_matiere('Informatique')}")

#test comparaison
difference = alice.comparer_etudiant(bob)
if difference > 0:
    print("Alice a une meilleure moyenne que Bob.")
elif difference < 0:
    print("Bob a une meilleure moyenne qu'Alice.")
else:
    print("Alice et Bob ont la même moyenne.")
#test promotion
promo = promotion("L1 Informatique")
promo.ajouter_etudiant(alice)
promo.ajouter_etudiant(bob)
print(f"Moyenne de la promotion: {promo.calculer_moyenne_promo()}")
admis = promo.lister_admis()
print("Étudiants admis:")
for etu in admis:
    print(etu)
print(f"Taux de réussite de la promotion: {promo.taux_de_reussite()}%")
best_student = promo.best_etu()
print(f"Le meilleur étudiant est : {best_student.nom} avec une moyenne de {best_student.calculer_moyenne()}")


#test admis et mention
alice.est_admis()
bob.est_admis()
print(f"Alice a obtenu la mention : {alice.obtention_mention()}")
print(f"Bob a obtenu la mention : {bob.obtention_mention()}")



#Challenge IA :
#Générez le code avec une IA de votre choix
#Identifiez 3 problèmes ou améliorations possibles dans le code généré
#Proposez et implémentez vos corrections


