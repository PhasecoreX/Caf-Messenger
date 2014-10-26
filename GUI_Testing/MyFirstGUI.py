import Tkinter as tk
from MyFirstGUI_Child import ChildWindow


class Application(tk.Frame):

    def helloWorld(self):
        print "Hello World!"

    def spawnWindow(self, source):
        t = ChildWindow(self, source, self.winCount)
        self.childlist.append(t)
        self.winCount = self.winCount + 1

    def spawnButtonPressed(self):
        self.spawnWindow("Root Window")

    def sendButtonPressed(self):
        s1 = self.numText.get(1.0, "end")
        s2 = self.messageText.get(1.0, "end")
        try:
            self.childlist[int(s1)].changeMessage(s2)
        except IndexError:
            print "No such child exists! (Or had existed)"
        except:
            t = ChildWindow(self, "Root Window", int(s1))
            self.childlist[int(s1)] = t
            self.childlist[int(s1)].changeMessage(s2)
        self.numText.delete(1.0, "end")
        self.messageText.delete(1.0, "end")

    def createWidgets(self):

        self.headerLabel.config(text="Damn kids!", width=390, height=40)
        self.headerLabel.place(x=5, y=5, anchor="nw", width=390,
                               height=40)

        self.quitButton.config(text="QUIT", fg="red", command=self.quit,
                               width=60, height=40)
        self.quitButton.place(x=5, y=50, anchor="nw", width=60, height=40)

        self.helloButton.config(text="Hello!", command=self.helloWorld,
                                width=60, height=40)
        self.helloButton.place(x=70, y=50, anchor="nw", width=60, height=40)

        self.spawnButton.config(text="Spawn", command=self.spawnButtonPressed,
                                width=60, height=40)
        self.spawnButton.place(x=135, y=50, anchor="nw", width=60, height=40)

        self.numLabel.config(text="Num:", width=20, height=40)
        self.numLabel.place(x=5, y=95, anchor="nw", width=20, height=40)

        self.numText.config(width=100, height=60)
        self.numText.place(x=30, y=95, anchor="nw", width=100, height=60)

        self.messageLabel.config(text="Msg:", width=20, height=40)
        self.messageLabel.place(x=135, y=95, anchor="nw", width=20, height=40)

        self.messageText.config(width=100, height=60)
        self.messageText.place(x=160, y=95, anchor="nw", width=100, height=60)

        self.sendButton.config(text="Send", command=self.sendButtonPressed,
                               width=60, height=40)
        self.sendButton.place(x=265, y=95, anchor="nw", width=60, height=40)

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.childlist = list()
        self.winCount = 0
        self.headerLabel = tk.Label(self)
        self.quitButton = tk.Button(self)
        self.helloButton = tk.Button(self)
        self.spawnButton = tk.Button(self)
        self.sendButton = tk.Button(self)
        self.numLabel = tk.Label(self)
        self.numText = tk.Text(self)
        self.messageLabel = tk.Label(self)
        self.messageText = tk.Text(self)
        self.createWidgets()

# Define that top is a TK GUI interface.
top = tk.Tk()
top.title("Parent >:[")
top.maxsize(400, 400)
top.minsize(400, 400)

# Add a frame to the interface, give it something to show.
top.app = Application(top)

top.app.place(x=0, y=0, anchor="nw", width=400, height=400)

# Run the frame, actually show something to the user.
top.mainloop()

# Destroy the window
# top.destroy()
