"""
The main window. The contents of the window is created by other classses.
"""

from Tkinter import *

from till import config
from till import gui


class Base(Frame):
	
	def __init__(self, master=None, store=None):
		Frame.__init__(self, master)
		self.store = store
		self.title = 'Starfish Till'
		self.master.title(self.title)
		self.frame_class = None
		self.create_widgets()
		self.grid(sticky=N+S+E+W)
		
		self.screen_login = gui.login.Login(self.frame_main, store)
		
		self.connect_handlers()
		
		self.current = None
		self.login()
		self.mainloop()
	
	def create_widgets(self):
		top = self.winfo_toplevel()
		top.geometry('640x480')
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)
		
		
		
		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=1)
		self.label_title = Label(self, text='Starfish Till (%s)' % config.get('tillname'), font=(24,), background='white')
		self.label_title.grid(row=0, column=0, sticky=E+W)
		self.frame_main = Frame(self)
		self.frame_main.grid(row=1, column=0, sticky=N+S+E+W)
		self.frame_main.rowconfigure(0, weight=1)
		self.frame_main.columnconfigure(0, weight=1)
	
	
	
	
	
	def login(self, event=None):
		if self.current:
			self.current.hide()
		self.screen_login.display()
		self.current = self.screen_login
	
	def sales(self, event=None):
		if self.current:
			self.current.hide()
		self.screen_sales.display(self.screen_login.user)
		self.current = self.screen_sales
	
	def products(self, event=None):
		if self.current:
			self.current.hide()
		self.screen_products.display()
		self.current = self.screen_products
	
		
	

