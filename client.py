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
        print("Client connecte !")

        

    def _receive(self):
        # pour recevoir des donnees
        data = client.recv(1024) # taille de reception de donnees 
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



try:
    chat = Chat()
    try:
        cmd = sys.argv[1]
    except IndexError:
        cmd = '_receive'
    try:
        param = sys.argv[2]
    except IndexError:
        param = ''
    
    if len(sys.argv)>3:
        e = 3 
        while e < len(sys.argv):
            param = param + ' ' + sys.argv[e]
            e+=1

    handlers = {'send':chat._send,'receive':chat._receive,'connected':chat._connectedPeople}
    if cmd in handlers:
        handlers[cmd]() if param == '' else handlers[cmd](param)


    # recevoir des donnees

    while running:
        chat._receive()

except Exception as e:
    print("Connexion echouee", e)

finally:
    client.close()