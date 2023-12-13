import hashlib
import os
import sys
import time
import calendar
import tqdm
import json
import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

class wallet:
    def __init__(self):
        self.un = ''
        self.up = ''

def create_keys(user_name,user_password):
    priv_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048, )
    pub_key = priv_key.public_key()
    priv_pem = priv_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(bytes(user_password,encoding='utf-8'))
    )
    f = open(user_name+'.pem', 'wb')
    f.write(priv_pem)

    public_pem = pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1
    )
    h = hashlib.sha256(public_pem)
    ac = str(h.hexdigest())
    f = open(user_name,'wb')
    f.write(public_pem)
    s.send(bytes("1","UTF-8"))
    s2.send(bytes("2", "UTF-8"))
    f = open(wall1.un, 'rb')
    s.send(bytes(wall1.un, "UTF-8"))
    print("Sending Public key")
    sendfile = f.read(1024)
    # while sendfile:
    s.send(sendfile)
    print("sending initial tran")
    s.send(bytes(ac,"UTF-8"))

        #sendfile = f.read(1024)
Host = '127.0.0.1'
port = 12345
s = socket.socket()
s.connect((Host,port))
wall1 = wallet()
print("UserName")
wall1.un = input()
print("Password")
wall1.up = input()
if(os.path.exists(wall1.un+".pem")):
    f = open(wall1.un+'.pem','rb')
    priv_key = serialization.load_pem_private_key(f.read(), password=bytes(wall1.up, encoding='utf-8'))
    pub_key = priv_key.public_key()
    public_pem = pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1
    )
    h = hashlib.sha256(public_pem)
    ac = str(h.hexdigest())
    s.send(bytes("2","UTF-8"))
    s.send(bytes(wall1.un,"UTF-8"))
else:
    create_keys(wall1.un, wall1.up)
    f = open(wall1.un + '.pem', 'rb')
    priv_key = serialization.load_pem_private_key(f.read(), password=bytes(wall1.up, encoding='utf-8'))
    pub_key = priv_key.public_key()
    public_pem = pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1
    )
    h = hashlib.sha256(public_pem)
    ac = str(h.hexdigest())
print(ac)

while True:
    print("Choose what function to perform")
    print("1.Check balance")
    print("2.Check other person's balance")
    print("3.Make a transaction")
    print("4.Exit")
    ch = input()
    s.send(bytes(ch, "UTF-8"))
    if (ch == "1"):
        s.send(bytes(ac, "UTF-8"))
        print(s.recv(1024).decode())
    elif (ch == "2"):
        print("Enter Account Number")
        a_n = input()
        s.send(bytes(a_n,"UTF-8"))
        print(s.recv(1024).decode())
    elif (ch == "3"):
        print("Enter receiving account number")
        to = input()
        print("Enter amount")
        amt = int(input())
        s.send(bytes(ac,"UTF-8"))
        time.sleep(3)
        cur_time = time.gmtime()
        tstmp = calendar.timegm(cur_time)
        d = {'timestamp': tstmp, 'from': ac, 'to': to, 'amount': amt}
        d_bytes = json.dumps(d)
        signature = priv_key.sign(
            d_bytes.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        s.send(bytes(d_bytes,'UTF-8'))
        print("Sending Username")
        time.sleep(3)
        s.send(bytes(wall1.un, "UTF-8"))
        time.sleep(3)
        s.send(signature)
    else:
        s.close()
        break