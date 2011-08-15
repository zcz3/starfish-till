"""
Model for the products table.
"""

import decimal

from till.lib.storm.locals import *
from till.tables.vat import *
from till.tables.categories import *


class NoVatCategory():
	pass


class Product(object):
	
	__storm_table__ = 'products'
	
	id = Int(primary=True)
	barcode = Unicode()
	name = Unicode()
	price = Decimal() # Excluding VAT
	vat_id = Int()
	vat = Decimal()
	category_id = Int()
	stock = Int()
	stock_warning_level = Int()
	available = Bool()
	image = RawStr()
	
	vat_o = Reference(vat_id, Vat.id)
	category_o = Reference(category_id, Category.id)
	
	def __init__(self):
		self.vat_id = None
	
	def set_vat(self):
		"""
		Set the VAT according to the VAT category. Should be called
		everytime before saving to the database.
		"""
		if not self.vat_id:
			raise NoVatCategory
		self.vat = decimal.Decimal(self.price * self.vat_o.rate / 100).quantize(decimal.Decimal('0.01'))

