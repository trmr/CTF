
import hashlib
import socket
from trmr import *

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

def strxor(s1, s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

host='172.16.12.139'
port=7777

username = pad('admin') + 'X'
admin_hash = hashlib.md5(pad('admin')).digest()
name_hash = hashlib.md5(pad(username)).digest()

p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
p.connect((host, port))
pf = p.makefile(mode='rw')
print pf.readline()
print pf.readline()
p.send('r'+'\n')
p.send(username+'\n')
print pf.readline()

data = pf.readline().strip().decode('hex')

IV = data[:BS]
hash_enc = data[BS:BS*2]
admin_enc = data[BS*2:BS*3]
pad_enc = data[BS*3:]

print "[DEBUG] iv "+IV.encode("hex")

print "[DEBUG] admin_hash "+admin_hash.encode("hex")
print "[DEBUG] name_hash "+name_hash.encode("hex")
print "[DEBUG] h_xor "+xor(name_hash, admin_hash).encode("hex")

new_IV = xor(xor(name_hash, admin_hash), IV)
print "[DEBUG] new_iv = "+new_IV.encode("hex")
ct = new_IV + hash_enc + admin_enc

print "[DEBUG] secret = "+ct.encode("hex")

p.send('l'+'\n')
p.send(ct.encode('hex')+'\n')
#print pf.readline()

interact(p)
