import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}
groupes = {}

print("Serveur démarré...")
print("En attente des clients...")


def gerer_client(client, adresse):

    pseudo = None

    try:
        while True:
            pseudo = client.recv(1024).decode()

            if not pseudo:
                client.close()
                return

            if pseudo not in clients:
                clients[pseudo] = client
                client.send("OK".encode())
                print(pseudo, "est connecté :", adresse)
                break
            else:
                client.send("PSEUDO_EXISTE".encode())

        while True:

            message = client.recv(1024).decode()

            if not message:
                break

            if message == "quit":
                break

            elif message.startswith("/msg "):

                parties = message.split(" ", 2)

                if len(parties) < 3:
                    client.send(
                        "Utilisation : /msg pseudo message".encode()
                    )
                    continue

                destinataire = parties[1]
                texte = parties[2]

                if destinataire in clients:

                    message_prive = (
                        "[PRIVE] " + pseudo + " : " + texte
                    )

                    clients[destinataire].send(
                        message_prive.encode()
                    )

                    client.send(
                        ("Message envoyé à " + destinataire).encode()
                    )

                else:
                    client.send(
                        ("Utilisateur " + destinataire + " introuvable").encode()
                    )

            elif message.startswith("/create "):

                parties = message.split(" ", 1)

                if len(parties) < 2:
                    client.send(
                        "Utilisation : /create groupe".encode()
                    )
                    continue

                nom_groupe = parties[1]

                if nom_groupe in groupes:
                    client.send(
                        "Ce groupe existe déjà.".encode()
                    )

                else:
                    groupes[nom_groupe] = [pseudo]

                    client.send(
                        ("Groupe " + nom_groupe + " créé.").encode()
                    )

                    print(
                        pseudo,
                        "a créé le groupe",
                        nom_groupe
                    )

            elif message.startswith("/add "):

                parties = message.split(" ", 2)

                if len(parties) < 3:
                    client.send(
                        "Utilisation : /add groupe pseudo".encode()
                    )
                    continue

                nom_groupe = parties[1]
                nouveau_membre = parties[2]

                if nom_groupe not in groupes:
                    client.send(
                        "Groupe introuvable.".encode()
                    )

                elif nouveau_membre not in clients:
                    client.send(
                        "Utilisateur introuvable.".encode()
                    )

                elif nouveau_membre in groupes[nom_groupe]:
                    client.send(
                        "Utilisateur déjà dans le groupe.".encode()
                    )

                else:
                    groupes[nom_groupe].append(
                        nouveau_membre
                    )

                    client.send(
                        (
                            nouveau_membre
                            + " ajouté au groupe "
                            + nom_groupe
                        ).encode()
                    )

            elif message.startswith("/groupmsg "):

                parties = message.split(" ", 2)

                if len(parties) < 3:
                    client.send(
                        "Utilisation : /groupmsg groupe message".encode()
                    )
                    continue

                nom_groupe = parties[1]
                texte = parties[2]

                if nom_groupe not in groupes:
                    client.send(
                        "Groupe introuvable.".encode()
                    )
                    continue

                if pseudo not in groupes[nom_groupe]:
                    client.send(
                        "Vous n'êtes pas membre de ce groupe.".encode()
                    )
                    continue

                message_groupe = (
                    "[GROUPE "
                    + nom_groupe
                    + "] "
                    + pseudo
                    + " : "
                    + texte
                )

                for membre in groupes[nom_groupe]:

                    if membre in clients:
                        clients[membre].send(
                            message_groupe.encode()
                        )

            else:
                client.send(
                    "Commande inconnue.".encode()
                )

    except:
        pass

    finally:

        if pseudo in clients:
            del clients[pseudo]

        client.close()

        if pseudo:
            print(pseudo, "est déconnecté.")


while True:

    client, adresse = server.accept()

    thread = threading.Thread(
        target=gerer_client,
        args=(client, adresse)
    )

    thread.start()