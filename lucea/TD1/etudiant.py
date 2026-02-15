import re

class Etudiant:
   universite = "Université des Antilles"
   compteur_total = 0


   def __init__(self, nom, prenom, numero_etudiant):
      self.nom = nom
      self.prenom = prenom
      if not re.fullmatch(r"E\d{5}", numero_etudiant):
            raise ValueError("Numéro étudiant invalide (format: E12345)")
      self.__numero_etudiant = numero_etudiant
      self._notes = []
      Etudiant.compteur_total += 1

   @classmethod
   def get_nombre_etudiants(cls):
      return cls.compteur_total
   

   @classmethod
   def changer_universite(cls, nouvelle_universite):
      cls.universite = nouvelle_universite
      return f"Université changée pour {Etudiant.universite}"


   @property
   def numero_etudiant(self):
      return self.__numero_etudiant


   def ajouter_note(self, note):
      if len(self._notes) >= 10:
        return "Nombre maximum de notes atteint (10)"
      
      if note >= 0 and note <= 20:
         self._notes.append(note)
         CompteurNotes.ajouter_note_historique(note)
         return "La note a été ajouté"
      else:
         return "Note invalide"


   @property
   def moyenne(self):
      if not self._notes:
         return None
      return sum(self._notes) / len(self._notes)


   def est_admis(self, seuil=10):
      if self.moyenne is None:
         print("Aucune note pour cet(te) étudiant(e)")
         return False

      if self.moyenne < seuil:
         print("L'étudiant(e) n'est pas admis")
         return False
      else:
         print("L'étudiant(e) est admis")
         return True


   def __str__(self):
      lignes = [
         f"Nom : {self.nom} {self.prenom}",
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
   def __init__(self, nom_promotion):
      self.nom_promotion = nom_promotion
      self.etudiants = []

   def ajouter_etudiant(self, etudiant):
      self.etudiants.append(etudiant)
      return "L'étudiant(e) a été ajouté à la promotion"
   
   def calculer_moyenne_promotion(self):
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

      
   
   def lister_admis(self):
      admis = []
      for etudiant in self.etudiants:
         if etudiant.est_admis():
            admis.append(etudiant)
      return admis


class CompteurNotes:
   historique = []


   @classmethod
   def ajouter_note_historique(cls, note):
      cls.historique.append(note)
      return "Note ajoutée à l'historique"
   
   @classmethod
   def statistiques(cls):
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
   
         
print(Etudiant.get_nombre_etudiants())  # 0

e1 = Etudiant("A", "A", "E00001")
e2 = Etudiant("B", "B", "E00002")
e3 = Etudiant("C", "C", "E00003")

print(Etudiant.get_nombre_etudiants())  # 3
print(e1.universite)  # Université des Antilles

Etudiant.changer_universite("UA - Campus de Schoelcher")
print(e2.universite)  # UA - Campus de Schoelcher

# Test statistiques
e1.ajouter_note(15)
e2.ajouter_note(12)
e3.ajouter_note(18)
print(CompteurNotes.statistiques())