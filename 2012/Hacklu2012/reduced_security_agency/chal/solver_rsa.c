#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <gmp.h>

#define BASE (10)

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

int main(void){
    mpz_t modulus;
    mpz_init(modulus);
    mpz_set_str(modulus,"22722894224038773929814775636904601515673859397989155133300163185627947633321633975704241497145720395273404316192999474778725912875508494273308320269781358702867219512580314666172594824245425911451272148490796650045564147140941703316188789260687476035616531481905254406433474344014307578584276679667557969975668976947956336031434666435952590321332975167296177887795585671612689328983070936991878977964299502596498534040990218479489217336854323101058354504473406364354711202090911113696921475193840294754741384944029677484734384080929752879383266268171405868789044211166431683626050133953997068531641045380470090779051",BASE);
    
    mpz_t pub_key;
    mpz_init(pub_key);
    mpz_set_str(pub_key, "8404303608555594412435859766076690642119945519817916792167349970365208529700436926276204116561533931538678787437133255030612551580238521886654400727785278735347205123287374093004638739395552231963821570273652714201448429840315771601453912210692938417977909646901029737551467118270160796173283088645256815599981900848629826421283751092619275251787343802046386128699080496721054225089549487992421727851547972722651518507947818454018249883661484379053786822329018383493413232606709441777850747570549037743111881964924327550204706559009992440852957484616351614889231119744710956814890845480267726365603088273639728332191", BASE);
    
    mpz_t result;
    mpz_init(result);

    find_seckey(result, pub_key, modulus);
}