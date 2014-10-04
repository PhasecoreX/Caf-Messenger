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


class FriendsPanel(tk.Frame):

    def createWidgets(self, controller):
        self.fheader.config(text="_ClientName_'s Friendlist")
        self.fheader.config(width=185, height=20)
        self.fheader.place(x=0, y=0, anchor="nw", width=185, height=20)

        self.flist.config(width=185, height=505)
        self.flist.place(x=0, y=25, anchor="nw", width=185, height=505)

        self.friendEntry.config(width=90, height=20)
        self.friendEntry.place(x=0, y=535, anchor="nw", width=90, height=20)
        self.friendEntry.bind("<Return>", self.enterKeyPress)

        self.addButton.config(text="Add Friend", width=90, height=20)
        self.addButton.config(command=self.addButtonPress)
        self.addButton.place(x=95, y=535, anchor="nw", width=90, height=20)

        self.chatButton.config(text="Chat", width=90, height=20)
        self.chatButton.config(command=self.chatButtonPress)
        self.chatButton.place(x=0, y=560, anchor="nw", width=90, height=20)

        self.removeButton.config(text="Remove", width=90, height=20)
        self.removeButton.config(command=self.removeButtonPress)
        self.removeButton.place(x=95, y=560, anchor="nw", width=90, height=20)

    def addButtonPress(self):
        print "Such Friend! Wow."
        self.flist.insert("end", self.friendEntry.get(1.0, "end"))
        self.friendEntry.delete(1.0, "end")

    def enterKeyPress(self, event):
        return 'break'

    def chatButtonPress(self):
        print "So chatty, much talk."

    def removeButtonPress(self):
        self.flist.delete("anchor")
        print "How mean, such enemy."

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.fheader = tk.Label(self)
        self.flist = tk.Listbox(self)
        self.addButton = tk.Button(self)
        self.removeButton = tk.Button(self)
        self.friendEntry = tk.Text(self)
        self.chatButton = tk.Button(self)
        self.createWidgets(controller)


if __name__ == "__main__":
    top = MainFrame()
    top.mainloop()
