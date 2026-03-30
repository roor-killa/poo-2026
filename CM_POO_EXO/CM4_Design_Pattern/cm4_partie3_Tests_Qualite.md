

## 📚 CM4 - Concepts avancés et bonnes pratiques (2h)

### Partie 3 : Tests et qualité (15min)

**Introduction aux tests unitaires**
```python
import unittest

class TestLivre(unittest.TestCase):
    def setUp(self):
        self.livre = Livre("1984", "Orwell", "123")
    
    def test_emprunt_disponible(self):
        self.assertTrue(self.livre.emprunter())
        self.assertFalse(self.livre.disponible)
    
    def test_emprunt_indisponible(self):
        self.livre.emprunter()
        self.assertFalse(self.livre.emprunter())
    
    def test_retour(self):
        self.livre.emprunter()
        self.livre.retourner()
        self.assertTrue(self.livre.disponible)
```

**Discussion : IA et tests**
- L'IA peut générer des tests, mais il faut vérifier la pertinence
- Importance des tests pour valider le code généré par IA

---