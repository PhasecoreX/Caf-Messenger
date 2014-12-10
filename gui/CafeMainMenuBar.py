# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   CIS 467 Capstone Project - Cafe Messenger
#   CafeNewUserFrame.py
#   Author: Michael Currie
#
#   This program is the main menu bar for the chat window interface. This was
#   created to fix the monolithic code issue with ChatMainFrame.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import Tkinter as tk


class MainMenu(tk.Menu):

    """
    """

    def create_widgets(self):
        """
        """
        # Add a cascade list called filemenu
        self.filemenu.add_command(label="Quit", command=self.parent.quit)

        # Add a cascade list called viewmenu
        self.viewmenu.add_command(label="View my Public Key")

        # Add a cascade list called helpmenu
        self.helpmenu.add_command(label="About Encryption")
        self.helpmenu.add_command(label="About Distributed Systems")
        self.helpmenu.add_command(label="About Cafe")

        # Add all the cascade menus to the main menubar
        self.add_cascade(label="File", menu=self.filemenu)
        self.add_cascade(label="View", menu=self.viewmenu)
        self.add_cascade(label="Help", menu=self.helpmenu)

    def __init__(self, parent):
        """
        """
        tk.Menu.__init__(self, parent)
        self.parent = parent
        self.filemenu = tk.Menu(self, tearoff=0)
        self.viewmenu = tk.Menu(self, tearoff=0)
        self.helpmenu = tk.Menu(self, tearoff=0)
        self.create_widgets()
