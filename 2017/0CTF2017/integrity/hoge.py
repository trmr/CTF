#!/usr/bin/env python

def xor(s1,s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))


s1 = "11111"
s2 = "bbbbb"

print(xor(s1,s2))