import random 
import math_utile
def miller_rabbin(n,k): #teste si un rand nombre est premier avec k testes 
    if n < 2: # forcement pas premier 
        return False
    if n == 2 or n == 3: # forcement premier 
        return True 
    if n%2 == 0: #forcement pas premier 
        return False 
    (s,d) = math_utile.decompose_for_miller_rabin(n)
    for i in range(k): #pour effectuer exacteement k testes
        a = random.randrange(2,n-2) #genere aleatoire pour le teste
        x = math_utile.Exponentiation(a,d,n)  #puissance modulaire
        if x == 1 or x == n-1: # #teste 1 validé si 
            continue
        for j in range(s-1): # je cntinue les testes 
            x = (x*x)% n
            if x == n-1:
                break
            elif x == 1:
                return False 
        if x != n-1:
            return False 
    return True #renvoie True si tout les testes sont passé

def gencle_RSA(): #je genere les cle RSA 
    i = 0
    L = []
    while i < 2:
        a = random.randint(1,2**512) #genere un entier sur max 512 bits 
        if miller_rabbin(a, 7): #teste la primalite 
            i += 1
            L += [a]
    p,q = L[0],L[1]# je definie p e tq avec les deux nombres premiers
    if p == q:
        print("restart")
        return None
    n = p * q #je definie n
    id_euler = (p-1)*(q-1) # je trouve phi de n
    e = random.randint(1,id_euler)
    while math_utile.pgcd(id_euler,e) != 1: #recherche d'un e qui possede un inverse modulaire avec phi
        e = random.randint(1,id_euler)
    d = math_utile.inverse(e,id_euler)
    if (e*d)%id_euler !=1: #teste si d*e est bien 
        print("error")
        return None
    cle_pub = (n,e) #je cree les cles publique et privé 
    cle_priv = (n,d)
    return cle_pub,cle_priv
    
    
def message_vers_entier(message):
    m = 0
    for c in message:
        m = m * 256 + ord(c)  # décale le bloc et ajoute le nouveau caractère
    return m

def chiffrement(cle_publique,m):
    n,e = cle_publique
    chiffre = math_utile.Exponentiation(m, e, n) #formule de conversion avec RSA
    return chiffre

def dechiffrement(cle_prive,m):
    n,d = cle_prive
    dechiffre = math_utile.Exponentiation(m, d, n) #formule de dechiffrement avec RSA
    return dechiffre


def entier_vers_texte(m):
    caracteres = []
    while m > 0:
        code = m % 256 # récupérer le code du dernier caractère
        caracteres.append(chr(code))
        m = m // 256 # avancer vers le caractère précédent
    caracteres.reverse() # inverser la liste pour retrouver l'ordre original
    return caracteres

def RSA(): #fonction qui enchaine toutes les etapes pour veriier le fonctionnement 
    a,b = gencle_RSA()
    print(a,b)
    message = message_vers_entier("salut : ")
    print("message sous forme d'entier : ",message)
    crypte = chiffrement(a, message)
    print("message apres cryptage : ",crypte)
    decrypte = dechiffrement(b, crypte)
    print("message apres decryptage : " ,decrypte)
    final = entier_vers_texte(decrypte)
    return "message final : ",final

print(RSA())
