# Transfert de données au serveur 

import json
import socket


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5577 # localhost est l'adresse du serveur local equivalent a l'ip 127.0.0.1

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

class Client_Handling:
    def __init__(self):
        pass
    
    def _connect_to_server(self):
        try:
            client.connect((HOST,PORT)) # pour connecter le client au serveur
            self.conn = ((HOST,PORT)) 
        except Exception:
            print("Deja connecté au serveur ")

    
    def _send(self,msg_dict):
        data = json.dumps(msg_dict).encode("utf-8")
        try:
            client.sendall(data)
            print(data)
        except:
            self._connect_to_server()
            self._send(msg_dict)
            print(data)


    # def _receive(self):
    #     # pour recevoir des données
    #     data = client.recv(1024) # taille de reception de données 
    #     data = data.decode("utf-8")
    #     if len(data)>0:
    #         print("Reponse du serveur :")
    #         print(data)
    #         running = False

    


    def _connectedPeople(self):
        request = "_connected_peoples".encode("utf8")
        client.sendall(request)
        self._receive()

    # def _client_options(self):
    #     print("1 : Envoyer un message")
    #     print("2 : Relever les derniers messages")
    #     print("3 : Quitter")