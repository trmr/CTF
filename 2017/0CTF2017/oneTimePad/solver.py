# -*- coding: utf-8 -*-
from sage.all import *

def ntopoly(npoly):
    return sum(c*X**e for e, c in enumerate(Integer(npoly).bits()))

def polyton(poly):
    if not hasattr(poly, 'list'):
        poly = poly.polynomial()
    a = poly.list()
    return sum(int(a[i])*(1 << i) for i in xrange(len(a)))


def str2num(s):
    return int(s.encode('hex'), 16)

def process(m, k):
    return (m + k)^2


X = GF(2).polynomial_ring().gen()
P = 0x10000000000000000000000000000000000000000000000000000000000000425L
P = ntopoly(P)

F = GF(2**256, 'x',  modulus=P)
X = F.gen()


fake_secret1 = "I_am_not_a_secret_so_you_know_me"
fake_secret1 = ntopoly(str2num(fake_secret1))
fake_secret2 = "feeddeadbeefcafefeeddeadbeefcafe"
fake_secret2 = ntopoly(str2num(fake_secret2))

with open('ciphertext','r') as f:
    c = f.readlines()

ctxt1 = ntopoly(int(c[0],16))
ctxt2 = ntopoly(int(c[1],16))
ctxt3 = ntopoly(int(c[2],16))

key2 = fake_secret1 + ctxt2
key3 = fake_secret2 + ctxt3

key1 = key2.sqrt() + key3.sqrt() + key2

print key1

print "flag{%s}" % hex(polyton(ctxt1 + key1)).decode("hex")
