
#Classe Tortue
# Je vis dans
#MRO = [Tortue → Terrestre → Aquatique → Animal → object]

# Creer une classe Animal avec l'attribut vivant et affiche "Je suis un animal"
class Animal:
    def __init__(self):
        print("Je suis un animal")
        self.vivant = True

# Creer une classe Terrestre qui herite les methodes et attributs d'Animal et affiche "Je vis sur terre"
class Terrestre(Animal):
    def __init__(self):
        print("Je vis sur terre")
        super().__init__()  # Appelle Animal

# Creer une classe Aquatique qui herite les methodes et attributs d'Animal et affiche "Je vis dans l'eau"
class Aquatique(Animal):
    def __init__(self):
        print("Je vis dans l'eau")
        super().__init__() # Appelle Animal

# Creer une classe Tortue qui herite les methodes et attributs des classes Aquatique et Terrestre + affiche "Je suis une tortue"
class Tortue(Aquatique, Terrestre):
    def __init__(self):
        print("Je suis une tortue")
        super().__init__()

tortue1 = Tortue()
print(Tortue.__mro__,"\n") # Affiche : (<class '__main__.Tortue'>, <class '__main__.Aquatique'>, <class '__main__.Terrestre'>, <class '__main__.Animal'>, <class 'object'>)

# Tortue.__mro__ permet d'afficher la maniere que python cherche dans les differents classes