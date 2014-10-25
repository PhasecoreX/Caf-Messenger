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
"""hdd.py

Functions to manage hard drive access.
"""
import os
PRIVATE_KEY = "user.pem"
# No support for Windows just yet...
# We would be saving in %User%\AppData\Roaming\cafe
HOME_DIR = os.path.expanduser("~/.config/cafe")
# We will put an if statement for "\" Windows paths
SLASH = "/"


def get_profile_list():
    """Looks up all profiles you have created

    Only returns profiles with a user.pem file (private key) inside of them.

    Returns:
        List of all currently available profiles
    """
    result = []
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
        os.makedirs(path)
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
    """
    path = HOME_DIR + SLASH + name + SLASH + PRIVATE_KEY
    if os.path.isfile(path):
        return path
    return False
