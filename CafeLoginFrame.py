# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#	CIS 467 Capstone Project - Cafe Messenger
#	CafeLoginFrame.py
#	Author: Michael Currie
#
#	This program is the GUI Frame for the Login portion of the GUI. This frame
#	will be the first one ran of the entire GUI program set, and it will
#	communicate with the Encryption portion of the project. It will have a drop
#	down menu of the different users and will request a password. It will lead
#	to either CafeNewUserFrame or CafeFriendFrame.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import Tkinter as tk


class MainFrame(tk.Tk):

    def CreatePanels(self, parent, controller):
        self.login = LoginPanel(self, self)
        self.login.config(width=600, height=400)
        self.login.place(x=0, y=0, anchor="nw")

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.login = LoginPanel(self, self)
        self.title("Cafe Login")
        self.maxsize(600, 400)
        self.minsize(600, 400)
        self.CreatePanels(self, self)


class LoginPanel(tk.Frame):

    def CreateWidgets(self, parent, controller):
        message = "Please select your username and enter your password.\n"
        message = message + "If you are a new user, please click 'New User'"
        self.mainLabel.config(text=message)
        self.mainLabel.place(x=15, y=15, anchor="nw", width=350, height=30)

        self.nameMenu.config(width=205, height=30)
        self.nameMenu.place(x=120, y=60, anchor="nw", width=205, height=30)
        self.PopulateNameMenu()

        self.passEntry.config(width=205)
        self.passEntry.place(x=120, y=105, anchor="nw", width=205, height=30)

        self.nameLabel.config(width=80, height=30, text="Name:")
        self.nameLabel.place(x=15, y=60, anchor="nw", width=80, height=30)

        self.passLabel.config(width=80, height=30, text="Password:")
        self.passLabel.place(x=15, y=105, anchor="nw", width=80, height=30)

        self.errLabel.config(width=290, height=30, text="")
        self.errLabel.place(x=15, y=150, anchor="nw", width=290, height=60)

        self.loginButton.config(width=100, height=30, text="Login")
        self.loginButton.config(command=self.LoginButtonPress)
        self.loginButton.place(x=200, y=195, anchor="nw", width=100, height=30)

        self.newusrButton.config(width=100, height=30, text="New User")
        self.newusrButton.config(command=self.NewUserButtonPress)
        self.newusrButton.place(x=45, y=195, anchor="nw", width=100, height=30)

    def LoginError(self):
        errLabel.config(text="Invalid Username or Password.")

    def PopulateNameMenu(self):
        # Obviously incomplete, combine work with Public Key storage for login.
        nameList = ["Mark", "Mike", "Ryan", "Christian"]
        return nameList

    def LoginButtonPress(self):
        print "lol login"

    def NewUserButtonPress(self):
        print "omg hai new usr"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.names = self.PopulateNameMenu()
        self.var = tk.StringVar(self)
        self.var.set(self.names[0])
        self.nameMenu = apply(
            tk.OptionMenu, (self, self.var) + tuple(self.names))

        self.mainLabel = tk.Label(self)
        self.passEntry = tk.Entry(self)
        self.nameLabel = tk.Label(self)
        self.passLabel = tk.Label(self)
        self.errLabel = tk.Label(self)
        self.loginButton = tk.Button(self)
        self.newusrButton = tk.Button(self)
        self.CreateWidgets(self, controller)


if __name__ == "__main__":
    top = MainFrame()
    top.mainloop()