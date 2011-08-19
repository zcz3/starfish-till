"""
Class storing data for a single transaction.
"""

from decimal import Decimal as D
import datetime

from till.tables import *
from till import config
from till.printers import maxatec


class Product:
	"""Stores information about a single product in the sale."""
	
	def __init__(self, id, name, price, vat, qty=1, barcode=''):
		"""
		'price' and 'vat' should be decimal values to a maximum of two
		decimal places. 'price' is excluding VAT.
		"""
		self.id = id
		self.name = name
		self.price = D(price)
		self.vat = D(vat)
		self.qty = qty
		self.barcode = barcode
	
	def total(self):
		"""
		Return the total cost to the buyer (price plus VAT all times the
		quantity).
		"""
		return (self.price + self.vat) * self.qty
	
	def total_vat(self):
		"""Return the total VAT."""
		return self.vat * self.qty


class Transaction:
	"""Stores information about a single transaction."""
	
	def __init__(self):
		self.id = '{0:0>3}-{1:0>6}'.format(config.get('tillid'), config.get('nextid'))
		config.set('nextid', int(config.get('nextid'))+1)
		self.products = []
		self.discount = D('0.00')
	
	def add(self, product, qty=1):
		"""
		Add a product to the transaction. 'product' should be the storm
		model. 'qty' can be a positive or negative value and can be used
		to alter the quantity of an existing product (by adding 'qty' to
		the existing quantity).
		"""
		for p in self.products:
			if p.id == product.id:
				self.change(p, qty)
				return p
		if qty <= 0:
			return
		p = Product(product.id, product.name, product.price, product.vat, qty, product.barcode)
		self.products.append(p)
		return p
	
	def change(self, product, qty=1):
		"""
		Allows modification of an existing product. 'product' should
		be a 'till.transactions.Product' instance already in the
		transaction. 'qty' is the change in quantity.
		"""
		product.qty += qty
		if product.qty <= 0:
			self.products.remove(product)
	
	def remove(self, product):
		"""
		Remove 'product' from the transaction.
		"""
		if product in self.products:
			self.products.remove(product)
	
	def total(self):
		"""The total, including VAT."""
		total = D()
		for p in self.products:
			total += p.total()
		return total - self.discount
	
	def total_vat(self):
		"""The total VAT."""
		total = D()
		for p in self.products:
			total += p.total_vat()
		return total - self.split_discount()[1]
	
	def split_discount(self):
		"""
		Split the discount proportionately between value and VAT.
		Returns a tuple in the form (value, vat).
		"""
		sale_value = D()
		sale_vat = D()
		for p in self.products:
			sale_value += p.qty * p.price
			sale_vat += p.qty * p.vat
		value = self.discount * sale_value / (sale_value + sale_vat)
		value.quantize(D('0.01'))
		vat = self.discount - value
		return value, vat
	
	def commit(self, store, user_id):
		"""Save the transaction."""
		date = datetime.datetime.today()
		
		sale = Sale()
		sale.receipt_number = unicode(self.id)
		sale.total = self.total() - self.total_vat()
		sale.vat = self.total_vat()
		sale.date = date
		sale.user_id = user_id
		sale.payment_method = 1
		sale.cash_paid = self.total()
		store.add(sale)
		
		for p in self.products:
			line = SaleItem()
			line.sale_o = sale
			line.product_id = p.id
			line.name = unicode(p.name)
			line.barcode = unicode(p.barcode)
			line.price_each = p.price
			line.vat_each = p.vat
			line.quantity = p.qty
			line.total_price = p.total() - p.total_vat()
			line.total_vat = p.total_vat()
			line.is_discount = False
			store.add(line)
		
		store.flush()
		#self.print_receipt(date)
	
	def print_receipt(self, date):
		printer = maxatec.MaxatecPrinter(config.get('printer'))
		printer.text('Starfish Books', 'hwc')
		printer.text('sales@starfishbooks.co.uk', 'c')
		printer.text('\n')
		printer.text('Receipt ID: ' + self.id)
		printer.text('Date: ' + date.ctime())
		printer.text('\n')
		printer.line()
		for p in self.products:
			if p.qty > 1:
				printer.text('{0: <31}'.format(p.name))
				printer.price('    {0} @ {1}'.format(p.qty, p.price), p.total())
			else:
				printer.price(p.name, p.total())
		printer.line()
		if self.discount:
			printer.price('Subtotal', self.total() + self.discount)
			printer.price('Discount', -self.discount)
		printer.price('Total', self.total(), 'h')
		printer.price('VAT', self.total_vat())
		printer.text('\n')
		printer.text('Thank you.', 'c')
		printer.barcode(self.id, 'code39')
		printer.part_cut()
		printer.open_draw()
	
	

