from sage.all import *
import math
from Crypto.Cipher import AES  
with warnings.catch_warnings() as w:
    warnings.simplefilter("ignore")
    from Crypto.Util.number import long_to_bytes

def create_matrix(c, pk):
    n = len(pk)
    i = matrix.identity(n)
    last_col = [0]*n
    data_row = []
    for p in pk:
        data_row.append(int(long(-p*100000)))
    data_row.append(c*100000)
    last_row = [0]*n
    last_row.append(1)

    m = i.augment(matrix(ZZ,n,1,last_col))
    m = m.stack(matrix(ZZ,1,n+1,data_row))
    m = m.stack(matrix(ZZ,1,n+1,last_row))
    return m

def find_short_vector(matrix):
    for col in matrix.columns():
        if col[-2] == 0 and col[-1] == 1:
            print col
            return col

def main():
    pubkey_file = "pubkey"
    ciphertext_file = "encrypted_flag"
    pk = eval(open(pubkey_file).read())
    a = pk[0]
    print len(a)
    print math.log(max(a),2)
    b = pk[1]
    z = pk[2]
    n = pk[3]
    cf = eval(open(ciphertext_file).read())
    c = cf[0]

    m = create_matrix(c, a)
    lllm = m.transpose().LLL().transpose()
    short_vector = find_short_vector(lllm)

    solution_vector = []
    m = 0  
    for a in range(n):  
        m = m + (short_vector[a] * b[a])  
    m %= z 
    key = m  
    key2 = "%x" % key  
    iv = "%x" % cf[0]  
    
    cipher = AES.new(key2.decode('hex'), AES.MODE_CBC, iv.decode('hex')[0:16] )  
    print "%r" % cipher.decrypt( cf[1] )  

main()