from abc import ABC, abstractmethod


class SortStrategy(ABC):
    """Interface pour les stratégies de tri"""
    
    @abstractmethod
    def sort(self, data: List) -> List:
        pass


class BubbleSortStrategy(SortStrategy):
    """Tri à bulles"""
    
    def sort(self, data: List) -> List:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        print("Trié avec Bubble Sort")
        return arr


class QuickSortStrategy(SortStrategy):
    """Tri rapide"""
    
    def sort(self, data: List) -> List:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        print("Trié avec Quick Sort")
        return self.sort(left) + middle + self.sort(right)


class Sorter:
    """Contexte utilisant une stratégie"""
    
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy):
        """Change la stratégie à la volée"""
        self.strategy = strategy
    
    def sort(self, data: List) -> List:
        """Délègue le tri à la stratégie"""
        return self.strategy.sort(data)


# Démonstration
data = [64, 34, 25, 12, 22, 11, 90]

print("\n--- Strategy Pattern ---")
print(f"Données: {data}")

sorter = Sorter(BubbleSortStrategy())
result1 = sorter.sort(data)
print(f"Résultat: {result1}")

# Changer de stratégie
sorter.set_strategy(QuickSortStrategy())
result2 = sorter.sort(data)
print(f"Résultat: {result2}")