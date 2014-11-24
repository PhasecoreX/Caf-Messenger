#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CafeAddFriendFrame.py
#
#  Copyright 2014 Michael Currie <CafeCurrie@gmail.com>
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

"""CafeAddFriendFrame.py

A class for implementing adding friends functionality.
"""

import Tkinter as tk
from CafeReadOnlyText import ReadOnlyText

class AddFriend(tk.Toplevel):

    """
    This class is called upon when the "Add Friend" bttn is pressed in the
    CafeMainFrame program. This program will communicate to the parent the
    arguments given by the user in various fields. It will display the current
    user's public key, then it will accept their friend's public key and name.
    
    If all fields are correct, then the window will exit gracefully and the
    parent will be updated accordingly. Otherwise nothing happens.
    """

    def __init__(self, parent, my_key):
        """Initialization function.
        
        Initializes all of the widgets and objects, then calls the 
        create_widgets function to configure and place them.
        
        Args:  
            parent: The parent window that created this Toplevel.
            my_key: The key associated with the client user.
        
        """
        tk.Toplevel.__init__(self, parent)
        self.maxsize(500, 600)
        self.minsize(500, 600)
        self.parent = parent
        self.my_key = my_key
        self.my_key_label = tk.Label(self)
        self.my_key_area = ReadOnlyText(self)
        self.cncl_bttn = tk.Button(self)
        self.add_bttn = tk.Button(self)
        self.key_area = tk.Text(self)
        self.name_entry = tk.Entry(self)
        self.name_label = tk.Label(self)
        self.key_label = tk.Label(self)
        self.info = {}
        self.error_label = tk.Label(self)
        self.create_widgets()

    def create_widgets(self):
        """A function that gets called on creation of the class.
        
        This function configures and places all widgets into their respective
        spots, and applies the commands to the various bttns and keys.
        
        """
        self.my_key_area.config(height=205, width=500, background="lightgray")
        self.my_key_area.insert("end", self.my_key)
        self.my_key_area.place(x=5, y=25, height=205, width=490)

        self.my_key_label.config(text="Give this key to your friend:")
        self.my_key_label.config(height=20, width=200)
        self.my_key_label.place(x=5, y=5, height=20, width=200)

        self.name_label.config(text="Enter your friend's name:")
        self.name_label.config(height=20, width=200)
        self.name_label.place(x=5, y=245, height=20, width=200)

        self.name_entry.config(width=200)
        self.name_entry.place(x=210, y=245, width=200)

        self.key_label.config(text="Enter your friend's key here:")
        self.key_label.config(height=20, width=200)
        self.key_label.place(x=5, y=265, height=20, width=200)

        self.key_area.config(height=200, width=500)
        self.key_area.place(x=5, y=285, height=200, width=490)

        self.add_bttn.config(text="Add Friend", command=self.add_bttn_press)
        self.add_bttn.config(width=120, height=80)
        self.add_bttn.place(x=5, y=495, width=120, height=80)

        self.cncl_bttn.config(text="Cancel", command=self.cncl_bttn_press)
        self.cncl_bttn.config(width=120, height=80)
        self.cncl_bttn.place(x=130, y=495, width=120, height=80)

        self.error_label.config(text="", width=245, height=80, fg="red")
        self.error_label.place(x=255, y=495, width=245, height=80)

    def add_bttn_press(self):
        """A function that gets called when the add bttn is pressed.
        
        This function will pull a name and a key from the nameentry and keyarea
        widgets and pass a dictionary containing them to the parent window with
        the function confirm_friend. The parent will then reply with various
        success/fail flags, which this program will respond to.
        
        -1: The key was invalid.
        0: Success.
        1: A friend of the same name already exists.
        
        """
        if self.name_entry.get() is "":
            self.error_label.config(text="Please enter a name.")
            return 'break'
        self.info["name"] = self.name_entry.get()
        self.info["key"] = self.key_area.get(1.0, "end")
        flag = self.parent.confirm_friend(self.info)
        if flag is 0:
            self.destroy()
        if flag is -1:
            self.error_label.config(text="RSA format not supported.")
        if flag is 1:
            self.error_label.config(
                text="A friend already exists with that name.")

    def cncl_bttn_press(self):
        """A function that gets called when the cncl bttn is pressed.
        
        This function will close the window, no changes were made to the parent.
        
        """
        self.destroy()
