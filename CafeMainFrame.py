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

from CafeFriendPanel import FriendPanel
from CafeChatPanel import ChatPanel
from CafeMainMenuBar import MainMenu
from CafeAddFriendFrame import AddFriend
import crypto_controller as crypto
import Tkinter as tk
import random as rndm
from twisted.internet import reactor

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

        # Create and place the Friends List
        self.friends.config(width=190, height=590)
        self.friends.place(x=5, y=5, anchor="nw")

    def quit(self):
        reactor.stop()

    def add_friend(self):
        t = AddFriend(self, crypto.get_public_key_string(self.myKeys))
        t.grab_set()

    def confirm_friend(self, info):
        try:
            crypto.add_friend(self.name, info["name"], info["key"])
        except:
            print "RSA format not supported."
            return 'break'
        self.friends.add_friend(info["name"])
        
    def remove_friend(self, name):
        if not crypto.delete_friend(self.name, name):
            print "Something went wrong with crypto.delete_friend."
            print "Consider reloading the client to get correct friend list."

    def chat(self, name):
        flag = True
        number = -1
        while flag:
            number = number + 1
            try:
                self.winlist[number]
            except KeyError:
                t = ChatPanel(self, name, number)
                self.winlist[number] = t
                print number
                flag = False
        """
        flag = True
        while flag:
            number = rndm.randrange(10000)
            try:
                self.winlist[number]
            except KeyError:
                t = ChatPanel(self, name, number)
                self.winlist[number] = t
                print number
                flag = False
        """

    def append_message(self, name, message):
        """This method sends a message and name to the chat panel.

        Invokes the text_area_append method of the ChatPanel class.
        It sends a name and a message to be appended on the textarea.

        """
        try:
            self.winlist[0].text_area_append(message)
        except IndexError:
            print "Another friend is trying to reach the client."
        except:
            print "A friend was previously chatting and the client closed out."

    def change_chat_name(self, name):
        """This method sends a name to the chat panel to be changed.

        Invokes the change_chat_name method of the ChatPanel class.

        """
        self.chat.change_chat_name(name)

    def send(self, message, num):
        """This method receives a message from its chat child and forwards it.

        This is a callback chain specific method. It will receive a message
        from the child, then forward that message to the controller which
        will have a method called "send_message(message)"

        Args:
        message: The message that will be sent to the controller.

        """

        # Chop off the \n
        print "Encrypting:\n" + message[:-1]
        emsg = crypto.encrypt_message(self.key, message[:-1])
        self.conn.transport.write(emsg + "\r\n")
        print "Sending:\n" + emsg + "\n"

    def __init__(self, controller, conn, myKeys, name, *args, **kwargs):
        """
        """
        self.name = name
        self.myKeys = myKeys
        self.conn = conn
        print "\nWelcome to CAFE Messenger! (debug mode)\n"
        tk.Tk.__init__(self, *args, **kwargs)
        self.key = b'01234567890123450123456789012345'
        self.chatCount = 0
        self.winlist = {}
        self.conn = conn
        self.controller = controller
        self.container_frame = tk.Frame(self)
        self.menubar = MainMenu(self)
        flist = crypto.get_friend_list(self.name)
        self.friends = FriendPanel(self, self.name, flist)

        self.title("Cafe")
        self.maxsize(200, 630)
        self.minsize(200, 630)

        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.create_panels()
