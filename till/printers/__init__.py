"""
Classes for printing receipts to various makes of printer.
"""


class PrinterBase:
	"""Base class for printers."""
	
	def __init__(self, location):
		self.location = location
	
	def text(self, string, style=''):
		pass
	
	def price(self, string, price, style=''):
		pass
	
	def line(self):
		pass
	
	def full_cut(self):
		pass
	
	def part_cut(self):
		pass
	
	def open_draw(self):
		pass
	
	def barcode(self, code, ctype):
		pass

