# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#	CIS 467 Capstone Project - Cafe Messenger
#	CafeFriendFrame.py
#	Author: Michael Currie
#
#	This program is the GUI Frame for the friends list for the current user. It
#	will be the main controller for CafeChatFrame, CafeAddFriendFrame, and many
#	of the help and about pages.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import Tkinter as tk
from CafeFriendPanel import FriendPanel
from CafeMainMenuBar import MainMenu
from CafeChatPanel import ChatPanel


class MainFrame(tk.Tk):

    def createPanels(self):
        # Create the menubar
        menubar = MainMenu(self)

        # Display the menu
        self.config(menu=menubar)

        # Create and place the Friends List
        friends = FriendPanel(self)
        friends.config(width=190, height=600)
        friends.place(x=5, y=5, anchor="nw")

    # Main constructor
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Cafe")
        self.maxsize(195, 620)
        self.minsize(195, 620)
        self.createPanels()

    def chat_button_pressed(self, name):
        
        

if __name__ == "__main__":
    top = MainFrame()
    top.mainloop()
