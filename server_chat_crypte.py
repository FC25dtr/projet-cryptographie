# coding: utf-8

""" Tcp Chat server. """

import socket
import select
import random
import gencleRSA

CONNECTION_LIST = []
RECV_BUFFER = 4096
HOST = "172.20.10.7"
PORT = random.randint(2000,4000)
mot_de_passe = 'tonin'

def MSG_nickname(from_sock,message,nickname):
    sock_dest = None
    adresse = None
    for addr, name in mon_dictionnaire.items():
        if name == nickname:
            adresse = addr
    print(adresse)
    if adresse == None:
        from_sock.send("erreur : le destinataire n'a pas été trouvé\n".encode('UTF-8'))
        print("erreur : le destinataire n'a pas été trouvé")
        return
    for sock in CONNECTION_LIST:
        try:
            if (sock.getpeername()) == (adresse[0],adresse[1]):
                sock_dest = sock 
        except:
                None
    if sock_dest == None:
        from_sock.send("erreur : le destinataire n'a pas été trouvé\n".encode('UTF-8'))
        return 
    sock_dest.send(message.encode('UTF-8'))
    from_sock.send(f"[à {nickname}] ton message a été envoyé.\n".encode('UTF-8'))
    
def cle_pub(from_sock,nickname):
    from_sock.send(("la cle publique est " + dico_key_pub[nickname]).encode('UTF-8'))

    
def broadcastToClients(the_sock, message):
    # Do not send the message to master socket and the client who has send us
    # the message
    for sock in CONNECTION_LIST:
        if sock != server_socket and socket != the_sock:
            try:
                print(message)
                sock.send(message.encode('UTF-8'))
            except:
                # La ligne suivante permet d'afficher l'erreur
                # print("Unexpected error: "+sys.exc_info()[0])
                # En général, c'est le client qui n'est disponible
                # On ferme la connexion et on le supprime
                sock.close()
                CONNECTION_LIST.remove(sock)
                
def get_socket_by_nickname(nickname): #permet de faciliter le travail en recuperant le socket associe au nickname
    for addr, name in mon_dictionnaire.items(): #permet d'eviter de perdre du temps la dessus a chaque fois
        if name == nickname:
            for sock in CONNECTION_LIST:
                try:
                    if sock.getpeername() == addr:
                        return sock
                except:
                    continue
    return None

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)


# On ajoute le serveur à la liste des connexions pour pouvoir "lire"
# la connexion d'un nouveau client

CONNECTION_LIST.append(server_socket)
mon_dictionnaire={}
dico_key_pub = {}
dico_key_priv = {}
print("Chat server started " + HOST + ":" + str(PORT))
while 1:
    try:
        # On recupère la liste des sockets dans lesquelles on peut lire dans
        # read_sockets
        # écrire dans write_sockets...
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            # Si on peut lire dans celle du serveur c'est une nouvelle
            # connexion
            if sock == server_socket:
                # On l'accepte et on ajoute la connexion à CONNECTION_LIST
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Client (" + addr[0] + ", " + str(addr[1]) +") connected")
                sockfd.send(("Hello from " + HOST + ":" + str(PORT) + "\nEntrez un nom d'utilisateur : ""\n").encode('UTF-8'))
                nickname = sockfd.recv(1024).decode('UTF-8').strip()
                mon_dictionnaire[addr[0],addr[1]] = nickname
                sockfd.send(("\nEntrez le mot de passe: ""\n").encode('UTF-8'))
                mdp = sockfd.recv(1024).decode('UTF-8').strip()
                if mdp != mot_de_passe:
                    sockfd.send("Mot de passe incorrect, vous êtes déconnecté.\n".encode('UTF-8'))
                    sockfd.close()                       # ferme le socket
                    CONNECTION_LIST.remove(sockfd)       # retire de la liste
                    mon_dictionnaire.pop(addr, None)     # retire le pseudo
                # On envoie le message à tous les clients
                cle_pub, cle_priv, n = gencleRSA.gencle_RSAA()
                #generation de cle publique et prive dans le dico
                dico_key_pub[nickname] = cle_pub
                dico_key_priv[nickname] = cle_priv
                print("clé publique et privé généré avec succes\ncle publique : " +  str(dico_key_pub[nickname]) + "\ncle prive : " + str(dico_key_priv[nickname]))
                broadcastToClients(sockfd, "[" + addr[0] + ":" + str(addr[1]) +"] est arrivée : " + nickname + "\n")
            # Sinon c'est qu'un message à été reçu d'un client.
            else:
                try:
                    data = sock.recv(RECV_BUFFER).decode('UTF-8')
                    if data.startswith("/msg "):
                        parts = data.split(" ", 2)  # sépare /msg pseudo message
                        if len(parts) < 3:
                            sock.send("Utilisation : /msg <pseudo> <message>\n".encode('UTF-8'))
                        else:
                            MSG_nickname(sock, parts[2], parts[1])
                    elif data.startswith("/key "):
                        parts = data.split(" ", 1)  # sépare /key pseudo
                        if len(parts) < 2 or len(parts) > 3:
                            sock.send("Utilisation : /key <pseudo>\n".encode('UTF-8'))
                        else:
                            cle_pub(sock, parts[1])
                    else:# message a été reçu pour ne pas lui retourner
                        broadcastToClients(sock, '<' +str(sock.getpeername())  +'> '+ mon_dictionnaire[sock.getpeername()] +" : " + data + "\n")

                except:
                    # La ligne suivante est utile pour savoir quelle erreur a
                    # été émise
                    # print("Unexpected error: " + sys.exc_info()[0])
                    broadcastToClients(sock, "Client [" + addr[0] + ":" +str(addr[1]) +"] is offline "+ nickname )
                    print("Client [" + addr[0] + ":" + str(addr[1]) +"] is offline")
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    except KeyboardInterrupt:
        print("Stop.\n")
        break

server_socket.close()
