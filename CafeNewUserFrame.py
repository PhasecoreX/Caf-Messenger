# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#	CIS 467 Capstone Project - Cafe Messenger
#	CafeNewUserFrame.py
#	Author: Michael Currie
#	
#	This program is the GUI frame for the new client/user portion of the GUI. It
#	is called upon after the "New User" button is pressed in the CafeLoginFrame.
#	
#	
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import Tkinter as tk

import crypto_controller as crypto

class NewUserWindow(tk.Toplevel):
    def createWidgets(self):
        self.namelabel.config(text="Please enter a Username:")
        self.namelabel.config(width=200, height=40)
        self.namelabel.place(x=5, y=5, anchor="nw", width=200, height=40)
        
        self.nameentry.config(width=200)
        self.nameentry.place(x=210, y=5, anchor="nw", width=200, height=40)
        
        self.passlabel.config(text="Please enter a Password:")
        self.passlabel.config(width=200, height=40)
        self.passlabel.place(x=5, y=50, anchor="nw", width=200, height=40)
        
        self.passentry.config(width=200)
        self.passentry.place(x=210, y=50, anchor="nw", width=200, height=40)
        
        self.createButton.config(command=self.createButtonPressed)
        self.createButton.config(text="Create User")
        self.createButton.place(x=5, y=95, anchor="nw", width=80,
                             height=30)
        
        self.statuslabel.config(text="", height=65, width=215)
        self.statuslabel.place(x=5, y=130, anchor="nw", width=290, height=65)
    
    def createButtonPressed(self):
        if self.nameentry.get() == "[Empty]":
            print "You're THAT kind of person."
            return 'break'
        if crypto.create_profile(self.nameentry.get(), self.passentry.get()):
            self.master.updateList()
            self.destroy()
        else:
            self.nameentry.delete(0, "end")
            self.passentry.delete(0, "end")
            self.statuslabel.config(text="Username already exists.")

    def quit(self):
        self.master.noNewUser()
        self.destroy()

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.maxsize(420, 200)
        self.minsize(420, 200)
        self.title("New User")
        self.namelabel = tk.Label(self)
        self.passlabel = tk.Label(self)
        self.statuslabel = tk.Label(self)
        self.nameentry = tk.Entry(self)
        self.passentry = tk.Entry(self)
        self.master = master
        self.createButton = tk.Button(self)
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.createWidgets()