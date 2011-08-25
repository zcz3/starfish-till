"""
Allows editing of the products.
"""

from Tkinter import *
from ttk import *
from tkMessageBox import *
from decimal import Decimal as D

from till.tables import products
from till.tables import categories
from till.tables import vat

from tillman.gui.list_template import ListTemplate


class Products(ListTemplate):
	
	def __init__(self, master, store):
		ListTemplate.__init__(self, master)
		self.store = store
		self.update_list()
		self.create_properties_widgets()
		self.connect_properties_handlers()
	
	def create_properties_widgets(self):
		grid_options = {'padx': 10, 'pady': 10, 'sticky': W}
		
		self.label_barcode = Label(self.frame_container, text='Barcode')
		self.label_barcode.grid(row=0, column=0, **grid_options)
		self.var_barcode = StringVar()
		self.input_barcode = Entry(self.frame_container, textvariable=self.var_barcode)
		self.input_barcode.grid(row=0, column=1, **grid_options)
		
		self.label_name = Label(self.frame_container, text='Name')
		self.label_name.grid(row=1, column=0, **grid_options)
		self.var_name = StringVar()
		self.input_name = Entry(self.frame_container, textvariable=self.var_name)
		self.input_name.grid(row=1, column=1, **grid_options)
		
		self.label_price = Label(self.frame_container, text='Price (excluding VAT)')
		self.label_price.grid(row=2, column=0, **grid_options)
		self.var_price = StringVar()
		self.input_price = Entry(self.frame_container, textvariable=self.var_price)
		self.input_price.grid(row=2, column=1, **grid_options)
		
		self.label_vat = Label(self.frame_container, text='VAT')
		self.label_vat.grid(row=3, column=0, **grid_options)
		self.var_vat = StringVar()
		self.input_vat = Entry(self.frame_container, state=DISABLED, textvariable=self.var_vat)
		self.input_vat.grid(row=3, column=1, **grid_options)
		
		self.label_vatcat = Label(self.frame_container, text='VAT category')
		self.label_vatcat.grid(row=4, column=0, **grid_options)
		self.vatcats = self.get_vat_cats()
		names = [v.name for v in self.vatcats]
		self.var_vatcat = StringVar()
		if len(names) > 0:
			self.var_vatcat.set(names[0])
		self.input_vatcat = OptionMenu(self.frame_container, self.var_vatcat, *names)
		self.input_vatcat.grid(row=4, column=1, **grid_options)
		
		self.label_cat = Label(self.frame_container, text='Category')
		self.label_cat.grid(row=5, column=0, **grid_options)
		self.cats = self.get_cats()
		names = [c.name for c in self.cats]
		self.var_cat = StringVar()
		if len(names) > 0:
			self.var_cat.set(names[0])
		self.input_cat = OptionMenu(self.frame_container, self.var_cat, *names)
		self.input_cat.grid(row=5, column=1, **grid_options)
		
		self.label_stock = Label(self.frame_container, text='Stock')
		self.label_stock.grid(row=6, column=0, **grid_options)
		self.var_stock = IntVar()
		self.input_stock = Entry(self.frame_container, textvariable=self.var_stock)
		self.input_stock.grid(row=6, column=1, **grid_options)
		
		self.label_stock_warn = Label(self.frame_container, text='Stock warning level')
		self.label_stock_warn.grid(row=7, column=0, **grid_options)
		self.var_stock_warn = IntVar()
		self.input_stock_warn = Entry(self.frame_container, textvariable=self.var_stock_warn)
		self.input_stock_warn.grid(row=7, column=1, **grid_options)
		self.label_stock_warn_note = Label(self.frame_container, text='Set to 0 to disable this feature.')
		self.label_stock_warn_note.grid(row=8, column=1, **grid_options)
		
		self.button_save = Button(self.frame_container, command=self.save, text='Save')
		self.button_save.grid(row=9, column=0, **grid_options)
		self.button_cancel = Button(self.frame_container, command=self.cancel, text='Cancel')
		self.button_cancel.grid(row=9, column=1, **grid_options)
	
	def item_list(self, search=''):
		if search:
			sql = "SELECT id, name, barcode FROM products WHERE barcode LIKE '%{0}%' OR name LIKE '%{0}%' ORDER BY name ASC;".format(search)
		else:
			sql = "SELECT id, name, barcode FROM products ORDER BY name ASC;"
		result = self.store.execute(sql)
		items = [('{0} ({1})'.format(r[1], r[2]), r[0]) for r in result]
		return items
	
	def connect_properties_handlers(self):
		self.input_price.bind('<KeyRelease>', self.update_vat)
		self.input_vatcat.bind('<Button-1>', self.update_vat)
	
	def get_vat_cats(self):
		"""Returns an iterable of vat objects."""
		return tuple(self.store.find(vat.Vat))
	
	def get_cats(self):
		"""Returns an iterable of categories."""
		return tuple(self.store.find(categories.Category))
	
	def properties(self, id):
		result = self.store.get(products.Product, id)
		if result:
			self.var_barcode.set(result.barcode)
			self.var_name.set(result.name)
			self.var_price.set(result.price)
			if result.vat_o:
				self.var_vatcat.set(result.vat_o.name)
			self.var_vat.set(result.vat)
			if result.vat_o:
				self.var_cat.set(result.category_o.name)
			self.var_stock.set(result.stock)
			self.var_stock_warn.set(result.stock_warning_level)
			self.current_product = result
	
	def properties_new(self):
		self.current_product = products.Product()
		self.var_barcode.set('')
		self.var_name.set('')
		self.var_price.set(0)
		if self.vatcats:
			self.var_vatcat.set(self.vatcats[0].name)
		self.var_vat.set(0)
		if self.cats:
			self.var_cat.set(self.cats[0].name)
		self.var_stock.set(0)
		self.var_stock_warn.set(0)
	
	def item_delete(self, id):
		sql = "DELETE FROM products WHERE id = %s;"
		self.store.execute(sql, (id,))
		self.update_list()
	
	def save(self, event=None):
		barcode = unicode(self.var_barcode.get().strip())
		name = unicode(self.var_name.get().strip())
		price = self.var_price.get().strip()
		vat_o = None
		for vatcat in self.vatcats:
			if vatcat.name == unicode(self.var_vatcat.get()):
				vat_o = vatcat
		vat = self.var_vat.get().strip()
		category_o = None
		for category in self.cats:
			if category.name == unicode(self.var_cat.get()):
				category_o = category
		stock = self.var_stock.get()
		stock_warning_level = self.var_stock_warn.get()
		error = ''
		if len(name) < 1:
			error += 'The name cannot be blank.\n'
		if not self.check_price(price):
			error += 'The price contains invalid characters.\n'
		if not vat_o:
			error += 'You must select a VAT category\n'
		if not self.check_price(vat):
			error += 'The VAT contains invalid characters.\n'
		if stock < 0:
			error += 'The stock cannot be negative.\n'
		if stock_warning_level < 0:
			error += 'The stock warning level cannot be negative.\n'
		if error:
			showerror('Starfish Till Manager', error)
		else:
			price = D(price).quantize(D('0.01'))
			vatrate = vat_o.rate
			vat = price * vatrate / 100
			vat = vat.quantize(D('0.01'))
			self.current_product.barcode = barcode
			self.current_product.name = name
			self.current_product.price = D(price)
			self.current_product.vat_o = vat_o
			self.current_product.vat = vat
			if category_o:
				self.current_product.category_o = category_o
			self.current_product.stock = stock
			self.current_product.stock_warning_level = stock_warning_level
			self.current_product.available = 1
			if not self.current_product.id:
				self.store.add(self.current_product)
			self.store.commit()
			self.update_list()
			self.properties(self.current_product.id)
	
	def cancel(self, event=None):
		self.var_barcode.set(self.current_product.barcode)
		self.var_name.set(self.current_product.name)
		self.var_price.set(self.current_product.price)
		self.var_vatcat.set(self.current_product.category_o.name)
		self.var_vat.set(self.current_product.vat)
		if self.current_product.category_o:
			self.var_cat.set(self.current_product.category_o.name)
		else:
			self.var_cat.set('')
		self.var_stock.set(self.current_product.stock)
		self.var_stock_warn.set(self.current_product.stock_warning_level)
	
	def update_vat(self, event=None):
		price = self.var_price.get().strip()
		if self.check_price(price):
			price = D(price)
			vat_o = None
			for vatcat in self.vatcats:
				if vatcat.name == self.var_vatcat.get():
					vat_o = vatcat
			if vat_o:
				rate = vat_o.rate
				vat = price * rate / 100
				vat = vat.quantize(D('0.01'))
				self.var_vat.set(vat)
	
	def check_price(self, price):
		"""
		Checks the string 'price' to see if it only contains digits and
		possibly a decimal point. Returns True or False.
		"""
		parts = price.partition('.')
		if parts[0]:
			if not parts[0].isdigit() and parts[0] != '.':
				return False
		if parts[1]:
			if parts[1] != '.':
				return False
		if parts[2]:
			if not parts[2].isdigit():
				return False
		return True

