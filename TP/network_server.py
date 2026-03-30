import socket
import json
import threading

from wallet import Wallet


class NetworkServer:
    def __init__(self, host: str, port: int, wallet: Wallet):
        # stocke lhost du serveur
        self.host = host

        # stocke le port du serveur
        self.port = port

        # stocke le wallet du serveur
        self.wallet = wallet

        # indique si le serveur tourne
        self.running = True

        # crée le socket tcp
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # évite les problèmes de port déjà utilisé après fermeture
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        # attache le serveur à lhost et au port
        self.server_socket.bind((self.host, self.port))

        # met le serveur en écoute
        self.server_socket.listen(5)

        print(f"\n🌐 serveur BKN démarré sur {self.host}:{self.port}")
        print(f"🏦 wallet {self.wallet.owner}")
        print(f"💰 solde initial {self.wallet.balance:.2f} BKN")
        print("en attente de connexions")

        # lance un thread pour les commandes locales
        command_thread = threading.Thread(target=self.handle_local_commands, daemon=True)
        command_thread.start()

        # boucle principale du serveur
        while self.running:
            try:
                # attend un client
                client_socket, client_address = self.server_socket.accept()

                print(f"\n🔗 connexion reçue depuis {client_address[0]}:{client_address[1]}")

                # traite le client dans un thread séparé
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()

            except OSError:
                break

            except Exception as e:
                print(f"❌ erreur serveur {e}")

    def handle_client(self, client_socket: socket.socket, client_address):
        try:
            # reçoit les données du client
            data = client_socket.recv(4096).decode("utf-8")

            if not data:
                client_socket.close()
                return

            # transforme le json reçu en dictionnaire
            request = json.loads(data)

            # traite la requête
            response = self.process_request(request)

            # renvoie la réponse au client
            client_socket.send(json.dumps(response).encode("utf-8"))

        except json.JSONDecodeError:
            error_response = {
                "status": "error",
                "message": "requête json invalide"
            }
            client_socket.send(json.dumps(error_response).encode("utf-8"))

        except Exception as e:
            error_response = {
                "status": "error",
                "message": f"erreur serveur {str(e)}"
            }
            try:
                client_socket.send(json.dumps(error_response).encode("utf-8"))
            except Exception:
                pass

        finally:
            client_socket.close()

    def process_request(self, request: dict) -> dict:
        # récupère laction demandée
        action = request.get("action")

        # retourne les infos du wallet
        if action == "get_info":
            return {
                "status": "success",
                "wallet": self.wallet.get_info()
            }

        # crédite le wallet serveur
        if action == "receive":
            amount = request.get("amount")
            from_address = request.get("from_address")

            # vérifie les champs requis
            if amount is None or from_address is None:
                return {
                    "status": "error",
                    "message": "champs manquants"
                }

            try:
                # crédite le wallet
                transaction_id = self.wallet.receive(float(amount), from_address)

                return {
                    "status": "success",
                    "message": f"réception de {float(amount):.2f} BKN confirmée",
                    "transaction_id": transaction_id,
                    "new_balance": self.wallet.balance
                }

            except ValueError as e:
                return {
                    "status": "error",
                    "message": str(e)
                }

        # action inconnue
        return {
            "status": "error",
            "message": "action inconnue"
        }

    def handle_local_commands(self):
        while self.running:
            try:
                command = input("\n[serveur] > ").strip().lower()

                if command == "info":
                    self.wallet.show_info()

                elif command == "hist":
                    self.wallet.show_history()

                elif command == "quit":
                    print("🛑 arrêt du serveur")
                    self.running = False
                    self.server_socket.close()
                    break

                else:
                    print("commandes disponibles info hist quit")

            except EOFError:
                break

            except Exception as e:
                print(f"❌ erreur commande {e}")


def main():
    print("🌐 SERVEUR DE WALLET BKN")

    # récupère les infos utilisateur
    owner = input("nom du propriétaire du wallet ").strip()
    if not owner:
        owner = "Alice"

    try:
        balance_input = input("solde initial BKN ")
        balance = float(balance_input) if balance_input else 1000.0
    except ValueError:
        print("❌ solde invalide")
        return

    host = input("host enter = localhost ").strip()
    if not host:
        host = "localhost"

    try:
        port_input = input("port enter = 5555 ").strip()
        port = int(port_input) if port_input else 5555
    except ValueError:
        print("❌ port invalide")
        return

    # crée le wallet du serveur
    wallet = Wallet(owner, balance, "SERVER")

    # crée et lance le serveur
    server = NetworkServer(host, port, wallet)

    try:
        server.start()
    except OSError as e:
        print(f"❌ impossible de démarrer le serveur {e}")
    except KeyboardInterrupt:
        print("\n🛑 serveur arrêté")


if __name__ == "__main__":
    main()