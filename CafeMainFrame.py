# CIS 467 Capstone Project - Cafe Messenger
#
# This will be the container for the main prototype window.
# It will simply feature a friend's list on the right side,
# and the chat window on the left side. I'm considering
# having every friend opened to have its own independent
# frame, but that may be implemented later in the long run.
#
#
#
#
#

from CafeFriendPanel import FriendsPanel
from CafeChatPanel import ChatPanel
from CafeMainMenuBar import MainMenu
import Tkinter as tk

from twisted.internet import reactor

import crypto

HOST = ''
PORT = 1025

class MainFrame(tk.Tk):
    """
    """

    def create_panels(self):
        """
        """

        self.container_frame.config(width=800, height=630)
        self.container_frame.place(x=0, y=0, anchor="nw")
        
        # Display the menu
        self.config(menu=self.menubar)

        # Create and place the Chat Panel
        self.chat.config(width=590, height=590)
        self.chat.place(x=5, y=5, anchor="nw")

        # Create and place the Friends List
        self.friends.config(width=190, height=590)
        self.friends.place(x=605, y=5, anchor="nw")

    def quit(self):
        reactor.stop()

    def append_message(self, name, message):
        """This method sends a message and name to the chat panel.

        Invokes the text_area_append method of the ChatPanel class.
        It sends a name and a message to be appended on the textarea.

        """
        self.chat.text_area_append(name, message)

    def change_chat_name(self, name):
        """This method sends a name to the chat panel to be changed.

        Invokes the change_chat_name method of the ChatPanel class.

        """
        self.chat.change_chat_name(name)

    def send(self, message):
        """This method receives a message from its chat child and forwards it.

        This is a callback chain specific method. It will receive a message
        from the child, then forward that message to the controller which
        will have a method called "send_message(message)"

        Args:
        message: The message that will be sent to the controller.

        """
        
        #Chop off the \n
        print "Encrypting:\n" + message[:-1]
        emsg = crypto.encrypt_message(self.key, message[:-1])
        self.conn.transport.write(emsg + "\r\n")
        print "Sending:\n" + emsg + "\n"

    def __init__(self, controller, conn, *args, **kwargs):
        """
        """
        self.conn = conn
        print "\nWelcome to CAFE Messenger! (debug mode)\n"
        tk.Tk.__init__(self, *args, **kwargs)
        self.key = b'01234567890123450123456789012345'
        self.conn = conn
        self.controller = controller
        self.container_frame = tk.Frame(self)
        self.menubar = MainMenu(self)
        self.chat = ChatPanel(self)
        self.friends = FriendsPanel(self)

        self.title("Cafe")
        self.maxsize(800, 630)
        self.minsize(800, 630)

        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.create_panels()