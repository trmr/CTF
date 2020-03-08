from trmr import *

import base64

def pad(msg):
    pad_length = 16-len(msg)%16
    return msg+chr(pad_length)*pad_length


s, f = sock("172.16.12.143",1234)

# proof of work
print "[+] Proofing of work..."

recv_until(s,"XXXX+")
end = recv_until(s,")")[:-1]
recv_until(s,"== ")
digest = recv_until(s,"\n").rstrip()
prefix = proof_of_work(end, digest)
send_line(s, prefix)
# on my laptop, the string has noise. I don't know the reason.
b64_enc_welcome = recv_line(s)[13:].rstrip()
print "[+] Done."
print ""

print "welcome: ", b64_enc_welcome

encrypted_welcome = divide_into_blocks(base64.b64decode(b64_enc_welcome),16)


send_line(s, base64.b64encode("".join(encrypted_welcome)))
b64_enc_not_found = recv_line(s).rstrip()

new_iv = flip_iv(pad('Welcome!!'), pad('get-token'), encrypted_welcome[0])
send_line(s,base64.b64encode(new_iv + encrypted_welcome[1]))
b64_enc_token = recv_line(s).rstrip()
encrypted_token = divide_into_blocks(base64.b64decode(b64_enc_token),16)

print "not found:", b64_enc_not_found
print "token: ", b64_enc_token
print "token blocks: ", encrypted_token

token_length = 56 # from given source
#print "token-length: ",token_length

def get_encrypted_md5_token(index):
    new_iv = flip_iv(pad("token: "), pad("get-md5"), encrypted_token[0])
    payload = new_iv + "".join(encrypted_token[1:])
    next_to_last_block = flip_iv(pad('Welcome!!'), "A"*15 + chr(16 + 16 + token_length - index), encrypted_welcome[0])
    payload += next_to_last_block
    payload += encrypted_welcome[1]
    send_line(s, base64.b64encode("".join(payload)))
    return recv_line(s).rstrip()


collections_enc_md5_token = []

print ""
print "[+] Collecting enc_md5_token..."

# collect the enc(md5(token[0])), enc(md5(token[0:1])), enc(md5(token[0:2]))...
# send about 50 requests.
for index in range(token_length + 1):
    enc_md5_token = get_encrypted_md5_token(index)
    collections_enc_md5_token.append(enc_md5_token)
    print index, enc_md5_token

print "[+] Done."
print ""

oracle_md5_token = {}

def make_oracle_md5_token(unpad):
    new_iv = flip_iv(pad("token: "), pad("get-md5"), encrypted_token[0]) # 1st block
    payload = new_iv + "".join(encrypted_token[1:]) # 5th block
    payload += "A"*16*11 # 16th block
    next_to_last_block = flip_iv(pad('Welcome!!'), "A"*15+chr(unpad), encrypted_welcome[0])
    payload += next_to_last_block # 17th block
    payload += encrypted_welcome[1] # 18th block
    send_line(s, base64.b64encode("".join(payload)))
    return recv_line(s).rstrip()

print ""
print "[+] Collecting oracle..."

# this attack can't use 1-32. for decreasing requests, I don't send requests.
for unpad in range(32,209):
    oracle_md5 = make_oracle_md5_token(unpad)
    oracle_md5_token[oracle_md5] = unpad
    print unpad, oracle_md5

# if unpad deletes 6th-18th blocks, the rest is same as enc_md5_token
for unpad in range(209, 256):
    oracle_md5 = collections_enc_md5_token[264 - unpad]
    oracle_md5_token[oracle_md5] = unpad
    print unpad, oracle_md5

#print oracle_md5_token

print "[+] Done."

print ""
print "[+] Listing token candidates..."
cand = ['']

for index in range(token_length):
    new_iv = flip_iv(pad("token: "), pad("get-md5"), encrypted_token[0])
    payload = new_iv + "".join(encrypted_token[1:])
    payload += "A"*16*11
    payload += base64.b64decode(collections_enc_md5_token[index])[:-16]
    send_line(s, base64.b64encode("".join(payload)))
    res = recv_line(s).rstrip()

    if res in oracle_md5_token:
        #print "res",res
        lastbyte = oracle_md5_token[res]
        #print "lastbyte", lastbyte
        new_cand = []
        for x in cand:
            for c in range(256):
                if hashlib.md5(x + chr(c)).digest()[-1] == chr(lastbyte):
                    #print hashlib.md5(x + chr(c)).digest()[-1]
                    # print chr(lastbyte)
                    new_cand.append(x + chr(c))

        cand = new_cand

    elif res == b64_enc_not_found:
        lastbyte = 0
        new_cand = []
        for x in cand:
            for c in range(256):
                if hashlib.md5(x + chr(c)).digest()[-1] == chr(lastbyte):
                    new_cand.append(x + chr(c))
        cand = new_cand
        #print "cand2",cand
    else:
        #print "Not found [1-32]"
        new_payload = payload[:-17] + xor_str(payload[-17], '\x80') + payload[-16:]
        send_line(s, base64.b64encode(new_payload))
        res = recv_line(s).rstrip()

        if res in oracle_md5_token:
            lastbyte = oracle_md5_token[res] ^ 0x80
            new_cand = []
            for x in cand:
                for c in range(256):
                    if hashlib.md5(x + chr(c)).digest()[-1] == chr(lastbyte):
                        new_cand.append(x + chr(c))
            cand = new_cand
            #print "cand3",cand

        elif res == b64_enc_not_found:
            lastbyte = 0
            new_cand = []
            for x in cand:
                for c in range(256):
                    if hashlib.md5(x + chr(c)).digest()[-1] == chr(lastbyte):
                        new_cand.append(x + chr(c))
            cand = new_cand
            #print "cand4",cand
    print index, cand

print "[+] Done."
print ""

print "candidates are: ", cand
print "number of candidates: ", len(cand)

print ""
print "[+] Checking legitimate token..."

new_iv = flip_iv(pad("token: "), pad("get-md5"), encrypted_token[0])
payload = new_iv + "".join(encrypted_token[1:])
payload += "A" * 16 * 11
payload += base64.b64decode(collections_enc_md5_token[56])[:-16]
send_line(s, base64.b64encode("".join(payload)))
res = recv_line(s).rstrip()

c = '\x01'

check_cand = []

if res in oracle_md5_token:
    lastbyte = oracle_md5_token[res]
    new_cand = []
    for x in cand:
        if hashlib.md5(x + c).digest()[-1] == chr(lastbyte):
            print hashlib.md5(x + c).digest()[-1]
            print chr(lastbyte)
            new_cand.append(x)

    check_cand = new_cand

elif res == b64_enc_not_found:
    lastbyte = 0
    new_cand = []
    for x in cand:
        if hashlib.md5(x + c).digest()[-1] == chr(lastbyte):
            new_cand.append(x)
    check_cand = new_cand
else:
    new_payload = payload[:-17] + xor_str(payload[-17], '\x80') + payload[-16:]
    send_line(s, base64.b64encode(new_payload))
    res = recv_line(s).rstrip()

    if res in oracle_md5_token:
        lastbyte = oracle_md5_token[res] ^ 0x80
        new_cand = []
        for x in cand:
            if hashlib.md5(x + c).digest()[-1] == chr(lastbyte):
                new_cand.append(x)
        check_cand = new_cand

    elif res == b64_enc_not_found:
        lastbyte = 0
        new_cand = []
        for x in cand:
            if hashlib.md5(x + c).digest()[-1] == chr(lastbyte):
                new_cand.append(x)
        check_cand = new_cand

print "[+] Done."
print ""
print "candidate[checked]: ",check_cand

token = check_cand[0]

print "token: ", token

new_iv = flip_iv(pad('Welcome!!'), pad('check-token'), encrypted_welcome[0])
send_line(s,base64.b64encode(new_iv + encrypted_welcome[1]))

print ''
print recv_line(s).rstrip()    # 'Give me the token!'
print '[+] Sending token...'

send_line(s, base64.b64encode(token))
flag = recv_line(s).rstrip()
print 'Flag:'
print flag