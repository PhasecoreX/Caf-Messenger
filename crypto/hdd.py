#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  hdd.py
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
"""hdd.py

Functions to manage hard drive access.
"""
import os
import shutil
import sys

# Set up default (Linux) values for variables
HOME_DIR = os.path.expanduser("~/.config/cafe")
SLASH = "/"
# Now, change variables if we are on a different OS
if sys.platform.startswith('win32'):
    HOME_DIR = os.path.expanduser("~\\AppData\\Roaming\\cafe")
    SLASH = "\\"
# Other stuff that won't change between different OS
PRIVATE_KEY = "user.pem"
FRIENDS = "friends"
F_END = ".pem"


def get_profile_list():
    """Looks up all profiles you have created

    Run this first to create the config directory!
    Only returns profiles with a user.pem file (private key) inside of them.

    Returns:
        List of all currently available profiles
    """
    result = []
    if not os.path.exists(HOME_DIR):
        return result
    for filename in os.listdir(HOME_DIR):
        if os.path.exists(HOME_DIR + SLASH + filename + SLASH + PRIVATE_KEY):
            result.append(filename)
    return result


def create_profile(name):
    """Creates folders for a new profile

    This doesn't actually save the "user.pem" file.
    Crypto library would have to save that file.

    Args:
        name: Profile name

    Returns:
        Path to private key file (that would need to be created)
        False if profile exists

    Raises:
        OSError - folder was not able to be created
    """
    path = HOME_DIR + SLASH + name
    if os.path.isdir(path):
        return False
    try:
        os.makedirs(path + SLASH + FRIENDS)
    except OSError:
        if not os.path.isdir(path):
            raise
    return path + SLASH + PRIVATE_KEY


def get_profile_key(name):
    """Get the absolute path to a private key for a given profile name

    Args:
        name: Profile name

    Returns:
        Absolute path to that private key
        False if profile was not found
    """
    path = HOME_DIR + SLASH + name + SLASH + PRIVATE_KEY
    if os.path.isfile(path):
        return path
    return False


def delete_profile(name):
    """Deletes a profile

    Args:
        name: Profile name to delete

    Returns:
        True if deleted
        False if error/profile doesn't exists
    """
    path = HOME_DIR + SLASH + name
    try:
        shutil.rmtree(path)
    except OSError:
        return False
    return True


def get_friend_list(name):
    """Looks up all friends you have

    Args:
        name: Profile name to search for friends

    Returns:
        List of all friends for given user
    """
    path = HOME_DIR + SLASH + name + SLASH + FRIENDS
    result = []
    if not os.path.exists(path):
        return result
    for filename in os.listdir(path):
        if os.path.isfile(path + SLASH + filename):
            if filename.endswith(F_END):
                result.append(filename)
    return result


def add_friend(name, friend_name, public_key):
    """Adds a friend (helper)

    Args:
        name:        Profile name
        friend_name: Name of friend

    Returns:
        True if written correctly
        False if friend already exists

    Raises:
        IOError: Can't write to disk
    """
    path = (HOME_DIR + SLASH + name + SLASH + FRIENDS + SLASH +
            friend_name + F_END)
    if os.path.isfile(path):
        return False
    try:
        writing = open(path, "w")
        writing.write(public_key)
        writing.close()
        return True
    except:
        raise


def load_friend(name, friend_name):
    """Loads a friends public key file name, for further processing

    Args:
        name:        Profile name
        friend_name: Name of friend

    Returns:
        Path to key file
        False if friend does not exist
    """
    path = (HOME_DIR + SLASH + name + SLASH + FRIENDS + SLASH +
            friend_name + F_END)
    if os.path.isfile(path):
        return path
    return False


def delete_friend(name, friend_name):
    """Deletes a friend

    Args:
        name:        Profile name
        friend_name: Friend to delete :(

    Returns:
        True if deleted
        False if OSError/friend doesn't exists
    """
    path = (HOME_DIR + SLASH + name + SLASH + FRIENDS + SLASH +
            friend_name + F_END)
    try:
        os.remove(path)
    except OSError:
        return False
    return True


def rename_friend(name, friend_old, friend_new):
    """Renames friend

    Args:
        name:       Profile name
        friend_old: Friends old name
        friend_new: Friends new name

    Returns:
        True on success
        False on OSError/friend not found
    """
    old = (HOME_DIR + SLASH + name + SLASH + FRIENDS + SLASH +
           friend_old + F_END)
    new = (HOME_DIR + SLASH + name + SLASH + FRIENDS + SLASH +
           friend_new + F_END)
    try:
        os.rename(old, new)
    except OSError:
        return False
    return True
