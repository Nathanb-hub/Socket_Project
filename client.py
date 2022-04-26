import socket 
import sys

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5566 # localhost est l'adresse du serveur local equivalent a l'ip 127.0.0.1

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
running = True

class Chat:
    def __init__(self):
        client.connect((HOST,PORT)) # pour connecter le client au serveur
        self.conn = ((HOST,PORT)) 
        print("Client connecté !")

        

    def _receive(self):
        # pour recevoir des données
        data = client.recv(1024) # taille de reception de données 
        data = data.decode("utf-8")
        if len(data)>0:
            print("Reponse du serveur :")
            print(data)
            running = False

    
    def _send(self,msg):
        data = msg.encode("utf-8")
        client.sendall(data)
        print(data)

    def _connectedPeople(self):
        request = "c".encode("utf8")
        client.sendall(request)
        self._receive()

    def _client_options(self):
        print("1 : Envoyer un message")
        print("2 : Relever les derniers messages")
        print("3 : Quitter")






