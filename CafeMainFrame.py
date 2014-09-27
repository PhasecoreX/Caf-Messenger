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
		containerFrame.config(width = 800, height = 630)
		containerFrame.place(x = 0, y = 0, anchor = "nw")
		
		
		#Create the menubar
		menubar = tk.Menu(self)
		
		#Add a cascade list called filemenu
		filemenu = tk.Menu(menubar, tearoff = 0)
		filemenu.add_command(label = "Print")
		filemenu.add_command(label = "Quit", command = self.quit)
		
		#Add a cascade list called editmenu
		editmenu = tk.Menu(menubar, tearoff = 0)
		editmenu.add_command(label = "Copy")
		editmenu.add_command(label = "Paste")
		editmenu.add_command(label = "Select All")
		
		#Add a cascade list called viewmenu
		viewmenu = tk.Menu(menubar, tearoff = 0)
		viewmenu.add_command(label = "View RSA Key Chain")
		viewmenu.add_command(label = "View Current Chat's Public Key")
		
		#Add a cascade list called helpmenu
		helpmenu = tk.Menu(menubar, tearoff = 0)
		helpmenu.add_command(label = "About Cafe")
		helpmenu.add_command(label = "About Encryption")
		helpmenu.add_command(label = "About Distributed Systems")
		
		#Add all the cascade menus to the main menubar
		menubar.add_cascade(label = "File", menu = filemenu)
		menubar.add_cascade(label = "Edit", menu = editmenu)
		menubar.add_cascade(label = "View", menu = viewmenu)
		menubar.add_cascade(label = "Help", menu = helpmenu)
		
		#Display the menu
		self.config(menu = menubar)
		
		#Create and place the Chat Panel
		chat = ChatPanel(containerFrame, self)
		chat.config(width = 590, height = 590)
		chat.place(x = 5, y = 5, anchor = "nw")
		
		#Create and place the Friends List
		friends = FriendsPanel(containerFrame, self)
		friends.config(width = 190, height = 590)
		friends.place(x = 605, y = 5, anchor = "nw")
		
	
	#Main constructor
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.title("Cafe")
		self.maxsize(800,630)
		self.minsize(800,630)
		
		self.createPanels()
	

class FriendsPanel(tk.Frame):
	def createWidgets(self, controller):
		self.fheader.config(text = "_ClientName_'s Friendlist")
		self.fheader.config(width = 185, height = 20)
		self.fheader.place(x = 0, y = 0, anchor = "nw", width = 185, height = 20)
		
		self.flist.config(width = 185, height = 505)
		self.flist.place(x = 0, y = 25, anchor = "nw", width = 185, height = 505)
		
		self.friendEntry.config(width = 90, height = 20)
		self.friendEntry.place(x = 0, y = 535, anchor = "nw", width = 90, height = 20)
		
		self.addButton.config(text = "Add Friend", width = 90, height = 20)
		self.addButton.config(command = self.addButtonPress)
		self.addButton.place(x = 95, y = 535, anchor = "nw", width = 90, height = 20)
		
		self.chatButton.config(text = "Chat", width = 90, height = 20)
		self.chatButton.config(command = self.chatButtonPress)
		self.chatButton.place(x = 0, y = 560, anchor = "nw", width = 90, height = 20)
		
		self.removeButton.config(text = "Remove", width = 90, height = 20)
		self.removeButton.config(command = self.removeButtonPress)
		self.removeButton.place(x = 95, y = 560, anchor = "nw", width = 90, height = 20)
		
		
	
	def addButtonPress(self):
		print "Such Friend! Very wow."
		
		
		
		
		
		
	
	def chatButtonPress(self):
		print "So chatty, much talk."
		
		
		
		
		
		
	
	def removeButtonPress(self):
		print "How mean, no friend."
		
		
		
		
		
		
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.fheader = tk.Label(self)
		self.flist = tk.Listbox(self)
		self.addButton = tk.Button(self)
		self.removeButton = tk.Button(self)
		self.friendEntry = tk.Text(self)
		self.chatButton = tk.Button(self)
		self.createWidgets(controller)
	

class ChatPanel(tk.Frame):
	def createWidgets(self, controller):
		self.label.config(text = "Chat with _FriendName_:")
		self.label.config(width = 570, height = 20)
		self.label.place(x = 0, y = 0, anchor = "nw", width = 570, height = 20)
		
		self.textArea.config(width = 570,height = 495, state = "disabled")
		self.textArea.place(x = 0, y = 25, anchor = "nw", width = 570,height = 495)
		self.textArea.config(background = "lightgray", borderwidth = 2)
		
		self.sendButton["text"] = "Send"
		self.sendButton.config(command = self.buttonPress)
		self.sendButton.config(width = 40, height = 20)
		self.sendButton.place(x = 525, y = 535, anchor = "nw", width = 45, height = 40)
		
		self.textEntry.config(width = 525)
		self.textEntry.place(x = 0, y = 525, width = 515, height = 60)
		self.textEntry.bind("<KeyPress-Return>", self.enterKeyPress)
		#self.textEntry.bind("<KeyPress-Return>", self.enterKeyPress)
		self.textEntry.bind("<Shift-Return>", self.shiftEnterPress)
		#self.textArea.config(yscrollcommand = self.scrollbar.set)
		#self.scrollbar.config(command = self.textArea.yview)
		
	def shiftEnterPress(self, event):
		self.textEntry.insert("end", "\n")
		return 'break'
	
	def enterKeyRelease(self, event):
		self.textEntry.delete(1.0, "end")
	
	def enterKeyPress(self, event):
		t = self.textEntry.get(1.0, "end")
		if(t == "\n"):
			return 'break'
		self.buttonPress()
		return 'break'
		
	
	def buttonPress(self):
		self.textArea.config(state = "normal")
		self.textArea.insert("end", "Client: ")
		self.textArea.insert("end", self.textEntry.get(1.0, "end"))
		self.textArea.see("end")
		self.textArea.config(state = "disabled")
		self.textEntry.delete(1.0, "end")
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.label = tk.Label(self)
		self.textArea = tk.Text(self)
		self.sendButton = tk.Button(self)
		self.textEntry = tk.Text(self)
		#self.scrollbar = tk.Scrollbar(self)
		self.createWidgets(controller)
	
if __name__ == "__main__":
	top = MainFrame()
	top.mainloop()