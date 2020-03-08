import re
import socket
import struct
import telnetlib
import functools
import math
import itertools
import hashlib
import string
import gmpy
import random
import Crypto


def p(a): return struct.pack("<I",a)


def u(a): return struct.unpack("<I",a)[0]


def pQ(a): return struct.pack("<Q",a&0xffffffffffffffff)


def uQ(a): return struct.unpack("<Q",a)[0]


def sock(remoteip, remoteport):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remoteip, remoteport))
    return s, s.makefile('rw', bufsize=0)


def disconnect(s):
    s.shutdown(socket.SHUT_WR)


def read_until(f, term='\n'):
    buf = ''
    while not buf.endswith(term):
        buf += f.read(1)
    return buf


def recv_until(s, term='\n'):
    buf = ''
    while not buf.endswith(term):
        buf += s.recv(1)
    return buf


def expect(s, term):
    buf = ''
    m = None
    while not m:
        buf += s.recv(1)
        m = re.search(term, buf)
    return m


def read_line(f):
    return read_until(f, '\n')


def recv_line(s):
    return recv_until(s, '\n')

def write_line(f, buf):
    f.write(buf+'\n')

def send_line(s, buf):
    s.sendall(buf+'\n')



def interact(s):
    t = telnetlib.Telnet()
    t.sock = s
    try:
        t.interact()
    finally:
        disconnect(s)

def process(*cmd):
    import subprocess
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.communicate()[0]


def proof_of_work(suffix, digest):
    for prefix in itertools.product(string.ascii_letters + string.digits, repeat=4):
        p = "".join(prefix)
        if hashlib.sha256(p + suffix).hexdigest() == digest:
            return p


# Kasiski test
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


def xor_str(x, y):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(x, y))


def divide_into_blocks(text, blocklen):
    return [text[i:i+blocklen] for i in xrange(0, len(text), blocklen)]


def flip_iv(oldplain, newplain, iv):
    flipmask = xor_str(oldplain, newplain)
    return xor_str(iv, flipmask)

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

nthroot = lambda a, r: int(gmpy.root(a, r)[0])
modinv = lambda a, m: int(gmpy.invert(a, m))
egcd = lambda x, y: map(int, gmpy.gcdext(x, y))

def str2num(s):
    return int(s.encode('hex'), 16)

def num2str(n):
    h = hex(n)
    if h[-1] == "L": h = h[:-1]
    return h[2:].decode('hex')

randstr = lambda n: ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

def bitsum32(vec):
    # z3py friendly
    res = vec & 1
    for i in range(1, 32):
        res += ((vec & (1 << i)) >> i) & 1
    return res

def rsapem(d, e, n):
    key = Crypto.PublicKey.RSA.construct(map(long, (n,e,d)))
    return key.exportKey()

# http://inaz2.hatenablog.com/entry/2016/01/15/011138
def continued_fraction(e, n):
    """
    415/93 = 4 + 1/(2 + 1/(6 + 1/7))

    >>> continued_fraction(415, 93)
    [4, 2, 6, 7]
    """
    cf = []
    while n:
        q = e // n
        cf.append(q)
        e, n = n, e - n * q
    return cf

def convergents_of_contfrac(cf):
    """
    4 + 1/(2 + 1/(6 + 1/7)) is approximately 4/1, 9/2, 58/13 and 415/93

    >>> list(convergents_of_contfrac([4, 2, 6, 7]))
    [(4, 1), (9, 2), (58, 13), (415, 93)]
    """
    n0, n1 = cf[0], cf[0]*cf[1]+1
    d0, d1 = 1, cf[1]
    yield (n0, d0)
    yield (n1, d1)

    for i in xrange(2, len(cf)):
        n2, d2 = cf[i]*n1+n0, cf[i]*d1+d0
        yield (n2, d2)
        n0, n1 = n1, n2
        d0, d1 = d1, d2

def wieners_attack(e, n):
    cf = continued_fraction(e, n)
    convergents = convergents_of_contfrac(cf)

    for k, d in convergents:
        if k == 0:
            continue
        phi, rem = divmod(e*d-1, k)
        if rem != 0:
            continue
        s = n - phi + 1
        # check if x^2 - s*x + n = 0 has integer roots
        D = s*s - 4*n
        if D > 0 and gmpy.is_square(D):
            return d

'''
Under this line, for Sagemath
'''
def ntopoly(npoly):
    return sum(c*X**e for e, c in enumerate(Integer(npoly).bits()))

def polyton(poly):
    if not hasattr(poly, 'list'):
      poly = poly.polynomial()
    a = poly.list()
    return sum(int(a[i])*(1 << i) for i in xrange(len(a)))
