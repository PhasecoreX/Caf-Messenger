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

"""packet_crypto.py

Makes encryption and packet generation even easier!
"""
from crypto import *
from packet import *


def gen_message(source, dest, message, encrypt_key, sign_key):
    """Creates a packet with data for message sending

    Args:
        source:      Source user ID
        dest:        Destination user ID
        message:     Message to send
        encrypt_key: Key used for symmetric encryption
        sign_key:    Private key for signing each packet

    Returns:
        Packet object ready for sending
    """
    data = Packet_Data("M", source, message)
    encrypt_data = encrypt_message(encrypt_key, data)
    signature = sign(sign_key, "M" + dest + encrypt_data)
    return Packet("M", dest, encrypt_data, signature)


def gen_command(source, dest, command, encrypt_key, sign_key):
    """Creates a packet with data for command sending

    Args:
        source:      Source user ID
        dest:        Destination user ID
        command:     Command to send
        encrypt_key: Key used for symmetric encryption
        sign_key:    Private key for signing each packet

    Returns:
        Packet object ready for sending
    """
    data = Packet_Data("C", source, command)
    encrypt_data = encrypt_message(encrypt_key, data)
    signature = sign(sign_key, "C" + dest + encrypt_data)
    return Packet("C", dest, encrypt_data, signature)


def gen_auth(source, dest, proposed_key, encrypt_key, sign_key):
    """Creates a packet with data for initializing a communication line

    Args:
        source:       Source user ID
        dest:         Destination user ID
        proposed_key: Proposed key to use in all future M and C-Packets
        encrypt_key:  Public key of recipient
        sign_key:     Private key for signing each packet

    Returns:
        Packet object ready for sending
    """
    data = Packet_Data("A", source, proposed_key)
    encrypt_data = encrypt_auth(encrypt_key, data)
    signature = sign(sign_key, "A" + dest + encrypt_data)
    return Packet("A", dest, encrypt_data, signature)


def decrypt_packet_A(packet, private_key, sender_key):
    """Decrypts a packet encrypted with your public key

    Args:
        packet:      Packet to be decrypted
        private_key: Private key for decrypting
        sender_key:  Public key of sender for checking signature

    Returns:
        Packet_Data object ready for parsing
    """
    to_verify = (packet.get_packet_type() +
                 packet.get_destination() +
                 packet.get_payload())
    if verify(sender_key, to_verify, packet.get_signature()):
        return decrypt_auth(private_key, packet.get_payload())
    return False


def decrypt_packet_S(packet, encrypt_key, sender_key):
    """Decrypts a packet encrypted with your public key

    Args:
        packet:      Packet to be decrypted
        encrypt_key: Symmetric key for decrypting
        sender_key:  Public key of sender for checking signature

    Returns:
        Packet_Data object ready for parsing
    """
    to_verify = (packet.get_packet_type() +
                 packet.get_destination() +
                 packet.get_payload())
    if verify(sender_key, to_verify, packet.get_signature()):
        return decrypt_message(encrypt_key, packet.get_payload())
    return False