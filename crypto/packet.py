#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  packet.py
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
"""packet.py

Definitions for packet formats to be sent over the network.
"""


class DecryptedPacketS(object):

    """Defines master packet format for symmetric packets (decrypted)

    This will be the object that will contain all decrypted information

    Args:
        packet_type: Type of packet (S, or M currently)
        source:      Where the packet came from
        convo_id:    Conversation ID (to know what window this packet goes to)
        data:        - (M) Message
                     - (C) Command
    """

    def __init__(self, packet_type, source, convo_id, data):
        self.packet_type = packet_type
        self.source = source
        self.convo_id = convo_id
        self.data = data

    def get_packet_type(self):
        """Gets packet type from decrypted packet"""
        return self.packet_type

    def get_source(self):
        """Gets source from decrypted packet"""
        return self.source

    def get_convo_id(self):
        """Gets ConvoID from decrypted packet"""
        return self.convo_id

    def get_data(self):
        """Gets data from decrypted packet"""
        return self.data


class DecryptedPacketA(DecryptedPacketS):

    """Defines master packet format for authentication packets (decrypted)

    This will be the object that will contain all decrypted information

    Args:
        source:       Where the packet came from
        convo_id:     Conversation ID other user wants you to use when replying
        proposed_key: Proposed symmetric key
        sender_key:   String of senders public key
    """

    def __init__(self, packet_type, source, convo_id, proposed_key,
                 sender_key):
        DecryptedPacketS.__init__(self, packet_type, source, convo_id,
                                  proposed_key)
        self.sender_key = sender_key

    def get_proposed_key(self):
        """Gets proposed key from decrypted packet"""
        return self.data

    def get_sender_key(self):
        """Gets senders public key string from decrypted packet"""
        return self.sender_key
