import re
import socket
from telnetlib import Telnet


def xor(x, y):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(x, y))

def disconnect(s):
    s.shutdown(socket.SHUT_WR)

def recvuntil(s, term):
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

def recvline(s):
    return recvuntil(s, '\n')

def sendline(s, buf):
    s.sendall(buf+'\n')

def interact(s):
    t = Telnet()
    t.sock = s
    try:
        t.interact()
    finally:
        disconnect(s)