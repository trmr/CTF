from Crypto.Util.number import *
import Crypto.PublicKey.RSA as RSA
import os
from sympy import *

n1 = long(open("key1").readline().rstrip())
n2 = long(open("key2").readline().rstrip())
e = long(65537)

a = 1
b = (n2 - n1 - 4)/2
c = n1

x = Symbol('x')

ans = solve(a*x**2-b*x+c)

p = long(ans[0])
q = long(n1/p)

#print p
#print q

def genkey():
    d1 = inverse(e, (p-1)*(q-1))
    d2 = inverse(e, (p+1)*(q+1))
    key1 = RSA.construct((n1, e, d1))
    key2 = RSA.construct((n2, e, d2))
    if n1 < n2:
        return (key1, key2)
    else:
        return (key2, key1)

rsa1, rsa2 = genkey()

c = long(open("encrypted").readline().rstrip())

c = rsa2.decrypt(c)
c = rsa1.decrypt(c)

print ("%x"%c).decode("hex")
