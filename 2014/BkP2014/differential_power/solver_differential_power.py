#!/usr/bin/env python2

from z3 import *
from trmr import *
import subprocess
import struct

n = 100

# making plaintext

data = {}

print "[+] Collecting flipped bits..."
for _ in range(n):
    s = randstr(8)
    d = subprocess.check_output(["./a.out", s]).replace("\x00", "")
    data[s] = eval("["+d+"]")
print "[+] Done."
print ""

print "[+]  Setting SMT..."

k0bitsum = data.values()[0][10]
k1bitsum = data.values()[0][11]
k2bitsum = data.values()[0][12]
k3bitsum = data.values()[0][13]

s = Solver()
k0, k1, k2, k3 = BitVecs("k0 k1 k2 k3", 32)

s.add(k0 & 0x80808080 == 0)
s.add(k1 & 0x80808080 == 0)
s.add(k2 & 0x80808080 == 0)
s.add(k3 & 0x80808080 == 0)
s.add(bitsum32(k0) == k0bitsum)
s.add(bitsum32(k1) == k1bitsum)
s.add(bitsum32(k2) == k2bitsum)
s.add(bitsum32(k3) == k3bitsum)

for plain, flipped_bit in data.items():
    v0 = struct.unpack(">I", plain[:4])[0]
    v1 = struct.unpack(">I", plain[4:8])[0]

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
    s.add(bitsum32(s4b ^ s4) == flipped_bit[18])
    s4 = s4b

    # 19  add $s3, $t6, $t0# (v1 + sum) part 2 is in s3 ; 01c89820
    s3b = (t6 + t0) & 0xffffffff
    s.add(bitsum32(s3b ^ s3) == flipped_bit[19])
    s3 = s3b

    # 20  srl $s2, $t6, 5# (v1 >> 5) ; 000e9142
    s2 = (t6 >> 5) & 0xffffffff

    # 21  add $s2, $s2, $s7# +k1, now do the xors part 3 in s2 ; 02579020
    s2b = (s2 + s7) & 0xffffffff
    s.add(bitsum32(s2b ^ s2) == flipped_bit[21])
    s2 = s2b

    # 22  xor $s1, $s2, $s3# xor 2 and 3 parts ; 02728826
    s1b = s2 ^ s3
    s.add(bitsum32(s1b ^ s1) == flipped_bit[22])
    s1 = s1b

    # 23  xor $s1, $s1, $s4# xor 1(2,3) ; 2348826
    s1b = s1 ^ s4
    s.add(bitsum32(s1b ^ s1) == flipped_bit[23])
    s1 = s1b

    # 24  add $t7, $t7, $s1# done with line 2 of the tea loop ; 01f17820
    t7b = (t7 + s1) & 0xffffffff
    s.add(bitsum32(t7b ^ t7) == flipped_bit[24])
    t7 = t7b

    # 25  sll $s4, $t7, 4# (v0 << 4) ; 000fa100
    s4b = (t7 << 4) & 0xffffffff
    s.add(bitsum32(s4b ^ s4) == flipped_bit[25])
    s4 = s4b

    # 26  add $s4, $s4, $s6# +k2 part 1 in s4 ; 0296a020
    s4b = (s4 + s6) & 0xffffffff
    s.add(bitsum32(s4b ^ s4) == flipped_bit[26])
    s4 = s4b

    # 27  add $s3, $t7, $t0# (v0 + sum) part 2 in s3  ; 01e89820
    s3b = (t7 + t0) & 0xffffffff
    s.add(bitsum32(s3b ^ s3) == flipped_bit[27])
    s3 = s3b

    # 28  srl $s2, $t7, 5# (v0 >> 5) ; 000f9142
    s2b = LShR(t7, 5)
    s.add(bitsum32(s2b ^ s2) == flipped_bit[28])
    s2 = s2b

    # 29  add $s2, $s2, $t3# +k3 part 2 in s2 ; 024b9020
    s2b = (s2 + t3) & 0xffffffff
    s.add(bitsum32(s2b ^ s2) == flipped_bit[29])
    s2 = s2b

    # 30  xor $s1, $s2, $s3# xor 2 and 3 parts ; 2728826
    s1b = s2 ^ s3
    s.add(bitsum32(s1b ^ s1) == flipped_bit[30])
    s1 = s1b

    # 31  xor $s1, $s1, $s4# xor 1(2,3) ; 2348826
    s1b = s1 ^ s4
    s.add(bitsum32(s1b ^ s1) == flipped_bit[31])
    s1 = s1b

    # 32  add $t6, $t6, $s1# done with line 2! ; 01d17020
    t6b = (t6 + s1) & 0xffffffff
    s.add(bitsum32(t6b ^ t6) == flipped_bit[32])
    t6 = t6b

    # 33  addi $s0, $zero, 32# for compare ; 20100020
    # 34  addi $t2, $t2, 1# the counter ; 214a0001
    # 35  bne $t2, $s0, 17# bne loop, now save back to the memory ; 15500010
print "[+] Done."
print ""


print "[+] Solving SMT..."

r = s.check()
if r == sat:
    m = s.model()
    print m
    print num2str(m[k0].as_long())
    print num2str(m[k1].as_long())
    print num2str(m[k2].as_long())
    print num2str(m[k3].as_long())
else:
    print r