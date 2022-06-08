import socket
import threading
import json



SERVER = socket.gethostbyname(socket.gethostname())
print("SERVER :")
print(SERVER)
PORT = 5577 # le serveur n'a pas besoin d'adresse car il ne fait qu'ecouter
print("PORT :")
print(PORT)


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((SERVER, PORT))
print("Le serveur est démarré ... ",sep='\n')
_connected_people = []


# pour gerer plusieur connexion de client simultanément 
class AppServer(threading.Thread): 
    # elle hérite de thread
    def __init__(self,conn,addr,client = {}):
        threading.Thread.__init__(self)
        self.conn = conn 
        self.client = client
        self.host = addr[0]
        self.port = server.getsockname()[1]

    def _connected_people(self):
        #il faut envoyer au client la liste _connected_people
        connected_people = {"Client0":'Michel',"Client1":'Donovan'}
        print("il faut envoyer au client la liste _connected_people")
        answer = json.dumps(connected_people).encode("utf-8")
        self.conn.send(answer)



    def _reply(self):
        pass

    def _receive(self):
        pass
        
    def run(self):
        handlers = {'reply':self._reply,'receive':self._receive,'connected':self._connected_people}
        options = {"_connected":self._connected_people}
        data = self.conn.recv(1024) # taille de reception de données 
        data = data.decode("utf-8")
        data = json.loads(data)
        #analyser le message recu
        print("DATA :")
        for key in data:
            if key in options:
                options[key]()
                print(options[key], "vient d'etre appellée")
        # if '_connected' in data.keys():
        #     print("C'est good")
        # if data[0]=='_':# dans ce cas il s'agit d'une commande 
        #     cmd = data[1:]
        #     if cmd in handlers:
        #         handlers[cmd]()
        # self.client[(self.host,self.port)] = json.loads(data)
        # username = self.client[(self.host,self.port)]['Username']

        # if username not in _connected_people:
        #     _connected_people.append(username)
        
        # content = self.client[(self.host,self.port)]
        # print ('Liste des clients connectés: ',_connected_people,sep='\n')
        print("Connected people",_connected_people)



            

# boucle infinie pour que le serveur ecoute tant qu'une machine est connectée
while True:
    server.listen(5) # le parametre est le nombre de connexion qui peuvent échouer avant de refuser d'autres connexions
    conn, addr = server.accept() # on stocke les info de la machine qui est actuellement connectée au serveur adress contient ip et le port 
    print(f"Un client de la connexion {addr[0]} vient de se connecter sur le port {server.getsockname()[1]}")
    
    _connected_people.append((conn,addr))
    
    # conn.send(answer)

    my_thread = AppServer(conn,addr)
    my_thread.start() # appelle la méthode run de la classe ClientsHandling
   


conn.close()
server.close()