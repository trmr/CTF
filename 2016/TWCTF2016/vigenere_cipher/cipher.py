# Python 3 Source Code
from base64 import b64encode, b64decode
import sys
import os
import random

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'

def shift(char, key, rev = False):
    if not char in chars:
        return char
    if rev:
        print(chars.index(char))
        print(key)
        print(chars.index(key))
        return chars[(chars.index(char) - chars.index(key)) % len(chars)]
    else:
        return chars[(chars.index(char) + chars.index(key)) % len(chars)]

def encrypt(message, key):
    encrypted = b64encode(message.encode('ascii')).decode('ascii')
    return ''.join([shift(encrypted[i], key[i % len(key)]) for i in range(len(encrypted))])

def decrypt(encrypted, key):
    encrypted = ''.join([shift(encrypted[i], key[i % len(key)], True) for i in range(len(encrypted))])
    return b64decode(encrypted.encode('ascii')).decode('ascii')

def generate_random_key(length = 5):
    return ''.join(map(lambda a : chars[a % len(chars)], os.urandom(length)))

if len(sys.argv) == 4 and sys.argv[1] == 'encrypt':
    f = open(sys.argv[3])
    plain = f.read()
    f.close()

    key = generate_random_key(random.randint(5,14))

    print(encrypt(plain, key))

    f = open(sys.argv[2], 'w')
    f.write(key)
    f.close()

elif len(sys.argv) == 4 and sys.argv[1] == 'decrypt':
    f = open(sys.argv[3])
    encrypted = f.read()
    f.close()

    f = open(sys.argv[2])
    key = f.read()
    f.close()

    print(decrypt(encrypted, key), end = '')

else:
    print("Usage: python %s encrypt|decrypt (key-file) (input-file)" % sys.argv[0])
