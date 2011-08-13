"""
Connects to the database.
"""

import sys
import sqlite3

from till.lib.storm.locals import *
from till import config


def install(store):
	"""Installs the database."""
	pass

def load():
	"""
	Connects to the database. Returns one of the following strings
	if there is an error:
	
	'connecterror' = Cannot connect.
	'nodberror' = No database present.
	
	Otherwise a tuple (Database, Store) containing the 'till.lib.storm'
	object instances.
	"""
	type = config.get('database')
	user = config.get('dbuser')
	password = config.get('dbpass')
	host = config.get('dbhost')
	name = config.get('dbname')

	uri = type + '://'
	if user:
		uri += user
		if password:
			uri += ':' + password
		uri += '@'
	uri += host
	if name:
		uri += '/'
		uri += name
	
	database = create_database(uri)
	try:
		store = Store(database)
	except Exception:
		return 'connecterror'
	try:
		result = store.execute('SELECT * FROM products')
	except Exception:
		return 'nodberror'
	return database, store

