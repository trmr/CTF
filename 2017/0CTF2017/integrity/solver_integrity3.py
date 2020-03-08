import hashlib
from trmr import *

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

expanded = 'admin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0bX'

s = socket.create_connection(('172.16.12.139', 7777))
print recvuntil(s, '[l]ogin\n')
sendline(s, 'r')
sendline(s, expanded)
print recvuntil(s, 'secret:\n')
secret_hex = recvline(s).rstrip()

secret = secret_hex.decode('hex')
iv, enc_md5, enc_msg1, enc_msg2 = secret[:16], secret[16:32], secret[32:48], secret[48:]

print "[DEBUG] iv "+iv.encode("hex")

h1 = hashlib.md5(expanded[:-1]).digest()
h2 = hashlib.md5(pad(expanded)).digest()
h_xor = xor(h1, h2)

print "[DEBUG] admin_hash "+h1.encode("hex")
print "[DEBUG] name_hash "+h2.encode("hex")
print "[DEBUG] raw_h_xor :" + h_xor
print "[DEBUG] h_xor :" + h_xor.encode("hex")

secret2 = xor(iv, h_xor) + enc_md5 + enc_msg1
secret2_hex = secret2.encode('hex')
print "[DEBUG] secret "+secret2_hex

print recvuntil(s, '[l]ogin\n')
sendline(s, 'l')
sendline(s, secret2_hex)

interact(s)