# dans se fichier je vais aborder les limites du chiffrement RSA elle ne seront surement pas toute cité mais je vais en citer plusieurs:
# 1 : le chiffrement d'un même message donnera exactement la même suite de chiffre ce qui peut crée un risque de dechiffrement et de comparaison des differents messages.
# 2 : comparaison de certains permet sans decrypter de comprendre certaine partie du message, exemple : un message commence souvent par bonjour s'il intercepte plusieurs message commencant par la meme suite de chiffre il en deduira le code du mot bonjour.
# 3 : si l'attaquand possède la cle publique il peut utiliser un dictionnaire de code realiser avec la cle publique etles tester pour le dechiffrer, c'est ce que je vais montrer avec le code dessous.

import math_utile
import gencleRSA
import random

def attaque_dictionnaire(cle_pub, message_crypte):
    liste_mot = ["oui", "non", "admin", "password", "message"]
    for mot in liste_mot:
        blocs_chiffres = gencleRSA.chiffrement_blocs(cle_pub, mot)
        for bloc_mot in blocs_chiffres:
            if bloc_mot in message_crypte:
                print("Mot reconnu dans le message :", mot)
                break
# attention de la facon dont j'ai programme RSA se code ne fonctionne pas, ils fonctionne si le RSA fais une liste de bloque ou chaque bloque est un element de la ligne
