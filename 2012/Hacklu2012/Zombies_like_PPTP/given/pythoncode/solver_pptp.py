#!/usr/bin/env python

from pyDes import *
import binascii
import hashlib
import string
import time



class PPTP:
    # constant for hash function
    constant = "Trololol"

    def lm_hash(self, input_password):
        # only use the first 14 bytes
        input_password = input_password[0:14]

        # convert all characters to uppercase chars
        input_password = input_password.upper()

        # split given password in two parts via 8 bytes
        password_part1 = input_password[0:8]

        # concat two 0 bytes to reach 8 bytes
        password_part2 = input_password[8:14] + "\0\0"

        # hash part 1
        part1_des = des(password_part1)
        hash_part1 = part1_des.encrypt(self.constant)

        # hash part 2
        part2_des = des(password_part2)
        hash_part2 = part2_des.encrypt(self.constant)

        # concat hash parts
        output_hash = hash_part1 + hash_part2

        # return hash as hex value
        return binascii.hexlify(output_hash)

    def response_lm(self, challenge, password):
        # generate lm_hash for response
        password_hash = self.lm_hash(password)

        if len(challenge) != 16:
            raise ValueError("Challenge has to be 8 byte hex value.")

        # create three passwords for the response
        password_res1 = password_hash[0:16]
        password_res2 = password_hash[12:28]
        password_res3 = password_hash[28:32] + "000000000000"

        # response part 1
        part1_des = des(binascii.unhexlify(password_res1))
        res_part1 = part1_des.encrypt(binascii.unhexlify(challenge))

        # response part 2
        part2_des = des(binascii.unhexlify(password_res2))
        res_part2 = part2_des.encrypt(binascii.unhexlify(challenge))

        # response part 3
        part3_des = des(binascii.unhexlify(password_res3))
        res_part3 = part3_des.encrypt(binascii.unhexlify(challenge))

        # create full response and return
        response = res_part1 + res_part2 + res_part3
        return binascii.hexlify(response)

    def search_lm3(self, challenge, password):
        # generate lm_hash for response
        password_hash = self.lm_hash(password)

        if len(challenge) != 16:
            raise ValueError("Challenge has to be 8 byte hex value.")

        password_res3 = password_hash[28:32] + "000000000000"

        # response part 3
        part3_des = des(binascii.unhexlify(password_res3))
        res_part3 = part3_des.encrypt(binascii.unhexlify(challenge))

        # create full response and return
        response = res_part3
        return binascii.hexlify(response)

    def search_lm2(self, challenge, password, lm):
        # generate lm_hash for response
        password_hash = self.lm_hash(password)

        if len(challenge) != 16:
            raise ValueError("Challenge has to be 8 byte hex value.")

        part_of_password_res2 = password_hash[16:28]

        for c1 in range(256):
            for c2 in range(256):
                password_res2 = binascii.hexlify(chr(c1)+chr(c2))+part_of_password_res2

                part2_des = des(binascii.unhexlify(password_res2))
                res_part2 = part2_des.encrypt(binascii.unhexlify(challenge))

                if lm[16:32] == binascii.hexlify(res_part2):
                    print password
                    print lm
                    print obj.response_lm(challenge, password)
                    raw_input()



if __name__ == '__main__':
    obj = PPTP()
    challenge = "dead234a1f13beef"
    lm = "78165eccbf53cdb11085e8e5e3626ba9bdefd5e9de62ce91"
    print len(lm)

    first_harf = "aaaaaaaa"

    candidate = "ABDFHJLNPRTVXZ"

    start = time.time()

    for c8 in candidate:
        for c9 in candidate:
            for c10 in candidate:
                print time.time() - start
                for c11 in candidate:
                    for c12 in candidate:
                        for c13 in candidate:

                            last_half = c8+c9+c10+c11+c12+c13+"\0\0"
                            password = first_harf+last_half

                            if lm[32:] == obj.search_lm3(challenge, password):
                                print password
                                obj.search_lm2(challenge, password, lm)

