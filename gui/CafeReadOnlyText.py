# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   CIS 467 Capstone Project - Cafe Messenger
#   CafeReadOnlyText.py
#   Author: Michael Currie
#
#   This program will allow the creation of a textbox that cannot be edited by
#   the user, but will be able to be copyable by the user, and only able to be
#   changed by the program.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import Tkinter as tk
from idlelib.WidgetRedirector import WidgetRedirector

class ReadOnlyText(tk.Text):

    """
    """

    def __init__(self, *args, **kwargs):
        """
        """
        tk.Text.__init__(self, *args, **kwargs)
        self.redirector = WidgetRedirector(self)
        self.insert = \
            self.redirector.register("insert", lambda *args, **kw: "break")
        self.delete = \
            self.redirector.register("delete", lambda *args, **kw: "break")