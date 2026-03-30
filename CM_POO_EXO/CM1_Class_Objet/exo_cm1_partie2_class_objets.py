class Livre:
    # Attribut de classe
    nombre_total = 0
    
    def __init__(self, titre, auteur, isbn):
        # Attributs d'instance
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.disponible = True
        Livre.nombre_total += 1
    
    # Méthode d'instance
    def emprunter(self):
        if self.disponible:
            self.disponible = False
            return True
        return False
    
    def retourner(self):
        self.disponible = True
    
    # Méthode pour affichage
    def __str__(self):
        statut = "Disponible" if self.disponible else "Emprunté"
        return f"{self.titre} par {self.auteur} - {statut}"


## QUESTIONS ##
# - Différence entre `Livre.nombre_total` et `self.titre`
#        Livre.nombre_total est un attribute de class (elle appartiens a tous les instances et est trouvée dans la memoire une seule fois)
#        self.titre est un attribut de instance (elle est unique a chaque instance)
# - Quand utiliser des méthodes vs des attributs ?
#        les methodes sont des instruction en forme de fonction qui appartien a une class
#        alors que les attributes sont des variables reutilisable par de different instances.
