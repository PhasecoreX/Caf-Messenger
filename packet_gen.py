#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_crypto.py
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

from crypto import encrypt_message, sign, encrypt_auth, verify,\
    decrypt_message, decrypt_auth, get_public_key_string
from packet import PacketS, PacketA, DecryptedPacketS, DecryptedPacketA
import cPickle as pickle


def gen_message_packet(source, dest, convo_id, message, encrypt_key, sign_key):
    """Creates a packet with data for message sending

    Args:
        source:      Where the packet came from (you)
        destination: 8 Hex character destination (them)
        convo_id:    Conversation ID (the one they want you to use)
        message:     Raw string message
        encrypt_key: Conversations symmetric encrtyption key
        sign_key:    Your private key for signing

    Returns:
        PacketS object ready for sending
    """
    e_source = encrypt_message(encrypt_key, source)
    e_message = encrypt_message(encrypt_key, message)
    signature = sign(sign_key,
                     "M" + pickle.dumps(e_source) +
                     dest + str(convo_id) +
                     pickle.dumps(e_message))
    return PacketS("M", e_source, dest, convo_id, e_message, signature)


def gen_command_packet(source, dest, convo_id, command, encrypt_key, sign_key):
    """Creates a packet with data for command sending

    Args:
        source:      Where the packet came from (you)
        destination: 8 Hex character destination (them)
        convo_id:    Conversation ID (the one they want you to use)
        command:     Raw string command
        encrypt_key: Conversations symmetric encrtyption key
        sign_key:    Your private key for signing

    Returns:
        PacketS object ready for sending
    """
    e_source = encrypt_message(encrypt_key, source)
    e_command = encrypt_message(encrypt_key, command)
    signature = sign(sign_key,
                     "C" + 
                     pickle.dumps(e_source) +
                     dest + 
                     str(convo_id) +
                     pickle.dumps(e_command))
    return PacketS("C", e_source, dest, convo_id, e_command, signature)


def gen_auth_packet(source, dest, convo_id, proposed_key,
                    encrypt_key, sign_key):
    """Creates a packet with data for initializing a communication line

    Args:
        source:       Where the packet came from (you)
        destination:  8 Hex character destination (them)
        convo_id:     Conversation ID (the one they want you to use)
        proposed_key: Proposed encryption key to use
        encrypt_key:  Conversations symmetric encryption key
        sign_key:     Your private key for signing

    Returns:
        PacketA object ready for sending
    """
    e_proposed_key = encrypt_auth(encrypt_key, proposed_key)
    e_source = encrypt_message(proposed_key, source)
    e_convo_id = encrypt_message(proposed_key, str(convo_id))
    e_sender_key = encrypt_message(proposed_key,
                                   get_public_key_string(sign_key))
    signature = sign(sign_key,
                     "A" + 
                     pickle.dumps(e_source) +
                     dest +
                     pickle.dumps(e_convo_id) +
                     pickle.dumps(e_proposed_key) + 
                     pickle.dumps(e_sender_key))
    return PacketA(e_source, dest, e_convo_id, e_proposed_key, e_sender_key,
                   signature)


def decrypt_packet_s(packet, encrypt_key, sender_key):
    """Decrypts a packet encrypted with an AES key

    Args:
        packet:      Packet to be decrypted
        encrypt_key: Symmetric key for decrypting
        sender_key:  Public key of sender for checking signature

    Returns:
        DecryptedPacketS object ready for parsing
    """
    to_verify = (packet.get_packet_type() +
                 pickle.dumps(packet.get_source()) +
                 packet.get_destination() +
                 str(packet.get_convo_id()) +
                 pickle.dumps(packet.get_data()))
    if verify(sender_key, to_verify, packet.get_signature()):
        d_source = decrypt_message(encrypt_key, packet.get_source())
        d_data = decrypt_message(encrypt_key, packet.get_data())
        return DecryptedPacketS(packet.get_packet_type(),
                                d_source,
                                int(packet.get_convo_id()),
                                d_data)
    return False


def decrypt_packet_a(packet, private_key):
    """Decrypts a packet encrypted with your public key

    Args:
        packet:      Packet to be decrypted
        private_key: Private key for decrypting

    Returns:
        DecryptedPacketA object ready for parsing
    """
    """
    to_verify = (packet.get_packet_type() +
                 pickle.dumps(packet.get_source()) +
                 packet.get_destination() +
                 str(packet.get_convo_id()) +
                 pickle.dumps(packet.get_data()))
    """
    # For auth packets, the proposed symmetric key used for encrypting the
    # rest of the packet.
    proposed_key = decrypt_auth(private_key, packet.get_proposed_key())
    d_source = decrypt_message(proposed_key, packet.get_source())
    d_convo_id = decrypt_message(proposed_key, packet.get_convo_id())
    d_sender_key = decrypt_message(proposed_key, packet.get_sender_key())
    # if verify(sender_key, to_verify, packet.get_signature()):
    return DecryptedPacketA(d_source,
                            int(d_convo_id),
                            proposed_key,
                            d_sender_key)
    # return False
