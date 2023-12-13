import json
import hashlib
import time
import calendar
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class blockchain(object):
    def __init__(self):
        self.target = "00"
        self.chain = []
        self.pending_trans = []
        self.previousblock = 'NA'
        self.blockhash = 'NA'
    def get_utxo(self,act):
        f = open("AcceptedFiles_Folder/utxo.json", 'rb')
        unsp_trans = json.loads(f.read())
        x = []
        for i in unsp_trans:
            if(i['acc_numb']==act):
                x.append(i['hash'])
        return x
    def new_block(self, chain_len,block):
        block = self.mine(block,chain_len)
        self.pending_trans = []
        self.previousblock = self.blockhash
        return block


    def mine(self,block,chain_len):
        found = False
        nonce=0
        while not found:
            block["Nonce"]=nonce
            j = json.dumps(block)
            self.blockhash = hashlib.sha256(j.encode('utf-8')).hexdigest()
            if str(self.blockhash)[0:len(self.target)]==self.target:
                found=True
            nonce += 1
        with open("AcceptedFiles_Folder/block" + str(chain_len + 1) + ".json", "w") as outfile:
            outfile.write(j)
        outfile.close()
        return block


    def validateBlock(self,block,hash):
        j = json.dumps(block)
        blockhash = hashlib.sha256(j.encode('utf-8')).hexdigest()
        if str(blockhash)[0:len(self.target)]==self.target and blockhash==hash:
            print("Block is valid")
        else:
            print("Block is Invalid")

    def new_transac(self, dic, sig,pub_key):
        signature = sig
        dicto = json.dumps(dic)
        en = dicto.encode()
        partial_hash = hashlib.sha256(en)
        hash_full = partial_hash.hexdigest()
        f = open("AcceptedFiles_Folder/utxo.json", 'rb')
        unsp_trans = json.loads(f.read())
        try:
            pub_key.verify(
                signature,
                en,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            self.pending_trans.append({'hash': hash_full, 'content': dic})
            unsp_trans.append({'hash': hash_full, 'acc_numb': dic.get('to'),'amt':dic.get('amount')})
            f = open("AcceptedFiles_Folder/utxo.json",'wb')
            x = json.dumps(unsp_trans)
            f.write(x.encode())
            f = open("AcceptedFiles_Folder/balance.json", 'rb')
            balan = json.loads(f.read())
            if(dic.get('to') in balan.keys()):
                balan[dic.get('to')] = balan.get(dic.get('to'))+dic.get('amount')
            else:
                balan[dic.get('to')] = dic.get('amount')
            balan['count'] += 1
            f = open("AcceptedFiles_Folder/balance.json", 'wb')
            f.write(json.dumps(balan).encode())
            with open(hash_full + ".json", "w") as outfile:
                outfile.write(dicto)
            outfile.close()
        except Exception as e:
            print(str(e))

    def get_bal(self,act):
        f = open("AcceptedFiles_Folder/balance.json", 'rb')
        balan = json.loads(f.read())
        return balan.get(act)

    def new_trans(self, fr, to, amt):
        cur_time = time.gmtime()
        tstmp = calendar.timegm(cur_time)
        transac = {'timestamp': tstmp, 'from': fr, 'to': to, 'amount': amt}
        j = json.dumps(transac)
        en = j.encode()
        partial_hash = hashlib.sha256(en)
        hash_full = partial_hash.hexdigest()
        f = open("AcceptedFiles_Folder/utxo.json", 'rb')
        self.unsp_trans = json.loads(f.read())
        self.pending_trans.insert(0,{'hash': hash_full, 'content': transac})
        self.unsp_trans.append({'hash': hash_full, 'acc_numb': to, 'amt': amt})
        f = open("AcceptedFiles_Folder/utxo.json", 'wb')
        x = json.dumps(self.unsp_trans)
        f.write(x.encode())
        f = open("AcceptedFiles_Folder/balance.json", 'rb')
        self.balan = json.loads(f.read())
        if (to in self.balan.keys()):
            self.balan[to] = self.balan.get(to) + amt
        else:
            self.balan[to] = amt
        self.balan['count'] += 1
        f = open("AcceptedFiles_Folder/balance.json", 'wb')
        f.write(json.dumps(self.balan).encode())
        # print(hash_full)
        with open(hash_full + ".json", "w") as outfile:
            outfile.write(j)
        outfile.close()
    def new_trans2(self, fr, to, amt,h):
        cur_time = time.gmtime()
        tstmp = calendar.timegm(cur_time)
        transac = {'timestamp':tstmp,'from':fr,'to':to,'amount':amt}
        j = json.dumps(transac)
        en = j.encode()
        partial_hash = hashlib.sha256(en)
        hash_full = partial_hash.hexdigest()
        f = open("AcceptedFiles_Folder/utxo.json", 'rb')
        unsp_trans = json.loads(f.read())
        self.pending_trans.append({'hash':hash_full,'content':transac})
        unsp_trans.append({'hash':hash_full,'acc_numb':to,'amt':amt})
        for i in unsp_trans:
            if(i['hash']==h):
                unsp_trans.remove(i)
        f = open("AcceptedFiles_Folder/utxo.json", 'wb')
        x = json.dumps(unsp_trans)
        f.write(x.encode())
        f = open("AcceptedFiles_Folder/balance.json", 'rb')
        balan = json.loads(f.read())
        balan[transac.get('to')] = transac.get('amount')
        balan['count'] += 1
        f = open("AcceptedFiles_Folder/balance.json",'wb')
        f.write(json.dumps(balan).encode())
        with open(hash_full+".json","w") as outfile:
            outfile.write(j)
        outfile.close()

