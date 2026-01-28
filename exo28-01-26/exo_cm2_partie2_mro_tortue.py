
#Classe Tortue
# Je vis dans
#MRO = [Tortue → Terrestre → Aquatique → Animal → object]

class Animal:
    def __init__(self):
        print("Je suis un animal")
        self.vivant = True

class Terrestre(Animal):
    def __init__(self):
        print("Je vis sur terre")
        super().__init__()  # Appelle Animal

class Aquatique(Animal):
    def __init__(self):
        print("Je vis dans l'eau")
        super().__init__() # Appelle Animal

class Tortue(Aquatique, Terrestre):
    def __init__(self):
        print("Je suis une tortue")
        super().__init__()

#test

# Création d'une tortue
tortue1 = Tortue()

# Vérification de l'attribut hérité de Animal
print("Vivante :", tortue1.vivant)

# Affichage de l'ordre de résolution des méthodes (MRO)
print("\nOrdre MRO :")
for classe in Tortue.__mro__:
    print(classe)

# Vérification du type de l'objet
print("\nType de l'objet :", type(tortue1))