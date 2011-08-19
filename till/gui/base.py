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
		self.clear_screens()
		
		self.connect_handlers()
		self.event_generate('<<role-0>>')
		
		self.current = None
		self.login()
		self.mainloop()
	
	def create_widgets(self):
		top = self.winfo_toplevel()
		top.geometry('640x480')
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)
		
		self.menu = Menu(self)
		top['menu'] = self.menu
		self.menu_user = Menu(self.menu)
		self.menu.add_cascade(menu=self.menu_user, label='User')
		self.menu_user.add_command(label='Logout')
		self.menu_user.add_command(label='Change password')
		self.menu_user.add_command(label='Exit')
		self.menu_screen = Menu(self.menu)
		self.menu.add_cascade(menu=self.menu_screen, label='Screen')
		#self.menu_screen.add_checkbutton(label='Sales', command=self.sales)
		#self.menu_screen.add_checkbutton(label='Receipts')
		#self.menu_screen.add_checkbutton(label='Products', command=self.products)
		#self.menu_screen.add_checkbutton(label='Quantity discounts')
		#self.menu_screen.add_checkbutton(label='Users')
		#self.menu_screen.add_checkbutton(label='Export data')
		self.menu_config = Menu(self.menu)
		self.menu.add_cascade(menu=self.menu_config, label='Configuration')
		#self.menu_config.add_command(label='Configuration editor')
		#self.menu_config.add_command(label='Settings')
		self.menu_help = Menu(self.menu)
		self.menu.add_cascade(menu=self.menu_help, label='Help')
		self.menu_help.add_command(label='About')
		
		self.menu_screen_items = 0
		self.menu_config_items = 0
		
		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=1)
		self.label_title = Label(self, text='Starfish Till (%s)' % config.get('tillname'), font=(24,), background='white')
		self.label_title.grid(row=0, column=0, sticky=E+W)
		self.frame_main = Frame(self)
		self.frame_main.grid(row=1, column=0, sticky=N+S+E+W)
		self.frame_main.rowconfigure(0, weight=1)
		self.frame_main.columnconfigure(0, weight=1)
	
	def menu_role_0(self, event=None):
		"""Create the menu items available when no-one is loggen in."""
		print 'Hi'
		screen_items = []
		config_items = []
		self.menu_add(screen_items, config_items)
	
	def menu_role_1(self, event=None):
		"""Create the menu items available to an administrator."""
		screen_items = (
			('Sales', self.sales),
			('Products', self.products),
		)
		config_items = []
		self.menu_add(screen_items, config_items)
	
	def menu_role_2(self, event=None):
		"""Create the menu items available to a member of staff."""
		screen_items = (
			('Sales', self.sales),
		)
		config_items = []
		self.menu_add(screen_items, config_items)
	
	def menu_add(self, screen, config):
		"""
		Adds options to the screen and config menus, replacing all the
		existing items. 'screen' and 'config' should be iterables of
		tuples, each tuple containing the name of the option and the
		function to invoke.
		"""
		if self.menu_screen_items:
			self.menu_screen.delete(0, self.menu_screen_items-1)
		if self.menu_config_items:
			self.menu_config.delete(0, self.menu_config_items-1)
		self.menu_screen_items = self.menu_config_items = 0
		for name, command in screen:
			self.menu_screen.add_checkbutton(label=name, command=command)
			self.menu_screen_items += 1
		for name, command in config:
			self.menu_config.add_command(label=name, command=command)
			self.menu_config_items += 1
	
	def connect_handlers(self):
		self.bind_all('<<login>>', self.clear_screens)
		self.bind_all('<<login>>', self.sales)
		self.bind_all('<<role-0>>', self.menu_role_0)
		self.bind_all('<<role-1>>', self.menu_role_1)
		self.bind_all('<<role-2>>', self.menu_role_2)
	
	def clear_screens(self, event=None):
		"""
		Reconstructs the screens when a user logs in so that any
		information entered but not saved has gone.
		"""
		self.screen_sales = gui.sales.Sales(self.frame_main, self.store)
		self.screen_products = gui.products.Products(self.frame_main, self.store)
	
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
	
	def role_0(self, event=None):
		"""No-one is logged in."""
		
	

