import Tkinter as tk

class ChildWindow(tk.Toplevel):
    def createWidgets(self):
        self.label.config(text="This is window " + str(self.num) +
                          "\nSpawned from " + str(self.parnum))
        self.label.config(width=300, height=40)
        self.label.place(x=5, y=5, anchor="nw", width=300,
                             height=40)
        
        self.closeButton.config(command=self.closeButtonPressed)
        self.closeButton.config(text="Close")
        self.closeButton.place(x=5, y=50, anchor="nw", width=80,
                             height=30)
        
        self.helloButton.config(command=self.helloButtonPressed)
        self.helloButton.config(text="Hello")
        self.helloButton.place(x=90, y=50, anchor="nw", width=80,
                             height=30)
        
        self.spawnButton.config(command=self.spawnButtonPressed)
        self.spawnButton.config(text="Spawn")
        self.spawnButton.place(x=175, y=50, anchor="nw", width=80, height=30)
        
        self.message.config(text="", height=290, width=215)
        self.message.place(x=5, y=85, anchor="nw", width=290, height=215)
    
    def changeMessage(self, message):
        self.message.config(text=message)
    
    def closeButtonPressed(self):
        self.destroy
    
    def helloButtonPressed(self):
        self.master.helloWorld()
        
    def spawnButtonPressed(self):
        self.master.spawnWindow(self.num)

    def __init__(self, master, parnum, num):
        tk.Toplevel.__init__(self, master)
        self.maxsize(300, 300)
        self.minsize(300, 300)
        self.title("Child :D")
        self.label = tk.Label(self)
        self.parnum = parnum
        self.num = num
        self.master = master
        self.message = tk.Label(self)
        self.closeButton = tk.Button(self)
        self.spawnButton = tk.Button(self)
        self.helloButton = tk.Button(self)
        self.createWidgets()