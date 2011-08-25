"""
Template class for any sections that comprise of a search box, list
and editor.
"""

from Tkinter import *
from ttk import *


class ListTemplate(Frame):
	"""
	This class is designed to be subclassed by any class which needs to
	implement a section that includes a list of items that can be edited.
	
	Classes implemeting this need to provide the following methods:
	
	item_list(filter) - 	returns a tuple of tuples in the form of
				(name, id). 'filter' is a search string that may 
				be blank.
	properties(id) - 	populate the propeties frame for the item with
				the provided id.
	properties_new() - 	populate the properties frame for a new item.
	item_delete(id) - 	remove the specified item from the database.
	
	To force the update of the list (e.g. after a new
	items has been saved) call the 'update_list' method.
	"""
	
	def __init__(self, master):
		Frame.__init__(self, master)
		self.items = []
		self.current_item_id = None
		self.create_widgets()
		self.connect_handlers()
		self.properties_hide()
	
	def create_widgets(self):
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		self.pane = PanedWindow(self, orient=VERTICAL)
		self.pane.grid(row=0, column=0, sticky=N+S+E+W)
		
		self.frame_list = Frame(self.pane, relief=SUNKEN)
		self.pane.add(self.frame_list)
		self.frame_list.rowconfigure(0, weight=1)
		self.frame_list.columnconfigure(0, weight=1)
		self.frame_toolbar = Frame(self.frame_list)
		self.frame_toolbar.grid(row=0, column=0, sticky=W)
		self.input_search = Entry(self.frame_toolbar)
		self.input_search.grid(row=0, column=0)
		self.button_search = Button(self.frame_toolbar, text='Search', command=self.update_list)
		self.button_search.grid(row=0, column=1)
		self.button_new = Button(self.frame_toolbar, text='New', command=self.new)
		self.button_new.grid(row=0, column=2)
		self.button_delete = Button(self.frame_toolbar, command=self.delete, text='Delete')
		self.button_delete.grid(row=0, column=3)
		self.list = Listbox(self.frame_list)
		self.list.grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)
		
		self.frame_properties = Frame(self.pane, relief=SUNKEN)
		self.pane.add(self.frame_properties)
		
		self.frame_container = Frame(self.frame_properties)
		self.frame_container.grid(row=0, column=0, padx=10, pady=10, sticky=N+S+E+W)
	
	def connect_handlers(self):
		self.input_search.bind('<KeyRelease>', self.update_list)
		self.list.bind('<ButtonRelease-1>', self.update_properties)
		self.list.bind('<KeyRelease>', self.update_properties)
	
	def update_list(self, event=None):
		search = self.input_search.get()
		self.list.delete(0, self.list.size()-1)
		self.items = self.item_list(search)
		for item in self.items:
			self.list.insert(END, item[0])
	
	def update_properties(self, event):
		selection = self.list.curselection()
		if selection:
			if event.keysym == 'Delete':
				self.delete()
			else:
				self.properties_show()
				item_id = self.items[int(selection[0])][1]
			
				if item_id != self.current_item_id:
					self.current_item_id = item_id
					self.properties(item_id)
		else:
			self.properties_hide()
	
	def new(self, event=None):
		self.list.selection_clear(0, self.list.size()-1)
		self.properties_show()
		self.properties_new()
	
	def delete(self, event=None):
		"""Deletes the selected item."""
		selection = self.list.curselection()
		if selection:
			item_id = self.items[int(selection[0])][1]
			if item_id == self.current_item_id:
				self.properties_hide()
			self.item_delete(item_id)
	
	def properties_hide(self):
		"""Hides the properties frame."""
		self.frame_container.grid_remove()
	
	def properties_show(self):
		"""Shows the properties frame."""
		self.frame_container.grid()

