#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys, re
from socket import *

HOST = "172.16.12.133"
PORT = 7777

# ----------------------------------------------------------------
# SERVICE
# ----------------------------------------------------------------
def main():
    sbox = [-1]
    for i in range(1,128):
        req = 'a' + chr(i)
        sbox += connect_receive(req)


    key_len = sbox[-1] # It is correct with high probability
    sub_key(sbox,'a')


    reversed_key = []

    for i in range(key_len)[::-1]:
        for x in xrange(len(sbox)):
            sbox[x] = (sbox[x] - 1) % 128
        k = sbox.index(i+i)
        reversed_key += chr(k)
        sbox[i], sbox[k] = sbox[k],sbox[i]

    print ''.join(reversed_key[::-1])



def connect_receive(data):
    f = socket(AF_INET, SOCK_DGRAM)
    f.connect((HOST, PORT))

    f.sendall(data)

    res = f.recv(4096)

    return [ord(res.decode("hex"))]

def sub_key(sbox, k):
    for i, c in enumerate(k):
        for x in xrange(len(sbox)):
            sbox[x] = (sbox[x] - 1) % 128
        sbox[i], sbox[ord(c)] = sbox[ord(c)], sbox[i]


if __name__ == "__main__":
    main()
