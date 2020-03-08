import mtrev, random, struct

def p(a): return struct.pack("<I", a)
def u(a): return struct.unpack("<I", a)[0]
def enc_xor(a,b): return ''.join([chr(ord(c1)^ord(c2)) for (c1,c2) in zip(a, b)])

# read
f1 = open("encrypt.cpp").read()
f2 = open("encrypt.enc").read()[4:]
f3 = open("flag.enc").read()[4:]

print "[+] len(f1)=", len(f1), "block=", len(f1)/4
print "[+] len(f2)=", len(f2), "block=", len(f2)/4
print "[+] len(f3)=", len(f3), "block=", len(f3)/4

# get MT's pre random
xor = enc_xor(f1, f2)

pre_random = []
for i in xrange(len(xor)/4):
  n = u(xor[i*4:(i+1)*4]) # byte -> long
  pre_random.append(n)

# check to exceed the recoverable minimum number of blocks
if len(pre_random)<624:
  print "too short. decode error", exit()
else:
  print "[+] len(pre_random)=", len(pre_random), "/ 624 ... ok"

# MT recover
r = mtrev.recoverRandom(pre_random[:624])

# adjust
print "[+] Here is garbage. 625 ...", len(pre_random)
for i in xrange(len(xor)/4 - 624):
  dummy = r.getrandbits(32)
  print dummy

post_rand=""
for i in xrange(len(f3)/4):
    post_rand += p(r.getrandbits(32))

recover = enc_xor(f3, post_rand)

with open("flag.jpg", "wb") as f:
    f.write(recover)

print "[+] recovering finish!"
