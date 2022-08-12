#!/usr/bin/env python3
#-- coding: utf-8 --

from queue import Empty
import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs
from pirc522 import RFID
import time
from datetime import datetime
import mysql.connector


#Code MySQL\
#connexion au serveur
conn = mysql.connector.connect(host="localhost", user="root", password="root", database="CISB")
cursor = conn.cursor()

#creation de table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS card (
#     id int(5) NOT NULL AUTO_INCREMENT,
#     name varchar(50) DEFAULT NULL,
#     id_card varchar(50) DEFAULT NULL,
    
# );
# """)
#la liste des id_cards dans la database   bngesp
cursor.execute("SELECT * FROM card")
#Définit la liste des UIDs du badge 
RFID_UID =[] 
for e in cursor.fetchall():
    if e != ():
        RFID_UID +=[e[2]] 



GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte

rc522 = RFID() #On instancie la lib
# nom_fichier = "/home/pi/resultats/resultats_" + datetime.now().strftime("%Y-%m-%d") + ".txt" #on cre un fichier par jour
print('En attente d\'un badge (pour quitter, Ctrl + c): ') #On affiche un message demandant à l'utilisateur de passer son badge

#On va faire une boucle infinie pour lire en boucle
while True :
    rc522.wait_for_tag() #On attnd qu'une puce RFID passe à portée
    (error, tag_type) = rc522.request() #Quand une puce a été lue, on récupère ses infos

    if not error : #Si on a pas d'erreur
        (error, uid) = rc522.anticoll() #On nettoie les possibles collisions, ça arrive si plusieurs cartes passent en même temps
        
        uid = ''.join(str(v) for v in uid)
        #enregistrer une nouvelle carte
        if uid not in RFID_UID:
            
            sql = "INSERT INTO card (name, id_card) VALUES (%s, %s)"
            name_ = input("Entrez un nom a enregistrer ")
            val = (name_, uid)
            cursor.execute(sql, val)
            conn.commit()
            conn.close()

        if not error : #Si on a réussi à nettoyer
            print('Vous avez passé le badge avec l\'id : {}'.format(uid)) #On affiche l'identifiant unique du badge RFID
            # fichier = open(nom_fichier, "a")
            # print(datetime.now().time())
            # fichier.write("\n" + str(format(uid))+"/" +str(datetime.now().time()))
            # fichier.close
            time.sleep(1) #On attend 1 seconde pour ne pas lire le tag des centaines de fois en quelques milli-secondes
            

