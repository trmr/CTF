#!/usr/bin/env python
#-*- coding:utf-8 -*-

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

flag = 'TWCTF{*******CENSORED********}'

#print ord(flag[0])
#print ord(flag[1])

data = open("encrypted").readline().strip('\n')
encrypted = [int(data[i:i+2],16) for i in range(0,len(data),2)]
denominator = modinv((ord(flag[1]) - ord(flag[0])),251)
numerator = (encrypted[1] - encrypted[0]) % 251
alpha = (numerator * denominator) % 251

#print alpha

beta = (encrypted[0] - alpha * ord(flag[0]) ) % 251

#print beta

recovered = ''
for i in encrypted:
    i = (i - beta) % 251
    i = (i * modinv(alpha,251)) % 251
    recovered += chr(i)

print recovered
