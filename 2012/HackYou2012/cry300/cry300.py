#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys, re
from socket import *

PORT = 7777 or int(sys.argv[1])
KEY = open("_flag.txt").read()

SBOX = list(range(128))
SALTED_SBOX = list(range(128))


# ----------------------------------------------------------------
# SERVICE
# ----------------------------------------------------------------
def main():
    print SALTED_SBOX
    add_key(SALTED_SBOX, KEY)
    print SALTED_SBOX
    serve()

def serve():
    f = socket(AF_INET, SOCK_DGRAM)
    f.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    f.bind(("", PORT))

    print "[*] Server started on %d" % PORT
    while True:
        data, addr = f.recvfrom(4096)
        client(data, addr, f)
    return

def client(data, addr, f):
    print "[.] GOT", repr(data), "FROM", addr

    print "test:%d" % len(data)

    if len(data) % 2 or len(data) > 64:
        return


    for ch in data:
        if ord(ch) >= 128:
            return

    mid = len(data) >> 1
    k = data[:mid].rstrip("\x00")
    m = data[mid:].rstrip("\x00")

    c = encrypt(SALTED_SBOX, k, m)
    f.sendto(c.encode("hex"), addr)
    print "[+] RESULT SENT", addr, "\n"
    return

# ----------------------------------------------------------------
# CRYPTO
# ----------------------------------------------------------------
def encrypt(sbox, k, m):
    sbox = sbox[::]
    add_key(sbox, k)

    c = ""
    for ch in m:
        c += chr(sbox[ord(ch)])
        sbox = combine(sbox, sbox)
    return c

def add_key(sbox, k):
    for i, c in enumerate(k):
        sbox[i], sbox[ord(c)] = sbox[ord(c)], sbox[i]
        for i in xrange(len(sbox)):
            sbox[i] = (sbox[i] + 1) % 128
    return

def combine(a, b):
    ret = [-1] * len(b)
    for i in range(len(b)):
        ret[i] = a[b[i]]
    return tuple(ret)


if __name__ == "__main__":
    main()
