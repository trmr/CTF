#!/usr/bin/env python2

from z3 import *

str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz_{}"
s = Solver()

pv = IntVector("X", 34)
sum = IntVector("Y", 14)

#enc = "POR4dnyTLHBfwbxAAZhe}}ocZR3Cxcftw9"
enc = [15,14,17,30,39,49,60,19,11,7,1,41,58,37,59,0,0,25,43,40,64,64,50,38,25,17,29,2,59,38,41,55,58,35]

s.add(pv[0] == 18)
s.add(pv[1] == 4)
s.add(pv[2] == 2)
s.add(pv[3] == 2)
s.add(pv[4] == 14)
s.add(pv[5] == 13)
s.add(pv[6] == 63)
s.add(pv[33] == 64)
s.add(sum[0] == 62)
s.add(sum[1] == 10)
s.add(sum[2] == 15)
s.add(sum[3] == 28)
s.add(sum[4] == 25)
s.add(sum[5] == 36)
s.add(sum[6] == 62)

s.add(sum[13] == 62)
s.add(sum[12] == 10)
s.add(sum[11] == 15)
s.add(sum[10] == 28)
s.add(sum[9] == 25)
s.add(sum[8] == 36)
s.add(sum[7] == 62)

for i in range(34):
    s.add((pv[i] + sum[i%14])%65 == enc[i])

r = s.check()
m = s.model()
for i in range(34):
    print str[m[pv[i]].as_long()]
    #print m[sum[i]].as_long()
