/**
 * Copyright: ErEsAh Securse-ID Token
 **/

#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <gmp.h>

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

void
chartompz(mpz_t result, char *msgptr)
{
	unsigned int size = strlen(msgptr);
	mpz_t msg;
	mpz_t tmp;
	mpz_init(tmp);
	mpz_init(msg);
	int i;

    printf("strlen = %d\n", size);
	for (i = 0; i < size; i++) {
		mpz_set_ui(tmp, (int)msgptr[i]);
		mpz_mul_2exp(tmp, tmp, 8*i);
		mpz_add(msg, msg, tmp);
	}

	mpz_set(result, msg);
}

char *
mpztochar(mpz_t code)
{
	int i, j;
    mpz_t tmp2;
    mpz_t and255;
    mpz_init(tmp2);
    mpz_init(and255);
    mpz_set_ui(and255, 255);
    int length = mpz_sizeinbase(code, 2);
    length = (length / 8) + 1;
	
	char *text;
	text = malloc((length)*sizeof(char));
	if (!text) {
		return NULL;
	}

    unsigned int tmp3;

    for(i = 0; i < length; i++) {
        mpz_set(tmp2, code);
        mpz_cdiv_q_2exp(tmp2, tmp2, i*7);

        for (j = 0; j < i; j++) {
            mpz_div_ui(tmp2, tmp2, 2);
        }

        mpz_and(tmp2, tmp2, and255);
        tmp3 = mpz_get_ui(tmp2);
        text[i] = (char) tmp3;
    }
	text[length] = '\0';
	return text;
}

void
gen_pubkey(mpz_t result, mpz_t key, mpz_t modulus)
{
    mpz_t pubkey;
    mpz_init(pubkey);
    mpz_invert(pubkey, key, modulus);
	mpz_set(result, pubkey);
}

int
gen_seckey(mpz_t result)
{
	mpz_t key;
	int i = 0, j;
	unsigned int seed, random;
	FILE *frand;
	mpz_init2(key, 2048);

	gmp_randstate_t state;
	gmp_randinit_default(state);
	frand = fopen("/dev/random", "r");
	if (frand == NULL) {
		printf("fopen() failed\n");
		return -1;
	}
	
	fread(&seed, sizeof(seed), 1, frand);
	fclose(frand);
	gmp_randseed_ui(state, seed);

	j = 2047;
	while(i != j) {
		random = gmp_urandomb_ui(state, 1);
		if(random) {
			mpz_setbit(key, i);
			i++;
		}
		else if(!random) {
			mpz_clrbit(key, j);
			j--;
		}
	}

	mpz_set(result, key);
	return 0;
}

void
encrypt(mpz_t result, mpz_t base, mpz_t key, mpz_t modulus)
{
	mpz_t msg;
	mpz_init(msg);

    mpz_t ciphertext;
    mpz_init(ciphertext);

    printf("encrypting...\n");
    mpz_powm(ciphertext, base, key, modulus);

	mpz_set(result, ciphertext);
}
