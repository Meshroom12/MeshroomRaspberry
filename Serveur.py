#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import select

host='0.0.0.0'
port=8000
etat=True # Variable d'état ON/OFF du serveur
Liste_Client=[] # Liste de tout les clients connectés sur le serveur


def Lecture_Client(client,adresse,numero):
    # Fonction de lecture du client
    global etat 
    global Liste_Client
    
    print("\n:: Connexion rentrante :: \nIP : {}" .format(adresse))
    print(":::::::::::::::::::::::::\n")
    
    msg_recu=""
    
    while msg_recu!="STOP" and msg_recu!="fin":
        
        # La lecture se ferme si le msg est "fin" ou "STOP"
        
        msg_recu = client.recv(1024)
        msg_recu = msg_recu.decode()
        
        print("Client {}".format(adresse))
        print("Reçu : {}\n".format(msg_recu))
        
        client.send(b"5 / 5")
    
        if msg_recu=="STOP":        # Si le serveur reçois "STOP", le serveur se termine
            etat=False
    
    Liste_Client[numero]=None
    client.close()
    print("\n:::::::::::::::::::::::::")
    print("\nIP : {}".format(adresse))
    print(":: Connexion sortante ::")
    
    return 0



serveur = socket.socket()               # Création du serveur socket
serveur.bind((host, port))                # Création du lien de connexion
serveur.listen(5)

print(":: Ouverture du Serveur ::")    
print(":: Port de connexion {} ::".format(port))
    
while etat==True:
    
    Liste_Connexion, wlist, xlist = select.select([serveur],[],[],0.1)
    for Connexion in Liste_Connexion:
        Client, Adresse = serveur.accept()      # Ouverture d'une connexion
        Liste_Client.append(Client)
        Numero=len(Liste_Client)-1
        threading._start_new_thread(Lecture_Client,(Client,Adresse,Numero))
        # Nouveau thread pour la gestion de ce nouveau client (Appelle de la fonction de lecture)
    
print(":: Fermeture du Serveur ::")
for Client_Restant in Liste_Client :
    if Client_Restant!=None:
        Client_Restant.close()
serveur.close()     # Fermeture du serveur 
        
        
        
    