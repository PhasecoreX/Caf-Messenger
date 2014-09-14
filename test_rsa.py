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
from Crypto import Random

key = RSA.generate(4096)
pubkey = key.publickey()
rng = Random.new()

keyfile = "mykey.pem"
f = open(keyfile,'w')
f.write(key.exportKey('PEM') + "\n" + pubkey.exportKey('PEM'))
f.close()
print "Public/private key written to " + keyfile + "\n"

encrypt_text = "Hello there!"
encrypted = pubkey.encrypt(encrypt_text, rng.read(8192))
decrypted = key.decrypt(encrypted)
print "Plaintext:\n"
print encrypt_text
print "\n\nEncrypted (tuples):\n"
print encrypted
print "\n\nDecrypted:\n"
print decrypted
