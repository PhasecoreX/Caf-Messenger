#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  crypto_controller.py
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

import base64
import json

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


def gen_packet_a(packet_type, source, dest, convo_id,
                 proposed_key, encrypt_key, sign_key):
    """Creates an encrypted authentication packet with data for sending

    Args:
        packet_type:  Type of packet we are sending:
                      - (A) authentication
        source:       Source user ID (yours)
        dest:         Destination user ID (theirs)
        convo_id:     ConvoID you want destination to use when contacting you
        proposed_key: Proposed symmetric key for future communications
        encrypt_key:  Their public key for encrypting
        sign_key:     Your private key for signing

    Returns:
        Packet object ready for sending
    """
    return packet_gen.gen_packet_a(packet_type, source, dest, convo_id,
                                   proposed_key, encrypt_key, sign_key)


def gen_packet_s(packet_type, source, dest, convo_id,
                 data, encrypt_key, sign_key):
    """Creates an encrypted packet with data for sending

    Args:
        packet_type: Type of packet we are sending:
                     - (M) message
                     - (C) command
        source:      Source user ID (yours)
        dest:        Destination user ID (theirs)
        convo_id:    Destination user conversation ID
        data:        Data to send:
                     - (M) Raw message
                     - (C) command
        encrypt_key: Conversations symmetric key for encrypting
        sign_key:    Your private key for signing

    Returns:
        Packet object ready for sending
    """
    return packet_gen.gen_packet_s(packet_type, source, dest, convo_id, data,
                                   encrypt_key, sign_key)


def decrypt_packet_a(packet, encrypt_key):
    """Decrypts an authentication packet

    Args:
        packet:      Authentication packet to be decrypted
        encrypt_key: Your private key for decrypting

    Returns:
        DecryptedPacketA object ready for parsing
    """
    return packet_gen.decrypt_packet_a(packet, encrypt_key)


def decrypt_packet_s(packet, encrypt_key, sender_key):
    """Decrypts a packet

    Args:
        packet:      Packet to be decrypted
        encrypt_key: Your private key for decrypting
        sender_key:  Public key of sender for checking signature

    Returns:
        DecryptedPacketS object ready for parsing
    """
    return packet_gen.decrypt_packet_s(packet, encrypt_key, sender_key)


def json_get_packet_type(json_packet_string):
    """Returns the packet type from a JSON packet

    Args:
        json_packet_string: Packet to get ConvoID from

    Returns:
        Packet type of packet
        False if packet_type is missing
    """
    return packet_gen.json_get_packet_type(json_packet_string)


def json_get_convo_id(json_packet_string):
    """Returns the ConvoID from a JSON packet

    Args:
        json_packet_string: Packet to get ConvoID from

    Returns:
        ConvoID of packet
        False if convo_id is encrypted/missing
    """
    return packet_gen.json_get_convo_id(json_packet_string)


def verify_packet(packet, sender_key):
    """Checks signature on packet

    Used oftentimes for checking Authentication packets, once we figure out
    who it's from

    Args:
        packet:      JSON string packet to be decrypted
        sender_key:  Public key of sender for checking signature

    Returns:
        True if authentic, false otherwise
    """
    if json_get_packet_type(packet) == "A":
        jsonpacket = json.loads(packet)
        to_verify = (jsonpacket['packet_type'] +
                     jsonpacket['e_source'] +
                     jsonpacket['dest'] +
                     jsonpacket['e_convo_id'] +
                     jsonpacket['e_proposed_key'] +
                     jsonpacket['e_sender_key'])
        return crypto.verify(sender_key, to_verify,
                             base64.b64decode(jsonpacket['signature']))
    else:
        return packet_gen.sym_verify(packet, sender_key)


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
        IOError:    File could not be written
        ValueError: Malformed string
    """
    try:
        success = hdd.add_friend(name, friend_name, public_key)
    except IOError:
        raise
    if success is False:
        return False
    try:
        load_friend(name, friend_name)
    except:
        delete_friend(name, friend_name)
        raise ValueError
    return True


def load_friend(name, friend_name):
    """Loads a friends public key

    Args:
        name:        Profile name
        friend_name: Name of friend

    Returns:
        RSA key object (_RSAobj) containing friends public key
        False if friend does not exist

    Raises:
        ValueError, IndexError, TypeError: File corrupt.
    """
    path = hdd.load_friend(name, friend_name)
    if path is False:
        return False
    try:
        return crypto.load_key(path)
    except IOError:
        return False
    except (ValueError, IndexError, TypeError):
        raise
    return True


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
    print "This is how you encrypt packets!"
    print ""

    print "Generating two asymmetric keys..."
    ALPHA_KEY = crypto.generate_key_pair()
    BETA_KEY = crypto.generate_key_pair()
    print ""

    ALPHA_PROPOSED_SYM = generate_symmetric_key()
    print "----------Node A----------"
    print "[A] Generating auth packet A->B using randomly generated"
    print "    symmetric key:   " + ALPHA_PROPOSED_SYM
    print "[A] Also, I want Node B to reply to me with ConvoID 42"
    ENCRYPTED_PACKET = gen_packet_a("A", "Node A", "Node B", 42,
                                    ALPHA_PROPOSED_SYM, BETA_KEY, ALPHA_KEY)
    print ENCRYPTED_PACKET
    print ""

    print "----------Node B----------"
    print "[B] Decrypting auth packet..."
    DECRYPTED_PACKET = decrypt_packet_a(ENCRYPTED_PACKET, BETA_KEY)
    SYMMETRIC_KEY = DECRYPTED_PACKET.get_data()
    print "[B] Got this key --> " + SYMMETRIC_KEY
    print ("[B] Got this convoID to use: " +
           str(DECRYPTED_PACKET.get_convo_id()))
    print ""

    print "[B] Accepted! Sending command packet 'accept 12' B->A"
    print "[B] I want Node A to reply to me using ConvoID 12"
    ENCRYPTED_PACKET = gen_packet_s("C", "None B", "Node A", 42, "accept 12",
                                    SYMMETRIC_KEY, BETA_KEY)
    print ENCRYPTED_PACKET
    print ""

    print "----------Node A----------"
    print ("[A] I got a command packet with ConvoID " +
           str(json_get_convo_id(ENCRYPTED_PACKET)))
    print "[A] This must be from Node B!"
    print "[A] Decrypting command packet..."
    DECRYPTED_PACKET = decrypt_packet_s(ENCRYPTED_PACKET, SYMMETRIC_KEY,
                                        BETA_KEY)
    print "[A] Got this response: '" + str(DECRYPTED_PACKET.get_data()) + "'"
    print "[A] Awesome! Now I shall send my message 'Hello World!'"
    print "    to Node B with his preferred ConvoID 12... A->B"
    ENCRYPTED_PACKET = gen_packet_s(
        "M", "Node A", "Node B", 12, "Hello World!", SYMMETRIC_KEY, ALPHA_KEY)
    print ENCRYPTED_PACKET
    print ""

    print "----------Node B----------"
    print ("[B] I got a message packet with ConvoID " +
           str(json_get_convo_id(ENCRYPTED_PACKET)))
    print "[B] This must be from Node A!"
    print "[B] Decrypting message packet..."
    DECRYPTED_PACKET = decrypt_packet_s(ENCRYPTED_PACKET, SYMMETRIC_KEY,
                                        ALPHA_KEY)
    print "[B] Got this response: '" + str(DECRYPTED_PACKET.get_data()) + "'"
    print ""
