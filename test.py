class Livre:

    nombre_total = 0

    def __init__(self, titre, auteur, isbn):


        # PUBLIC
        self.titre = titre

        # PROTÉGÉ (convention)
        self._auteur = auteur

        # PRIVÉ (name mangling)
        self.__isbn = isbn

        # PUBLIC
        self.disponible = True

        Livre.nombre_total += 1


    def emprunter(self):
        if self.disponible:
            self.disponible = False
            print("Livre emprunté.")
            return True
        print("Livre déjà emprunté.")
        return False

    def retourner(self):
        self.disponible = True
        print("Livre retourné.")

    def afficher_infos(self):
        print(self)

  
    def _get_auteur(self):
        return self._auteur

 
    def __get_isbn(self):
        return self.__isbn


    def afficher_isbn(self):
        print("ISBN :", self.__get_isbn())

   
    def __str__(self):
        statut = "Disponible" if self.disponible else "Emprunté"
        return f"{self.titre} par {self._auteur} - {statut}"



if __name__ == "__main__":

    print("=== CRÉATION DU LIVRE ===")
    livre1 = Livre("1984", "George Orwell", "ISBN-123")

    print("\n=== ACCÈS AUX ATTRIBUTS ===")
    print("Titre (public) :", livre1.titre)
    print("Auteur (protégé) :", livre1._auteur)

    print("\n=== ACCÈS AU PRIVÉ VIA MÉTHODE ===")
    livre1.afficher_isbn()

    print("\n=== TEST DES MÉTHODES ===")
    livre1.afficher_infos()
    livre1.emprunter()
    livre1.afficher_infos()
    livre1.emprunter()
    livre1.retourner()
    livre1.afficher_infos()

    print("\n=== ATTRIBUT DE CLASSE ===")
    print("Nombre total de livres :", Livre.nombre_total)
