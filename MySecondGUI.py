# A quick little test to learn how to interchange multiple frames inside a parent frame.

import Tkinter as tk

class MainFrame(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.title("My Second GUI")
		self.maxsize(400,400)
		self.minsize(400,400)
		
		containerFrame = tk.Frame(self)
		containerFrame.pack(side="top", fill="both", expand=True)
		containerFrame.grid_rowconfigure(0, weight = 1)
		containerFrame.grid_columnconfigure(0, weight = 1)
		
		self.frames = {}
		
		for F in (CoverPage, PageOne, PageTwo, PageThree, FinalPage):
			frame = F(containerFrame, self)
			self.frames[F] = frame
			frame.grid(row=0,column=0,sticky="nsew")
		
		self.showFrame(CoverPage)
		
	def showFrame(self, c):
		frame = self.frames[c]
		frame.tkraise()
	

class CoverPage(tk.Frame):
	def createWidgets(self, controller):
		self.headerLabel = tk.Label(self, text = "Welcome to my test!").grid(row = 0, column = 0, columnspan = 2)
		self.nextButton = tk.Button(self, text = "Next", command = lambda: controller.showFrame(PageOne)).grid(row = 1, column = 1)
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#self.pack()
		self.createWidgets(controller)
	

class PageOne(tk.Frame):
	def createWidgets(self, controller):
		self.headerLabel = tk.Label(self, text = "Page One:").grid(row = 0, column = 0, columnspan = 2)
		self.backButton = tk.Button(self, text = "Back", command = lambda: controller.showFrame(CoverPage)).grid(row = 1, column = 0)
		self.nextButton = tk.Button(self, text = "Next", command = lambda: controller.showFrame(PageTwo)).grid(row = 1, column = 1)
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#self.pack()
		self.createWidgets(controller)
	

class PageTwo(tk.Frame):
	def createWidgets(self, controller):
		self.headerLabel = tk.Label(self, text = "Page Two:").grid(row = 0, column = 0, columnspan = 2)
		self.backButton = tk.Button(self, text = "Back", command = lambda: controller.showFrame(PageOne)).grid(row = 1, column = 0)
		self.nextButton = tk.Button(self, text = "Next", command = lambda: controller.showFrame(PageThree)).grid(row = 1, column = 1)
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#self.pack()
		self.createWidgets(controller)
	

class PageThree(tk.Frame):
	def createWidgets(self, controller):
		self.headerLabel = tk.Label(self, text = "Page Three:").grid(row = 0, column = 0, columnspan = 2)
		self.backButton = tk.Button(self, text = "Back", command = lambda: controller.showFrame(PageTwo)).grid(row = 1, column = 0)
		self.nextButton = tk.Button(self, text = "Next", command = lambda: controller.showFrame(FinalPage)).grid(row = 1, column = 1)
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#self.pack()
		self.createWidgets(controller)
		

class FinalPage(tk.Frame):
	def createWidgets(self, controller):
		self.headerLabel = tk.Label(self, text = "Thank you for reading!").grid(row = 0, column = 0, columnspan = 2)
		self.explainLabel = tk.Label(self, text = "Please press \"Quit\" to exit.").grid(row = 1, column = 0, columnspan = 2)
		self.backButton = tk.Button(self, text = "Back", command = lambda: controller.showFrame(PageThree)).grid(row = 2, column = 0)
		self.quitButton = tk.Button(self, text = "Quit", command = self.quit).grid(row = 2, column = 1)
	

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#self.pack()
		self.createWidgets(controller)
	



if __name__ == "__main__":
	top = MainFrame()
	top.mainloop()







