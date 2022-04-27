import socket
import threading



SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5566 # le serveur n'a pas besoin d'adresse car il ne fait qu'ecouter

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((SERVER, PORT))
print("Le serveur est démarré ... ")


# pour gerer plusieur connexion de client simultanément 
class ClientsHandling(threading.Thread): 
    # elle hérite de thread
    def __init__(self,conn,addr,clients = {}):
        threading.Thread.__init__(self)
        self.conn = conn 
        self.clients = clients
        self.host = addr[0]
        self.port = server.getsockname()[1]
    
    def run(self):
        data = self.conn.recv(1024) # taille de reception de données 
        data = data.decode("utf-8")
        #print("Data : \n",data)
        self.clients[(self.host,self.port)] = data
        print(self.clients)
        if data =='c':
            #server.connect((self.host,self.port))
            msg = ""
            for client in self.clients:
                print('client', client)
                msg += client[0]
            self.conn.sendall(msg.encode("utf8"))

            

# boucle infinie pour que le serveur ecoute tant qu'une machine est connectée
while True:
    server.listen(5) # le parametre est le nombre de connexion qui peuvent échouer avant de refuser d'autres connexions
    conn, addr = server.accept() # on stocke les info de la machine qui est actuellement connectée au serveur adress contient ip et le port 
    print(f"Un client de la connexion {addr[0]} vient de se connecter sur le port {server.getsockname()[1]}")


    my_thread = ClientsHandling(conn,addr)
    my_thread.start() # appelle la méthode run de la classe ClientsHandling
   


conn.close()
server.close()