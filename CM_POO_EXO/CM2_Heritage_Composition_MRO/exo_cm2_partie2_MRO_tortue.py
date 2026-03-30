
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

tortue1 = Tortue()
print(Tortue.__mro__,"\n")