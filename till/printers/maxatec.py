"""
Maxatec MT-150
"""

import time

from till.printers import PrinterBase
from till.lib import serial

INIT = ('\x1b\x3d\x01'		# Enable the printer
	+ '\x1b\x25\x00'	# Cancels user-defined character set
	+ '\x1b\x21\x00'	# Reset printer mode
	+ '\x1b\x32'		# Default line spacing
	+ '\x1b\x52\x03'	# Select UK character set
)

PART_CUT = '\x1b\x64\x05\x1d\x56\x01'
FULL_CUT = PART_CUT	# Not available
PULSE = ('\x10\x14\x01\x00\x01'		# pin 2
	+ '\x10\x14\x01\x01\x01')	# pin 5
UNDERLINE_ON = '\x1b\x2d\x02'
UNDERLINE_OFF = '\x1b\x2d\x00'
DOUBLE_H_ON = '\x1d\x21\x01'
DOUBLE_W_ON = '\x1d\x21\x10'
DOUBLE_HW_ON = '\x1d\x21\x11'
DOUBLE_OFF = '\x1d\x21\x00'
ALIGN_C = '\x1b\x61\x01'
ALIGN_R = '\x1b\x61\x02'
ALIGN_L = '\x1b\x61\x00'

# Approximate width of the paper in characters.
WIDTH = 42


class BadBarcodeString(Exception):
	pass


class BadBarcodeType(Exception):
	pass


class MaxatecPrinter(PrinterBase):
	
	def __init__(self, location):
		PrinterBase.__init__(self, location)
		self.out = serial.Serial(
			port=location,
			baudrate=9600,
			bytesize=serial.EIGHTBITS,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			xonxoff=True
		)
		self.out.write(INIT)
	
	def write(self, data):
		"""
		Sends data to the printer at the correct rate. This prevents a
		buffer overflow when large amounts of data are send to
		self.out.write() in a short space of time.
		"""
		for c in data:
			self.out.write(c)
			time.sleep(0.001)
			
	
	def text(self, string, style=''):
		"""
		Print a line of text. Automatically inserts a new line.
		'style' should be a string with a combination of any of the
		following characters:
		
		u - underline
		h - double height
		w - double width
		c - center align
		r - right align
		"""
		if 'u' in style:
			self.write(UNDERLINE_ON)
		if 'h' in style and 'w' in style:
			self.write(DOUBLE_HW_ON)
		elif 'h' in style:
			self.write(DOUBLE_H_ON)
		elif 'w' in style:
			self.write(DOUBLE_W_ON)
		if 'c' in style:
			self.write(ALIGN_C)
		elif 'r' in style:
			self.write(ALIGN_R)
		self.write(string + '\r\n')
		self.write(UNDERLINE_OFF)
		self.write(DOUBLE_OFF)
		self.write(ALIGN_L)
	
	def price(self, string, price, style=''):
		"""
		Prints a price right aligned and a description left aligned on
		the same line.
		"""
		# Double width messes up the alignment.
		if style.find('w') >= 0:
			p = style.find('w')
			style = style[:p] + style[p+1:]
		if len(string) > 31:
			string = string[:31]
		self.text('{0: <31} \x23{1: >9.2f}'.format(string, price), style)
	
	def full_cut(self):
		"""Cut the paper fully."""
		self.write(FULL_CUT)
	
	def part_cut(self):
		"""Partially cuts the paper."""
		self.write(PART_CUT)
	
	def open_draw(self):
		self.write(PULSE)
	
	def barcode(self, code, ctype, position='l', print_code=True):
		"""
		Prints a barcode. 'code' is the code to print, and 'ctype' is
		the type of barcode, which should be one of the following:
		
		upca
		upce
		ean8
		ean13
		code39
		code93
		code128
		itf
		codabar
		
		'position' should be a single character specifying the barcode
		alignment - 'l' (left), 'c' (center) or 'r' (right).
		
		If 'print_code' is True, then 'code' is printed below the
		barcode.
		
		BadBarcodeString is raised if the code does not contain the
		right number of characters for the barcode type selected.
		"""
		l = len(code)
		if ctype[:3] == 'ucp':
			if l < 11 or l > 12:
				raise BadBarcodeString()
		elif ctype == 'ean13':
			if l < 12 or l > 13:
				raise BadBarcodeString()
		elif ctype == 'ean8':
			if l < 7 or l > 8:
				raise BadBarcodeString()
		elif ctype == 'code39' or ctype == 'code93' or ctype == 'codabar':
			if l < 1 or l > 255:
				 raise BadBarcodeString()
		elif ctype == 'code128':
			if l < 2 or l > 255:
				raise BadBarcodeString()
		elif ctype == 'itf':
			if l < 1 or l > 255 or (l % 2) != 0:
				raise BadBarcodeString()
		
		type_codes = (
			('upca', '\x41'),
			('upce', '\x42'),
			('ean8', '\x44'),
			('ean13', '\x43'),
			('code39', '\x45'),
			('code93', '\x48'),
			('code128', '\x49'),
			('itf', '\x46'),
			('codabar', '\x47'),
		)
		m = None
		for name, char in type_codes:
			if ctype == name:
				m = char
		if not m:
			raise BadBarcodeType()
		
		if 'c' in position:
			self.write(ALIGN_C)
		elif 'r' in postition:
			self.out.write(ALIGN_R)
		self.write('\x1d\x68\x32')
		self.write('\x1d\x6b' + m + chr(l) + code)
		if print_code:
			self.text(code, position)
		self.write('\n')
		if 'c' in position or 'r' in position:
			self.write(ALIGN_L)
	
	def line(self):
		"""Prints a horizontal line."""
		self.write('-' * WIDTH)

