# -*- coding: utf-8 -*-
"""
The sales screen.
"""

from Tkinter import *
#from ttk import *
from tkMessageBox import *
from decimal import Decimal as D

from till import transaction
from till.tables.products import Product


class Sales(Frame):
	
	def __init__(self, master, store, user):
		Frame.__init__(self, master)
		self.master = master
		self.store = store
		self.user = user
		self.buffer = []
		self.index = []
		self.create_widgets()
		self.new_transaction()
		self.connect_handlers()
	
	def run(self):
		"""Enter the mainloop."""
		self.grid(padx=20, pady=20, sticky=N+S+E+W)
		
		top = self.winfo_toplevel()
		swidth = self.winfo_screenwidth()
		sheight = self.winfo_screenheight()
		top.geometry('%dx%d' % (swidth, sheight))
		
		self.listen()
		self.mainloop()
		return True
	
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
		self.input_buffer = Label(self.frame_keypad, anchor=W, relief=SUNKEN)
		self.input_buffer.grid(row=4, column=0, columnspan=3, sticky=E+W)
		self.button_clear = Button(self.frame_keypad, text='Clr')
		self.button_clear.grid(row=4, column=3)
	
	def connect_handlers(self):
		self.button_clear.bind('<ButtonRelease-1>', self.clear_buffer)
		self.button_commit.bind('<ButtonRelease-1>', self.commit)
		self.button_cancel.bind('<ButtonRelease-1>', self.cancel)
		
		self.key_enter.bind('<ButtonRelease-1>', lambda e: key.event_generate('<Return>'))
		keys = (
			self.key_0,
			self.key_1,
			self.key_2,
			self.key_3,
			self.key_4,
			self.key_5,
			self.key_6,
			self.key_7,
			self.key_8,
			self.key_9,
			#self.key_multiply,
			#self.key_minus,
			#self.key_plus,
			#self.key_percent,
		)
		for key in keys:
			key.bind('<ButtonRelease-1>', lambda e: key.event_generate('<KeyRelease-%s>' % e.widget['text']))
		self.key_minus.bind('<ButtonRelease-1>', lambda e: self.key_minus.event_generate('<KeyRelease-KP_Subtract>'))
		self.key_plus.bind('<ButtonRelease-1>', lambda e: self.key_plus.event_generate('<KeyRelease-KP_Add>'))
		self.key_multiply.bind('<ButtonRelease-1>', lambda e: self.key_multiply.event_generate('<KeyRelease-KP_Multiply>'))
		self.key_percent.bind('<ButtonRelease-1>', lambda e: self.key_percent.event_generate('<percent>'))
	
	def listen(self):
		"""
		Start listening for keyboard input on all widgets. Must be
		disabled with 'self.listen_off()' when displaying another
		window or changing screens.
		"""
		self.bind_all('<KeyRelease>', self.input)
		self.bind_all('<Return>', self.input)
	
	def listen_off(self):
		"""Stop listening for keyboard input."""
		self.unbind_all('<KeyRelease>')
		self.unbind_all('<Return>')
	
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
			string = unicode(''.join(self.buffer))
			# Search for a product.
			result = self.store.find(Product, Product.barcode == string).one()
			if result:
				p = self.transaction.add(result, 1)
				self.update_list()
				self.list_products.selection_set(self.index.index(p))
				self.bell()
			else:
				self.listen_off()
				showerror('Starfish Till', 'Product not found.')
				self.listen()
			self.clear_buffer()
		elif event.char.isalpha() or event.char.isdigit():
			self.buffer.append(event.char)
			self.input_buffer.configure(text=''.join(self.buffer))
		elif event.char == '-' or event.char == '+':
			if event.char == '-' and len(self.buffer) > 0:
				# Issue a discount.
				string = ''.join(self.buffer)
				if not string.isdigit():
					self.clear_buffer()
					return
				amount = D(string) / 100
				self.transaction.discount += amount
				self.transaction.discount = self.transaction.discount.quantize(D('0.01'))
				self.update_list()
			else:
				
				product = self.get_selected()
				if product == 'discount':
					if event.char == '-':
						# Remove the discount.
						self.transaction.discount = D(0)
						self.update_list()
				elif product:
					# Change selected product quantity.
					if event.char == '-':
						qty = -1
					else:
						qty = +1
					self.transaction.change(product, qty)
					self.update_list()
					if product in self.index:
						self.list_products.selection_set(self.index.index(product))
			
			self.clear_buffer()
		elif event.char == '*':
			# Set absolute quantity.
			string = ''.join(self.buffer)
			if string:
				if string.isdigit():
					product = self.get_selected()
					if product != 'discount' and product is not None:
						product.qty = int(string)
						if product.qty == 0:
							self.transaction.remove(product)
						self.update_list()
						if product.qty != 0:
							self.list_products.selection_set(self.index.index(product))
			self.clear_buffer()
		elif event.keysym == 'percent':
			# Issue a percentage discount.
			string = ''.join(self.buffer)
			if string:
				if string.isdigit():
					perc = int(string)
					amount = self.transaction.total() * D(perc) / 100
					self.transaction.discount += amount
					self.transaction.discount = self.transaction.discount.quantize(D('0.01'))
					self.update_list()
			self.clear_buffer()
		elif event.keysym == 'Escape':
			self.clear_buffer()
		elif event.keysym == 'BackSpace':
			del self.buffer[len(self.buffer)-1]
			self.input_buffer.configure(text=''.join(self.buffer))
	
	def clear_buffer(self, event=None):
		"""Clears the input buffer."""
		self.buffer = []
		self.input_buffer.configure(text='')
	
	def emit_key(self, event, key):
		"""Handles key presses from the keypad."""
		event = Event()
		event.char = None
		if key == 'Return':
			event.keysym = 'Return'
		else:
			event.keysym = 'KeyRelease'
			event.char = key
		self.input(event)
	
	def update_list(self):
		"""
		Updates the product list and total according to
		'self.transactions'.
		"""
		self.list_products.delete(0, self.list_products.size())
		self.index = []
		for p in self.transaction.products:
			description = '{0} - {1} @ {2} = {3}'.format(p.name, p.qty, p.price+p.vat, p.total())
			self.list_products.insert(END, description)
			self.index.append(p)
		if self.transaction.discount > 0:
			self.list_products.insert(END, 'Discount = {0}'.format(self.transaction.discount))
		self.label_price.configure(text='£{0:.2f}'.format(self.transaction.total()))
	
	def get_selected(self):
		"""
		Returns a 'till.transactions.Product' instance, a string
		equal to 'discount', or None, according to the selected item
		in the list.
		"""
		selected = self.list_products.curselection()
		if not selected:
			return None
		index = int(selected[0])
		if self.transaction.discount > 0:
			if index == self.list_products.size() - 1:
				return 'discount'
		return self.index[index]
	
	def commit(self, event=None):
		"""Save the sale."""
		if self.transaction.products:
			self.transaction.commit(self.store, self.user.id)
			self.new_transaction()
	
	def cancel(self, event=None):
		"""Cancel the sale."""
		self.transaction.products = []
		self.discount = D()
		self.update_list()
	
	def new_transaction(self):
		self.transaction = transaction.Transaction()
		self.label_price.configure(text='£0.00')
		self.label_id.configure(text='ID: '+self.transaction.id)
		self.update_list()

