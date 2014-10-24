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


class MainFrame(tk.Tk):

    def createPanels(self):
        # Create the menubar
        menubar = tk.Menu(self)

        # Add a cascade list called filemenu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Print")
        filemenu.add_command(label="Quit", command=self.quit)

        # Add a cascade list called editmenu
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Copy")
        editmenu.add_command(label="Paste")
        editmenu.add_command(label="Select All")

        # Add a cascade list called viewmenu
        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="View RSA Key Chain")
        viewmenu.add_command(label="View Current Chat's Public Key")

        # Add a cascade list called helpmenu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About Cafe")
        helpmenu.add_command(label="About Encryption")
        helpmenu.add_command(label="About Distributed Systems")

        # Add all the cascade menus to the main menubar
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Edit", menu=editmenu)
        menubar.add_cascade(label="View", menu=viewmenu)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # Display the menu
        self.config(menu=menubar)

        # Create and place the Friends List
        friends = FriendsPanel(self, self)
        friends.config(width=190, height=600)
        friends.place(x=5, y=5, anchor="nw")

    # Main constructor
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Cafe")
        self.maxsize(195, 620)
        self.minsize(195, 620)

        self.createPanels()

if __name__ == "__main__":
    top = MainFrame()
    top.mainloop()
