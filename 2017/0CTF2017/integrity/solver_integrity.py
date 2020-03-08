#!/usr/bin/env python3

import binascii
from hashlib import md5
from trmr import *
import struct

HOST = "172.16.12.139"
PORT = 7777

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

def sock(remoteip, remoteport):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remoteip, remoteport))
    return s, s.makefile(mode='rw', buffering=None)

s, sf = sock(HOST, PORT)

print(sf.readline())
print(sf.readline())
s.send(b"r\n")
s.send((pad("admin")+"X"+"\n").encode())
print(sf.readline())
raw_secret2 = sf.readline()
raw_secret = raw_secret2.rstrip()
secret = binascii.unhexlify(raw_secret)

enc = secret[:-BS]
iv = enc[:BS]
enc = enc[BS:]

#new_iv = iv + md5(Pad(admin)) + md5(Pad(admin)||X)

admin_digest = md5(pad("admin").encode()).digest()
raw = pad('admin')+'X'

digest = md5(pad(raw).encode()).digest()

admin_digest = binascii.hexlify(admin_digest).decode("ascii")
digest = binascii.hexlify(digest).decode("ascii")
iv = binascii.hexlify(iv).decode("ascii")

print("[DEBUG] admin_hash : "+admin_digest)
print("[DEBUG] user_hash : "+digest)
print("[DEBUG] iv : "+iv)

new_iv2 = xor(iv, xor(admin_digest, digest))
print(new_iv2)
#print(struct.pack('s',new_iv2))
print(struct.pack('b','a'))

new_iv = int(iv, 16) ^ (int(admin_digest, 16) ^ int(digest, 16))
print(hex(new_iv)[2:].encode('ascii'))
print("[DEBUG] new_iv : "+ hex(new_iv)[2:])


new_secret = hex(new_iv)[2:] + binascii.hexlify(enc).decode("ascii")
print("[DEBUG] new_secret ; "+new_secret)

print(sf.readline())
s.send(b"l\n")
s.send((new_secret+'\n').encode())

interact(s)
