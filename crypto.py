#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  crypto.py
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

'''crypto.py

A bunch of functions for encryption in Cafe Messenger
'''

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
import logging


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logging.basicConfig(filename='/home/ryan/Desktop/example.log',
                    filemode='w', level=logging.DEBUG)
# logging.warning('is when this event was logged.')


def generate_key_pair():
    """Generates a public/private 4096 bit RSA key

    Returns:
        RSA key object (_RSAobj) containing the full key pair
    """
    return RSA.generate(4096)


def get_public_key(private_key):
    """Extracts the public key from a full key pair

    Args:
        private_key: RSA key object (_RSAobj) containing a private/public key

    Returns:
        RSA key object (_RSAobj) containing only the public key
    """
    return private_key.publickey()


def get_public_key_string(private_key):
    """Extracts the public key from a full key pair

    Args:
        private_key: RSA key object (_RSAobj) containing a private/public key

    Returns:
        String representing public key
    """
    return private_key.publickey().exportKey('PEM')


def save_full_key(key, keyfile_path, password):
    """Saves key to encrypted user.pem file

    Args:
        key:      RSA key object (_RSAobj) to write to disk
        location: Path of folder to save to

    Returns:
        True on success, False otherwise

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """
    exported_key = key.exportKey('PEM', password, pkcs=1)
    try:
        file_obj = open(keyfile_path, 'w')
        file_obj.write(exported_key)
        file_obj.close()
        return True
    except IOError:
        return False


def load_key(keyfile_path, password):
    '''Loads key from .pem file

    Will work with both public and private key files

    Args:
        file: Full path and file name of .pem key

    Returns:
        RSA key object (_RSAobj) containing public and/or private key
    '''
    try:
        return RSA.importKey(open(keyfile_path).read(), password)
    except:
        raise


def encrypt_auth(pub_key, plaintext):
    '''Encrypts data using RSA key (used for authentication)

    Args:
        pub_key:   RSA key object (_RSAobj) containing public key of recipient,
                   used for encrypting
        plaintext: Text to encrypt

    Returns:
        Encrypted result asymmetric key - tuple list(?)
    '''
    rng = Random.new()
    return pub_key.encrypt(plaintext, rng.read(8192))


def decrypt_auth(private_key, ciphertext):
    '''Decrypts data using RSA (used for authentication)

    Args:
        private_key: RSA key object (_RSAobj) containing users private key,
                     used for decrypting
        ciphertext:  Tuple list(?) representing encrypted message

    Returns:
        Decrypted message - string
    '''
    return private_key.decrypt(ciphertext)


def sign(private_key, data):
    '''Signs data

    Args:
        private_key: RSA key object (_RSAobj) containing users private key,
                     used for signing
        data:        Data to sign

    Returns:
        Signature for given data and private key
    '''
    hash_obj = SHA.new()
    hash_obj.update(data)
    signer = PKCS1_PSS.new(private_key)
    return signer.sign(hash_obj)


def unsign(public_key, data, signature):
    '''Checks signature on data

    Args:
        public_key: RSA key object (_RSAobj) containing signers public key
        data:       Signed data in question
        signature:  Proposed signature to test

    Returns:
        True if authentic, False otherwise
    '''
    hash_obj = SHA.new()
    hash_obj.update(data)
    signer = PKCS1_PSS.new(public_key)
    return signer.verify(hash_obj, signature)


def encrypt_message(key, message):
    '''Encrypts data using AES Cipher

    Args:
        key:     Key used for encrypting.
                 Keys can be 128, 192, or 256 bits long (we will use 256)
        message: Message to encrypt

    Returns:
        Encrypted Text
    '''
    logging.debug('Plaintext to be encrypted:/n%s', message)
    iv_random = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv_random)
    pad_len = AES.block_size - (len(message) % AES.block_size)
    padding = ''.join([chr(pad_len)] * pad_len)
    encrypted_text = iv_random + cipher.encrypt(message + padding)
    logging.debug('Encrypted text:/n%s', encrypted_text)
    return encrypted_text


def decrypt_message(key, ciphertext):
    '''Decrypts data using AES Cipher

    Args:
        key:        Key used for decrypting
        ciphertext: Message to decrypt

    Returns:
        Decrypted Text
        Keys can be 128, 192, or 256 bits long (we will use 256)
    '''
    logging.debug('Ciphertext to be decrypted:/n%s', ciphertext)
    iv_random = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CFB, iv_random)
    padded_msg = cipher.decrypt(ciphertext[AES.block_size:])
    pad_len = ord(padded_msg[-1])
    decrypted_text = padded_msg[:len(padded_msg) - pad_len]
    logging.debug('Decrypted text:/n%s', decrypted_text)
    return decrypted_text
