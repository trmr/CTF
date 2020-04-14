cipher = "NPEBFF ZNATB QVTAVGL JNTBA"


s = 13
plain = ""
for i in range(len(cipher)):
    c = cipher[i]

    if (c.isupper()):
        plain += chr((ord(c) + s - 65) % 26 + 65)

    else:
        plain += chr((ord(c) + s - 97) % 26 + 97)

print(plain)

