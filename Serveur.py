import socket
import select
import threading

host='0.0.0.0'
port=8000
etat=True

def Lecture_Client(client,iport):
    
    ip_client=iport[0]
    port_client=iport[1]
    
    print(":: Connexion rentrante :: \nClient : " .format(client))
    print("\nIP : " .format(ip_client))
    
    msg_recu = client.recv(1024)
    msg_recu = msg_recu.decode()
    
    print("Reçu {}".format(msg_recu))
    
    client.send("5 / 5")
    
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
        threading._start_new_thread(Lecture_Client(Client,Adresse))
        
    except:
        pass

serveur.close()
        
        
        
    