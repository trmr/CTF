#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <gmp.h>

#define BASE (10)

unsigned int
gen_auth(mpz_t key, mpz_t modulus, mpz_t nonce)
{
    time_t now = time(NULL);
    unsigned int range = now / 3600;
    unsigned int token;

    mpz_t t;
    mpz_init(t);

    mpz_set_ui(t, range);

    mpz_t auth;
    mpz_init(auth);

    mpz_add(t, t, nonce);
    mpz_t newmod;
    mpz_init(newmod);
    mpz_set_ui(newmod, 13371337);
    mpz_powm(auth, t, key, newmod);
    token = mpz_get_ui(auth);

    return token;
}

void encrypt(mpz_t result, mpz_t base, mpz_t key, mpz_t modulus)
{
	mpz_t msg;
	mpz_init(msg);

    mpz_t ciphertext;
    mpz_init(ciphertext);

    printf("encrypting...\n");
    mpz_powm(ciphertext, base, key, modulus);

    mpz_set(result, ciphertext);
}

void decrypt(mpz_t result, mpz_t base, mpz_t key, mpz_t modulus)
{
	mpz_t msg;
	mpz_init(msg);

    mpz_t plaintext;
    mpz_init(plaintext);

    mpz_powm(plaintext, base, key, modulus);

    mpz_set(result, plaintext);
}

void find_seckey(mpz_t result, mpz_t pub_key, mpz_t modulus){

    mpz_t msg;
    mpz_init(msg);
    mpz_set_str(msg, "65535", BASE);

    mpz_t seckey;
    mpz_init(seckey);

    mpz_t two;
    mpz_init(two);
    mpz_set_str(two, "2", BASE);

    mpz_t one;
    mpz_init(one);
    mpz_set_str(one, "1", BASE);

    mpz_t j;
    mpz_init(j);

    mpz_t plaintext;
    mpz_init(plaintext);

    mpz_t ciphertext;
    mpz_init(ciphertext);
    
    encrypt(ciphertext, msg, pub_key, modulus);


    unsigned int i = 0;
    
    for (i = 0; i < 2048; i++){
        mpz_set_ui(j, i);
        mpz_powm(seckey, two, j, modulus);
        mpz_sub(seckey, seckey, one); // 2^n - 1 = 111....1111
        decrypt(plaintext, ciphertext, seckey, modulus);
        if (!mpz_cmp(plaintext,msg)){
            mpz_out_str(stdout, BASE, seckey);
            printf("\n");
            printf("i = %u",i);
        }

    }

    
}

int main(int argc, char *argv[]){

    unsigned int token = 0;

    mpz_t nonce;
    mpz_init(nonce);
    mpz_set_str(nonce, argv[1], BASE);

    mpz_t seckey;
    mpz_init(seckey);
    mpz_set_str(seckey, "179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137215",BASE);

    mpz_t modulus;
    mpz_init(modulus);
    mpz_set_str(modulus,"22722894224038773929814775636904601515673859397989155133300163185627947633321633975704241497145720395273404316192999474778725912875508494273308320269781358702867219512580314666172594824245425911451272148490796650045564147140941703316188789260687476035616531481905254406433474344014307578584276679667557969975668976947956336031434666435952590321332975167296177887795585671612689328983070936991878977964299502596498534040990218479489217336854323101058354504473406364354711202090911113696921475193840294754741384944029677484734384080929752879383266268171405868789044211166431683626050133953997068531641045380470090779051",BASE);

    token = gen_auth(seckey, modulus, nonce);
    printf("%u", token);

    return 0;
}