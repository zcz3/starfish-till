
from till import config
from till.gui import db_connect

from gui import base

def main():
	"""The entry point for the program."""
	config.load()
	result = False
	while result == False:
		result = db_connect.connect()
	database, store = result
	window = base.Base(store)
	window.run()

