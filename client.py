import socket
import threading

HOST = "192.168.0.122"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:

    pseudo = input("Votre pseudo : ")

    client.send(pseudo.encode())

    reponse = client.recv(1024).decode()

    if reponse == "OK":
        print("Connexion réussie !")
        break

    else:
        print("Ce pseudo est déjà utilisé.")


def recevoir_messages():

    while True:

        try:

            message = client.recv(1024).decode()

            if not message:
                break

            print("\n" + message)

        except:
            break


thread_reception = threading.Thread(
    target=recevoir_messages
)

thread_reception.start()

print("/msg pseudo message")
print("/create groupe")
print("/add groupe pseudo")
print("/groupmsg groupe message")
print("quit")


while True:

    try:

        message = input("Votre message : ")

        client.send(message.encode())

        if message == "quit":
            break

    except:
        break


client.close()