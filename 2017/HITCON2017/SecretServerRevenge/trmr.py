import re
import socket
import struct
import telnetlib
import functools
import math
import itertools
import hashlib
import string


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


def send_line(s, buf):
    s.sendall(buf+'\n')


def interact(s):
    t = telnetlib.Telnet()
    t.sock = s
    try:
        t.interact()
    finally:
        disconnect(s)


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
