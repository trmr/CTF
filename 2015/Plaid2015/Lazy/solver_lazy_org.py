# Usage: sage -python solve.py  
import warnings  
with warnings.catch_warnings() as w:  
    warnings.simplefilter("ignore")  
    from Crypto.Util.number import GCD, bytes_to_long, long_to_bytes, inverse  
    
import sys  
import socket  
import math  
from sage.all import *  
    
def bitvector_to_bytes(l):  
    x = 0  
    for b in l[::-1]:  
        x = (x << 1) | b  
    return long_to_bytes(x)  
    
def lll_reduction(mat):  
    sage_reduced = mat.transpose().LLL().transpose()  
    return sage_reduced  
    
def is_valid_column(v):  
    if v[-1] != 0:  
        return False  
    found = True  
    for x in v[:-1]:  
        if x != -1 and x != 1:  
            found = False  
            break  
    return found  
    
def find_answer(columns):  
    for i in range(len(columns)):  
        v = columns[i]  
        if is_valid_column(v): return v  
    return None  
    
class AbortException(Exception):  
    pass  
    
def cryptanalysis(c, pk):  
    n = len(pk)  
    mat = []  
    lam = 1000000000000000000  
    for i in xrange(n):  
        v = [0] * (n + 1)  
        v[i] = 2  
        v[-1] = -1  
        mat.append(v)  
    mat.append(map(lambda x: lam*x, pk + [-c]))  
    mat = matrix(mat)  
    reduced = lll_reduction(mat)  
    columns = reduced.columns()  
    x = find_answer(columns)  
    print x
    if x is None:  
        raise AbortException()  
    x = map(lambda t: (int(t)+1)/2, list(x[:-1]))  
    print x  
    return bitvector_to_bytes(x)  
    
def main():  
    pubkey_file = "pubkey.txt"  
    ciphertext_file = "ciphertext.txt"  
    pk = eval(open(pubkey_file).read())  
    c = int(open(ciphertext_file).read())  
    print cryptanalysis(c, pk)  
    
main()  