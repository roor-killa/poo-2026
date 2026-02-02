class Animal:
    """Classe de base"""
    
    def __init__(self, name):
        self.name = name
    
    def make_sound(self):
        """Produit le cri de l'animal (méthode de base à redéfinir)"""
        return "Un son quelconque"
    
    def move(self):
        """Définit le déplacement de l'animal (méthode de base à redéfinir)"""
        return f"{self.name} se déplace"


class Dog(Animal):
    """Chien"""
    
    def make_sound(self):
        return "Woof! Woof!"
    
    def move(self):
        return f"{self.name} court en remuant la queue"


class Cat(Animal):
    """Chat"""
    
    def make_sound(self):
        return "Miaou!"
    
    def move(self):
        return f"{self.name} se déplace silencieusement"


class Bird(Animal):
    """Oiseau"""
    
    def make_sound(self):
        return "Cui cui!"
    
    def move(self):
        return f"{self.name} vole dans le ciel"


# ============================================================================
# DÉMONSTRATION DU POLYMORPHISME
# ============================================================================

def make_animal_perform(animal: Animal):
    """
    Fonction polymorphique.
    Grâce à l'héritage, cette fonction peut recevoir n'importe quel sous-type d'Animal.
    Elle appelle les méthodes sans savoir quel est l'animal spécifique.
    """
    print(f"\n{animal.name}:")
    print(f"  Son: {animal.make_sound()}")
    print(f"  Mouvement: {animal.move()}")


if __name__ == "__main__":
    print("=" * 70)
    print("CM3 - POLYMORPHISME PAR HÉRITAGE - DÉMONSTRATION")
    print("=" * 70)
    
    # Créer différents animaux
    animals = [
        Dog("Rex"),
        Cat("Minou"),
        Bird("Tweety"),
        Dog("Médor")
    ]
    
    # Polymorphisme en action
    print("\n--- Polymorphisme: même fonction, comportements différents ---")
    for animal in animals:
        make_animal_perform(animal)
    
    # Tous sont des Animal
    print("\n--- Vérification de type ---")
    for animal in animals:
        print(f"{animal.name} est un Animal ? {isinstance(animal, Animal)}")