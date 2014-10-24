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

"""packet_crypto_test.py

Tests packet_crypto
"""

from packet_crypto import *


def test_everything():
    """Test if everything works 100% forever with no errors ever"""
    print "Generating key pair A..."
    key_a = generate_key_pair()
    print "Generating key pair B..."
    key_b = generate_key_pair()

    print "Generating symmetric key..."
    symm = generate_symmetric_key()
    print symm
    print ""

    print "Creating auth packet A->B..."
    # This will be the packet sent to initiate a connection
    packet = gen_auth("A", "B", "ConvoID_1", symm,
                      key_b, key_a)

    print "Decrypting packet..."
    decrypted_packet = decrypt_packet_A(packet, key_b, key_a)
    # Get data from decrypted packet
    proposed_symm = decrypted_packet.get_data()
    print "Received key:"
    print proposed_symm
    print ""

    print "Creating command packet B->A..."
    packet = gen_command("B", "A", "ConvoID_2", "accept",
                         proposed_symm, key_b)

    print "Decrypting packet..."
    decrypted_packet = decrypt_packet_S(packet, proposed_symm, key_b)
    # Get data from decrypted packet
    recvd = decrypted_packet.get_data()
    print "Received command:"
    print recvd
    print ""

    print "Creating message packet A->B..."
    packet = gen_message("A", "B", "ConvoID_1", "Hello World!",
                         proposed_symm, key_a)

    print "Decrypting packet..."
    decrypted_packet = decrypt_packet_S(packet, proposed_symm, key_a)
    # Get data from decrypted packet
    recvd = decrypted_packet.get_data()
    print "Received message:"
    print recvd
    print ""

    print "Creating message packet B->A..."
    packet = gen_message("B", "A", "ConvoID_2", "Hello World!",
                         proposed_symm, key_a)

    print "Decrypting packet with incorrect signature..."
    decrypted_packet = decrypt_packet_S(packet, proposed_symm, key_b)
    print "Verify result:"
    print decrypted_packet
    print ""


test_everything()
