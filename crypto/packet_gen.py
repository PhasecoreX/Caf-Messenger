#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  packet_gen.py
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
from hachoir_parser.network.tcpdump import Packet
"""packet_gen.py

Makes encryption and packet generation even easier!
"""

import ast
import base64
import json

from crypto import encrypt_message, sign, encrypt_auth, verify,\
    decrypt_message, decrypt_auth, get_public_key_string
from packet import DecryptedPacketS, DecryptedPacketA
import cPickle as pickle


def gen_packet_s(packet_type, source, dest, convo_id, data, encrypt_key,
                 sign_key):
    """Creates a JSON formatted packet with data for symmetric key sending

    Args:
        packet_type: Packet type
        source:      Where the packet came from (you)
        dest:        8 Hex character destination (them)
        convo_id:    Conversation ID (the one they want you to use)
        data:        Raw string command
        encrypt_key: Conversations symmetric encryption key
        sign_key:    Your private key for signing

    Returns:
        PacketS object ready for sending
    """
    e_source = encrypt_message(encrypt_key, source)
    e_data = encrypt_message(encrypt_key, data)
    signature = sign(sign_key,
                     str(packet_type) +
                     base64.b64encode(e_source) +
                     str(dest) +
                     str(convo_id) +
                     base64.b64encode(e_data))
    return json.dumps({"packet_type": str(packet_type),
                       "e_source": base64.b64encode(e_source),
                       "dest": str(dest),
                       "convo_id": str(convo_id),
                       "e_data": base64.b64encode(e_data),
                       "signature": base64.b64encode(signature)})
    # return PacketS(str(packet_type), e_source, str(dest), str(convo_id),
    #                e_data, str(signature))


def gen_packet_a(packet_type, source, dest, convo_id, proposed_key,
                 encrypt_key, sign_key):
    """Creates a JSON formatted packet with data for
    initializing a communication line

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
                     str(packet_type) +
                     base64.b64encode(e_source) +
                     str(dest) +
                     base64.b64encode(e_convo_id) +
                     repr(e_proposed_key) +
                     base64.b64encode(e_sender_key))
    return json.dumps({"packet_type": str(packet_type),
                       "e_source": base64.b64encode(e_source),
                       "dest": str(dest),
                       "e_convo_id": base64.b64encode(e_convo_id),
                       "e_proposed_key": repr(e_proposed_key),
                       "e_sender_key": base64.b64encode(e_sender_key),
                       "signature": base64.b64encode(signature)})
    # return PacketA(e_source, dest, e_convo_id, e_proposed_key, e_sender_key,
    #                signature)


def decrypt_packet_s(packet, encrypt_key, sender_key):
    """Decrypts a packet encrypted with an AES key

    Args:
        packet:      JSON string packet to be decrypted
        encrypt_key: Symmetric key for decrypting
        sender_key:  Public key of sender for checking signature

    Returns:
        DecryptedPacketS object ready for parsing
    """
    jsonpacket = json.loads(packet)
    to_verify = (jsonpacket['packet_type'] +
                 jsonpacket['e_source'] +
                 jsonpacket['dest'] +
                 jsonpacket['convo_id'] +
                 jsonpacket['e_data'])
    if verify(sender_key, to_verify,
              base64.b64decode(jsonpacket['signature'])):
        d_source = decrypt_message(encrypt_key,
                                   base64.b64decode(jsonpacket['e_source']))
        d_data = decrypt_message(encrypt_key,
                                 base64.b64decode(jsonpacket['e_data']))
        return DecryptedPacketS(jsonpacket['packet_type'],
                                d_source,
                                jsonpacket['convo_id'],
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
    jsonpacket = json.loads(packet)
    prop_key = decrypt_auth(private_key,
                            ast.literal_eval(jsonpacket['e_proposed_key']))
    d_source = decrypt_message(prop_key,
                               base64.b64decode(jsonpacket['e_source']))
    d_convo_id = decrypt_message(prop_key,
                                 base64.b64decode(jsonpacket['e_convo_id']))
    d_send_key = decrypt_message(prop_key,
                                 base64.b64decode(jsonpacket['e_sender_key']))
    # if verify(sender_key, to_verify, packet.get_signature()):
    return DecryptedPacketA(jsonpacket['packet_type'],
                            d_source,
                            d_convo_id,
                            prop_key,
                            d_send_key)
    # return False


def json_get_convo_id(json_packet_string):
    """Returns the ConvoID from a JSON packet

    Args:
        json_packet_string: Packet to get ConvoID from

    Returns:
        ConvoID of packet
        False if convo_id is encrypted/missing
    """
    jsonpacket = json.loads(json_packet_string)
    if jsonpacket['convo_id']:
        return jsonpacket['convo_id']
    else:
        return False


def json_get_packet_type(json_packet_string):
    """Returns the packet type from a JSON packet

    Args:
        json_packet_string: Packet to get ConvoID from

    Returns:
        Packet type of packet
        False if packet_type is missing
    """
    jsonpacket = json.loads(json_packet_string)
    if jsonpacket['packet_type']:
        return jsonpacket['packet_type']
    else:
        return False
