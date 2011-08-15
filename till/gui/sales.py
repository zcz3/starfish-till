# -*- coding: utf-8 -*-
"""
The sales screen.
"""

from Tkinter import *
from Tix import *
from tkMessageBox import *


class Sales(Frame):
	
	def __init__(self, master, store):
		Frame.__init__(self, master)
		self.master = master
		self.store = store
		self.buffer = []
		self.create_widgets()
		self.connect_handlers()
	
	def create_widgets(self):
		self.rowconfigure(0, weight=2)
		self.rowconfigure(1, weight=3)
		self.columnconfigure(0, weight=11)
		self.columnconfigure(1, weight=2)
		
		grid_options = {'padx': 10, 'pady': 10, 'sticky': N+S+E+W}
		
		self.list_products = Listbox(self)
		self.list_products.grid(row=0, column=0, **grid_options)
		
		self.frame_info = Frame(self)
		self.frame_info.grid(row=0, column=1, **grid_options)
		self.frame_info.columnconfigure(0, weight=1)
		self.label_price = Label(self.frame_info, font=('Helvetica', '36'), pady=5, text='£0.00')
		self.label_price.grid(row=0, column=0)
		self.label_id = Label(self.frame_info, text='ID: ')
		self.label_id.grid(row=1, column=0)
		self.button_commit = Button(self.frame_info, bg='#a6f16c', font=('Helvetica', '18'), text='Commit')
		self.button_commit.grid(row=2, column=0, pady=10, sticky=N+S+E+W)
		self.frame_info.rowconfigure(2, weight=3)
		self.button_cancel = Button(self.frame_info, bg='#ff7373', text='Cancel')
		self.button_cancel.grid(row=3, column=0, pady=5, sticky=N+S+E+W)
		self.frame_info.rowconfigure(3, weight=1)
		
		self.frame_catalogue = Frame(self)
		self.frame_catalogue.grid(row=1, column=0, **grid_options)
		
		self.frame_keypad = Frame(self)
		self.frame_keypad.grid(row=1, column=1, **grid_options)
		for i in range(4):
			self.frame_keypad.rowconfigure(i, weight=1)
		for i in range(4):
			self.frame_keypad.columnconfigure(i, weight=1)
		keypad_options = {'padx': 5, 'pady': 5, 'sticky': N+S+E+W}
		self.key_multiply = Button(self.frame_keypad, text='X')
		self.key_multiply.grid(row=0, column=2, **keypad_options)
		self.key_minus = Button(self.frame_keypad, text='-')
		self.key_minus.grid(row=0, column=0, **keypad_options)
		self.key_plus = Button(self.frame_keypad, text='+')
		self.key_plus.grid(row=0, column=1, **keypad_options)
		self.key_percent = Button(self.frame_keypad, text='%')
		self.key_percent.grid(row=0, column=3, **keypad_options)
		self.key_enter = Button(self.frame_keypad, text='E\nN\nT')
		self.key_enter.grid(row=2, column=3, rowspan=2, **keypad_options)
		self.key_7 = Button(self.frame_keypad, text='7')
		self.key_7.grid(row=1, column=0, **keypad_options)
		self.key_8 = Button(self.frame_keypad, text='8')
		self.key_8.grid(row=1, column=1, **keypad_options)
		self.key_9 = Button(self.frame_keypad, text='9')
		self.key_9.grid(row=1, column=2, **keypad_options)
		self.key_4 = Button(self.frame_keypad, text='4')
		self.key_4.grid(row=2, column=0, **keypad_options)
		self.key_5 = Button(self.frame_keypad, text='5')
		self.key_5.grid(row=2, column=1, **keypad_options)
		self.key_6 = Button(self.frame_keypad, text='6')
		self.key_6.grid(row=2, column=2, **keypad_options)
		self.key_1 = Button(self.frame_keypad, text='1')
		self.key_1.grid(row=3, column=0, **keypad_options)
		self.key_2 = Button(self.frame_keypad, text='2')
		self.key_2.grid(row=3, column=1, **keypad_options)
		self.key_3 = Button(self.frame_keypad, text='3')
		self.key_3.grid(row=3, column=2, **keypad_options)
		self.key_0 = Button(self.frame_keypad, text='0')
		self.key_0.grid(row=1, column=3, **keypad_options)
	
	def connect_handlers(self):
		self.bind_all('<KeyRelease>', self.input)
	
	def input(self, event):
		"""
		Handle keyboard input (this could also be from the barcode
		scanner). Stores in a buffer, and when the enter key is pressed,
		checks the buffer for matching products, vouchers and
		transactions.
		"""
		if event.keysym == 'Return':
			if len(self.buffer) == 0:
				return
			pass
			self.buffer = []
		elif event.char.isalpha() or event.char.isdigit():
			self.buffer.append(event.char)

