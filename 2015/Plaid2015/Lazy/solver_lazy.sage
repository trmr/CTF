"""
usage: sage -python solver_lazy.py
"""

from sage.all import *
import math
with warnings.catch_warnings() as w:
    warnings.simplefilter("ignore")
    from Crypto.Util.number import long_to_bytes

def create_matrix(c, pk):
    n = len(pk)
    i = matrix.identity(n)*2
    last_col = [-1]*n
    first_row = []
    for p in pk:
        first_row.append(int(long(p)))
    first_row.append(-c)

    m = matrix(ZZ,1,n+1,first_row)
    bottom =i.augment(matrix(ZZ,n,1,last_col)) 
    m = m.stack(bottom)
    return m

def is_short_vector(vector):
    for v in vector:
        if v != 1 and v != -1 and v != 0:
            return False
    return True

def find_short_vector(matrix):
    for col in matrix.columns():
        if col[0] != 0:
            continue
        if is_short_vector(col):
            return col

def main():
    pubkey_file = "pubkey.txt"
    ciphertext_file = "ciphertext.txt"
    pk = eval(open(pubkey_file).read())
    c = int(open(ciphertext_file).read())

    m = create_matrix(c, pk)
    lllm = m.transpose().LLL().transpose()
    short_vector = find_short_vector(lllm)

    solution_vector = []
    for v in short_vector:
        if v == 1:
            solution_vector.append(1)
        elif v == -1:
            solution_vector.append(0)
            

    flag = hex(int(''.join([str(i) for i in solution_vector])[::-1], 2))[2:-1].decode('hex')
    print flag

main()