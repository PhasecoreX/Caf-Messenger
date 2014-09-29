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
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA
from atk import Text

'''
Generates a public/private 4096 bit RSA key
Returns an RSA key object (_RSAobj) containing the full key pair
'''
def generate_key_pair():
    return RSA.generate(4096)

'''
Extracts the public key from a full key pair
Returns an RSA key object (_RSAobj) containing only the public key
---
private_key - RSA key object (_RSAobj) containing users private and public key
'''
def get_public_key(private_key):
    return private_key.publickey()

'''
Saves key to encrypted user.pem file
Returns True on success, False otherwise
---
key      - RSA key object (_RSAobj) to write to disk
location - Path of folder to save to
---
NOT DONE YET!
'''
def save_full_key(key, location):
    pubkey = key.publickey()
    keyfile = location + "user.pem"
    f = open(keyfile,'w')
    f.write(key.exportKey('PEM') + "\n" + pubkey.exportKey('PEM'))
    f.close()
    return 1

'''
Loads key from .pem file
Returns RSA key object (_RSAobj) containing 
---
file - Full path and file name of .pem key
'''
def load_key(file_path):
    return RSA.importKey(open(file_path).read())

'''
Encrypts data using RSA key (used for authentication)
Returns encrypted result asymmetric key - tuple list(?)
---
pub_key   - RSA key object (_RSAobj) containing public key of recipient, used for encrypting
plaintext - Text to encrypt
'''
def encrypt_auth(pub_key, plaintext):
    rng = Random.new()
    return pub_key.encrypt(plaintext, rng.read(8192))

'''
Decrypts data using RSA (used for authentication)
Returns decrypted message - string
---
private_key - RSA key object (_RSAobj) containing users private key, used for decrypting
ciphertext  - Tuple list(?) representing encrypted message
'''
def decrypt_auth(private_key, ciphertext):
    return private_key.decrypt(ciphertext)

'''
Signs data
Returns signature for given data and private key
---
private_key - RSA key object (_RSAobj) containing users private key, used for signing
data        - Data to sign
'''
def sign(private_key, data):
    h = SHA.new()
    h.update(data)
    signer = PKCS1_PSS.new(private_key)
    return signer.sign(h)

'''
Checks signature on data
Returns True if authentic, False otherwise
---
public_key - RSA key object (_RSAobj) containing signers public key
data       - Signed data in question
signature  - Proposed signature to test
'''
def unsign(public_key, data, signature):
    h = SHA.new()
    h.update(data)
    signer = PKCS1_PSS.new(public_key)
    return signer.verify(h, signature)

'''
Encrypts data using AES Cipher
Returns encrypted Text
---
key     - Key used for encrypting. Keys can be 128, 192, or 256 bits long (we will use 256)
message - Message to encrypt
'''
def encrypt_message(key, message):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    pad_len = AES.block_size - (len(message) % AES.block_size)
    padding = ''.join([chr(pad_len)]*pad_len)
    return iv + cipher.encrypt(message + padding)

'''
Decrypts data using AES Cipher
Returns decrypted Text. Keys can be 128, 192, or 256 bits long (we will use 256)
---
key        - Key used for decrypting
ciphertext - Message to decrypt
'''
def decrypt_message(key, ciphertext):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    padded_msg = cipher.decrypt(ciphertext[AES.block_size:])
    pad_len = ord(padded_msg[-1])
    return padded_msg[:len(padded_msg)-pad_len]