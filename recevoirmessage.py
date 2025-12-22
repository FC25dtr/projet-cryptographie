import math_utile
import gencleRSA
import random

def recevoir_message(blocs_chiffres): #recois le message et le dechiffre à l'aide des cle dans le fichier cle_priv
    with open("cle_priv") as f:
        n = int(f.readline().strip())
        d = int(f.readline().strip())
    cle_priv = (n,d)
    message_dechiffre = gencleRSA.dechiffrement_blocs(cle_priv, blocs_chiffres)
    print("Message déchiffré :", message_dechiffre)

a = int(input("entrez le message : "))
liste = [a]
print(recevoir_message(liste))
