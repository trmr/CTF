from trmr import *

import base64

def pad(msg):
    pad_length = 16-len(msg)%16
    return msg+chr(pad_length)*pad_length

original_iv = '2jpmLoSsOlQrqyqE'

s, f = sock("172.16.12.142",1234)

print recv_until(s,"XXXX+")
end = recv_until(s,")")[:-1]
print recv_until(s,"== ")
digest = recv_until(s,"\n").rstrip()

prefix = proof_of_work(end, digest)

print "digest",digest

print "prefix",prefix

send_line(s, prefix)

recv_line(s)
encrypted_welcome = divide_into_blocks(base64.b64decode(recv_line(s).rstrip()),16)

print "welcome: ", encrypted_welcome

send_line(s, base64.b64encode("".join(encrypted_welcome)))
encrypted_not_found = divide_into_blocks(base64.b64decode(recv_line(s).rstrip()),16)

new_iv = flip_iv(pad('Welcome!!'), pad('get-flag'), encrypted_welcome[0])
send_line(s,base64.b64encode(new_iv + encrypted_welcome[1]))
encrypted_flag = divide_into_blocks(base64.b64decode(recv_line(s).rstrip()),16)

print "flag",encrypted_flag


#print "not found:", encrypted_not_found
#print "flag: ", encrypted_flag

flag_length = len("".join(encrypted_flag))
#print "flag-length: ",flag_length

def get_encrypted_md5_flag(index):
    new_iv = flip_iv(pad("hitcon{"), pad("get-md5"), encrypted_flag[0])
    payload = new_iv + "".join(encrypted_flag[1:])
    next_to_last_block = flip_iv(pad('Welcome!!'), "A"*15+chr(16 + 16 + flag_length - 7 - index), encrypted_welcome[0])
    payload += next_to_last_block
    payload += encrypted_welcome[1]
    send_line(s, base64.b64encode("".join(payload)))
    return divide_into_blocks(base64.b64decode(recv_line(s).rstrip()),16)

known_flag = ""

for index in range(flag_length - 7):
    encrypted_md5_flag = get_encrypted_md5_flag(index)
    for guess in range(256):
        guess_md5 = hashlib.md5(known_flag + chr(guess)).digest()
        payload = flip_iv(guess_md5, pad("get-time"), encrypted_md5_flag[0])
        payload += "".join(encrypted_md5_flag[1:])
        send_line(s, base64.b64encode("".join(payload)))
        res = divide_into_blocks(base64.b64decode(recv_line(s).rstrip()), 16)
        if len(res) != 3:
            print "Found!"
            known_flag += chr(guess)
            print "Flag: hitcon{", known_flag
            break

print 'hitcon{'+known_flag




