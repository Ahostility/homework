# This is Alice (client).

print('Welcome to STS, Alice!')
import time
import sys
import math
import socket
import random
import hashlib
from Crypto.Hash import SHA512
from Crypto.Random import random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from simplecrypt import encrypt, decrypt
from passlib.hash import sha512_crypt
from fuzzywuzzy import process,fuzz

# Le chiavi di Alice sono state generate e salvate con i seguenti metodi.
#from Crypto import Random
#sha = hashlib.sha256()
#random_generator = Random.new().read
#keys = RSA.generate(1024, random_generator)
#file = open('Apriv.pem', 'w')
#file.write(keys.exportKey('PEM'))
#file.close()
#file = open('Apub.pem', 'w')
#file.write(keys.publickey().exportKey('PEM'))
#file.close()

# Read Apriv
key = open('Apriv.pem', 'r').read()
Apriv = RSA.importKey(key)

# Read Bpub
key = open('Bpub.pem', 'r').read()
Bpub = RSA.importKey(key)

# RFC-3526, Chiavi da 2048 bit (618 cifre decimali).
p = int('FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7E', 16)#DEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2
Sa = random.randint(1, p-1)
Ta = pow(g, Sa, p)

HOST = ''
PORT = 24069

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
print('Connecting to server...')
try:
    client_socket.connect((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]) 
    sys.exit() # Chiude il sistema.
    
print('Socket bind complete. Running authentication protocol...')

# Invio Ta, p e g.
data = str(p) + '\n' + str(g) + '\n' + str(Ta)
client_socket.send(data.encode().strip())

# Ricevo Tb ed Ekb per generare Kt.
data = client_socket.recv(4096)
print(f"data:{data}")
temp = data.split(b'EOL')
print(temp)
Tb = int(temp[0].decode('latin-1'))
Ekb = temp[1]
Kt = pow(Tb, Sa, p)
print(f"Kt: {Kt}")
print(f"Ekb:{Ekb}")
signatureB = decrypt(str(Kt),Ekb)
print("signatureB: ",signatureB)
#---------------------Check SignatyreB----------------
client_socket.send(signatureB)
#---------------------Finish Check SignatureB---------

#----------------------Chech Messageb-----------------
messageFromB = str(Tb) + str(Ta)
print(f"MessageFromB: {messageFromB}")
exampleMessageB = client_socket.recv(4096).decode()
print("Check message procent",fuzz.ratio(messageFromB,exampleMessageB))
#----------------------Chech Finish Messageb-----------

bytes_message_from_B = bytes(messageFromB,encoding='latin-1')
h = SHA512.new()
h.update(bytes_message_from_B)
verifier = PKCS1_v1_5.new(Bpub);
if verifier.verify(h, signatureB):
    print("The signature received from the server is authentic.")
    print("Type 'exit' to quit this session.")
    # Invio Eka.
    message = str(Ta) + str(Tb)
    print("Check message procent", fuzz.ratio(messageFromB, message))
    byte_message_revers = bytes(message,encoding='latin-1')
    h = SHA512.new()
    h.update(byte_message_revers)
    signer = PKCS1_v1_5.new(Apriv)
    signatureA = signer.sign(h)
    Eka = encrypt(str(Kt), signatureA)
    client_socket.send(Eka)
    send = 0
    print('Send SugnatureA')

    # Scambio di messaggi successivi all'autenticazione.
    while message != 'exit':
        if send == 1:
            message = input('Your message: ')
            if message == 'exit':
                print('Session terminated.')
                encrypted = encrypt(str(Kt), message)
                client_socket.send(encrypted)
            else:
                encrypted = encrypt(str(Kt), message)
                client_socket.send(encrypted)
                print('Message sent successfully.')
                send = 0
        elif send == 0:
            print("Waiting for Bob's message...")
            messageFromB = client_socket.recv(1024)
            answer = decrypt(str(Kt), messageFromB).decode('latin-1')
            print(answer)
            if answer == 'Authentication failed.':
                print('Authentication failed.')
                message = 'exit'

            if answer != 'exit':
                print('Bob said: ' + answer)
                send = 1
            else:
                print('Session terminated by Bob.')
                message = 'exit'

else:
    print("The signature received from the server is NOT authentic.")

Sa = None
Kt = None

client_socket.close()
