"""
Base window.
"""

from Tkinter import *
from ttk import *

import till

from tillman.gui import categories
from tillman.gui import products


class Base(Frame):
	
	items = (
		('Stock',
			(('Categories', categories.Categories),
			('Products', products.Products),
			'VAT categories',
			'Stock report',
			)),
		('Discounts',
			('Quantity discounts',
			'Vouchers',
			'Voucher usage report',
			)),
		('Transactions',
			('Sales',
			'Refunds',
			'Revenue report',
			'VAT report',
			)),
		('System',
			('User accounts',
			'Locations',
			'Tills',
			)),
	)
	
	def __init__(self, store):
		Frame.__init__(self)
		self.store = store
		self.current_section = None
		self.tree_index = {}
		self.create_widgets()
		self.connect_handlers()
	
	def run(self):
		"""Enter the main loop."""
		self.grid(row=0, column=0, sticky=N+S+E+W)
		
		top = self.winfo_toplevel()
		width = 800
		height = 600
		swidth = self.winfo_screenwidth()
		sheight = self.winfo_screenheight()
		dleft = (swidth - width) / 2
		dtop = (sheight - height) / 2
		top.geometry('%dx%d+%d+%d' % (width, height, dleft, dtop))
		
		self.mainloop()
	
	def create_widgets(self):
		top = self.winfo_toplevel()
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		top.title('Starfish Till Manager')
		
		self.panes = PanedWindow(self, orient=HORIZONTAL)
		self.panes.grid(row=0, column=0, sticky=N+S+E+W)
		
		self.tree = Treeview(self.panes, selectmode='browse', show='tree')
		for item in self.items:
			id = self.tree.insert('', 'end', text=item[0], open=True)
			for subitem in item[1]:
				if type(subitem) is type(tuple()):
					text = subitem[0]
					item_id = self.tree.insert(id, 'end', text=subitem[0])
					self.tree_index[item_id] = subitem[1]
				else:
					self.tree.insert(id, 'end', text=subitem)
		self.panes.add(self.tree)
		
		self.frame_main = Frame(self.panes)
		self.frame_main.rowconfigure(0, weight=1)
		self.frame_main.columnconfigure(0, weight=1)
		self.panes.add(self.frame_main)
	
	def connect_handlers(self):
		self.tree.bind('<<TreeviewSelect>>', self.change_section)
	
	def change_section(self, event):
		if self.current_section:
			self.current_section.destroy()
		item = self.tree.focus()
		if item:
			if item in self.tree_index.keys():
				frame_class = self.tree_index[item]
				frame = frame_class(self.frame_main, self.store)
				frame.grid(row=0, column=0, sticky=N+S+E+W)

