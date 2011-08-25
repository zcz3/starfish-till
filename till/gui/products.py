"""
The products editor.
"""

from Tkinter import *

from till.tables.products import Product


class Products(Frame):
	
	def __init__(self, master, store):
		Frame.__init__(self, master)
		self.store = store
		self.create_widgets()
		self.connect_handlers()
		self.load_list()
	
	def display(self):
		self.grid(row=0, column=0, padx=10, pady=10, sticky=N+S+E+W)
	
	def hide(self):
		self.grid_forget()
	
	def create_widgets(self):
		self.frame_list = Frame(self)
		self.frame_list.grid(row=0, column=0, sticky=N+S+E+W)
		self.label_search = Label(self.frame_list, text='Search:')
		self.label_search.grid(row=0)
		self.input_search = Entry(self.frame_list)
		self.input_search.grid(row=1)
		self.list_products = Listbox(self.frame_list)
		self.list_products.grid(row=2, sticky=N+S+E+W)
		
		self.frame_product = Frame(self)
		self.frame_product.grid(row=0, column=1, sticky=N)
		self.frame_toolbar = Frame(self.frame_product)
		self.frame_toolbar.grid(row=0, column=0, columnspan=2)
		self.button_save = Button(self.frame_toolbar, text='Save')
		self.button_save.grid(row=0, column=0)
		self.button_delete = Button(self.frame_toolbar, text='Delete')
		self.button_delete.grid(row=0, column=1)
		self.button_new = Button(self.frame_toolbar, text='New')
		self.button_new.grid(row=0, column=2)
		
		grid_options = {'sticky': W}
		
		self.label_name = Label(self.frame_product, text='Name')
		self.label_name.grid(row=1, column=0, **grid_options)
		self.input_name = Entry(self.frame_product)
		self.input_name.grid(row=1, column=1, **grid_options)
		
		self.label_barcode = Label(self.frame_product, text='Barcode')
		self.label_barcode.grid(row=2, column=0, **grid_options)
		self.input_barcode = Entry(self.frame_product)
		self.input_barcode.grid(row=2, column=1, **grid_options)
		
		self.label_price = Label(self.frame_product, text='Price')
		self.label_price.grid(row=3, column=0, **grid_options)
		self.input_price = Entry(self.frame_product)
		self.input_price.grid(row=3, column=1, **grid_options)
	
	def connect_handlers(self):
		self.input_search.bind('<KeyRelease>', self.load_list)
	
	def load_list(self, event=None):
		"""Reload the list of products."""
		self.list_products.delete(0, self.list_products.size()-1)
		search = self.input_search.get()
		if search:
			sql = "SELECT * FROM products WHERE name LIKE '%{0}%' OR barcode LIKE '%{0}%';".format(search)
		else:
			sql = "SELECT * FROM products;"
		result = self.store.execute(sql)
		products = [r.name for r in result]
		if products:
			self.list_products.insert(END, *products)

