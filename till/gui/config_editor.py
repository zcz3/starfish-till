"""
Stand-alone window for editing the configuration file. Sould not be running
when any other part of the till is running.
This is opened by the driver when '-o' is passed as an argument.
"""

import sys
from Tkinter import *
from tkMessageBox import *

from till import config


DBTYPES = (
	('SQLite', 'sqlite'),
	('MySQL', 'mysql'),
	('PostgreSQL', 'postgres'),
)


class ConfigEditor(Frame):
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.title = 'Configuration editor - Starfish Till'
		self.master.title(self.title)
		self.create_widgets()
		self.populate()
		self.connect_handlers()
		self.grid(sticky=N+S+E+W)
	
	def create_widgets(self):
		top = self.winfo_toplevel()
		top.columnconfigure(0, weight=1)
		top.rowconfigure(0, weight=1)
		
		for i in range(4):
			self.columnconfigure(i, weight=1)
		for i in range(4):
			self.rowconfigure(i, weight=1)
		
		self.label_title = Label(self, text='Configuration editor',
			font=(24,),
			background='white')
		self.label_title.grid(row=0, column=0, columnspan=4, sticky=N+S+E+W)
		
		grid_options = {'padx': 10, 'pady': 2, 'sticky': W}
		
		
		# Databases
		self.frame_database = LabelFrame(self, text='Database')
		self.frame_database.columnconfigure(0, weight=1)
		self.frame_database.columnconfigure(1, weight=1)
		self.frame_database.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky=N+S+E+W)
		self.label_dbtype = Label(self.frame_database, text='Type')
		self.label_dbtype.grid(row=0, column=0, **grid_options)
		self.currentdb = StringVar()
		self.input_dbtype = OptionMenu(self.frame_database, self.currentdb, *[t[0] for t in DBTYPES])
		self.input_dbtype.grid(row=0, column=1, **grid_options)
		self.label_dbuser = Label(self.frame_database, text='Username')
		self.label_dbuser.grid(row=1, column=0, **grid_options)
		self.input_dbuser = Entry(self.frame_database)
		self.input_dbuser.grid(row=1, column=1, **grid_options)
		self.label_dbpass = Label(self.frame_database, text='Password')
		self.label_dbpass.grid(row=2, column=0, **grid_options)
		self.input_dbpass = Entry(self.frame_database, show='*')
		self.input_dbpass.grid(row=2, column=1, **grid_options)
		self.label_dbhost = Label(self.frame_database, text='Host')
		self.label_dbhost.grid(row=3, column=0, **grid_options)
		self.input_dbhost = Entry(self.frame_database)
		self.input_dbhost.grid(row=3, column=1, **grid_options)
		self.label_dbname = Label(self.frame_database, text='Database name')
		self.label_dbname.grid(row=4, column=0, **grid_options)
		self.input_dbname = Entry(self.frame_database)
		self.input_dbname.grid(row=4, column=1, **grid_options)
		self.button_testdb = Button(self.frame_database, text='Test connection')
		self.button_testdb.grid(row=5, column=1, padx=10, pady=2, sticky=E)
		
		# Till
		self.frame_till = LabelFrame(self, text='Till')
		self.frame_till.columnconfigure(0, weight=1)
		self.frame_till.columnconfigure(1, weight=1)
		self.frame_till.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky=N+S+E+W)
		self.label_id = Label(self.frame_till, text='ID')
		self.label_id.grid(row=0, column=0, **grid_options)
		self.input_id = Entry(self.frame_till)
		self.input_id.grid(row=0, column=1, **grid_options)
		self.label_name = Label(self.frame_till, text='Name')
		self.label_name.grid(row=1, column=0, **grid_options)
		self.input_name = Entry(self.frame_till)
		self.input_name.grid(row=1, column=1, **grid_options)
		
		# Action buttons
		self.button_cancel = Button(self, text='Cancel')
		self.button_cancel.grid(row=3, column=2, sticky=E+W)
		self.button_save = Button(self, text='Save')
		self.button_save.grid(row=3, column=3, sticky=E+W)
	
	def populate(self):
		"""Populates the widgets with the current configuration values."""
		for name, value in DBTYPES:
			if value == config.get('database'):
				self.currentdb.set(name)
		self.input_dbuser.insert(0, config.get('dbuser'))
		self.input_dbpass.insert(0, config.get('dbpass'))
		self.input_dbhost.insert(0, config.get('dbhost'))
		self.input_dbname.insert(0, config.get('dbname'))
		self.input_id.insert(0, config.get('tillid'))
		self.input_name.insert(0, config.get('tillname'))
	
	def connect_handlers(self):
		self.button_save.bind('<ButtonRelease-1>', self.save)
		self.button_save.bind('<KeyPress-KP_Enter>', self.save)
		self.button_cancel.bind('<ButtonRelease-1>', self.cancel)
		self.button_cancel.bind('<KeyPress-KP_Enter>', self.cancel)
	
	def save(self, args=None):
		dbtype = ''
		for name, value in DBTYPES:
			if name == self.currentdb.get():
				dbtype = value
		dbuser = self.input_dbuser.get()
		dbpass = self.input_dbpass.get()
		dbhost = self.input_dbhost.get()
		dbname = self.input_dbname.get()
		id = self.input_id.get()
		name = self.input_name.get()
		
		error_message = ''
		if not id:
			error_message += 'The till ID field cannot be blank.\n'
		if not name:
			error_message += 'The till name field cannot be blank.\n'
		if error_message:
			showerror(self.title, error_message)
			return
		
		config.set('database', dbtype)
		config.set('dbuser', dbuser)
		config.set('dbpass', dbpass)
		config.set('dbhost', dbhost)
		config.set('dbname', dbname)
		config.set('tillid', id)
		config.set('tillname', name)

		self.quit()
	
	def cancel(self, args=None):
		self.quit()

