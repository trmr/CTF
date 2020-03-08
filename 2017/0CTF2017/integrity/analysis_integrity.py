#!/usr/bin/python -u

from Crypto.Cipher import AES
from hashlib import md5
from Crypto import Random
from signal import alarm

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]


class Scheme:
    def __init__(self,key):
        self.key = key

    def encrypt(self,raw):
        raw = pad(raw)
        raw = md5(raw).digest() + raw

        iv = Random.new().read(BS)
        cipher = AES.new(self.key,AES.MODE_CBC,iv)

        return ( iv + cipher.encrypt(raw) ).encode("hex")

    def decrypt(self,enc):
        enc = enc.decode("hex")

        iv = enc[:BS]
        enc = enc[BS:]

        cipher = AES.new(self.key,AES.MODE_CBC,iv)
        blob = cipher.decrypt(enc)

        checksum = blob[:BS]
        data = blob[BS:]

        if md5(data).digest() == checksum:
            return unpad(data)
        else:
            return

def xorstr(s1, s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

key = Random.new().read(BS)
scheme = Scheme(key)

flag = open("flag",'r').readline()
alarm(30)

###
#print(pad("admin")+"a")
sign = "cf1209905940ebf98aa76a7c7d814da0b0c435646dd42984030232785c52485dd0fe44f6d988c821b6de9d4413990b1c720b1e6c1e2a45948d58d4d306608493"
sign = sign[:-BS]
enc = sign.decode("hex")
iv = enc[:BS]
enc = enc[BS:]

data = md5(pad("admin")).digest()
new_iv = xorstr(data, xorstr(iv, enc))
new_sig = new_iv + sign
print new_sig.encode("hex")

###

print "Welcome to 0CTF encryption service!"
while True:
    print "Please [r]egister or [l]ogin"
    cmd = raw_input()

    if not cmd:
        break

    if cmd[0]=='r' :
        name = raw_input().strip()

        if(len(name) > 32):
            print "username too long!"
            break
        if pad(name) == pad("admin"):
            print "You cannot use this name!"
            break
        else:
            print "Here is your secret:"
            print scheme.encrypt(name)


    elif cmd[0]=='l':
        data = raw_input().strip()
        name = scheme.decrypt(data)

        if name == "admin":
            print "Welcome admin!"
            print flag
        else:
            print "Welcome %s!" % name
    else:
        print "Unknown cmd!"
        break


