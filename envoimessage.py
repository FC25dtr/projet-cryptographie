import gencleRSA
import math_utile
import random
def envoyer_message(): #fonction qui permet d'envoyer le message crypte en placant les cle dans un fichier cle_pub
    with open("cle_pub") as f:
        n = int(f.readline().strip())
        e = int(f.readline().strip())
    cle_pub = (n,e)
    message = input("Entrez un message : ")
    print("Message original :", message)
    blocs_chiffres = gencleRSA.chiffrement_blocs(cle_pub, message)
    print("Message chiffré :", blocs_chiffres)

print(envoyer_message())
