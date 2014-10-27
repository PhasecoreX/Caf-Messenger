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
"""crypto_controller.py

A bunch of functions for encryption in Cafe Messenger
"""

import crypto
import hdd
import packet_gen


def generate_symmetric_key():
    """Generates a symmetric 256 bit AES key

    Returns:
        String (I think?)
    """
    return crypto.generate_symmetric_key()


def get_public_key_string(private_key):
    """Extracts the public key from a full key pair

    Args:
        private_key: RSA key object (_RSAobj) containing a private/public key

    Returns:
        String representing public key
    """
    return crypto.get_public_key_string(private_key)


def gen_packet(packet_type, source, dest, convo_id, data,
               encrypt_key, sign_key):
    """Creates an encrypted packet with data for sending

    Args:
        packet_type: Type of packet we are sending:
                     - (M) message
                     - (C) command, or
                     - (A) authentication
        source:      Source user ID
        dest:        Destination user ID
        convo_id:    Destination user conversation ID
        data:        Data to send:
                     - (M) message
                     - (C) command, or
                     - (A) proposed symmetric key
        encrypt_key: Key for encrypting (symmetric or private, depending.)
        sign_key:    Private key for signing each packet

    Returns:
        Packet object ready for sending
    """
    if packet_type.equals("M"):
        return packet_gen.gen_message_packet(source, dest, convo_id, data,
                                             encrypt_key, sign_key)
    if packet_type.equals("C"):
        return packet_gen.gen_command_packet(source, dest, convo_id, data,
                                             encrypt_key, sign_key)
    if packet_type.equals("A"):
        return packet_gen.gen_auth_packet(source, dest, convo_id, data,
                                          encrypt_key, sign_key)


def decrypt_packet(packet_type, packet, encrypt_key, sender_key):
    """Decrypts a packet

    Args:
        packet_type: Type of packet we are decrypting
                     - (M) message
                     - (C) command, or
                     - (A) authentication
        packet:      Packet to be decrypted
        encrypt_key: Key for decrypting (symmetric or private, depending.)
        sender_key:  Public key of sender for checking signature

    Returns:
        Decrypted_Packet object ready for parsing
    """
    if packet_type.equals("A"):
        return packet_gen.decrypt_packet_A(packet, encrypt_key, sender_key)
    if packet_type.equals("M") or packet_type.equals("C"):
        return packet_gen.decrypt_packet_S(packet, encrypt_key, sender_key)


def get_profile_list():
    """Looks up all profiles you have created

    Only returns profiles with a user.pem file (private key) inside of them.

    Returns:
        List of all currently available profiles
    """
    return hdd.get_profile_list()


def create_profile(name, password):
    """Creates a new profile

    Args:
        name:     Profile name
        password: Password for the new profile

    Returns:
        True on success
        False if profile exists

    Raises:
        OSError: Folder was not able to be created
        IOError: An error occurred writing file to disk
    """
    try:
        key_file = hdd.create_profile(name)
    except:
        raise
    if key_file is False:
        return False
    key_object = crypto.generate_key_pair()
    try:
        return crypto.save_key(key_object, key_file, password)
    except:
        raise


def load_profile(name, password):
    """Creates a new profile

    Args:
        name:     Profile name
        password: Password for that profile

    Returns:
        RSA key object (_RSAobj) containing a private/public key
        False if password is wrong

    Raises:
        IOError: File was not found
    """
    key_file = hdd.get_profile_key(name)
    if key_file is False:
        raise IOError
    try:
        return crypto.load_key(key_file, password)
    except (ValueError, IndexError, TypeError):
        return False


def delete_profile(name):
    """Get the absolute path to a private key for a given profile name

    Args:
        name: Profile name to delete

    Returns:
        True if deleted
        False if error/profile doesn't exists
    """
    return hdd.delete_profile(name)


def get_friend_list(name):
    """Looks up all friends you have

    Args:
        name: Profile name to search for friends

    Returns:
        List of all friends for given user
        False if user (or friends directory) doesn't exist
    """
    return hdd.get_friend_list(name)


def add_friend(name, friend_name, public_key):
    """Adds a friend

    Args:
        name:        Profile name
        friend_name: Name of friend
        public_key:  String of friends public key

    Returns:
        True if friend was added
        False if friend exists

    Raises:
        IOError:                           File could not be written
        ValueError, IndexError, TypeError: Malformed string
    """
    try:
        success = hdd.add_friend(name, friend_name, public_key)
    except IOError:
        raise
    if success is False:
        return False
    if load_friend(name, friend_name) is False:
        delete_friend(name, friend_name)
        return False
    return True


def load_friend(name, friend_name):
    """Loads a friends public key

    Args:
        name:        Profile name
        friend_name: Name of friend

    Returns:
        RSA key object (_RSAobj) containing friends public key
        False if friend does not exist/friend file is corrupt
    """
    path = hdd.load_friend(name, friend_name)
    if path is False:
        return False
    try:
        return crypto.load_key(path)
    except:
        return False


def delete_friend(name, friend_name):
    """Deletes a friend

    Args:
        name:        Profile name
        friend_name: Friend to delete :(

    Returns:
        True if deleted
        False if error/friend doesn't exists
    """
    return hdd.delete_friend(name, friend_name)


def rename_friend(name, friend_old, friend_new):
    """Renames friend

    Args:
        name:       Profile name
        friend_old: Friends old name
        friend_new: Friends new name

    Returns:
        True on success
        False on failure/friend not found
    """
    return hdd.rename_friend(name, friend_old, friend_new)


if __name__ == "__main__":
    print rename_friend("user1", "friend1", "friend2")
