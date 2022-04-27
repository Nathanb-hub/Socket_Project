from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image



"""
_____________________________________________________________________________________CLIENT SOCKET PART_____________________________________________________________________________________
"""
import socket 
import sys

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5566 # localhost est l'adresse du serveur local equivalent a l'ip 127.0.0.1

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
running = True




class Send:
    def __init__(self):
        
        print("Client connecté !")

        
    def _connect_to_server(self):
        client.connect((HOST,PORT)) # pour connecter le client au serveur
        self.conn = ((HOST,PORT)) 
    def _receive(self):
        # pour recevoir des données
        data = client.recv(1024) # taille de reception de données 
        data = data.decode("utf-8")
        if len(data)>0:
            print("Reponse du serveur :")
            print(data)
            running = False

    
    def _send(self,msg_dict):
        
        data = str(msg_dict).encode("utf-8")
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






"""

_____________________________________________________________________________________INTERFACE PART_____________________________________________________________________________________ 

"""
white = (1,1,1,1)
red = (1,0,0,1)
black = (0,0,0,0)
green = [0, 1, 0, 1] 
blue = [0, 0, 1, 1] 
purple = [1, 0, 1, 1] 

sm = ScreenManager()
send = Send()






class TestApp(App):
    def login(self,instance):
        """faire une form validation avec regex"""

        #stocker les users dans un json
        if (len(self.username.text)!=0) and (len(self.password.text)>5):
            self.page_manager(instance)
            #print(self.username.text,self.password.text)
        else: 
            self.info.text = "Infos non valides"

    def connect_to_server(self,instance):
        try:
            send._connect_to_server()
        except Exception():
            print("Already connected")

    def send(self,instance):
        # verifier qu'on soit connecter au serveur 
        try:
            send._send({'From':self.username.text,'message':self.message.text,'destinator':self.destinator.text})
        except:
            print("Not connected to server")
            self.send_info.text="Not connected to server"

    def page_manager(self,instance):
        pages = {'_login':'loginScreen','_send':'sendScreen'}
        sm.current = pages[instance.id]


    def build(self):
        #Initialisation des variables 
        self.contacts = []
        self.ids = {}

        """
                SCREEN FOR LOGIN 
        """
        #Home Screen
        _loginScreen = Screen(name="loginScreen")
        login_layout = BoxLayout(orientation='vertical',size_hint=(0.5,0.6),pos_hint={'center_x':0.5,'center_y':0.5})

        image = Image(source="logo.jfif")
        #USERNAME
        username_container = BoxLayout(orientation='vertical',size_hint=(1,0.2))
        self.username = TextInput(text='User',multiline=False,font_size=20)#background_color=black,foreground_color=white,cursor_color=white,
        
        
        username_container.add_widget(self.username)
  
        #PASSWORD
        password_container = BoxLayout(orientation='vertical',size_hint=(1,0.2))
        self.password = TextInput(text='Password',multiline=False,font_size=20)#background_color=black,foreground_color=white,cursor_color=white,
        
        password_container.add_widget(self.password)

        #SEND BUTTON
        send_btn = Button(text='Sign In',size_hint=(1,0.2),color=white,background_color=black)
        send_btn.id="_send"
        self.info = Label(text='',size_hint=(1,0.2),color=white)
        send_btn.bind(on_press=self.login)


        login_layout.add_widget(image)
        login_layout.add_widget(username_container)
        login_layout.add_widget(password_container)
        login_layout.add_widget(send_btn)
        login_layout.add_widget(self.info)

        #adding components to screen 
        _loginScreen.add_widget(login_layout)





        """
                SCREEN FOR SENDING MESSAGES
        """
        _sendScreen = Screen(name="sendScreen")
        send_layout = BoxLayout(orientation='vertical',size_hint=(0.8,0.6),pos_hint={'center_x':0.5,'center_y':0.5})#pos_hint={'center_x':0.5,'center_y':0.5}

        header_buttons = BoxLayout(orientation="horizontal")
        connect = Button(text="Connexion",size_hint=(0.3,0.2),color=green,background_color=white)
        connect.bind(on_press=self.connect_to_server)
        dontKnow = Button(text="dontKnow",size_hint=(0.3,0.2),color=white,background_color=white)
        dontKnow.bind(on_press=self.connect_to_server)
        login = Button(text="Back to login",size_hint=(0.3,0.2),color=blue,background_color=white)
        login.id = "_login"
        login.bind(on_press=self.page_manager)
        header_buttons.add_widget(connect)
        header_buttons.add_widget(dontKnow)
        header_buttons.add_widget(login)


        sender_label = Label(text="Envoyer un message",font_size=25)
        self.message = TextInput(text="",multiline=False,font_size=20,size_hint=(1,0.5))
        receiver_label = Label(text="à",font_size=25)
        self.destinator = TextInput(text="destinataire",multiline=False,font_size=20,size_hint=(1,0.5))
        send_btn = Button(text='Envoyer',size_hint=(1,0.2),color=white,background_color=black)
        send_btn.bind(on_press=self.send)
        self.send_info = Label(text='',size_hint=(1,0.2),color=white)



        send_layout.add_widget(header_buttons)
        send_layout.add_widget(sender_label)
        send_layout.add_widget(self.message)
        send_layout.add_widget(receiver_label)
        send_layout.add_widget(self.destinator)
        send_layout.add_widget(send_btn)
        send_layout.add_widget(self.send_info)

        _sendScreen.add_widget(send_layout)


        sm.add_widget(_loginScreen)
        sm.add_widget(_sendScreen)




        return sm







# try:
#     send = send()
#     handlers = {'send':send._send,'receive':send._receive,'connected':send._connectedPeople,'options':send._client_options}
    
#     try:
#         handlers['options']()
#         cmd = input("Que voulez vous faire ?")
#     except IndexError:
#         cmd = '_receive'
#     try:
#         param = sys.argv[2]
#     except IndexError:
#         param = ''
    
#     if len(sys.argv)>3:
#         e = 3 
#         while e < len(sys.argv):
#             param = param + ' ' + sys.argv[e]
#             e+=1

    
#     if cmd in handlers:
#         handlers[cmd]() if param == '' else handlers[cmd](param)


#     # recevoir des données

#     while running:
#         # action = input("Que voulez vous faire ?")
#         # display_client_options()
#         send._receive()
        

# except Exception as e:
#     print("Connexion échouée", e)

# finally:
#     client.close()


TestApp().run()