"""
The main entry point of the program. Controls the GUI by loading various
classes into the 'till.gui.base.Base' class when requested.
"""

import sys
import Tkinter
from tkMessageBox import *

from till import config
from till import db
from till.gui import *

class Driver:
	
	def __init__(self):
		config.load()
		self.master = Tkinter.Tk()
		self.master.geometry('+10+10')
		result = db.load()
		if result[0] == 'connecterror':
			self.master.withdraw()
			response = askyesno('Starfish Till', 'Cannot connect to the database.\nDo you want to open the confiuration editor?', parent=None)
			self.master.deiconify()
			if response:
				self.config_editor() 
			sys.exit(0)
		elif result[0] == 'nodberror':
			dialog = no_database.DatabasePrompt(self.master)
			dialog.mainloop()
			dialog.destroy()
			response = dialog.response
			if response == 'yes':
				result = db.install(result[1], result[2])
				if result[0] == 'success':
					self.__init__()
				else:
                                        showerror('Starfish Till', 'Could not install the database.\n%s' % result[1])
			elif response == 'config':
				self.config_editor()
			sys.exit(0)
		self.database, self.store = result[1:]
		self.base = base.Base(self.master)
		self.user = None
		self.role = 0
		self.login()
	
	def config_editor(self):
		"""Displays the configuration editor."""
		w = config_editor.ConfigEditor(self.master)
		w.mainloop()
	
	def login(self):
		"""Displays the login screen."""
		frame = login.Login(self.base.frame_main, self.store)
		self.base.attach_frame(frame, None)
		self.base.mainloop()
		if frame.response == 'exit':
			sys.exit(0)
		elif frame.response == 'login':
			self.user = frame.user
			self.role = frame.role
		frame.destroy()
		self.sales()
	
	def sales(self):
		"""Displays the sales screen."""
		frame = sales.Sales(self.base.frame_main, self.store)
		self.base.attach_frame(frame, Tkinter.N+Tkinter.S+Tkinter.E+Tkinter.W)
		self.base.mainloop()

