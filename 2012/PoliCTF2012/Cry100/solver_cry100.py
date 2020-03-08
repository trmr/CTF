#!/usr/bin/env python3

import math
import hashlib

f = open('chinese.txt')
chinese = int(f.read().rstrip())
f.close()

f = open('mod.txt')
mod = int(f.read().rstrip())
f.close()

f = open('steady.txt')
sign = int(f.read().rstrip())
f.close()


p = math.gcd(sign - chinese,mod)
q = mod // p

#print(p)
#print(q)

seed = "part1=%d\npart2=%d" % (p,q)
#print(seed)

print(hashlib.sha1(seed.encode('utf-8')).hexdigest())
