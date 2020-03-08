import re
import socket
import struct
import telnetlib

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

def readuntil(f, term='\n'):
    buf = ''
    while not buf.endswith(term):
        buf += f.read(1)
    return buf

def recvuntil(s, term='\n'):
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

def readline(f):
    return readuntil(f, '\n')

def recvline(s):
    return recvuntil(s, '\n')

def sendline(s, buf):
    s.sendall(buf+'\n')

def interact(s):
    t = telnetlib.Telnet()
    t.sock = s
    try:
        t.interact()
    finally:
        disconnect(s)

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

def xor(x, y):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(x, y))
