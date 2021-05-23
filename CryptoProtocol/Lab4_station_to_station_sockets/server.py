# This is Bob (server).

print('Welcome to STS, Bob!')

import sys
import math
import time
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

# Le chiavi di Bob sono state generate e salvate con i seguenti metodi.
#from Crypto import Random
#sha = hashlib.sha256()
#random_generator = Random.new().read
#keys = RSA.generate(1024, random_generator)

#file = open('Bpriv.pem', 'w')
#file.write(keys.exportKey('PEM'))
#file.close()
#file = open('Bpub.pem', 'w')
#file.write(keys.publickey().exportKey('PEM'))
#file.close()

# Read Bpriv
key = open('Bpriv.pem', 'r').read()
Bpriv = RSA.importKey(key)

# Read Apub
key = open('Apub.pem', 'r').read()
Apub = RSA.importKey(key)

HOST = '' # 'localhost'.
PORT = 24069 # Porta arbitraria.

# Il primo parametro dice che usiamo un dominio IPv4.
# Il secondo parametro ci dice che usiamo la connessione TCP.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
    server_socket.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]) 
    sys.exit() # Chiude il sistema.

print('Socket bind complete')
server_socket.listen(5)
print('Socket now listening')

# Accetto la connessione del client.
(client_socket, address) = server_socket.accept()    
print('Got connection from client ' + address[0] + '. Running authentication protocol...')

# Ricevo Ta, p e g per generare Kt.
data = client_socket.recv(4096)
# print(f"data {type(data)}")
temp = data.decode().split('\n')
# print(f"temp: {type(temp)}")

p = int(temp[0])
g = int(temp[1])
Ta = int(temp[2])
Sb = random.randint(1, p-1)
Tb = pow(g, Sb, p)
Kt = pow(Ta, Sb, p)
# Invio Tb ed Ekb.
message = str(Tb) + str(Ta)
byte_message = bytes(message,encoding='latin-1')
h = SHA512.new()
h.update(byte_message)
signer = PKCS1_v1_5.new(Bpriv)
signatureB = signer.sign(h)

# print(type(signatureB))
print(f"Kt: {Kt}")
Ekb = encrypt(str(Kt), signatureB)
print(f"Ekb{Ekb}")
print("signatureB: ",signatureB)

data = str(Tb).encode('latin-1') + 'EOL'.encode('latin-1') + Ekb
client_socket.send(data)
print(f"Send data")
#---------------------Check SignatyreB----------------
exampleB = client_socket.recv(4096)
print(fuzz.ratio(signatureB,exampleB))
#---------------------finish Check SignatyreB---------
#-----------------Check messageB----------------------
client_socket.send(message.encode())
#-----------------Finish Check Message B--------------

# Ricevo Eka.
Eka = client_socket.recv(1024)
print('take signatureA')
if Eka != '':
    print("SignatureA is't empty")
    signatureA = decrypt(str(Kt), Eka)
    messageFromA = str(Ta) + str(Tb)
    byte_mewssage_revers = bytes(messageFromA,encoding='latin-1')
    h = SHA512.new()
    h.update(byte_mewssage_revers)
    verifier = PKCS1_v1_5.new(Apub)
    if verifier.verify(h, signatureA):
        print("The signature received from the client is authentic.")
        print("Type 'exit' to quit this session.")

        # Scambio di messaggi successivi all'autenticazione.
        send = 1
        #.encode('latin-1')
        #.decode('latin-1')
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
                print("Waiting for Alice's message...")
                messageFromA = client_socket.recv(1024)
                answer = decrypt(str(Kt), messageFromA).decode('latin-1')
                print(answer)
                if answer != 'exit':
                    print('Alice said: ' + answer)
                    send = 1
                else:
                    print('Session terminated by Alice.')
                    message = 'exit'

    else:
        print("The signature received from the client is NOT authentic.")
        error = encrypt(str(Kt), message)
        client_socket.send(error)
else:
    print("Authentication failed.")

Sb = None
Kt = None

client_socket.close()
server_socket.close()
