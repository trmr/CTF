#!/usr/bin/env python

from z3 import *

f = open('org/ciphertext')
actual = int(f.readline())


state = [BitVec("state%d"%i, 64) for i in range(2)]
#state = [0,1]
#state = [16792192752041738357, 15780247886525933760]

#print f.readline()

act = []

for _ in range(32):
    act.append(actual & (pow(2,64) - 1))
    actual = actual >> 64


act.reverse()
#print act

s = Solver()

for i in range(2):
    s1 = state[0]
    s0 = state[1]
    state[0] = s0
    s1 ^= (s1 << 23) & ( pow(2,64) - 1)
    state[1] = s1 ^ s0 ^ LShR(s1, 18) ^ LShR(s0, 5)
    #state[1] = s1 ^ s0 ^ (s1 >> 18) ^ (s0 >> 5)
    output = (state[1] + s0) & (pow(2,64) - 1)
    s.add(output == act[i])
    #print output

print s.check()
m = s.model()
print m
