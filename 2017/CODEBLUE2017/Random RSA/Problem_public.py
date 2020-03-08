import os, struct
from Crypto.Util.number import *

def genkey(k):
    e = 4919 # [check] Why 4919?
    while True:
        p = getPrime(k/2)
        q = getPrime(k/2)
        N = p*q
        phi = (q*q-1) * (p*p-1) / GCD(q*q-1, p*p-1)
        if GCD(phi, e) == 1:
            break
    d = inverse(e, phi)
    pk = (N, e)
    sk = (p, q, d)
    return (pk, sk)

(pk, sk) = genkey(2048)
(N, e) = pk
(p, q, d) = sk

def randgen(): # [Check] Why use original RNG?
    s = []
    for a in range(0,2):
      s.append( struct.unpack("<Q",os.urandom(8))[0] )

    while True:
      s1 = s[0]
      s0 = s[1]
      s[0] = s0
      s1 ^= (s1 << 23) & ( pow(2,64) - 1)
      s[1] = s1 ^ s0 ^ (s1 >> 18) ^ (s0 >> 5)

      yield (s[1] + s0) & ( pow(2,64) - 1)

with open("publickey", "w") as f:
    f.write(str(N) + "\n")
    f.write(str(e) + "\n")
with open("secretkey", "w") as f:
    f.write(str(p) + "\n")
    f.write(str(q) + "\n")
    f.write(str(d) + "\n")

flag = "CBCTF{ *** censored *** len(flag) = ? ***}"
L = size(N)/8-1 # size(N) = 2048, so L = 255
pad = os.urandom(L-len(flag)-1) # length of pad is 254 - len(flag)
m = bytes_to_long(pad+"\0"+flag) # len(m) = 255

rand = randgen()

with open("ciphertext", "w") as f:
  print "RNG test."
  test = 0
  for x in range(2048/64): # 2048/64 = 32
    z = next(rand)
    test = (test<<64)+z
  f.write(str(test) + "\n") # test = rand32

  for a in range(0,e):
    b = 0
    for x in range(2048/64 - 1):
      b = (b<<64)+next(rand) # b = rand31

    c = pow(m + b,e,N) # (m + rand31) ^ e mod N
    assert pow(c,d,N) == m+b
    assert "CBCTF" not in long_to_bytes(m+b)
    assert "CBCTF" in long_to_bytes(pow(c,d,N)-b)

    print long_to_bytes(m+b)
    print long_to_bytes(c)
    f.write(str(c) + "\n")

