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

"""packet.py

Definitions for packet format. To be sent over the network.
"""


class Packet(object):

    """Defines master packet format

    This will be the object that will be sent over the network

    Args:
        packet_type: Type of packet (A, S, or M currently)
        source:      (Encrypted) Where the packet came from
        destination: 8 Hex character destination
        convo_id:    Conversation ID (to know what convo this packet goes to)
        data:        (Encrypted) Data
        signature:   Signature over all above fields
    """

    def __init__(self,
                 packet_type,
                 source,
                 destination,
                 convo_id,
                 data,
                 signature):
        self.packet_type = packet_type
        self.source = source
        self.destination = destination
        self.convo_id = convo_id
        self.data = data
        self.signature = signature

    def get_packet_type(self):
        """Gets packet type (not encrypted) from encrypted packet"""
        return self.packet_type

    def get_source(self):
        """Gets source (encrypted) from encrypted packet"""
        return self.source

    def get_destination(self):
        """Gets destination (not encrypted) from encrypted packet"""
        return self.destination

    def get_convo_id(self):
        """Gets ConvoID (not encrypted) from encrypted packet"""
        return self.convo_id

    def get_data(self):
        """Gets data (encrypted) from encrypted packet"""
        return self.data

    def get_signature(self):
        """Gets signature (not encrypted) from encrypted packet"""
        return self.signature


class DecryptedPacket(object):

    """Defines master packet format (decrypted)

    This will be the object that will contain all decrypted information

    Args:
        packet_type: Type of packet (A, S, or M currently)
        source:      Where the packet came from
        convo_id:    Conversation ID (to know what convo this packet goes to)
        data:        Data
    """

    def __init__(self,
                 packet_type,
                 source,
                 convo_id,
                 data):
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
