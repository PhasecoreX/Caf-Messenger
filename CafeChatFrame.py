# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#	CIS 467 Capstone Project - Cafe Messenger
#	CafeChatFrame.py
#	Author: Michael Currie
#	
#	This program is the main GUI frame for the chat functionality of Cafe. This
#	frame will be communicating with the Cryptography and Networking portions
#	of the project, using Symmetric encryption and a peer-to-peer connection.
#	
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import Tkinter as tk

class MainFrame(tk.Tk):
	def CreatePanels(self, parent, controller):
		self.chat = ChatPanel(self, self)
		self.chat.config(width = 600, height = 600)
		self.chat.place(x = 5, y = 5, anchor = "nw")
		
	
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.login = ChatPanel(self, self)
		self.title("Cafe Login")
		self.maxsize(600, 600)
		self.minsize(600, 600)
		self.CreatePanels(self, self)
		
	

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
		self.sendButton.place(x = 525, y = 535, anchor = "nw")
		self.sendButton.place(width = 45, height = 40)
		
		self.textEntry.config(width = 525)
		self.textEntry.place(x = 0, y = 525, width = 515, height = 60)
		self.textEntry.bind("<KeyPress-Return>", self.enterKeyPress)
		self.textEntry.bind("<Shift-Return>", self.shiftEnterPress)
		
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
		self.createWidgets(controller)
		

if __name__ == "__main__":
	top = MainFrame()
	top.mainloop()
