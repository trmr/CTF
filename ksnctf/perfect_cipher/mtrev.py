import random

# Usage
#   import mtrev, random
#   l = [0x********, ...] * 624
#   r = mtrev.recoverRandom(l)
#   print r.getrandbits(32)

def undoTemperShiftL(y):
    last14 = y >> 18
    final = y ^ last14
    return final

def undoTemperShiftT(y):
    temperingMaskC = 0xefc60000
    first17 = y << 15
    final = y ^ (first17 & temperingMaskC)
    return final

def undoTemperShiftS(y):
    temperingMaskB = 0x9d2c5680
    a = y << 7
    b = y ^ (a & temperingMaskB)
    c = b << 7
    d = y ^ (c & temperingMaskB)
    e = d << 7
    f = y ^ (e & temperingMaskB)
    g = f << 7
    h = y ^ (g & temperingMaskB)
    i = h << 7

    final = y ^ (i & temperingMaskB)
    return final

def undoTemperShiftU(y):
    a = y >> 11;
    b = y ^ a;
    c = b >> 11;
    final = y ^ c;
    return final

def untemper(y):
    y = undoTemperShiftL(y)
    y = undoTemperShiftT(y)
    y = undoTemperShiftS(y)
    y = undoTemperShiftU(y)
    return y

def recoverRandom(l):
    r = random.Random()
    l = map(untemper, l)
    st = (3, tuple(l+[624]), None)
    r.setstate(st)
    return r

if __name__ == '__main__':
    r = random.Random()
    r.seed(0x12345678)

    l = []
    for i in range(624):
        l.append(r.getrandbits(32))

    r2 = recoverRandom(l)

    print r.getrandbits(32)
    print r2.getrandbits(32)  
