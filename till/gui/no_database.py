"""
These dialog boxes are displayed by the 'till.db' module when it cannot connect
to the database or the database had not been installed.
"""

from Tkinter import *


class DatabasePrompt(Frame):
	"""
	Asks the user weather he or she wishes to install the database, open
	the configuration editor or exit.
	"""
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.response = 'exit'
		self.master.title('Starfish Till')
		self.create_widgets()
		self.connect_handlers()
		self.grid(padx=10, pady=10)
	
	def create_widgets(self):
		top = self.winfo_toplevel()
		top.geometry('+300+200')
		self.label_info = Label(self, text='No database has been detected.\nWould you like to create a new one?')
		self.label_info.grid(row=0, column=0, columnspan=3, ipady=20)
		self.button_yes = Button(self, text='Yes')
		self.button_yes.grid(row=1, column=0)
		self.button_config = Button(self, text='Open configuration editor')
		self.button_config.grid(row=1, column=1)
		self.button_exit = Button(self, text='Exit')
		self.button_exit.grid(row=1, column=2)
	
	def connect_handlers(self):
		self.button_yes.bind('<ButtonRelease-1>', self.r_yes)
		self.button_config.bind('<ButtonRelease-1>', self.r_config)
		self.button_exit.bind('<ButtonRelease-1>', self.r_exit)
	
	def r_yes(self, args=None):
		self.response = 'yes'
		self.quit()
	
	def r_config(self, args=None):
		self.response = 'config'
		self.quit()
	
	def r_exit(self, args=None):
		self.response = 'exit'
		self.quit()

