import Tkinter as tk

class ChatPanel(tk.Toplevel):
    """
    """
    def create_widgets(self, parent):
        """
        """

        self.textarea.config(width=570, height=495, state="disabled")
        self.textarea.place(x=0, y=25, anchor="nw", width=570,
                            height=495)
        self.textarea.config(background="lightgray", borderwidth=2)

        self.sendbutton["text"] = "Send"
        self.sendbutton.config(command=self.send_button_pressed)
        self.sendbutton.config(width=40, height=20)
        self.sendbutton.place(x=525, y=535, anchor="nw", width=45,
                              height=40)

        self.textentry.config(width=525)
        self.textentry.place(x=0, y=525, width=515, height=60)
        self.textentry.bind("<KeyPress-Return>", self.enter_key_pressed)
        self.textentry.bind("<Shift-Return>", self.shift_enter_pressed)

    def shift_enter_pressed(self, event):
        """
        """
        self.textentry.insert("end", "\n")
        return 'break'

    def text_area_append(self, message):
        """
        """
        self.textarea.config(state="normal")
        self.textarea.insert("end", self.name + ": " + message + "\n")
        self.textarea.config(state="disabled")

    def enter_key_released(self, event):
        """
        """
        self.textentry.delete(1.0, "end")

    def enter_key_pressed(self, event):
        """
        """
        t = self.textentry.get(1.0, "end")
        if t == "\n":
            return 'break'
        self.send_button_pressed()
        return 'break'

    def send_button_pressed(self):
        """This method is called when the send button is pressed.
        
        This will send the message to the panel's parent, who has
        its own callback method to send to the controller.
        
        """
        message = self.textentry.get(1.0, "end")
        self.parent.send(message, self.chatID)
        self.textarea.config(state="normal")
        self.textarea.insert("end", "Client: ")
        self.textarea.insert("end", self.textentry.get(1.0, "end"))
        self.textarea.see("end")
        self.textarea.config(state="disabled")
        self.textentry.delete(1.0, "end")

    def __init__(self, parent, name, num):
        """
        """
        tk.Toplevel.__init__(self, parent)
        self.maxsize(600, 600)
        self.minsize(600, 600)
        self.title("Chat with " + name)
        self.name = name
        self.chatID = num
        self.parent = parent
        self.textarea = tk.Text(self)
        self.sendbutton = tk.Button(self)
        self.textentry = tk.Text(self)
        self.create_widgets(parent)
