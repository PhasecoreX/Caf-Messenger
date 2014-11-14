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
from packet import Packet, DecryptedPacket
import cPickle as pickle


def gen_message_packet(source, dest, convo_id, message, encrypt_key, sign_key):
    """Creates a packet with data for message sending

    Args:
        source:      Source user ID
        dest:        Destination user ID
        convo_id:    Destination user conversation ID
        message:     Message to send
        encrypt_key: Key used for symmetric encryption
        sign_key:    Private key for signing each packet

    Returns:
        Packet object ready for sending
    """
    e_source = encrypt_message(encrypt_key, source)
    e_message = encrypt_message(encrypt_key, message)
    signature = sign(sign_key,
                     "M" + pickle.dumps(e_source) +
                     dest + convo_id +
                     pickle.dumps(e_message))
    return Packet("M", e_source, dest, convo_id, e_message, signature)


def gen_command_packet(source, dest, convo_id, command, encrypt_key, sign_key):
    """Creates a packet with data for command sending

    Args:
        source:      Source user ID
        dest:        Destination user ID
        convo_id:    Destination user conversation ID
        command:     Command to send
        encrypt_key: Key used for symmetric encryption
        sign_key:    Private key for signing each packet

    Returns:
        Packet object ready for sending
    """
    e_source = encrypt_message(encrypt_key, source)
    e_command = encrypt_message(encrypt_key, command)
    signature = sign(sign_key,
                     "M" + pickle.dumps(e_source) +
                     dest + convo_id +
                     pickle.dumps(e_command))
    return Packet("C", e_source, dest, convo_id, e_command, signature)


def gen_auth_packet(source, dest, convo_id, proposed_key,
                    encrypt_key, sign_key):
    """Creates a packet with data for initializing a communication line

    Args:
        source:       Source user ID
        dest:         Destination user ID
        convo_id:     Destination user conversation ID
        proposed_key: Proposed key to use in all future M and C-Packets
        encrypt_key:  Public key of recipient
        sign_key:     Private key for signing each packet

    Returns:
        Packet object ready for sending
    """
    e_source = encrypt_auth(encrypt_key, source)
    e_proposed_data = encrypt_auth(encrypt_key, str(convo_id) + "\"" + get_public_key_string(sign_key) + "\"" + proposed_key)
    signature = sign(sign_key,
                     "M" + pickle.dumps(e_source) +
                     dest +
                     pickle.dumps(e_proposed_data))
    return Packet("A", e_source, dest, None, e_proposed_data, signature)


def decrypt_packet_s(packet, encrypt_key, sender_key):
    """Decrypts a packet encrypted with an AES key

    Args:
        packet:      Packet to be decrypted
        encrypt_key: Symmetric key for decrypting
        sender_key:  Public key of sender for checking signature

    Returns:
        Decrypted_Packet object ready for parsing
    """
    to_verify = (packet.get_packet_type() +
                 pickle.dumps(packet.get_source()) +
                 packet.get_destination() +
                 packet.get_convo_id() +
                 pickle.dumps(packet.get_data()))
    if verify(sender_key, to_verify, packet.get_signature()):
        d_source = decrypt_message(encrypt_key, packet.get_source())
        d_data = decrypt_message(encrypt_key, packet.get_data())
        return DecryptedPacket(packet.get_packet_type(),
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
        Decrypted_Packet object ready for parsing
    """
    """
    to_verify = (packet.get_packet_type() +
                 pickle.dumps(packet.get_source()) +
                 packet.get_destination() +
                 packet.get_convo_id() +
                 pickle.dumps(packet.get_data()))
    """
    d_source = decrypt_auth(private_key, packet.get_source())
    d_data = decrypt_auth(private_key, packet.get_data())
    convo_id = d_data.split("\"")[0]
    sender_key = d_data.split("\"")[1]
    proposed_key = d_data[len(convo_id)+len(sender_key)+2:]
    # if verify(sender_key, to_verify, packet.get_signature()):
    return DecryptedPacketA(packet.get_packet_type(),
                            d_source,
                            int(convo_id),
                            proposed_key,
                            sender_key)
    return False
