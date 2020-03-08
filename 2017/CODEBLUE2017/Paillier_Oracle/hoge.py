# coding: utf-8

import string
from trmr import *
from hashlib import sha256
from itertools import product
from fractions import Fraction
from time import sleep


remoteip = "127.0.0.1"
remoteport = 7485
s,f = sock(remoteip, remoteport)

def proof_of_work():
    data = read_until(f).strip()
    print data
    suffix = data.split(" ")[0].strip("SHA256()").strip("XXXX+")
    print "[+] suffix:", suffix
    _hash = data.split(" ")[-1]
    print "[+] Correct Hash:", _hash
    print "[+] BruteForce... "
    rep = 4
    for x in product(string.ascii_letters+string.digits, repeat=rep):
        x = "".join(x)
        if sha256(x+suffix).hexdigest() == _hash:
            print "[+] Detect! :",x
            break
    read_until(f, "What is XXXX? ")
    s.send(x+"\n")

def get_pk_and_flag():
    read_until(f,"Done.\n")
    recv_data = read_until(f).strip()
    #print recv_data
    n, g = eval(recv_data.split(":")[-1])
    print "[+] n:", type(n)
    print "[+] g:", g
    recv_data = read_until(f).strip()
    print recv_data
    enc_flag = long(recv_data.split(":")[-1])
    return n, g, enc_flag

def get_lsb(cipher,i):
    read_until(f).strip() # "Your ciphertext here: "
    s.send(str(cipher)+"\n")
    recv_data = read_until(f).strip()
    print i,recv_data
    return int(recv_data.split()[-1])

def main():
    #proof_of_work()
    n, g, enc_flag = get_pk_and_flag()
    print "n",n
    print "g",g
    print "e",enc_flag

    # LSB Oracle Attack for Paillier Oracle
    # Reference: http://inaz2.hatenablog.com/entry/2016/11/09/220529
    lb = 0
    ub = Fraction(n)
    send_cipher = enc_flag
    nn = n**2
    i = 0
    while True:
        print "OK" if (send_cipher * send_cipher) > nn  else "NG"
        send_cipher = (send_cipher * send_cipher) % nn
        print send_cipher
        lsb = get_lsb(send_cipher,i)
        if lsb:
            lb = (lb+ub)/2
        else:
            ub = (lb+ub)/2
        diff = ub - lb
        diff = diff.numerator / diff.denominator
        if diff == 0:
            m = ub.numerator / ub.denominator
            break
        i+=1
        sleep(0.1)
    print "[+] m:", m
   #print "[+] Flag:",l2b(m)

    s.close()
    f.close()

if __name__ == "__main__":
    main()