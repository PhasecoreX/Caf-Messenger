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

from Crypto.PublicKey import RSA

'''
Generates a public/private 4096 bit RSA key
Returns an RSA key object (_RSAobj)
'''
def generate_private_key():
    return RSA.generate(4096)

'''
Saves key to encrypted user.pem file
Returns 1 on success, 0 otherwise
---
key      - RSA key object (_RSAobj) to write to disk
location - Path of folder to save to
---
NOT DONE YET!
'''
def save_key(key, location):
    pubkey = key.publickey()
    keyfile = location + "user.pem"
    f = open(keyfile,'w')
    f.write(key.exportKey('PEM') + "\n" + pubkey.exportKey('PEM'))
    f.close()
    return 1

'''
Encrypts data using RSA key (used for authentication)
Returns encrypted result asymmetric key - tuple list(?)
---
pub_key   - RSA key object (_RSAobj) containing public key of recipient, used for encrypting
plaintext - Text to encrypt
'''
def encrypt_auth(pub_key, plaintext):
    return pub_key.encrypt(plaintext)

'''
Decrypts data using RSA (used for authentication)
Returns decrypted message - string
---
private_key - RSA key object (_RSAobj) containing users private key, used for decrypting
ciphertext  - Tuple list(?) representing encrypted message
'''
def decrypt_auth(private_key, ciphertext):
    return private_key.decrypt(ciphertext)