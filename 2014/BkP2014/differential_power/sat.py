#!/usr/bin/python
#-*- coding:utf-8 -*-

import re
import random

from struct import unpack

from z3.z3 import *


def randstrnp(n):
    while True:
        s = "".join(random.choice(map(chr, range(65, 70))) for i in range(n))
        if "/" not in s:  # this was banned by HTTP server
            return s


def get_data(s):
    # use locally compiled binary if service is down
    if 1:
        import subprocess
        if "\x00" in s or "\x2f" in s:
            raise IndexError("qwe")
        data = subprocess.check_output(["./a.out", s]).replace("\x00", "")
        return eval("[" + data + "]")
    else:
        import requests
        from urllib import quote
        r = requests.get("http://54.218.22.41:6969/" + quote(s))
        data = re.findall(r"Array\(([\s\d,\[\]]*?)\);", r.content, re.DOTALL)[0]
        arr = eval(data)
        return map(lambda x: x[1], arr)


def bitsum(vec):
    # z3py friendly
    res = vec & 1
    for i in range(1, 32):
        res += ((vec & (1 << i)) >> i) & 1
    return res


known = {}
for i in range(10):
    s = randstrnp(16)
    known[s] = get_data(s)

data = known.values()[0]
k0bitsum = data[10]
k1bitsum = data[11]
k2bitsum = data[12]
k3bitsum = data[13]

print len(known), "collected"

S = Solver()
k0, k1, k2, k3 = BitVecs("k0 k1 k2 k3", 32)
S.add(k0 & 0x80808080 == 0)
S.add(k1 & 0x80808080 == 0)
S.add(k2 & 0x80808080 == 0)
S.add(k3 & 0x80808080 == 0)
S.add(bitsum(k0) == k0bitsum)
S.add(bitsum(k1) == k1bitsum)
S.add(bitsum(k2) == k2bitsum)
S.add(bitsum(k3) == k3bitsum)

for s, data in known.items():
    v0 = unpack(">I", s[:4])[0]
    v1 = unpack(">I", s[4:8])[0]

    s0 = s1 = s2 = s3 = s4 = s5 = s6 = s7 = s8 = 0
    t0 = t1 = t2 = t3 = t4 = t5 = t6 = t7 = t8 = 0

    # 0  add $t1, $zero, $zero# clear out $t1 ; 00004820
    # 1  addi $t1, $t1, 0x9e# TEA magic is 0x9e3779b7 ; 2129009E
    # 2  sll $t1, $t1, 8# shift out making room in the bottom 4; 00094a00
    # 3  addi $t1, $t1, 0x37 ; 21290037
    # 4  sll $t1, $t1, 8 ; 00094a00
    # 5  addi $t1, $t1, 0x79 ; 21290079
    # 6  sll $t1, $t1, 8 ; 00094a00
    # 7  addi $t1, $t1, 0xb9 # now $t1 holds the magic 0x9e3779b9 ; 212900b9
    t1 = 0x9e3779b9

    # 8  add $t2, $zero, $zero# $t2 is the counter ; 00005020
    t2 = 0

    # 9  add $t0, $zero, $zero# $t0 is the sum ; 00004020
    t0 = 0

    # 10  lw $t8, $zero, 8# k0 mem[8-23] = k ; 8c180008
    t8 = k0

    # 11  lw $s7, $zero, 12# k1 ; 8C17000C
    s7 = k1

    # 12  lw $s6, $zero, 16# k2 ; 8C160010
    s6 = k2

    # 13  lw $t3, $zero, 20# k3 now our keys are in registers ;  8c0b0014
    t3 = k3

    # 14  lw $t7, $zero, 0# v0 mem[0-7] = v ; 8c0f0000
    t7 = v0

    # 15  lw $t6, $zero, 4# v1, our plaintext is in the registers ; 8c0e0004
    t6 = v1

    # 16  loop: add $t0, $t0, $t1# sum+=delta ; 01094020
    t0 = (t0 + t1) & 0xffffffff

    # 17  sll $s4, $t6, 4# (v1 << 4) ; 000ea100
    s4 = (t6 << 4) & 0xffffffff

    # 18  add $s4, $s4, $t8# +k0  part 1 is in s4 ; 0298a020
    s4b = (s4 + t8) & 0xffffffff
    S.add(bitsum(s4b ^ s4) == data[18])
    s4 = s4b

    # 19  add $s3, $t6, $t0# (v1 + sum) part 2 is in s3 ; 01c89820
    s3b = (t6 + t0) & 0xffffffff
    S.add(bitsum(s3b ^ s3) == data[19])
    s3 = s3b

    # 20  srl $s2, $t6, 5# (v1 >> 5) ; 000e9142
    s2 = (t6 >> 5) & 0xffffffff

    # 21  add $s2, $s2, $s7# +k1, now do the xors part 3 in s2 ; 02579020
    s2b = (s2 + s7) & 0xffffffff
    S.add(bitsum(s2b ^ s2) == data[21])
    s2 = s2b

    # 22  xor $s1, $s2, $s3# xor 2 and 3 parts ; 02728826
    s1b = s2 ^ s3
    S.add(bitsum(s1b ^ s1) == data[22])
    s1 = s1b

    # 23  xor $s1, $s1, $s4# xor 1(2,3) ; 2348826
    s1b = s1 ^ s4
    S.add(bitsum(s1b ^ s1) == data[23])
    s1 = s1b

    # 24  add $t7, $t7, $s1# done with line 2 of the tea loop ; 01f17820
    t7b = (t7 + s1) & 0xffffffff
    S.add(bitsum(t7b ^ t7) == data[24])
    t7 = t7b

    # 25  sll $s4, $t7, 4# (v0 << 4) ; 000fa100
    s4b = (t7 << 4) & 0xffffffff
    S.add(bitsum(s4b ^ s4) == data[25])
    s4 = s4b

    # 26  add $s4, $s4, $s6# +k2 part 1 in s4 ; 0296a020
    s4b = (s4 + s6) & 0xffffffff
    S.add(bitsum(s4b ^ s4) == data[26])
    s4 = s4b

    # 27  add $s3, $t7, $t0# (v0 + sum) part 2 in s3  ; 01e89820
    s3b = (t7 + t0) & 0xffffffff
    S.add(bitsum(s3b ^ s3) == data[27])
    s3 = s3b

    # 28  srl $s2, $t7, 5# (v0 >> 5) ; 000f9142
    s2b = LShR(t7, 5)
    S.add(bitsum(s2b ^ s2) == data[28])
    s2 = s2b

    # 29  add $s2, $s2, $t3# +k3 part 2 in s2 ; 024b9020
    s2b = (s2 + t3) & 0xffffffff
    S.add(bitsum(s2b ^ s2) == data[29])
    s2 = s2b

    # 30  xor $s1, $s2, $s3# xor 2 and 3 parts ; 2728826
    s1b = s2 ^ s3
    S.add(bitsum(s1b ^ s1) == data[30])
    s1 = s1b

    # 31  xor $s1, $s1, $s4# xor 1(2,3) ; 2348826
    s1b = s1 ^ s4
    S.add(bitsum(s1b ^ s1) == data[31])
    s1 = s1b

    # 32  add $t6, $t6, $s1# done with line 2! ; 01d17020
    t6b = (t6 + s1) & 0xffffffff
    S.add(bitsum(t6b ^ t6) == data[32])
    t6 = t6b

    # 33  addi $s0, $zero, 32# for compare ; 20100020
    # 34  addi $t2, $t2, 1# the counter ; 214a0001
    # 35  bne $t2, $s0, 17# bne loop, now save back to the memory ; 15500010


def n2s(n):
    return ("%08x" % n).decode("hex")


print S.check()
m = S.model()
print m
print hex(m[k0].as_long()), n2s(m[k0].as_long())
print hex(m[k1].as_long()), n2s(m[k1].as_long())
print hex(m[k2].as_long()), n2s(m[k2].as_long())
print hex(m[k3].as_long()), n2s(m[k3].as_long())
