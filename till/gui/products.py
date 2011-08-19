"""
The products editor.
"""

from Tkinter import *


class Products(Frame):
	
	def __init__(self, master, store):
		Frame.__init__(self, master)
		self.store = store
		self.display_widgets()
		self.connect_handlers()
	
	def display(self):
		self.grid(row=0, column=0, sticky=N+S+E+W)
	
	def hide(self):
		self.grid_forget()
	
	def display_widgets(self):
		self.label_temp = Label(self, text='Products')
		self.label_temp.grid(row=0, column=0)
	
	def connect_handlers(self):
		pass

