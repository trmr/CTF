#! /usr/bin/env python
# -*- coding:utf-8 -*-

from Crypto.Util.number import inverse, long_to_bytes
import Crypto.Cipher.DES as DES

N = eval(open("pubkey").read())

p = N[1022] * 2 - N[1023]
q = (N[1023] * inverse(2**1023,p)) % p

ciphertext = int(open("encrypted").readline().rstrip())
c = (ciphertext * inverse(q, p)) % p

x = ""

for i in range(len(N)):
    s = bin(c)[2:]
    if c % 2**(i+1):
        x += "1"
        w = (N[i] * inverse(q, p)) % p
        c -= w
    else:
        x += "0"

message = long_to_bytes(int(x,2))
KEY = "testpass"
plaintext = DES.new(KEY, DES.MODE_ECB).decrypt(message)
print plaintext
