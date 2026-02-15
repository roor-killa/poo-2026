- Exercice du TD1 :

- Exercice 1 :
    - Q1 : notes doit être une liste car un étudiant peut avoir plusieurs notes.

    - Q2 : Si notes était un attribut de classe, toutes les instances de la classe Etudiant partageraient la même liste de notes.

    - Q3 : La méthode ajouter_note vérifie que la note est valide (entre 0 et 20) avant de l'ajouter à la liste des notes de l'étudiant.


- Exercice 2 :
    - Q1 : _attribut est une convention et reste accéssible depuis l'extérieur de la classe, tandis que __attribut utilise le name mangling pour rendre l'attribut plus difficile d'accès depuis l'extérieur.
    
    - Q2 : En python, on ne peut pas rendre un attribut totalement privé, on ne peut que simuler la confidentialité en utilisant des conventions de nommage et le name mangling.
    
    - Q3 : En python on préfere acceder a une donnée calculée comme si c'était un attributs plutot que d'utiliser des getters et setters (moyenne est une caractéristique pas une action).