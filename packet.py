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


class Packet:

    """Defines master packet format

    This will be the packet/class/object that will be sent over the network

    Args:
        destination:       8 Hex character destination
        encrypted_payload: Encrypted packet (see Packet_Data below)
        signature:         Signature over destination and encrypted payload
    """

    def __init__(self, packet_type, destination, payload, signature):
        self.packet_type = packet_type
        self.destination = destination
        self.payload = payload
        self.signature = signature

    def get_packet_type(self):
        return self.packet_type

    def get_destination(self):
        return self.destination

    def get_payload(self):
        return self.payload

    def get_signature(self):
        return self.signature


class Packet_Data:

    """Defines the data format (payload) in the packet

    This will be encrypted for sending, or decrypted when received.

    Args:
        packet_type: Type of packet (A, C, or M thus far)
        source:      8 Hex character source
        data:        Symmetric key to use for future communications
    """

    def __init__(self, packet_type, source, data):
        self.packet_type = packet_type
        self.source = source
        self.data = data

    def get_packet_type(self):
        return self.packet_type

    def get_source(self):
        return self.source

    def get_data(self):
        return self.data
