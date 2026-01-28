class Livre:
    # Attribut de classe
    nombre_total = 0
    
    def __init__(self, titre, auteur, isbn):
        # Attributs d'instance
        # Creer un object avec les attributs : titre, auteur, isbn ete disponible + ajoute 1 a l'attribut de classe nombre_total
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.disponible = True
        Livre.nombre_total += 1
    
    # Méthode d'instance
    # Verifie si le livre est disponible, si oui la fct retoure True et affecte False dans disponible sinon la fct retourne False
    def emprunter(self):
        if self.disponible:
            self.disponible = False
            return True
        return False
    
    # Méthode d'instance
    # Change la disponibilité du livre en Vrai
    def retourner(self):
        self.disponible = True
        
   # Méthode pour affichage
   # Sa nous permet quand on code print(Livre()), la console affiche un texte personnalisé : Titre par Auteur - Status
    def __str__(self):
        statut = "Disponible" if self.disponible else "Emprunté"
        return f"{self.titre} par {self.auteur} - {statut}"


livre1 = Livre("Peau noir et masque blanc", "Fanon", "E129N")
print(livre1) # Affiche Peau noir et masque blanc par Fanon - Disponible
print(livre1.emprunter()) # True prc le livre etait disponible donc il a ete emprunter
print(livre1.emprunter()) # False prc le livre etait pas disponible comme il a ete deja emprunter
livre1.retourner() 
print(livre1) # Livre disponible prc on la retourner