# Python 3 Source Code
from base64 import b64encode, b64decode
import sys
import os
import random
import functools
import math

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'

def shift(char, key, rev = False):
    if not char in chars:
        return char
    if rev:
        return chars[(chars.index(char) - chars.index(key)) % len(chars)]
    else:
        return chars[(chars.index(char) + chars.index(key)) % len(chars)]

f = open("encrypted.txt")
encrypted = f.read()
f.close()

def decrypt(encrypted, key):
    return b64decode(''.join([shift(c, key[i % len(key)], True) for i, c in enumerate(encrypted)]))

# First, we try to determine the key length with Kasiski test.
def kasiski_test(s, l):
    dists = []
    for i in range(len(s) - l):
        word = s[i : i+l]
        j = s[i + l : ].find(word)
        if j != -1:
            dist = (i+l+j) - i
            dists += [ dist ]
    dist = functools.reduce(math.gcd, dists)
    return dist
keylen = kasiski_test(encrypted, 3)

isascii = lambda s: all([ c < 128 for c in s ]) # for bytes
chunk = lambda s, l: [s[i:i+l] for i in range(0, len(s), l)]

# BASE64 changes 3 characters to 4 encoded characters.
# We can check every 4 encoded characters if key is True by recovering

def is_valid_key_block(key, k, restricts=3):
    key += 'A'*(4 - len(key))
    plaintext = decrypt(encrypted, key)
    for s in chunk(plaintext, 3)[k::keylen//4]: # 3文字ごとにリスト化した文字列を鍵長文抜き出し
        if not isascii(s[:restricts]):
            return False
    return True

for i in range(keylen//4):
    for k1 in chars:
        for k2 in chars:
            if not is_valid_key_block(k1+k2, i, 1):
                continue
            for k3 in chars:
                if not is_valid_key_block(k1+k2+k3, i, 2):
                    continue
                for k4 in chars:
                    if is_valid_key_block(k1+k2+k3+k4, i, 3):
                        key = k1+k2+k3+k4
                        plaintext = decrypt(encrypted, key)
                        print(i, key, b'  '.join(chunk(plaintext, 3)[i::keylen//4]))
