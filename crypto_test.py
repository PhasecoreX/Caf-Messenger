#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_rsa.py
#  
#  Copyright 2014 Ryan Foster <phasecorex@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from crypto import *

def bad_sign_test():
    print "Generating key pair A..."
    keyA = generate_key_pair()
    print "Generating key pair B..."
    keyB = generate_key_pair()

    pubB = get_public_key(keyB)
    
    data = "Signing sample text with key A..."
    
    print data
    signature = sign(keyA, data)
    
    print "Checking signature with key B (should be false)..."
    result = unsign(pubB, data, signature)
    
    print result

def sign_test():
    print "Generating key pair..."
    keyA = generate_key_pair()
    pubA = get_public_key(keyA)
    
    data = "Signing sample text..."
    
    print data
    signature = sign(keyA, data)
    
    print "Checking signature..."
    result = unsign(pubA, data, signature)
    
    print result

def load_key_sign_test():
    print "Loading mykey.pem..."
    keyA = load_key("mykey.pem")
    pubA = get_public_key(keyA)
    
    data = "Signing sample text..."
    
    print data
    signature = sign(keyA, data)
    
    print "Checking signature..."
    result = unsign(pubA, data, signature)
    
    print result

def save_key_sign_test():
    print "Generating key pair..."
    keyA = generate_key_pair()
    
    data = "Signing sample text..."
    
    print data
    signature = sign(keyA, data)
    
    print "Saving key with password 'hello'..."
    save_full_key(keyA, "/home/ryan/Desktop/user.pem", "hello")
    
    print "Loading key with password 'hell'..."
    keyB = load_key("/home/ryan/Desktop/user.pem", "hello")
    pubB = get_public_key(keyB)
    
    print "Checking signature..."
    result = unsign(pubB, data, signature)
    
    print result
    
def save_key_wrong_pass_test():
    print "Generating key pair..."
    keyA = generate_key_pair()
    
    data = "Signing sample text..."
    
    print data
    signature = sign(keyA, data)
    
    print "Saving key with password 'hello'..."
    save_full_key(keyA, "/home/ryan/Desktop/user.pem", "hello")
    
    print "Loading key with password 'hell'..."
    try:
        keyB = load_key("/home/ryan/Desktop/user.pem", "hell")
    except:
        print "Incorrect password..."
        return 'break'
    
    pubB = get_public_key(keyB)
    
    print "Checking signature..."
    result = unsign(pubB, data, signature)
    
    print result

def bad_encrypt_test():
    print "Generating key pair A..."
    keyA = generate_key_pair()
    print "Generating key pair B..."
    keyB = generate_key_pair()
    
    pubA = get_public_key(keyA)
    pubB = get_public_key(keyB)
    
    print "Adding 42+12..."
    print "Encrypting 42 with pubkey B..."
    encrypted_b = encrypt_auth(pubB, 42)
    print "Encrypting 12 with pubkey A..."
    encrypted_a = encrypt_auth(pubA, 12)
    
    print "Decrypting encrypted_a with private key B (should fail)..."
    numberA = decrypt_auth(keyB, encrypted_a)
    print "Decrypting encrypted_b with private key A (should fail)..."
    numberB = decrypt_auth(keyA, encrypted_b)
    
    print "Adding results..."
    result = numberA + numberB
    
    if (result==42+12):
        print("Result is %s. Something went wrong..." % (result))
    else:
        print("Result is %s. Yay! We need to figure out how to detect incorrect keys..." % (result))

def encrypt_test():
    print "Generating key pair A..."
    keyA = generate_key_pair()
    print "Generating key pair B..."
    keyB = generate_key_pair()
    
    pubA = get_public_key(keyA)
    pubB = get_public_key(keyB)
    
    print "Adding 42+12..."
    print "Encrypting 42 with pubkey B..."
    encrypted_b = encrypt_auth(pubB, 42)
    print "Encrypting 12 with pubkey A..."
    encrypted_a = encrypt_auth(pubA, 12)
    
    print "Decrypting encrypted_a with private key A..."
    numberA = decrypt_auth(keyA, encrypted_a)
    print "Decrypting encrypted_b with private key B..."
    numberB = decrypt_auth(keyB, encrypted_b)
    
    print "Adding results..."
    result = numberA + numberB
    
    if (result==42+12):
        print("Result is %s. Yay!" % (result))
    else:
        print("Result is %s. Something went wrong..." % (result))

def sym_cipher_test():
    key = b'0123456789012345'
    encrypted = encrypt_message(key, "Test")
    print encrypted
    print decrypt_message(key, encrypted)

def get_public_key_test():
    print "Generating key pair..."
    keyA = generate_key_pair()
    
    print "Public key:"
    print get_public_key_string(keyA)

save_key_wrong_pass_test()

