"""
The main entry point of the program. Controls the GUI by loading various
classes into the 'till.gui.base.Base' class when requested.
"""

import sys

from till import config
from till.gui import *

class Driver:
	
	def __init__(self):
		config.load()
		result = False
		while not result:
			result = db_connect.connect()
		self.database, self.store = result
		self.user = self.login()
		if self.user:
			self.sales()
	
	def login(self):
		"""Displays the login screen."""
		frame = login.Login(None, self.store)
		self.top = frame.winfo_toplevel()
		frame.run()
		return frame.user
	
	def sales(self):
		"""Displays the sales screen."""
		frame = sales.Sales(self.top, self.store, self.user)
		frame.run()

