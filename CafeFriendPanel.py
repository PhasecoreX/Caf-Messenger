import Tkinter as tk

class FriendPanel(tk.Frame):

    def create_widgets(self):
        """
        """
        self.fheader.config(text="My Friendlist")
        self.fheader.config(width=185, height=20)
        self.fheader.place(x=0, y=0, anchor="nw", width=185, height=20)

        self.flist.config(width=185, height=505)
        self.flist.place(x=0, y=25, anchor="nw", width=185, height=505)

        self.friendentry.config(width=90, height=20)
        self.friendentry.place(x=0, y=535, anchor="nw", width=90,
                               height=20)
        self.friendentry.bind("<Return>", self.enter_key_pressed)

        self.addbutton.config(text="Add Friend", width=90, height=20)
        self.addbutton.config(command=self.add_button_pressed)
        self.addbutton.place(x=95, y=535, anchor="nw", width=90,
                             height=20)

        self.chatbutton.config(text="Chat", width=90, height=20)
        self.chatbutton.config(command=self.chat_button_pressed)
        self.chatbutton.place(x=0, y=560, anchor="nw", width=90,
                              height=20)

        self.removebutton.config(text="Remove", width=90, height=20)
        self.removebutton.config(command=self.remove_button_pressed)
        self.removebutton.place(x=95, y=560, anchor="nw", width=90,
                                height=20)

    def enter_key_pressed(self):
        return 'break'

    def add_button_pressed(self):
        """
        """
        print "Such Friend! Wow."
        name = self.friendentry.get(1.0, "end")
        name = name[:-1]
        self.flist.insert("end", name)
        self.friendentry.delete(1.0, "end")

    def chat_button_pressed(self):
        """
        """
        self.parent.chat(self.flist.get("anchor"))

    def remove_button_pressed(self):
        """
        """
        self.flist.delete("anchor")
        print "How mean, such enemy."

    def __init__(self, parent):
        """
        """
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.fheader = tk.Label(self)
        self.flist = tk.Listbox(self)
        self.addbutton = tk.Button(self)
        self.removebutton = tk.Button(self)
        self.friendentry = tk.Text(self)
        self.chatbutton = tk.Button(self)
        self.create_widgets()