#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CafeChatPanel.py
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

"""CafeChatPanel.py

A class for the chat window that pops up when the chat button is pressed.
"""

from CafeReadOnlyText import ReadOnlyText 
import Tkinter as tk

class ChatPanel(tk.Toplevel):

    """
    
    """

    def create_widgets(self):
        """A function that gets called on creation of the class.
        
        This function configures and places all widgets into their respective
        spots, and applies the commands to the various buttons and keys.
        
        """

        self.textarea.config(width=570, height=495, state="disabled")
        self.textarea.place(x=0, y=25, anchor="nw", width=570,
                            height=495)
        self.textarea.config(background="lightgray", borderwidth=2)

        self.sendbutton["text"] = "Send"
        self.sendbutton.config(command=self.send_button_pressed)
        self.sendbutton.config(width=40, height=20)
        self.sendbutton.place(x=525, y=535, anchor="nw", width=45,
                              height=40)

        self.textentry.config(width=525)
        self.textentry.place(x=0, y=525, width=515, height=60)
        self.textentry.bind("<KeyPress-Return>", self.enter_key_pressed)
        self.textentry.bind("<Shift-Return>", self.shift_enter_pressed)

    def shift_enter_pressed(self, event):
        """A function that gets called when shift+enter is pressed.
        
        This function will insert a newline into the message box. This was
        needed for users to insert newlines after the enter key was binded to
        the send button.
        
        Args:
            event:  The event that associates with a specific key.
            
        Returns:
            A break sequence.
        
        """
        self.textentry.insert("end", "\n")
        return 'break'

    def text_area_append(self, name, message):
        """A function that appends the given message to the chat area.
        
        This will unlock the chat area, append the name and message, then lock
        the chat area again. This is used by the parent when a message from
        another user is received.
        
        Args:
            name:   The name of the other client.
            parent: The message of the other client.
        
        """
        self.textarea.config(state="normal")
        self.textarea.insert("end", name + ": " + message + "\n")
        self.textarea.config(state="disabled")

    def enter_key_pressed(self, event):
        """A function that gets called whenever the enter key is pressed.
        
        This will check to see if there is any tangible text in the message
        box, then if there is it simulates a send button press.
        
        Args:
            event:  The event that associates with a specific key.
            
        Returns:
            A break sequence.
        
        """
        t = self.textentry.get(1.0, "end")
        if t == "\n":
            return 'break'
        self.send_button_pressed()
        return 'break'

    def send_button_pressed(self):
        """This method is called when the send button is pressed.

        This will send the message to the panel's parent, who has
        its own callback method to send to the controller.

        """
        message = self.textentry.get(1.0, "end")
        self.parent.send(message, self.convo_id, self.s_key)
        self.textarea.config(state="normal")
        self.textarea.insert("end", self.name + ": ")
        self.textarea.insert("end", self.textentry.get(1.0, "end"))
        self.textarea.see("end")
        self.textarea.config(state="disabled")
        self.textentry.delete(1.0, "end")

    def get_sym_key(self):
        """This method is called by the parent to get the symmetric key.
        
        This will return the symmetric key associated with this chat instance.
        
        """
        return self.s_key

    def get_name(self):
        """
        """
        return self.friend_name
    
    def set_friend_convo_id(self, convo_id):
        self.friend_convo_id = convo_id
    
    def get_friend_convo_id(self):
        return self.friend_convo_id

    def __init__(self, parent, name, friend_name, convo_id, friend_convo_id, s_key):
        """Initialization function.
        
        Initializes all of the widgets and objects, then calls the 
        create_widgets function to configure and place them.
        
        Args:  
            parent:         The parent window that created this Toplevel.
            name:           The name associated with the current user.
            friend_name:    The name associated with the friend.
            convo_id:         The number associated with the current window.
        
        """
        tk.Toplevel.__init__(self, parent)
        self.maxsize(600, 600)
        self.minsize(600, 600)
        self.title("Chat with " + friend_name)
        self.name = name
        self.friend_convo_id = friend_convo_id
        self.s_key = s_key
        self.friend_name = friend_name
        self.convo_id = convo_id
        self.parent = parent
        self.textarea = ReadOnlyText(self)
        self.sendbutton = tk.Button(self)
        self.textentry = tk.Text(self)
        self.create_widgets()
