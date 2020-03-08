#!/usr/bin/env python2

from trmr import *
from fractions import Fraction
import time

HOST = '127.0.0.1'
PORT = 7485

s,f = sock(HOST,PORT)


print "[+] Proofing of work..."
read_until(f, 'XXXX+')
suffix = read_until(f,')')[:-1]
read_until(f, '== ')
digest = read_until(f,'\n').rstrip()

print "[*]suffix: ", suffix
print "[*]digest: ", digest
prefix =  proof_of_work(suffix, digest)
print "[*]prefix: ", prefix
print ""

write_line(f, prefix)

read_until(f, "Public key is here:")
pk = read_line(f)
#print pk
pk = eval(pk.strip())
n = pk[0]
g = pk[1]
read_until(f, "Encrypted Flag:")
enc_flag = read_line(f)
#print enc_flag
enc_flag = int(enc_flag.strip())

print "[*]n: ",n
print "[*]g: ",g
print "[*]Encrypted Flag: ",enc_flag
print ""

def oracle(x):
    read_line(f)
    f.write(str(x)+'\n')
    return int(read_line(f).strip()[-1])

def lsb_decryption_oracle(c, oracle):
    bounds = [0, Fraction(n)]

    nn = pow(n,2)
    i = 0
    #start = time.time()
    while True:
        #print "OK" if (c * c) > nn else "NG"
        i += 1
        if i % 100 == 0:
            #stop = time.time()
            print "{0}".format(i)
            #print stop - start

        c2 = (c * c) % nn
        lsb = oracle(c2)
        if lsb == 1:
            bounds[0] = sum(bounds)/2
        else:
            bounds[1] = sum(bounds)/2
        diff = bounds[1] - bounds[0]
        diff = diff.numerator / diff.denominator
        #print bounds
        if diff == 0:
            m = bounds[1].numerator / bounds[1].denominator
            return m
        c = c2

print "[+]Asking Oracle..."
m = lsb_decryption_oracle(enc_flag, oracle)
print m
print num2str(m)