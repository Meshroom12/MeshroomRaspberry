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
from image_slicer import join

host='0.0.0.0'
port=8000
etat=True # Variable d'état ON/OFF du serveur
Liste_Client=[] # Liste de tout les clients connectés sur le serveur

ImageFile.LOAD_TRUNCATED_IMAGES=True


def Lecture_Client(client,adresse):
    # Fonction de lecture du client
    global etat 
    
    print("\n:: Connexion rentrante :: \nIP : {}" .format(adresse))
    print(":::::::::::::::::::::::::\n")
    
    i=0
    
    while etat==True:
        
        i+=1
                
        # try :
        image_len=1
        print("Image_len {}" .format(image_len)) 
        image_len = struct.unpack('<L', client.recv(4))[0]
            # On recupère la taille de l'image codé sur 1024-bits non signé
        print("Image_len {}" .format(image_len))     
        print(i)
            
        if not image_len:
            break
                # Si le client lui envoi une longueur de 0 -> on arrête la lecture
        print("Image_len {}" .format(image_len))    
        image_stream = io.BytesIO()
            # On créer le stream pour recevoir les datas
        image_stream.write(client.recv(image_len))
            # On recupère l'image envoyé par le client dans le stream
            # On créer un fichier pour sauvegarder l'image sur le serveur
        image_stream.seek(0)
        
        print(type(image_stream))
        print(image_stream)
        
        image = Image.open(image_stream).convert("RGB")
        image.save("IMG" + str(adresse[1]) + "_" + str(i) + ".jpeg")
        
        del image_len
                
        # except :
        #     print("\n:::::::::::::::::::::::::\n::  Erreur de lecture  ::")
        #     break
    
    print("\n:::::::::::::::::::::::::")
    print("IP : {}".format(adresse))
    print(":: Connexion  sortante ::")
    
    return 0



serveur = socket.socket()               # Création du serveur socket
serveur.bind((host, port))                # Création du lien de connexion
serveur.listen(5)

print("::: Ouverture du Serveur :::")    
print(":: Port de connexion {} ::".format(port))

while etat==True:
    
    Liste_Connexion, wlist, xlist = select.select([serveur],[],[],0.1)
    
    if keyboard.is_pressed("q"):
        etat=False
    # Pour sortir de la boucle il faut presser la touche 'q'
    
    for Connexion in Liste_Connexion:
        
        Client, Adresse = serveur.accept()      # Ouverture d'une connexion
        Client.makefile('rb')
        Liste_Client.append(Client)
        
        try :
            threading._start_new_thread(Lecture_Client,(Client,Adresse,))
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