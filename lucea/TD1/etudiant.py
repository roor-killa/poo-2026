class Etudiant:
   universite = "Université des Antilles"
   nombre_etudiants = 0


   def __init__(self, nom, prenom, numero_etudiant, filiere):
      self.nom = nom
      self.prenom = prenom
      self.numero_etudiant = numero_etudiant
      self.filiere = filiere
      self.notes = {}
      Etudiant.nombre_etudiants += 1


   def ajouter_note(self, matiere, note):
      if matiere not in self.notes:
         self.notes[matiere] = []

      if note >= 0 and note <= 20:
         self.notes[matiere].append(note)
         return "La note a été ajouté a la matiere :" + matiere
      else:
         return "Note invalide"


   def calculer_moyenne(self):
      total_notes = 0
      nb_notes = 0
       
      for matiere, note in self.notes.items():
         total_notes += sum(note)
         nb_notes += len(note)

      if nb_notes > 0:
         self.moyenne = total_notes / nb_notes
         return "Moyenne général =" + self.moyenne
      else:
         return "Aucune note pour cet(te) étudiant(e)"
    

   def calculer_moyenne_matiere(self, matiere):
      nb_notes = len(self.notes[matiere])
      if nb_notes == 0:
         return "Aucune note pour cet(te) étudiant(e)"
      else :
         for i in range(nb_notes):
            total_notes += self.notes[matiere][i]

         moyenne = total_notes / nb_notes
         return "Moyenne pour la matiere :" + matiere + "=" + moyenne


   def est_admis(self, seuil=10):
      if self.moyenne < seuil:
         print("L'étudiant(e) n'est pas admis")
         return False
      else:
         print("L'étudiant(e) est admis")
         return True


   def obtenir_mention(self):
      if self.est_admis():
         if self.moyenne <= 12:
            self.mention = "Passable"
         elif self.moyenne <= 14:
            self.mention = "Asser bien"
         elif self.moyenne <= 16:
            self.mention = "Bien"
         else:
            self.mention = "Très bien"
         return "La mention de l'étudiant(e) est :" + self.mention
      else:
         return "L'étudiant(e) n'a pas de mention" 
      
   def comparer_avec(self, autre_etudiant):
      if self.moyenne > autre_etudiant.moyenne:
         return f"{self.nom, self.prenom, self.numero_etudiant} a une meilleur moyenne que {autre_etudiant.nom, autre_etudiant.prenom, autre_etudiant.numero_etudiant}"
      else:
         return f"{autre_etudiant.nom, autre_etudiant.prenom, autre_etudiant.numero_etudiant} a une meilleur moyenne que {self.nom, self.prenom, self.numero_etudiant}"

          
   #Affichage par -GPT5
   def __str__(self):
      lignes = [
         f"Nom : {self.nom} {self.prenom}",
         f"Numéro étudiant : {self.numero_etudiant}",
         f"Filière : {self.filiere}",
         f"Université : {Etudiant.universite}",
         f"Nombre total d'étudiants : {Etudiant.nombre_etudiants}"
         ]

      if hasattr(self, 'moyenne'):
         lignes.append(f"Moyenne générale : {self.moyenne:.2f}")
         if hasattr(self, 'mention'):
            lignes.append(f"Mention : {self.mention}")
      if self.notes:
         lignes.append("Notes par matière :")
         for matiere, notes in self.notes.items():
            lignes.append(f"  {matiere} : {notes}")
      return "\n".join(lignes)
