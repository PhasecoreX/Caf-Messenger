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

import Tkinter as tk

class MainFrame(tk.Tk):
	def createPanels(self):
		containerFrame = tk.Frame(self)
		containerFrame.pack(side = "top", fill = "both", expand = True)
		containerFrame.grid_rowconfigure(0, weight = 1)
		containerFrame.grid_columnconfigure(0, weight = 1)
		
		friends = FriendsPanel(containerFrame, self)
		friends.grid(row = 0, column = 2, columnspan = 1)
		
		chat = ChatPanel(containerFrame, self)
		chat.grid(row = 0, column = 0, columnspan = 2)
		
	
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.title("Cafe")
		self.maxsize(800,600)
		self.minsize(800,600)
		
		self.createPanels()
	
	
	

class FriendsPanel(tk.Frame):
	def createWidgets(self, controller):
		self.label = tk.Label(self, text = "Test!").grid(row = 0, column = 0)
		
		
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.createWidgets(controller)
		
	
	
	
	
	

class ChatPanel(tk.Frame):
	def createWidgets(self, controller):
		self.label["text"] = "Test!"
		self.label.grid(row = 0, column = 0)
		self.textArea.grid(row = 1, column = 0, rowspan = 3, columnspan = 3)
		
		self.sendButton["text"] = "Send"
		self.sendButton.grid(row = 4, column = 2)
		
		self.textEntry.grid(row = 4, column = 0, columnspan = 2)
		
		self.textArea.config(yscrollcommand = self.scrollbar.set)
		self.scrollbar.config(command = self.textArea.yview)
		self.scrollbar.grid(row = 1, rowspan = 3, column = 4)
		self.sendButton.config(command = lambda: self.buttonPress())
		
	
	def buttonPress(self):
		self.textArea.insert("end", "Client: ")
		self.textArea.insert("end", self.textEntry.get())
		self.textArea.insert("end", "\n")
		self.textEntry.delete(0, "end")
		
		
		
		
		
		
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.label = tk.Label(self)
		self.textArea = tk.Text(self)
		self.sendButton = tk.Button(self)
		self.textEntry = tk.Entry(self)
		self.scrollbar = tk.Scrollbar(self)
		self.createWidgets(controller)
		
	

	
	
	
	

if __name__ == "__main__":
	top = MainFrame()
	top.mainloop()