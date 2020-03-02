#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
from PyQt4 import QtGui
from PyQt4 import QtCore
import os
import subprocess
import tempfile
from os import listdir
from os.path import isfile, join
import io


#variables globales
nb_rpi = 5
timer = QTimer()
lon = 400
haut = 270
state_log=0

app = QtGui.QApplication(sys.argv)

txtbtnpasadress = "Ce bouton n'est pas disponible sans adresse"
txtbtnadress = "Envoyer les images a l'adresse selectionnee"

# Create tabs
tabs	= QtGui.QTabWidget()
tab1	= QtGui.QWidget()
tab2	= QtGui.QWidget()
tab3	= QtGui.QWidget()
tab4	= QtGui.QWidget()
tab5	= QtGui.QWidget()
tab6	= QtGui.QWidget()

#création des différents widgets
combo = QComboBox(tab1)
qnbphoto=QLabel(tab1)
startbtn = QtGui.QPushButton("\nStart\n", tab1)
stopbtn = QtGui.QPushButton("\nStop\n", tab1)

textnbrpi = QLabel(tab2)
textnbrphotos = QLabel(tab2)

usbbtn = QtGui.QPushButton("\nChoisissez votre cle USB\n", tab3)
dirusb=QLabel(tab3)
envoibtn=QtGui.QPushButton(txtbtnpasadress, tab3)
envoibtnok=QtGui.QPushButton(txtbtnadress, tab3)


rebootbtn = QtGui.QPushButton("\nReboot\n", tab4)
arretbtn=QtGui.QPushButton("\nArret\n", tab4)

terminal=QLabel(tab5)
lctbtn=QtGui.QPushButton("\n Lecture du fichier selectionne\n", tab5)
envlogbtn=QtGui.QCheckBox("\n Envoi du fichier selectionne via usb\n", tab5)
combolog = QComboBox(tab5)
      
        


class Logger():
    stdout = sys.stdout
    messages = []

    def start(self): 
        sys.stdout = self

    def stop(self): 
        sys.stdout = self.stdout

    def write(self, text): 
        self.messages.append(text)

log = Logger()




class QProgBar(QProgressBar):

    value = 0

    @pyqtSlot()
    def increaseValue(progressBar):
        progressBar.setValue(progressBar.value)
        progressBar.value = progressBar.value+1
        
@pyqtSlot()
def click_start():
	 nb_photos_up=combo.currentText()
	 
	 textnbrphotos.setText("Vous avez choisi {} photos".format(QString("%1").arg(nb_photos_up)))
	 startbtn.deleteLater()
	 combo.deleteLater()
	 qnbphoto.deleteLater()

	 bar = QProgBar(tab1)
	 bar.resize(320,70)
	 bar.move(45,40) 
	 bar.setValue(0)
	 bar.show()
	 stopbtn.move(45,120)
	 bar.connect(timer,SIGNAL("timeout()"),bar,SLOT("increaseValue()"))
	 timer.start(400)
	 print("start")
	 print("nb de photos : {}".format(str(textnbrphotos)))
	 terminal.setText(terminal_output2())

# ~ def centre_x(QWidget fenetre):
	# ~ longueur = fenetre.window_width()
	# ~ place_x = longueur - int(0.8*longueur/2.0)
	# ~ return place_x
	


@pyqtSlot()
def click_stop():
	 timer.stop()
	 print("stop")

@pyqtSlot()
def click_usb():
	 filename = QFileDialog.getExistingDirectory(tab3, 'Choisissez votre cle USB', '/')
	 dirusb.setText("Vous avez choisi la direction :\n{}".format(QString("%1").arg(filename)))
	 print(filename)
	 if filename!='':
		 envoibtn.deleteLater()
		 envoibtnok.show()

@pyqtSlot()
def click_reboot():
	 os.system("reboot")	 


def click_envoilog():
	global state_log
	fichier=combolog.currentText()
	if state_log == 0:
		os.system("cp " + str(fichier) + " ../Images")
		state_log=1
	else:
		state_log =0


def click_lecture_log():
	global tab6
	tab6.deleteLater()
	fichier=combolog.currentText()
	print(fichier)
	tab6	= QtGui.QWidget()
	log = QTextEdit(tab6)
	log.setReadOnly(True)
	log.resize(350,200)
	mon_fichier=open(fichier,"r")
	contenu=mon_fichier.read()
	log.setText(contenu)
	tabs.addTab(tab6,"Fichier Log")
	tab6.update()
	
		 
def main():
 
    # Resize width and height
    tabs.resize(400, 270)


####### TAB 1 #######

    startbtn.resize(320,70)
    startbtn.move(45,70)
    
    stopbtn.resize(320,70)
    stopbtn.move(45,150)
    #stopbtn.move(300,0)
    
    qnbphoto.move(10, 20)
    qnbphoto.resize(300,20)
    qnbphoto.setText("Combien de photos souhaitez-vous prendre ?")
    
    
    #déclaration du combo
    combo.addItem("8")
    combo.addItem("16")
    combo.addItem("32")
    combo.addItem("64")
    combo.addItem("128")
    combo.move(320,15)
    
    # ~ tab1.setLayout(layout1)
    tab1.show()
    
    
    nb_photos=combo.currentText()

####### TAB 2 #######
    
      # Set layout of 2nd tab
    layout2	= QtGui.QVBoxLayout()
    textnbrpi.move(10, 10)
    textnbrpi.resize(250,20)
    textnbrpi.setText("Nombre de RPi connectees : {}".format(QString("%1").arg(nb_rpi)))
    
    textnbrphotos.move(10, 30)
    textnbrphotos.resize(250,20)
    textnbrphotos.setText("Vous avez choisi {} photos".format(QString("%1").arg(nb_photos)))
    
####### TAB 3 #######    
    
    
    usbbtn.resize(320,40)
    usbbtn.move(45,40)
    usbbtn.clicked.connect(click_usb)
    dirusb.resize(380,80)
    dirusb.move(45,140)
    dirusb.setText("Vous n'avez pas choisi de direction ")
    envoibtnok.move(45,100)
    envoibtnok.hide()
    envoibtn.move(45,100)
    envoibtn.setEnabled(False)

    
    
####### TAB 4 #######    
       
    rebootbtn.resize(320,40)
    rebootbtn.move(45,40)
    rebootbtn.clicked.connect(click_reboot)
        
    arretbtn.resize(320,40)
    arretbtn.move(45,100)
    arretbtn.clicked.connect(exit)
    
    
####### TAB 5 #######
        
    
    listelogs = [f for f in listdir('/home/paul/Documents/MeshroomRaspberry/') if isfile(join('/home/paul/Documents/MeshroomRaspberry/', f))]

    combolog.move(45,10)
    lctbtn.move(45,40)
    envlogbtn.move(45,100)
    envlogbtn.setChecked(False)
    envlogbtn.toggled.connect(click_envoilog)
    lctbtn.clicked.connect(click_lecture_log)
    for i in listelogs:
		combolog.addItem(i)
	
	
	
	
    
    
####### AJOUT DES TABS #######

    tabs.addTab(tab1,"Menu")
    tabs.addTab(tab2,"Informations")
    tabs.addTab(tab3,"USB")
    tabs.addTab(tab4,"Alimentation")
    tabs.addTab(tab5,"Logs")

 
    startbtn.clicked.connect(click_start)
    startbtn.clicked.connect(startbtn.deleteLater)
    stopbtn.clicked.connect(click_stop)
    # ~ exitbtn.clicked.connect(exit)

   
    
    # Set title and show
    tabs.setWindowTitle('Projet Meshroom - FabMSTIC')
    tabs.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
