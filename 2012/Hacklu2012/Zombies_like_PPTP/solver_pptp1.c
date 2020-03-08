#include <openssl/des.h>
#include "brute.h"
 
char input[] = "Trololol";
char chall[] = "\xde\xad\x23\x4a\x1f\x13\xbe\xef";
char lm_resp1[] = "\x78\x16\x5e\xcc\xbf\x53\xcd\xb1";
char lm_resp2[] = "\x10\x85\xe8\xe5\xe3\x62\x6b\xa9";
char lm_resp3[] = "\xbd\xef\xd5\xe9\xde\x62\xce\x91";
 
void checker_second(char *pw, int len) {
    DES_key_schedule k;    
 
    char buf_hash2[16];
    char buf_resp2[8];
    char buf_resp3[8];
 
    DES_set_key_unchecked(pw, &k);
    DES_ecb_encrypt(input, buf_hash2, &k, 1);
 
    bzero(&buf_hash2[8], 6);
 
    DES_set_key_unchecked(&buf_hash2[6], &k);
    DES_ecb_encrypt(chall, buf_resp3, &k, 1);
 
    if (memcmp(buf_resp3, lm_resp3, 8))
        return;
 
    char key_for_resp2[8];
    memcpy(&key_for_resp2[2], buf_hash2, 6);
 
    unsigned int low;
    for (low = 0; low < 65535; low++) {
        *(unsigned short*)key_for_resp2 = low;
 
        DES_set_key_unchecked((void*)key_for_resp2, &k);
        DES_ecb_encrypt(chall, buf_resp2, &k, 1);
        if (!memcmp(buf_resp2, lm_resp2, 8)) {
            printf("6-byte part: %s\n", pw);
            return;
        }
    }
}
 
int main(int argc, char **argv) {
    bruteforce_set_debug(1);
 
    bruteforce_set_key("", 6);
    bruteforce_set_charset("ABDFHJLNPRTVXZ", 14);
    bruteforce(6, checker_second);
}