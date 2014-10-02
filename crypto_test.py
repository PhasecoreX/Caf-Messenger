#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  crypto_test.py
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
    key_a = generate_key_pair()
    print "Generating key pair B..."
    key_b = generate_key_pair()

    pub_b = get_public_key(key_b)

    data = "Signing sample text with key A..."

    print data
    signature = sign(key_a, data)

    print "Checking signature with key B (should be false)..."
    result = unsign(pub_b, data, signature)

    print result


def sign_test():
    print "Generating key pair..."
    key_a = generate_key_pair()
    pub_a = get_public_key(key_a)

    data = "Signing sample text..."

    print data
    signature = sign(key_a, data)

    print "Checking signature..."
    result = unsign(pub_a, data, signature)

    print result


def save_key_sign_test():
    print "Generating key pair..."
    key_a = generate_key_pair()

    data = "Signing sample text..."

    print data
    signature = sign(key_a, data)

    print "Saving key with password 'hello'..."
    save_full_key(key_a, "/home/ryan/Desktop/user.pem", "hello")

    print "Loading key with password 'hell'..."
    key_b = load_key("/home/ryan/Desktop/user.pem", "hello")
    pub_b = get_public_key(key_b)

    print "Checking signature..."
    result = unsign(pub_b, data, signature)

    print result


def save_key_wrong_pass_test():
    print "Generating key pair..."
    key_a = generate_key_pair()

    data = "Signing sample text..."

    print data
    signature = sign(key_a, data)

    print "Saving key with password 'hello'..."
    save_full_key(key_a, "/home/ryan/Desktop/user.pem", "hello")

    print "Loading key with password 'hell'..."
    try:
        key_b = load_key("/home/ryan/Desktop/user.pem", "hell")
    except IOError:
        print "Incorrect password..."
        return 'break'

    pub_b = get_public_key(key_b)

    print "Checking signature..."
    result = unsign(pub_b, data, signature)

    print result


def bad_encrypt_test():
    print "Generating key pair A..."
    key_a = generate_key_pair()
    print "Generating key pair B..."
    key_b = generate_key_pair()

    pub_a = get_public_key(key_a)
    pub_b = get_public_key(key_b)

    print "Adding 42+12..."
    print "Encrypting 42 with pubkey B..."
    encrypted_b = encrypt_auth(pub_b, 42)
    print "Encrypting 12 with pubkey A..."
    encrypted_a = encrypt_auth(pub_a, 12)

    print "Decrypting encrypted_a with private key B (should fail)..."
    number_a = decrypt_auth(key_b, encrypted_a)
    print "Decrypting encrypted_b with private key A (should fail)..."
    number_b = decrypt_auth(key_a, encrypted_b)

    print "Adding results..."
    result = number_a + number_b

    if (result == 42 + 12):
        print("Result is %s. Something went wrong..." % (result))
    else:
        print(
            "Result is %s. Yay! "
            "We need to figure out how to detect incorrect keys..." % (result))


def encrypt_test():
    print "Generating key pair A..."
    key_a = generate_key_pair()
    print "Generating key pair B..."
    key_b = generate_key_pair()

    pub_a = get_public_key(key_a)
    pub_b = get_public_key(key_b)

    print "Adding 42+12..."
    print "Encrypting 42 with pubkey B..."
    encrypted_b = encrypt_auth(pub_b, 42)
    print "Encrypting 12 with pubkey A..."
    encrypted_a = encrypt_auth(pub_a, 12)

    print "Decrypting encrypted_a with private key A..."
    number_a = decrypt_auth(key_a, encrypted_a)
    print "Decrypting encrypted_b with private key B..."
    number_b = decrypt_auth(key_b, encrypted_b)

    print "Adding results..."
    result = number_a + number_b

    if result == 42 + 12:
        print "Result is %s. Yay!" % result
    else:
        print "Result is %s. Something went wrong..." % result


def sym_cipher_test():
    key = b'0123456789012345'
    encrypted = encrypt_message(key, "Test")
    print encrypted
    print decrypt_message(key, encrypted)


def get_public_key_test():
    print "Generating key pair..."
    key_a = generate_key_pair()

    print "Public key:"
    print get_public_key_string(key_a)

encrypt_test()
