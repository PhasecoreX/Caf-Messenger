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


def gen_message(source, dest, message, signing_key):
    encrypt_data = MPacket(source, message)
    signature = sign(signing_key, dest + encrypt_data)
    return Packet(dest, encrypt_data, signature)


def gen_command(source, dest, command, signing_key):
    encrypt_data = CPacket(source, command)
    signature = sign(signing_key, dest + encrypt_data)
    return Packet(dest, encrypt_data, signature)


def gen_auth(source, dest, proposed_key, signing_key):
    encrypt_data = APacket(source, proposed_key)
    signature = sign(signing_key, dest + encrypt_data)
    return Packet(dest, encrypt_data, signature)
