from Crypto.Util.number import *
from Crypto.Random.random import randint

import gmpy
import math
import key

FLAG = long(key.FLAG.encode("hex"), 16)

def get_random_prime(bits=1024):
  return int(gmpy.next_prime(randint(2**(bits-1), 2**bits)))

def gen_n(bits=1024):
  p = getStrongPrime(bits)
  q = getStrongPrime(bits)
  return p*q, p, q

def encrypt(pk, m):
  assert m < pk[0]
  return pow(m, pk[1], pk[0])

def decrypt(pk, sk, c):
  return pow(c, sk[0], pk[0])

def test(n, p, q, bits=1024):
  d_ = get_random_prime(int(math.floor(1024 * 0.2)))
  d = (p-1) * (q-1) - d_
  pk, sk = (p*q, long(gmpy.invert(d, (p-1)*(q-1)))), (d, )
  print "[+] RSA Self Test: %r" % (pk, )
  c = encrypt(pk, FLAG)
  print "[+] ciphertext = %d" % c
  m = decrypt(pk, sk, c)
  print "[+] Dec(Enc(m)) == m? : %s" % (m == FLAG)


if __name__ == "__main__":
  n, p, q = gen_n()
  test(n, p, q)
