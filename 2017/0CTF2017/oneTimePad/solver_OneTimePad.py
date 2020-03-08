from sage.all import *
from trmr import *


def ntopoly(npoly):
    return sum(c*X**e for e, c in enumerate(Integer(npoly).bits()))

def polyton(poly):
    if not hasattr(poly, 'list'):
      poly = poly.polynomial()
    a = poly.list()
    return sum(int(a[i])*(1 << i) for i in xrange(len(a)))

def process(m, k):
    return (m + k)**2


X = GF(2).polynomial_ring().gen()
P = 0x10000000000000000000000000000000000000000000000000000000000000425L #trmr:
PX = ntopoly(P)
print PX # X^256 + X^10 + X^5 + X^2 + 1

F = GF(2**256, 'x', modulus=PX)
print F
X = F.gen()

plain1 = "I_am_not_a_secret_so_you_know_me"
plain1 = ntopoly(str2num(plain1))
plain2 = "feeddeadbeefcafefeeddeadbeefcafe"
plain2 = ntopoly(str2num(plain2))

with open('ciphertext','r') as f:
    c = f.readlines()

cp1 = ntopoly(int(c[0], 16))
cp2 = ntopoly(int(c[1], 16))
cp3 = ntopoly(int(c[2], 16))

t1 = plain1 + cp1
t2 = plain2 + cp2

rs = t1.sqrt()
s = t2.sqrt() + t1

r = rs + s

assert process(r, s) == t1

print hex(polyton(cp3 + r)).decode("hex")

