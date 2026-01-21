class Livre:                     # Définition de la classe Livre

    nombre_total = 0             # Attribut de classe (commun à tous les livres)

    def __init__(self, titre, auteur, isbn):   # Constructeur
        if not titre or not auteur or not isbn:    # Vérification des paramètres
            raise ValueError("Champs obligatoires manquants")  # Erreur si vide

        self.titre = titre        # Attribut public
        self._auteur = auteur     # Attribut protégé (convention)
        self.__isbn = isbn        # Attribut privé (name mangling)
        self.disponible = True    # Indique si le livre est disponible

        Livre.nombre_total += 1   # Incrémente le nombre total de livres

    def emprunter(self):          # Méthode publique
        if not self.disponible:   # Vérifie si le livre est déjà emprunté
            raise Exception("Livre déjà emprunté")  # Lève une erreur
        self.disponible = False   # Change l'état du livre
        return True               # Retourne succès

    def retourner(self):          # Méthode publique
        if self.disponible:       # Vérifie si le livre est déjà retourné
            raise Exception("Livre déjà disponible")  # Lève une erreur
        self.disponible = True    # Rend le livre disponible

    def afficher_infos(self):     # Méthode publique
        print(self)               # Appelle __str__()

    def _get_auteur(self):        # Méthode protégée
        return self._auteur       # Retourne l'auteur

    def __get_isbn(self):         # Méthode privée
        return self.__isbn        # Retourne l'ISBN

    def afficher_isbn(self):      # Méthode publique
        print("ISBN :", self.__get_isbn())  # Accès sécurisé à l'ISBN

    def __str__(self):            # Méthode spéciale d'affichage
        statut = "Disponible" if self.disponible else "Emprunté"  # État du livre
        return f"{self.titre} par {self._auteur} - {statut}"      # Texte final


# =====================
# TEST DU PROGRAMME
# =====================
if __name__ == "__main__":        # Point d'entrée du programme

    try:
        livre1 = Livre("1984", "George Orwell", "ISBN-123")  # Création objet
        livre1.afficher_infos()   # Affiche les infos

        livre1.emprunter()        # Emprunt du livre
        livre1.afficher_infos()   # Affiche après emprunt

        livre1.emprunter()        # Erreur volontaire

    except Exception as e:        # Capture de l'erreur
        print("Erreur :", e)      # Affichage du message d'erreur

    try:
        livre1.retourner()        # Retour du livre
        livre1.retourner()        # Erreur volontaire

    except Exception as e:        # Capture de l'erreur
        print("Erreur :", e)      # Affichage du message

    print("Nombre total de livres :", Livre.nombre_total)  # Affiche le total
