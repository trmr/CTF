#include <openssl/des.h>
#include "brute.h"
 
char input[] = "Trololol";
char chall[] = "\xde\xad\x23\x4a\x1f\x13\xbe\xef";
char lm_resp1[] = "\x78\x16\x5e\xcc\xbf\x53\xcd\xb1";
char lm_resp2[] = "\x10\x85\xe8\xe5\xe3\x62\x6b\xa9";
char lm_resp3[] = "\xbd\xef\xd5\xe9\xde\x62\xce\x91";
 
void checker_first(char *pw, int len) {
    DES_key_schedule k;    
 
    char buf_hash1[8];
    char buf_resp1[8];
 
    DES_set_key_unchecked(pw, &k);
    DES_ecb_encrypt(input, buf_hash1, &k, 1);
 
    DES_set_key_unchecked(buf_hash1, &k);
    DES_ecb_encrypt(chall, buf_resp1, &k, 1);
 
    if (!memcmp(buf_resp1, lm_resp1, 8)) {
        printf("8-byte part: %s\n", pw);
        return;
    }
 
}
 
int main(int argc, char **argv) {
    bruteforce_set_debug(1);
 
    bruteforce_set_key("", 8);
    bruteforce_set_charset("ABDFHJLNPRTVXZ", 14);
    bruteforce(8, checker_first);
}