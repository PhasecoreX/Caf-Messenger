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
        encrypted_payload: Encrypted packet (see packets below)
        signature:         Signature over destination and encrypted payload
    """

    def __init__(self, destination, encrypted_payload, signature):
        self.destination = destination
        self.encrypted_payload = encrypted_payload
        self.signature = signature


class APacket:

    """Defines A-Packet format

    Used for initiating communication.
    One option for the encrypted_payload filed in Packet

    Args:
        source:       8 Hex character source
        proposed_key: Symmetric key to use for future communications
    """

    def __init__(self, source, proposed_key):
        self.source = source
        self.proposed_key = proposed_key

    def get_source(self):
        return self.source

    def get_key(self):
        return self.proposed_key


class MPacket:

    """Defines M-Packet format

    Used for sending messages.
    One option for the encrypted_payload filed in Packet

    Args:
        source:  8 Hex character source
        message: Message to send
    """

    def __init__(self, source, message):
        self.source = source
        self.message = message

    def get_source(self):
        return self.source

    def get_message(self):
        return self.message


class CPacket:

    """Defines C-Packet format

    Used for sending commands.
    One option for the encrypted_payload filed in Packet

    Args:
        source:  8 Hex character source
        command: Command to send
    """

    def __init__(self, source, command):
        self.source = source
        self.command = command

    def get_source(self):
        return self.source

    def get_command(self):
        return self.command
