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
		self.master.withdraw()
		result = db.load()
		if result == 'connecterror':
			response = askyesno('Starfish Till', 'Cannot connect to the database.\nDo you want to open the confiuration editor?', parent=None)
			if response:
				self.config_editor()
			sys.exit(0)
		elif result == 'nodberror':
			dialog = no_database.DatabasePrompt()
			dialog.mainloop()
			response = dialog.response
			if response == 'yes':
				if db.install():
					self.__init__()
			elif response == 'config':
				self.config_editor()
			sys.exit(0)
		self.database, self.store = result
		self.master.deiconify()
		self.base = base.Base(self.master)
		self.login()
	
	def config_editor(self):
		"""Displays the configuration editor."""
		self.master.deiconify()
		w = config_editor.ConfigEditor(self.master)
		w.mainloop()
	
	def login(self):
		"""Displays the login window."""
		frame = login.Login(self.base.frame_main, self.store)
		self.base.attach_frame(frame, None)
		self.base.mainloop()
	
	

