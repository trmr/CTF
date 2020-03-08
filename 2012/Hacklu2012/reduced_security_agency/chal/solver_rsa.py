#!/usr/bin/env python

import commands

def get_nonce():
    print "test"
    #connect server and get nonce
    # return nonce

def get_token(nonce):
    msg = "./solver_rsa2 "+nonce
    token = commands.getoutput(msg)
    print token
    return token

def send_token(token):
    print "test"

    # send token

if __name__ == '__main__':
    get_nonce()
    nonce = "3357534731"
    token = get_token(nonce)
    send_token(token)
