"""
The first screen to appear. Logs the user into a specific account.
"""

from Tkinter import *
from tkMessageBox import *
import md5

from till.db import store
from till.tables import User


class Login(Frame):
	
	def __init__(self, master):
		"""'master' must be the frame of the containing window. See the Base class."""
		Frame.__init__(self, master)
		self.title = 'Login - Starfish Till'
		self.create_widgets()
		self.connect_handlers()
		self.input_user.focus_set()
	
	def create_widgets(self):
		self.frame_login = LabelFrame(self, text='Login')
		self.frame_login.grid(row=0, column=0, ipadx=10, ipady=10)
		
		grid_options = {'padx': 10, 'pady': 2, 'sticky': W}
		
		self.label_user = Label(self.frame_login, text='Username')
		self.label_user.grid(row=0, column=0, **grid_options)
		self.input_user = Entry(self.frame_login)
		self.input_user.grid(row=0, column=1, **grid_options)
		self.label_password = Label(self.frame_login, text='Password')
		self.label_password.grid(row=1, column=0, **grid_options)
		self.input_password = Entry(self.frame_login, show='*')
		self.input_password.grid(row=1, column=1, **grid_options)
		self.button_login = Button(self.frame_login, text='Login')
		self.button_login.grid(row=2, column=1, **grid_options)
	
	def connect_handlers(self):
		self.button_login.bind('<ButtonRelease-1>', self.login)
		self.frame_login.bind('<KeyPress-KP_Enter>', self.login)
	
	def login(self, args=None):
		user = unicode(self.input_user.get())
		if not user:
			return
		password = self.input_password.get()
		password_hash = unicode(md5.new(password).hexdigest())
		result = store.find(User, User.name == user).one()
		if not result:
			showerror(self.title, 'User not found.')
			self.input_user.select_range(0, len(self.input_user.get()))
			return
		if password_hash != result.password:
			showerror(self.title, 'Incorrect password.')
			self.input_password.select_range(0, len(self.input_password.get()))
		
			

