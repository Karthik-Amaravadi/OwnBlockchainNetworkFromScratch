import hashlib
import os
import socket
import time
import calendar
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
import BlockChain



def MakeTransaction1(obj1,d, sig, un):
    f = open('pub_keys/' + un, 'rb')
    pub_key = serialization.load_pem_public_key(f.read())
    obj1.new_transac(d, sig, pub_key)


def MakeTransaction2(obj1,fr, to, amt,h):
    obj1.new_trans2(fr, to, amt,h)

class wallet:
    def __init__(self):
        self.un = ""
        self.up = ""
        self.coinbase = {}
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
    f = open('pub_keys/'+user_name, 'wb')
    f.write(public_pem)

ut1 = []
chain = []
obj1 = BlockChain.blockchain()
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
    # p = str(pub_key)
    h = hashlib.sha256(public_pem)
    ac = str(h.hexdigest())
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
def receive_data(conn2):
    ut1 = []
    print("Receiving utxo.json")
    l = conn2.recv(1024).decode()
    print(l)
    for j in range(int(l)):
        ut1.append(json.loads(conn2.recv(1024).decode()))
    print(ut1)
    f = open("AcceptedFiles_Folder/utxo.json", 'wb')
    f.write(json.dumps(ut1).encode())
    f.close()
    for i in ut1:
        f = open(i['hash'] + '.json', 'wb')
        tran = conn2.recv(1024)
        f.write(tran)
        obj1.pending_trans.append({'hash': i['hash'], 'content': json.loads(tran)})
        f.close()
    bl = block_create()
    start = time.time()
    block = obj1.new_block(bl, len(chain))
    end = time.time()
    f = open("AcceptedFiles_Folder/block" + str(len(chain) + 1) + ".json", 'wb')
    f.write(json.dumps(block).encode())
    f.close()
    chain.append(block)
    time.sleep(1)
    conn2.send(bytes(str(end - start), "UTF-8"))
    print("Receiving Balance")
    f = open("AcceptedFiles_Folder/balance.json", 'wb')
    f.write(conn2.recv(1024))
    f.close()
    data_con = conn2.recv(1024).decode()
    if (data_con == "1"):
        send_data(conn2)
    else:
        receive_data2(conn2)
def receive_data2(conn2):
    coin_tran = conn2.recv(1024)
    h = hashlib.sha256(coin_tran).hexdigest()
    with open(h + ".json", 'wb') as outfile:
        outfile.write(coin_tran)
    outfile.close()
    ut1 = conn2.recv(1024)
    with open("AcceptedFiles_Folder/utxo.json", 'wb') as outfile:
        outfile.write(ut1)
    outfile.close()
    print("Receiving Balance")
    f = open("AcceptedFiles_Folder/balance.json", 'wb')
    f.write(conn2.recv(1024))
    f.close()
    bl = conn2.recv(1024)
    with open("AcceptedFiles_Folder/block" + str(len(chain))+".json", 'wb') as outfile:
        outfile.write(bl)
    outfile.close()
def send_data(s2):
    hash_coin = hashlib.sha256(json.dumps(wall1.coinbase).encode()).hexdigest()
    with open(hash_coin + ".json", 'wb') as outfile:
        outfile.write(json.dumps(wall1.coinbase).encode())
    outfile.close()
    s2.send(json.dumps(wall1.coinbase).encode())
    time.sleep(1)
    f = open("AcceptedFiles_Folder/utxo.json", 'rb')
    ut = json.loads(f.read())
    f.close()
    ut.append({'hash': hash_coin, 'acc_numb': ac, 'amt': 6})
    s2.send(json.dumps(ut).encode())
    f = open("AcceptedFiles_Folder/utxo.json", 'wb')
    f.write(json.dumps(ut).encode())
    f = open("AcceptedFiles_Folder/balance.json", 'rb')
    balan = json.loads(f.read())
    balan['count'] = 0
    f = open("AcceptedFiles_Folder/balance.json", 'wb')
    f.write(json.dumps(balan).encode())
    f.close()
    print("Sending Balance")
    f = open("AcceptedFiles_Folder/balance.json", 'rb')
    balan = json.loads(f.read())
    f.close()
    balan[ac] = 6
    f = open("AcceptedFiles_Folder/balance.json",'wb')
    f.write(json.dumps(balan).encode())
    f.close()
    print(balan)
    time.sleep(1)
    s2.send(json.dumps(balan).encode())
    f = open("AcceptedFiles_Folder/block"+str(len(chain))+".json",'rb')
    bl = f.read()
    time.sleep(1)
    s2.send(bl)
def block_create():
    cur_time = time.gmtime()
    tstmp = calendar.timegm(cur_time)
    j = json.dumps(obj1.pending_trans)
    wall1.coinbase = {"timestamp": tstmp, "from": "coinbase", "to": ac, "amount": 6}
    x = json.dumps(wall1.coinbase).encode()
    hash_coin = hashlib.sha256(x).hexdigest()
    obj1.pending_trans.insert(0, {"hash": hash_coin, "content": wall1.coinbase})
    hash_part1 = j.encode()
    hash_part2 = hashlib.sha256(hash_part1)
    hash_full = hash_part2.hexdigest()
    block = {
        'header': {'height': len(obj1.chain),
                   'timestamp': tstmp,
                   'previousblock': obj1.previousblock,
                   'hash': hash_full},
        'body': obj1.pending_trans
    }
    return block
def serve_client(conn):
    x = conn.recv(1024).decode()
    print(x)
    if (x == '1' or x == '2'):
        conn.send(bytes(str(obj1.get_bal(conn.recv(1024).decode())),"UTF-8"))
        if (minecond == 1):
            serve_client(conn)
    elif(x=='3'):
        act = conn.recv(1024).decode()
        ut = obj1.get_utxo(act)
        print("Getting Transaction")
        dx = json.loads(conn.recv(1024).decode())
        print("Getting Username")
        un = conn.recv(1024).decode()
        print("Getting Signature")
        sig = conn.recv(1024)
        for i in ut:
            if (obj1.get_bal(act) >= dx['amount']):
                print("Verifying and making tranasaction")
                MakeTransaction1(obj1, dx, sig, un)
                if (obj1.get_bal(dx['from']) > dx['amount']):
                    print("Making change transaction")
                    MakeTransaction2(obj1, dx['from'], dx['from'], obj1.get_bal(dx['from']) - dx['amount'], i)
                else:
                    f = open("AcceptedFiles_Folder/balance.json", 'rb')
                    x = json.loads(f.read())
                    x[dx['from']] = 0
                    f = open("AcceptedFiles_Folder/balance.json", 'wb')
                    f.write(json.dumps(x).encode())
        f = open("AcceptedFiles_Folder/balance.json", 'rb')
        balan = json.loads(f.read())
        if (balan['count'] == 2):
            s2.connect((Host, port2))
            f = open("AcceptedFiles_Folder/utxo.json", 'rb')
            ut1 = json.loads(f.read())
            f.close()
            s2.send(bytes(str(len(ut1)), "UTF-8"))
            print("Sending UTXO")
            for j in ut1:
                print(j)
                s2.send(json.dumps(j).encode())
            for i in ut1:
                f = open(i['hash'] + '.json', 'rb')
                tr = json.loads(f.read())
                f.close()
                print("Transaction" + i['hash'])
                time.sleep(1)
                s2.send(json.dumps(tr).encode())
            print("Creating Block")
            bl = block_create()
            start = time.time()
            chain.append(obj1.new_block(len(chain),bl))
            end = time.time()
            n2_time = float(s2.recv(1024).decode())
            f = open("AcceptedFiles_Folder/balance.json", 'rb')
            balan = json.loads(f.read())
            balan['count'] = 0
            f = open("AcceptedFiles_Folder/balance.json", 'wb')
            f.write(json.dumps(balan).encode())
            f.close()
            s2.send(json.dumps(balan).encode())
            if(n2_time < (end-start)):
                s2.send(bytes("1","UTF-8"))
                receive_data2(s2)
            else:
                s2.send(bytes("0", "UTF-8"))
                send_data(s2)
        if (minecond == 1):
            serve_client(conn)
    else:
        conn.close()
        conn, addr = s.accept()
        if (minecond == 1):
            cond = conn.recv(1024).decode()
            print(cond)
            print("Getting Username")
            un = conn.recv(1024).decode()
            if (cond == "1"):
                print("Getting Public Key")
                f = open('pub_keys/' + un, 'wb')
                pub_key = conn.recv(1024)
                f.write(pub_key)
                f.close()
                print("Getting inialt tran")
                act = conn.recv(1024).decode()
                obj1.new_trans(act, act, 100)
            if(minecond==1):
                serve_client(conn)

s = socket.socket()
port = 12345
Host = '127.0.0.1'
s2 = socket.socket()
port2 = 12348
Threadcount = 0
try:
    s.bind(('', port))
except socket.error as e:
    print(str(e))
s.listen(5)
print("1.Mining Mode 2.Wallet Mode")
cho = input()
minecond = 1
conn, addr = s.accept()
if (minecond == 1):
    cond = conn.recv(1024).decode()
    print("Getting Username")
    un = conn.recv(1024).decode()
    if (cond == "1"):
        print("Getting Public Key")
        f = open('pub_keys/' + un, 'wb')
        pub_key = conn.recv(1024)
        f.write(pub_key)
        f.close()
        print("Getting inialt tran")
        act = conn.recv(1024).decode()
        obj1.new_trans(act, act, 100)

while (1):
    if(cho=='1' and minecond==1):
        serve_client(conn)

    if(cho=='2'):
        utxo = obj1.get_utxo(ac)
        print(utxo)
        print("Choose what function to perform")
        print("1.Check balance")
        print("2.Check other person's balance")
        print("3.Make a transaction")
        print("4.Exit")
        ch = input()
        if (ch == "1"):
            print(obj1.get_bal(ac))
        elif (ch == "2"):
            print("Enter Account Number")
            a_n = input()
            print(obj1.get_bal(a_n))
        elif (ch == "3"):
            print("Enter receiving account number")
            to = input()
            print("Enter amount")
            amt = int(input())
            for i in utxo:
                if (obj1.get_bal(ac) >= amt):
                    cur_time = time.gmtime()
                    tstmp = calendar.timegm(cur_time)
                    d = {'timestamp': tstmp, 'from': ac, 'to': to, 'amount': amt}
                    d_bytes = json.dumps(d).encode('utf-8')
                    signature = priv_key.sign(
                        d_bytes,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                    MakeTransaction1(obj1, d, signature, wall1.un)
                    f = open("AcceptedFiles_Folder/utxo.json", 'wb')
                    u = json.loads(f.read())
                    u.remove(i)
                    if (obj1.get_bal(ac) > amt):
                        MakeTransaction2(obj1, ac, ac, obj1.get_bal(ac) - amt, i)
                    else:
                        print("No Balance")
                        f = open("AcceptedFiles_Folder/balance.json", 'rb')
                        x = json.loads(f.read())
                        x[ac] = 0
                        f = open("AcceptedFiles_Folder/balance.json", 'wb')
                        f.write(json.dumps(x).encode())
    ut1=[]
    if(minecond==0):
        receive_data(conn)
