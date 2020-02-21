#!/usr/bin/env python 
#-*-coding: latin-1-*-
# libraries
import time
import RPi.GPIO as GPIO

def Init_GPIO():
    
    #Definition des variables globales
    global StepPins
    global WaitTime
    global StepCount1
    global Seq1
    global StepCount2
    global Seq2
    
    # Utilisation de BCM pour les GPIOs
    GPIO.setmode(GPIO.BCM)
    # Définitions des GPIOs sur les Pins 18,22,24,26 -> GPIO24,GPIO25,GPIO8,GPIO7
    
    StepPins = [24,25,8,7]
    # Paramétrage des Pins en sortie
    for pin in StepPins:
           #print ("Setup pins")
           GPIO.setup(pin,GPIO.OUT)
           GPIO.output(pin, False)
           
    # Définition(s) de quelque(s) paramètre(s)
    WaitTime = 0.005
    
    # Définition de la séquence 1 (pas par pas)
    StepCount1 = 4
    Seq1 = []
    Seq1 = range(0, StepCount1)
    Seq1[0] = [1,0,0,0]
    Seq1[1] = [0,1,0,0]
    Seq1[2] = [0,0,1,0]
    Seq1[3] = [0,0,0,1]
    
    # Définition de la séquence 2 (demi-pas par demi-pas)
    StepCount2 = 8
    Seq2 = []
    Seq2 = range(0, StepCount2)
    Seq2[0] = [1,0,0,0]
    Seq2[1] = [1,1,0,0]
    Seq2[2] = [0,1,0,0]
    Seq2[3] = [0,1,1,0]
    Seq2[4] = [0,0,1,0]
    Seq2[5] = [0,0,1,1]
    Seq2[6] = [0,0,0,1]
    Seq2[7] = [1,0,0,1]

def steps(nb,num_seq):
    
    # Paramétrage en fonction du choix de la séquence
    if num_seq==1 :
        Seq=Seq1
        StepCount=StepCount1
    else :
        Seq=Seq2
        StepCount=StepCount2
    
    StepCounter = 0
    
    # Le signe défini le sens de rotation (positif = sens horaire)
    if nb<0: sign=-1
    else: sign=1
    
    # Définition du nombre de pas à faire
    nb=sign*nb*num_seq
    #print("nbsteps {} and sign {}".format(nb,sign))
    
    for i in range(nb):
            for pin in range(4):
                    xpin = StepPins[pin]
                    if Seq[StepCounter][pin]!=0:
                            GPIO.output(xpin, True)
                    else:
                            GPIO.output(xpin, False)
            StepCounter += sign
    
            if (StepCounter==StepCount):
                    StepCounter = 0
            if (StepCounter<0):
                    StepCounter = StepCount-1
                    
            # Petite pause
            time.sleep(WaitTime)
            

def Rotation(nb_tour,num_seq=1):
    if num_seq==1 or num_seq==2:
        nb_Steps=int(2048*nb_tour)
        #print("Début de la rotation")
        steps(nb_Steps,num_seq)
        #print("Fin de la rotation")
    else:
        print("num_seq doit être égale à 1 ou 2\nVoir la fonction help_rotation si besoin")

def Close_GPIO():
    # Fermeture de toutes les Pins
    for pin in StepPins:
           GPIO.output(pin, False)            

def help_rotation():
    print("\nLe premier paramètre correspond au nombre de tour.\nCette valeur peut être inférieur à 1 pour des rotations inférieurs au tour.\nCe nombre peut aussi correspondre à (1/nb_photo_par_tour).\n")
    print("Pour le choix du sens de la rotation dépend du premier paramètre:\n  - Si positif : sens horaire\n  - Si négatif : sens anti-horaire\n\n")
    print("Le deuxième paramètre permet de choisir la séquence à utiliser.\nCela concerne l'utilisation des pas (1) ou des demi-pas (2).\nLaisser vide si vous ne savez pas.\n")
