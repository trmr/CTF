#!/usr/bin/env python

from sage.all import *
from Crypto.Util.number import *

f = open('org/ciphertext')
test = int(f.readline())

state = [16792192752041738357, 15780247886525933760]

N = 19453732258977745326025388758153985268982006451140824757000875212184286083381433617263912942983251278765032307210603967448246956716093385842705010547192205186910095528300402766101045595333634096500655068058435734427982638921074554555571353505677629583868624108023562705093181155852260863983232786900810202073059839371840527359556882787435383770700645818449308217497410666233956061743392826535373069509760643989700464609464412901676248732563432520371024184711302194691802836944113690223114313957200851128792883769170373839498570722327593478812307737852154233310488665561546258102925094401429619023719535721669309886801
e = 4919

bob = []

def randgen(): # [Check] Why use original RNG?
    s = [16792192752041738357, 15780247886525933760]

    while True:
        s1 = s[0]
        s0 = s[1]
        s[0] = s0
        s1 ^= (s1 << 23) & ( pow(2,64) - 1)
        s[1] = s1 ^ s0 ^ (s1 >> 18) ^ (s0 >> 5)

        yield (s[1] + s0) & ( pow(2,64) - 1)

#print b

rand = randgen()

print "RNG test."
test = 0
for x in range(2048 / 64):  # 2048/64 = 32
    z = next(rand)
    test = (test << 64) + z
print str(test) + "\n"  # test = rand32

for a in range(2):
    b = 0
    for x in range(2048 / 64 - 1):
        b = (b << 64) + next(rand)  # b = rand31
    bob.append(b)

print "[*]b1: ",bob[0]
print "[*]b2: ",bob[1]


c = []
for _ in range(2):
    c.append(int(f.readline().rstrip()))

#print c
print "[*]c1: ",c[0]
print "[*]c2: ",c[1]


x = PolynomialRing(Zmod(N),'x').gen()

g1 = (x + bob[0] - bob[1])**e -c[0]
g2 = (x)**e -c[1]

# gcd
while g2:
    g1, g2 = g2, g1 % g2

#print g1
g = g1.monic()
assert g.degree() == 1, "Failed 2"

#print g

print "[*]m+b:",-int(g[0])%N

msg = (-int(g[0]) - bob[1]) % N
#print msg
print long_to_bytes(msg)


