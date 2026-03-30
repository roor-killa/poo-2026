from abc import ABC, abstractmethod
from typing import List


class PaymentMethod(ABC):
    """Interface pour les méthodes de paiement"""
    
    @abstractmethod
    def process_payment(self, amount: float) -> dict:
        """Traite un paiement"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retourne le nom de la méthode"""
        pass

class CreditCard(PaymentMethod):
    """Paiement par carte de crédit"""
    
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv
    
    def process_payment(self, amount: float) -> dict:
        print(f"💳 Traitement CB de {amount}€")
        print(f"   Carte: ****{self.card_number[-4:]}")
        return {
            'status': 'success',
            'method': self.get_name(),
            'amount': amount,
            'transaction_id': f"CC-{self.card_number[-4:]}-001"
        }
    
    def get_name(self) -> str:
        return "Carte de Crédit"


class PayPal(PaymentMethod):
    """Paiement via PayPal"""
    
    def __init__(self, email: str):
        self.email = email
    
    def process_payment(self, amount: float) -> dict:
        print(f"💰 Traitement PayPal de {amount}€")
        print(f"   Compte: {self.email}")
        return {
            'status': 'success',
            'method': self.get_name(),
            'amount': amount,
            'transaction_id': f"PP-{hash(self.email) % 10000}"
        }
    
    def get_name(self) -> str:
        return "PayPal"


class BankTransfer(PaymentMethod):
    """Paiement par virement"""
    
    def __init__(self, iban: str):
        self.iban = iban
    
    def process_payment(self, amount: float) -> dict:
        print(f"🏦 Traitement virement de {amount}€")
        print(f"   IBAN: {self.iban[:10]}...")
        return {
            'status': 'pending',
            'method': self.get_name(),
            'amount': amount,
            'transaction_id': f"BT-{self.iban[-4:]}-001",
            'estimated_days': 3
        }
    
    def get_name(self) -> str:
        return "Virement Bancaire"


class Cryptocurrency(PaymentMethod):
    """Paiement en crypto-monnaie"""
    
    def __init__(self, wallet_address: str, crypto_type: str = "BoKryptoNou"):

        self.wallet_address = wallet_address
        self.crypto_type = crypto_type
    
    def process_payment(self, amount: float) -> dict:
        print(f"₿ Traitement {self.crypto_type} de {amount}€")
        print(f"   Wallet: {self.wallet_address[:10]}...")
        return {
            'status': 'success',
            'method': self.get_name(),
            'amount': amount,
            'transaction_id': f"CRYPTO-{self.wallet_address[-6:]}"
        }
    
    def get_name(self) -> str:
        return f"Crypto ({self.crypto_type})"


# ============================================================================
# SYSTÈME DE COMMERCE - UTILISE LE POLYMORPHISME
# ============================================================================

class Order:
    """Commande"""
    
    def __init__(self, order_id: str, items: List[str], total: float):
        self.order_id = order_id
        self.items = items
        self.total = total
        self.payment_method = None
        self.payment_result = None
    
    def process_payment(self, payment_method: PaymentMethod):
        """
        Traite le paiement - POLYMORPHISME !
        Accepte n'importe quelle PaymentMethod
        """
        print(f"\n--- Commande {self.order_id} ---")
        print(f"Articles: {', '.join(self.items)}")
        print(f"Total: {self.total}€")
        print(f"Méthode: {payment_method.get_name()}")
        
        # Le polymorphisme en action
        self.payment_result = payment_method.process_payment(self.total)
        self.payment_method = payment_method
        
        if self.payment_result['status'] == 'success':
            print(f"✓ Paiement réussi!")
        else:
            print(f"⏳ Paiement en cours...")
        
        return self.payment_result


class ECommercePlatform:
    """Plateforme e-commerce"""
    
    def __init__(self):
        self.orders: List[Order] = []
    
    def create_order(self, order_id: str, items: List[str], 
                    total: float, payment_method: PaymentMethod):
        """
        Crée et traite une commande
        Le polymorphisme permet d'accepter n'importe quelle méthode de paiement
        """
        order = Order(order_id, items, total)
        order.process_payment(payment_method)
        self.orders.append(order)
        return order


# ============================================================================
# DÉMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SYSTÈME DE PAIEMENT - POLYMORPHISME EN ACTION")
    print("=" * 70)
    
    # Créer la plateforme
    platform = ECommercePlatform()
    
    # Différentes méthodes de paiement
    payment_methods = [
        CreditCard("1234567890123456", "123"),
        PayPal("marie@example.com"),
        BankTransfer("FR7612345678901234567890123"),
        Cryptocurrency("1A2B3C4D5E6F7G8H9I0J", "Bitcoin")
    ]
    
    # Traiter des commandes avec différentes méthodes
    items_list = [
        ["Livre POO", "Clavier"],
        ["Écran", "Souris"],
        ["Chaise de bureau"],
        ["GPU", "RAM 32GB"]
    ]
    
    for i, payment_method in enumerate(payment_methods, 1):
        order_id = f"ORD{i:03d}"
        platform.create_order(order_id, items_list[i-1], 
                            50.0 * i, payment_method)
    
    print("\n" + "=" * 70)
    print("AVANTAGES DU POLYMORPHISME:")
    print("- Code générique (Order ne connaît pas les détails)")
    print("- Facile d'ajouter de nouvelles méthodes de paiement")
    print("- Pas de if/elif pour chaque type")
    print("- Respect du principe Open/Closed (SOLID)")
    print("=" * 70)