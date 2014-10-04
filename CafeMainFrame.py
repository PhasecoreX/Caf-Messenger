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
        """This method gets the text out of the entrytext widget of chat.
        
        Invokes the get_entry_text method of the ChatPanel 
        
        """
        return self.chat.get_entry_text()

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
        print "whoo!"

    def __init__(self, controller, factory, *args, **kwargs):
        """
        """
        tk.Tk.__init__(self, *args, **kwargs)
        self.factory = factory
        self.controller = controller
        self.container_frame = tk.Frame(self)
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.viewmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.chat = ChatPanel(self, factory)
        self.friends = FriendsPanel(self, factory)

        self.title("Cafe")
        self.maxsize(800, 630)
        self.minsize(800, 630)

        self.create_panels()

if __name__ == "__main__":
    top = MainFrame(None, None)
    top.mainloop()
