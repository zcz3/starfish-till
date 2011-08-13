"""
The main window. The contents of the window is created by other classses.
"""

from Tkinter import *


class Base(Frame):
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.title = 'Starfish Till'
		self.master.title(self.title)
		self.frame_class = None
		self.create_widgets()
		self.grid(sticky=N+S+E+W)
	
	def create_widgets(self):
		top = self.winfo_toplevel()
		top.geometry('640x480')
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=1)
		self.label_title = Label(self, text='Starfish Till', font=(24,), background='white')
		self.label_title.grid(row=0, column=0, sticky=E+W)
		self.frame_main = Frame(self)
		self.frame_main.grid(row=1, column=0, sticky=N+S+E+W)
		self.frame_main.rowconfigure(0, weight=1)
		self.frame_main.columnconfigure(0, weight=1)
	
	def attach_frame(self, frame_class, sticky=N+S+E+W):
		"""
		Places 'frame_class' on the main area of the window. If one is already attached,
		it is hidden. The frame class must already have 'Base.frame_main' as its
		parent widget.
		"""
		frame_class.grid(row=0, column=0, sticky=sticky)
		

