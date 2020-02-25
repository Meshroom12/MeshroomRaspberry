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
import numpy as np
import Motor as m

host='0.0.0.0'
port=8000
etat=True # Variable d'état ON/OFF du serveur
Liste_Client=[] # Liste de tout les clients connectés sur le serveur
Liste_IP=[]

ImageFile.LOAD_TRUNCATED_IMAGES=True

def Nb_photos():
    n=input("Nombre de photos : ")
    return n

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
    global Liste_IP
    global Nb_Ph
    global Client_fini
    global Cpt
    global T
    
    Nom=Lecture_Nom(adresse[0])
    i=0
    
    
    print(":: Client n°{} connecté ::" .format(Nom))
    
    while etat==True:
        
        i+=1
                
        try :
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
            image.save("IMG" + "_" + T + "_" + Nom + "_" + str(i) + ".jpeg")
            
            Client_fini+=1
            # Dès que la photo est prise, on incrémente Client_fini de 1
            # Tant que cette variable n'est pas égale au nombre de client, on attend.        
            while Client_fini != len(Liste_IP):
                time.sleep(0.25)
            
            del image_len  
            
            if Cpt==Nb_Ph:
                while Cpt!=0:
                    time.sleep(0.1)
                    # Dès que le nombre de photo (par client) correspond à ce qui était voulu,
                    # on attend un reset.
        except :
            print("\n::  Erreur de lecture  ::\n:: Client n°{} ::\n" .format(Nom))
            break
        
        

    
    x,y=np.where(Liste_IP==Nom)
    Liste_IP=np.delete(Liste_IP,x[0],axis=0)
    print("\n:: Client n°{} déconnecté ::" .format(Nom))
    
    return 0



serveur = socket.socket()               # Création du serveur socket
serveur.bind((host, port))                # Création du lien de connexion
serveur.listen(5)

print("::: Ouverture du Serveur :::")    
print(":: Port de connexion {} ::\n".format(port))

Nb_Ph=Nb_photos()
Client_fini=0
Cpt=0
T=hex(int(time.time()))[6:10]

while etat==True:
    
    Liste_Connexion, wlist, xlist = select.select([serveur],[],[],0.1)
    
    if Client_fini == len(Liste_IP):
        # Dès que tout les clients ont pris leur photo, on réalise la rotation
        m.Rotation(1./Nb_Ph)
        # On réinitialise le compteur Client_fini et on incrémente Cpt de 1
        Client_fini=0
        Cpt=+1
    
    if Cpt==Nb_Ph:
        # Dès que Cpt==Nb_Ph, ça veut dire qu'on a pris toute les photos
        time.sleep(0.5)
        # On attend juste une nouvelle valeur pour recommencer.
        Nb_Ph=Nb_photos()
        T=hex(int(time.time()))[6:10]
        Cpt=0
    
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

for Client_Restant in Liste_Client :
    
    try:    
        Client_Restant.close()
        # On ferme toute les connexions clients
    except:
        pass

serveur.close()     # Fermeture du serveur 

print("\n::::::::::::::::::::::::::")    
print(":: Fermeture du Serveur ::\n::::::::::::::::::::::::::")