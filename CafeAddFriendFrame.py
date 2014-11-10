# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#	CIS 467 Capstone Project - Cafe Messenger
#	CafeAddFriendFrame.py
#	Author: Michael Currie
#	
#	This program is the main GUI frame for the "Add Friend" feature. It will
#	spawn off of CafeChatFrame when the "Add Friend" button is pressed. This
#	GUI will accept a Public RSA Key in order to find another user in the
#	distributed system, and after finding the person it will give their actual
#	name, and the user will be able to set a nickname and a quick note about
#	them.
#	
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import Tkinter as tk

class AddFriend(tk.Toplevel):
    def __init__(self, parent, myKey):
        """
        """
        tk.Toplevel.__init__(self, parent)
        self.maxsize(500, 600)
        self.minsize(500, 600)
        self.parent = parent
        self.myKey = myKey
        self.myKeyLabel = tk.Label(self)
        self.myKeyArea = tk.Text(self)
        self.cancelButton = tk.Button(self)
        self.fileEntry = tk.Entry(self)
        self.addButton = tk.Button(self)
        self.keyArea = tk.Text(self)
        self.nameEntry = tk.Entry(self)
        self.nameLabel = tk.Label(self)
        self.keyLabel = tk.Label(self)
        self.info = {}
        self.createWidgets()

    def createWidgets(self):
        self.addButton.config(text="Add", command=self.addButtonPress)
        self.addButton.config(width=60, height=20)
        self.addButton.place(x=0, y=460, width=60, height=20)

        self.cancelButton.config(text="Cancel", command=self.cancelButtonPress)
        self.cancelButton.config(width=60, height=20)
        self.cancelButton.place(x=65, y=460, width=60, height=20)

        self.myKeyArea.config(height=200, width=500)
        self.myKeyArea.insert("end", self.myKey)
        self.myKeyArea.place(x=0, y=20, height=200, width=500)

        self.myKeyLabel.config(text="Give this key to your friend:")
        self.myKeyLabel.config(height=20, width=200)
        self.myKeyLabel.place(y=0, x=0, height=20, width=200)
        
        self.nameLabel.config(text="Enter name of friend here:")
        self.nameLabel.config(height=20, width=200)
        self.nameLabel.place(x=5, y=220, height=20, width=200)
        
        self.nameEntry.config(width=200)
        self.nameEntry.place(x=200, y=220, width=200)
        
        self.keyLabel.config(text="Enter public key of friend here:")
        self.keyLabel.config(height=20, width=200)
        self.keyLabel.place(x=5, y=240, height=20, width=200)
        
        self.keyArea.config(height=200, width=500)
        self.keyArea.place(x=0, y=260, height=200, width=500)
        
    def addButtonPress(self):
        self.info["name"] = self.nameEntry.get()
        self.info["key"] = self.keyArea.get(1.0, "end")
        self.parent.confirm_friend(self.info)
        self.destroy()
        
    def cancelButtonPress(self):
        self.destroy()
        
    