import re

class Etudiant: 
   compteur_total = 0 # Attribut de classe pour compter le nombre total d'étudiants
   universite = "Université des Antilles" # Attribut de classe pour stocker le nom de l'université

   def __init__(self, nom, prenom, numero_etudiant): # Attributs d'instance pour le nom, prénom et numéro étudiant
      self.nom = nom
      self.prenom = prenom
      if not re.fullmatch(r"E\d{5}", numero_etudiant):
            raise ValueError("Numéro étudiant invalide (format: E12345)")
      self.__numero_etudiant = numero_etudiant
      self._notes = []
      Etudiant.compteur_total += 1

   @classmethod
   def get_nombre_etudiants(cls): # Méthode de classe pour obtenir le nombre total d'étudiants
      return cls.compteur_total
   

   @classmethod
   def changer_universite(cls, nouvelle_universite): # Méthode de classe pour changer l'université
      cls.universite = nouvelle_universite
      return f"Université changée pour {cls.universite}"


   @property
   def numero_etudiant(self): # Propriété pour accéder au numéro étudiant de manière sécurisée
      return self.__numero_etudiant


   def ajouter_note(self, note): # Méthode pour ajouter une note à l'étudiant, avec validation et mise à jour de l'historique des notes
      if len(self._notes) >= 10:
        return "Nombre maximum de notes atteint (10)"
      
      if note >= 0 and note <= 20:
         self._notes.append(note)
         CompteurNotes.ajouter_note_historique(note)
         return "La note a été ajouté"
      else:
         return "Note invalide"


   @property
   def moyenne(self): # Propriété pour calculer la moyenne des notes de l'étudiant, avec gestion du cas où il n'y a pas de notes
      if not self._notes:
         return None
      return sum(self._notes) / len(self._notes)


   def est_admis(self, seuil=10): # Méthode pour déterminer si l'étudiant est admis en fonction de sa moyenne et d'un seuil, avec gestion du cas où il n'y a pas de notes
      if self.moyenne is None:
         print("Aucune note pour cet(te) étudiant(e)")
         return False

      if self.moyenne < seuil:
         print("L'étudiant(e) n'est pas admis")
         return False
      else:
         print("L'étudiant(e) est admis")
         return True


   def __str__(self): # Méthode spéciale pour représenter l'étudiant sous forme de chaîne de caractères, avec affichage des informations et des notes
      lignes = [
         f"Nom : {self.nom}",
         f"Prénom : {self.prenom}",
         f"Numéro étudiant : {self.numero_etudiant}",
         f"Université : {Etudiant.universite}",
         f"Nombre total d'étudiants : {Etudiant.nombre_etudiants}"
      ]

      if self.moyenne is not None:
        lignes.append(f"Moyenne générale : {self.moyenne:.2f}")

      if self._notes:
         lignes.append("Notes :")
         for note in self._notes:
            lignes.append(f"  {note}")
      return "\n".join(lignes)


class Promotion: 
   def __init__(self, nom_promotion): # Attribut d'instance pour le nom de la promotion et une liste d'étudiants
      self.nom_promotion = nom_promotion
      self.etudiants = []

   def ajouter_etudiant(self, etudiant): # Méthode pour ajouter un étudiant à la promotion, avec vérification du type de l'objet et gestion du cas où l'étudiant n'est pas valide
      if not isinstance(etudiant, Etudiant):
         return "L'objet fourni n'est pas un étudiant valide"
      self.etudiants.append(etudiant)
      return "L'étudiant(e) a été ajouté à la promotion"
   
   def calculer_moyenne_promotion(self): # Méthode pour calculer la moyenne de la promotion en utilisant les moyennes des étudiants, avec gestion du cas où aucun étudiant n'a de moyenne
      total_moyennes = 0
      nb_etudiants = 0

      for etudiant in self.etudiants:
         if etudiant.moyenne is not None:
            total_moyennes += etudiant.moyenne
            nb_etudiants += 1

      if nb_etudiants > 0:
         moyenne_promotion = total_moyennes / nb_etudiants
         return f"Moyenne de la promotion {self.nom_promotion} : {moyenne_promotion:.2f}"
      else:
         return f"Aucun étudiant n'a de moyenne dans la promotion {self.nom_promotion}"

      
   
   def lister_admis(self): # Méthode pour lister les étudiants admis dans la promotion en utilisant la méthode est_admis de chaque étudiant
      admis = []
      for etudiant in self.etudiants:
         if etudiant.est_admis():
            admis.append(etudiant)
      return admis


class CompteurNotes:
   historique = []


   @classmethod
   def ajouter_note_historique(cls, note): # Méthode de classe pour ajouter une note à l'historique des notes
      cls.historique.append(note)
      return "Note ajoutée à l'historique"
   
   @classmethod
   def statistiques(cls): # Méthode de classe pour calculer les statistiques de l'historique des notes, avec gestion du cas où il n'y a pas de notes dans l'historique
      if cls.historique:
         min = cls.historique[0]
         max = cls.historique[0]
         moyenne = sum(cls.historique) / len(cls.historique)
      else:
         return "Aucune note dans l'historique"
      for note in cls.historique:
         if note < min:
            min = note
         if note > max:
            max = note
      return f"Statistiques de l'historique : Min = {min}, Max = {max}, moyenne = {moyenne:.2f}"