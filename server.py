import socket
import threading



SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5566 # le serveur n'a pas besoin d'adresse car il ne fait qu'ecouter

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((SERVER, PORT))
print("Le serveur est demarre ... ")


# pour gerer plusieur connexion de client simultanement 
class ClientsHandling(threading.Thread): 
    # elle herite de thread
    def __init__(self,conn,addr,clients = {}):
        threading.Thread.__init__(self)
        self.conn = conn 
        self.clients = clients
        self.host = addr[0]
        self.port = server.getsockname()[1]
    
    def run(self):
        data = self.conn.recv(1024) # taille de reception de donnees 
        data = data.decode("utf-8")
        print(data)
        self.clients[(self.host,self.port)] = data
        print(self.clients)
        if data =='c':
            #server.connect((self.host,self.port))
            msg = ""
            for client in self.clients:
                print('client', client)
                msg += client[0]
            self.conn.sendall(msg.encode("utf8"))

            


        



# boucle infinie pour que le serveur ecoute tant qu'une machine est connectee
while True:
    server.listen(5) # le parametre est le nombre de connexion qui peuvent echouer avant de refuser d'autres connexions
    conn, addr = server.accept() # on stocke les info de la machine qui est actuellement connectee au serveur adress contient ip et le port 
    print("Un client de la connexion {0} vient de se connecter sur le port {1}".format(addr[0],server.getsockname()[1]))


    my_thread = ClientsHandling(conn,addr)
    my_thread.start() # appelle la methode run de la classe ClientsHandling
   


conn.close()
server.close()