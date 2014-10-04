from Tkinter import *

class Application(Frame):
	def helloWorld(self):
		print "Hello World!"
	
	def createWidgets(self):
		
		self.headerLabel = Label(self, text = "My first frame!").grid(row=0)
		
		self.quitButton = Button(self, text = "QUIT", fg = "red", command = self.quit).grid(row = 1, column = 1)
		
		self.helloButton = Button(self, text = "Hello!", command = self.helloWorld).grid(row = 1, column = 0)
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

#Define that top is a TK GUI interface.
top = Tk()
top.title("My First GUI!")
top.maxsize(400,400)
top.minsize(400,400)

#Add a frame to the interface, give it something to show.
app = Application(master = top)

#Run the frame, actually show something to the user.
app.mainloop()

#Destroy the window
#top.destroy()