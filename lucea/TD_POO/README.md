- Exercice des TD de POO :

- Exercice 1 :
    - Q1 : notes doit être une liste car un étudiant peut avoir plusieurs notes.

    - Q2 : Si notes était un attribut de classe, toutes les instances de la classe Etudiant partageraient la même liste de notes.

    - Q3 : La méthode ajouter_note vérifie que la note est valide (entre 0 et 20) avant de l'ajouter à la liste des notes de l'étudiant.


- Exercice 2 :
    - Q1 : _attribut est une convention et reste accéssible depuis l'extérieur de la classe, tandis que __attribut utilise le name mangling pour rendre l'attribut plus difficile d'accès depuis l'extérieur.
    
    - Q2 : En python, on ne peut pas rendre un attribut totalement privé, on ne peut que simuler la confidentialité en utilisant des conventions de nommage et le name mangling.
    
    - Q3 : En python on préfere acceder a une donnée calculée comme si c'était un attributs plutot que d'utiliser des getters et setters (moyenne est une caractéristique pas une action).


- Exercice 3 :
    - Q1 : Dans l'état actuel de la class Etudiant, si on ajoute 5 étudiants puis qu'on en supprime 2 compteur_total serait égal à 5.

    - Q2 : Il faudrait ajouter un Etudiant.compteur_total -= 1 a l'endroit de la suppression d'un étudiant pour que le compteur_total soit à jour.

    - Q3 : Si on change universite pour un etudiant (comme un attribut d'instance e1.universite), cela n'affectera pas les autres étudiants, car universite est un attribut de classe et non d'instance. Chaque étudiant peut avoir sa propre université sans affecter les autres.


Diagramme UML :
                    
                  Utilisateur
                       |
            ______________________
            |          |         |
        Etudiant   Enseignant   Personnel


- Exercice 4 :
    - Q1 : Utiliser super().__init__() dans les classes filles pour appeler le constructeur de la classe parent et éviter la redondance de code. De plus cela permet de garantir que les attributs de la classe parent sont correctement initialisés. Cela facilite également la maintenance du code, car si le constructeur de la classe parent change, les classes filles n'ont pas besoin d'être modifiées.

    - Q2 : Si on oublie d'appeler super().__init__() dans les classes filles, les attributs de la classe parent ne seront pas initialisés, ce qui peut entraîner des erreurs lors de l'accès à ces attributs ou lors de l'utilisation de méthodes qui dépendent de ces attributs.

    - Q3 : On ne peut pas créer une instance de Utilisateur car c'est une classe abstraite, elle est conçue pour être héritée et ne peut pas être instanciée directement. Les classes filles (Etudiant, Enseignant, Personnel) doivent implémenter les méthodes abstraites de la classe Utilisateur pour pouvoir être instanciées.


- Exercice 5 :
    - Q1 : Le MRO de la classe Doctorant affiche l'ordre d'appel des classes utilisées donc :
    (<class '__main__.Doctorant'>, <class '__main__.Utilisateur'>, <class 'abc.ABC'>, <class '__main__.AccesSalleRecherche'>, <class '__main__.PrioriteReservation'>, <class 'object'>)

    - Q2 : Python cherche les méthodes dans l'ordre dans laquelle les classes sont définies dans la déclaration de la classe Doctorant (Il prend également en compte les classes appelées par les classes parentes).

    - Q3 : Le Diamond Problem se produit avec l’héritage multiple quand une méthode est présente dans plusieurs parents, et Python le résout automatiquement grâce au MRO (C3 Linearization) qui définit un ordre unique pour rechercher les méthodes.


- Exercice 6 :
    - Q1 : L’approche A (héritage) permet de représenter clairement une hiérarchie, de réutiliser le code du parent, de bénéficier du polymorphisme et de clarifier les catégories de bibliothèques.

    - Q2 : L’approche B (composition) permet de créer des bibliothèques flexibles en assemblant des sections modulaires, de changer ou ajouter des composants facilement sans modifier la hiérarchie, et favorise la réutilisation et l’extensibilité du code.

    - Q3 : Je préfère l’approche B (composition) car elle est plus flexible, modulable et facilite l’extension ou la modification des bibliothèques sans dépendre d’une hiérarchie rigide.


- Exercice 7 :
    - Q1 : Dans cet exercice le polymorphisme permet d’utiliser différentes implémentations (Email, SMS, Push) via une même interface commune (Notification) sans modifier le code du gestionnaire.

    - Q2 : Notification est abstraite pour imposer une interface commune et forcer chaque type de notification à implémenter sa propre méthode d’envoi.

    - Q3 : On peut ajouter un nouveau canal en créant une nouvelle sous-classe de Notification et en l’ajoutant au gestionnaire, sans modifier le code existant.


- Exercice 8 :
    - Q1 : Le pattern Factory permet de découpler la création des objets de leur utilisation, rendant le code plus flexible et plus facile à maintenir.

    - Q2 : Pour ajouter un nouveau type, on crée la classe correspondante puis on ajoute son cas dans la méthode creer() de la fabrique.

    - Q3 : Oui, utiliser un dictionnaire permet d’associer dynamiquement un type à une classe et rend la factory plus propre, flexible et maintenable.


- Exercice 9 :
    - Q1 : Un observer notifie plusieurs abonnés lorsqu’il change tandisqu'un strategy change son comportement en choisissant dynamiquement une implémentation interchangeable.

    - Q2 : La liste d’observateurs permet de notifier dynamiquement tous les abonnés d’un événement, garantissant flexibilité et extensibilité.

    - Q3 : On peut éviter les références circulaires en stockant les observateurs sous forme de références faibles (weakref) ou en les retirant explicitement, ce qui permet au garbage collector de libérer les objets normalement.