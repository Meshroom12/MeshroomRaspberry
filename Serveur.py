import socket
import select
import threading

host='0.0.0.0'
port=8000
etat=True

def Lecture_Client(client,adresse):
    
    print("\n:: Connexion rentrante :: \nIP : {}" .format(adresse))
    
    msg_recu = client.recv(1024)
    msg_recu = msg_recu.decode()
    
    print("Reçu : {}".format(msg_recu))
    
    client.send(b"5 / 5")
    
    if msg_recu=="STOP":
        etat=False
    
    
    return 0



serveur = socket.socket()               # Création du serveur socket
serveur.bind((host, port))                # Création du lien de connexion
serveur.listen(5)
    
print("Le serveur écoute à présent sur le port {}".format(port))
    
while etat:
    
    try:
        Client, Adresse = serveur.accept()
        Lecture_Client(Client,Adresse)
        
    except:
        pass

serveur.close()
        
        
        
    