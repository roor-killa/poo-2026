from abc import ABC, abstractmethod


class Animal(ABC):
    """Classe abstraite"""
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def make_sound(self):
        """Méthode abstraite : DOIT être implémentée"""
        pass
    
    @abstractmethod
    def move(self):
        """Méthode abstraite : DOIT être implémentée"""
        pass
    
    def sleep(self):
        """Méthode concrète : peut être utilisée telle quelle"""
        print(f"{self.name} dort")


# ✗ Impossible d'instancier une classe abstraite
# animal = Animal("Test")  # TypeError

class Bird(Animal):
    def toto(self):
        pass

    def make_sound(self):
        """Implémentation obligatoire"""
        print(f"{self.name} Cui cui") 

    def move(self):
        print("Je ne bouge pas, je vol !")

class Dog(Animal):
    """Classe concrète : implémente TOUTES les méthodes abstraites"""
    
    def make_sound(self):
        """Implémentation obligatoire"""
        print(f"{self.name} aboie: Woof!")
    
    def move(self):
        """Implémentation obligatoire"""
        print(f"{self.name} court")


class Cat(Animal):
    """Classe concrète"""
    
    def make_sound(self):
        print(f"{self.name} miaule: Miaou!")
    
    def move(self):
        print(f"{self.name} marche silencieusement")


# ✓ On peut maintenant instancier les classes concrètes
dog = Dog("Rex")
cat = Cat("Minou")
bird = Bird("Mika")

dog.make_sound()  # Woof!
dog.move()        # court
dog.sleep()       # dort (méthode concrète héritée)

cat.make_sound()  # Miaou!
cat.move()        # marche
cat.sleep()       # dort

bird.make_sound()
bird.move()