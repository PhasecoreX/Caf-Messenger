#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CafeFriendPanel.py
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

"""CafeFriendPanel.py

A class for the Friend List window that appears on startup.
"""

import Tkinter as tk
import CafeAddFriendFrame as add

class FriendPanel(tk.Frame):

    """
    """

    def create_widgets(self):
        """
        """
        self.fheader.config(text=str(self.name) + "'s Friendlist")
        self.fheader.config(width=185, height=20)
        self.fheader.place(x=0, y=0, anchor="nw", width=185, height=20)

        self.flist.config(width=185, height=505)
        self.flist.place(x=0, y=25, anchor="nw", width=185, height=505)

        self.addbutton.config(text="Add Friend", width=90, height=20)
        self.addbutton.config(command=self.add_button_pressed)
        self.addbutton.place(x=0, y=535, anchor="nw", width=185,
                             height=20)

        self.chatbutton.config(text="Chat", width=90, height=20)
        self.chatbutton.config(command=self.chat_button_pressed)
        self.chatbutton.place(x=0, y=560, anchor="nw", width=90,
                              height=20)
        print self.flist.get("anchor")

        self.removebutton.config(text="Remove", width=90, height=20)
        self.removebutton.config(command=self.remove_button_pressed)
        self.removebutton.place(x=95, y=560, anchor="nw", width=90,
                                height=20)
        if (self.flist.get(0) is ""):
            self.chatbutton.config(state="disabled")
            self.removebutton.config(state="disabled")

    def add_button_pressed(self):
        """
        """
        self.parent.add_friend()

    def add_friend(self, name):
        """
        """
        self.flist.insert("end", name)
        self.chatbutton.config(state="normal")
        self.removebutton.config(state="normal")

    def chat_button_pressed(self):
        """
        """
        self.parent.send_chat(self.flist.get("anchor"))

    def remove_button_pressed(self):
        """
        """
        self.parent.remove_friend(self.flist.get("anchor"))
        self.flist.delete("anchor")
        if self.flist.get(0) is "":
            self.chatbutton.config(state="disabled")
            self.removebutton.config(state="disabled")

    def __init__(self, parent, name, flist):
        """Initialization function.
        
        Initializes all of the widgets and objects, then calls the 
        create_widgets function to configure and place them.
        
        Args:  
            parent: The parent window that created this Toplevel.
            name: The name associated with the current user.
            flist: A list of friends.
        
        """
        tk.Frame.__init__(self, parent)
        self.name = name
        self.parent = parent
        self.fheader = tk.Label(self)
        self.flist = tk.Listbox(self)
        for friend in flist:
            self.flist.insert("end", friend[:-4])
        self.addbutton = tk.Button(self)
        self.removebutton = tk.Button(self)
        self.chatbutton = tk.Button(self)
        self.create_widgets()
