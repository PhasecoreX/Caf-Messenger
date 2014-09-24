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

print "Decrypting erncrypted_a with private key A..."
numberA = decrypt_auth(keyA, encrypted_a)
print "Decrypting erncrypted_b with private key B..."
numberB = decrypt_auth(keyB, encrypted_b)

print "Adding results..."
result = numberA + numberB

if (result==42+12):
    print("Result is %s. Yay!" % (result))
else:
    print("Result is %s. Something went wrong..." % (result))