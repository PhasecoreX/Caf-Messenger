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

from CafeFriendFrameS1 import FriendsPanel
from CafeChatFrameS1 import ChatPanel
import Tkinter as tk


class MainFrame(tk.Tk):
    """
    """

    def create_panels(self):
        """
        """

        self.container_frame.config(width=800, height=630)
        self.container_frame.place(x=0, y=0, anchor="nw")

        # Add a cascade list called filemenu
        self.filemenu.add_command(label="Print")
        self.filemenu.add_command(label="Quit", command=self.quit)

        # Add a cascade list called editmenu
        self.editmenu.add_command(label="Copy")
        self.editmenu.add_command(label="Paste")
        self.editmenu.add_command(label="Select All")

        # Add a cascade list called viewmenu
        self.viewmenu.add_command(label="View RSA Key Chain")
        self.viewmenu.add_command(label="View Current Chat's Public Key")

        # Add a cascade list called helpmenu
        self.helpmenu.add_command(label="About Cafe")
        self.helpmenu.add_command(label="About Encryption")
        self.helpmenu.add_command(label="About Distributed Systems")

        # Add all the cascade menus to the main menubar
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.menubar.add_cascade(label="View", menu=self.viewmenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        # Display the menu
        self.config(menu=self.menubar)

        # Create and place the Chat Panel
        self.chat.config(width=590, height=590)
        self.chat.place(x=5, y=5, anchor="nw")

        # Create and place the Friends List
        self.friends.config(width=190, height=590)
        self.friends.place(x=605, y=5, anchor="nw")

    def get_entry_text(self):
        return self.chat.get_entry_text()

    def append_message(self, name, message):
        """
        """
        self.chat.text_area_append(name, message)

    def change_chat_name(self, name):
        """
        """
        self.chat.change_chat_name(name)

    # Main constructor
    def __init__(self, *args, **kwargs):
        """
        """
        tk.Tk.__init__(self, *args, **kwargs)
        self.container_frame = tk.Frame(self)
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.viewmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.chat = ChatPanel(self)
        self.friends = FriendsPanel(self)

        self.title("Cafe")
        self.maxsize(800, 630)
        self.minsize(800, 630)

        self.create_panels()





if __name__ == "__main__":
    top = MainFrame()
    top.mainloop()
