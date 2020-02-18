#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import select
import keyboard
import struct
import io
from PIL import Image
from PIL import ImageFile
import time

host='0.0.0.0'
port=8000
etat=True # Variable d'état ON/OFF du serveur
Liste_Client=[] # Liste de tout les clients connectés sur le serveur
Liste_IP=[]

ImageFile.LOAD_TRUNCATED_IMAGES=True

def Lecture_Nom(IP):
    MON=str()
    k=1
    while IP[-k]!=".":
        MON+=IP[-k]
        k+=1
    if len(MON)==2:
        MON+="0"
    NOM=''.join(reversed(MON))
    return NOM
    
    
def Consigne_Clients(Liste_Client, msg):
    for Cl in Liste_Client :
        Cl.send(msg)
    
    return 0

def Lecture_Client(client,adresse):
    # Fonction de lecture du client
    global etat 
    Nom=Lecture_Nom(adresse[0])
    i=0
    
    print(":: Client n°{} connecté ::" .format(Nom))
    
    while etat==True:
        
        i+=1
                
        # try :
        image_len = struct.unpack('<L', client.read(4))[0]
            # On recupère la taille de l'image codé sur 1024-bits non signé
        
            
        if not image_len:
            break
                # Si le client lui envoi une longueur de 0 -> on arrête la lecture
        
        print("Client : {}" .format(Nom), ":: Photo n°{}" .format(i))
        #print("Image_len = {}" .format(image_len))
        image_stream = io.BytesIO()
            # On créer le stream pour recevoir les datas
        image_stream.write(client.read(image_len))
            # On recupère l'image envoyé par le client dans le stream
            # On créer un fichier pour sauvegarder l'image sur le serveur
        image_stream.seek(0)
        
        image = Image.open(image_stream).convert("RGB")
        image.save("IMG" + Nom + "_" + str(i) + ".jpeg")
        
        del image_len        
        # except :
        #     print("\n:::::::::::::::::::::::::\n::  Erreur de lecture  ::")
        #     break
    
    print("\n:: Client n°{} déconnecté ::" .format(Nom))
    
    return 0



serveur = socket.socket()               # Création du serveur socket
serveur.bind((host, port))                # Création du lien de connexion
serveur.listen(5)

print("::: Ouverture du Serveur :::")    
print(":: Port de connexion {} ::\n".format(port))

while etat==True:
    
    Liste_Connexion, wlist, xlist = select.select([serveur],[],[],0.1)
    
    if keyboard.is_pressed("q"):
        etat=False
        msg=b"stop"
        Consigne_Clients(Liste_Client, msg)
    # Pour sortir de la boucle il faut presser la touche 'q'
        
    if keyboard.is_pressed("p"):
        msg=b"photo"
        Consigne_Clients(Liste_Client, msg)
        time.sleep(0.5)
        
    if keyboard.is_pressed("l"):
        
        print("\n:: Liste des clients connectés ::\n_______________________________________________________")
        for addr in Liste_IP:
            print("  Nom : {}\t".format(Lecture_Nom(addr[0])), "IP : {}\t".format(addr[0]), "Port : {}".format(addr[1]))
        print("\n")
    
    for Connexion in Liste_Connexion:
        
        Client, Adresse = serveur.accept()      # Ouverture d'une connexion
        Client_Co=Client.makefile('rb')
        Liste_Client.append(Client)
        Liste_IP.append(Adresse)
        time.sleep(0.5)
        
        try :
            threading._start_new_thread(Lecture_Client,(Client_Co,Adresse,))
            # Nouveau thread pour la gestion de ce nouveau client (Appelle de la fonction de lecture)
        except :
            pass

print("\n::::::::::::::::::::::::::")    
print(":: Fermeture du Serveur ::\n::::::::::::::::::::::::::")

for Client_Restant in Liste_Client :
    
    try:    
        Client_Restant.close()
        # On ferme toute les connexions clients
    except:
        pass

serveur.close()     # Fermeture du serveur 