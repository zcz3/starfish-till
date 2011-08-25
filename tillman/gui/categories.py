"""
Allows editing of the product categories.
"""

from Tkinter import *
from ttk import *
from tkMessageBox import *

from till.tables import categories

from tillman.gui.list_template import ListTemplate


class Categories(ListTemplate):
	
	def __init__(self, master, store):
		ListTemplate.__init__(self, master)
		self.store = store
		self.update_list()
		self.create_properties_widgets()
	
	def create_properties_widgets(self):
		grid_options = {'padx': 10, 'pady': 10, 'sticky': W}
		
		self.label_name = Label(self.frame_container, text='Name')
		self.label_name.grid(row=0, column=0, **grid_options)
		self.var_name = StringVar()
		self.input_name = Entry(self.frame_container, textvariable=self.var_name)
		self.input_name.grid(row=0, column=1, **grid_options)
		
		self.button_save = Button(self.frame_container, command=self.save, text='Save')
		self.button_save.grid(row=1, column=0, **grid_options)
		self.button_cancel = Button(self.frame_container, command=self.cancel, text='Cancel')
		self.button_cancel.grid(row=1, column=1, **grid_options)
	
	def item_list(self, search=''):
		if search:
			sql = "SELECT * FROM categories WHERE name LIKE '%{0}%' ORDER BY name ASC;".format(search)
		else:
			sql = "SELECT * FROM categories ORDER BY name ASC;"
		result = self.store.execute(sql)
		items = [(r[1], r[0]) for r in result]
		return items
	
	def properties(self, id):
		result = self.store.get(categories.Category, id)
		if result:
			self.var_name.set(result.name)
			self.current_category = result
	
	def properties_new(self):
		self.current_category = categories.Category()
		self.var_name.set('')
	
	def item_delete(self, id):
		sql = "DELETE FROM categories WHERE id = %s;"
		self.store.execute(sql, (id,))
		self.update_list()
	
	def save(self, event=None):
		name = unicode(self.var_name.get())
		if len(name) < 1:
			showerror('Starfish Till Manager', 'The name cannot be blank.')
		else:
			self.current_category.name = name
			if not self.current_category.id:
				self.store.add(self.current_category)
			self.store.commit()
			self.update_list()
			self.properties(self.current_category.id)
	
	def cancel(self, event=None):
		self.var_name.set(self.current_category.name)

