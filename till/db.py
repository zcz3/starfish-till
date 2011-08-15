"""
Connects to the database.
"""

import os
import os.path
import sys
import sqlite3

from till.lib.storm.locals import *
from till import config


def install(database, store):
	"""Installs the database."""
	if 'TILLFILES' in os.environ.keys():
                database = config.get('database')
                if database == 'mysql':
                        sql_file = 'database_mysql.sql'
                elif database == 'sqlite':
                        sql_file = 'database_sqlite.sql'
                else:
                        sql_file = 'database.sql'
                sql = os.path.join(os.environ['TILLFILES'], sql_file)
                try:
                        with open(sql, 'r') as f:
                                store.execute(f.read())
                                store.flush()
                                store.commit()
                except Exception as e:
                        raise e
                        return 'error', e
        return ('success',)
        

def load():
	"""
	Connects to the database. Returns a tuple - the first element is one of
	the following strings if there is an error:
	
	'connecterror' = Cannot connect.
	'nodberror' = No database present.
	
	Otherwise a tuple ('success', Database, Store) is returned containing
	the 'till.lib.storm' object instances.
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
		return ('connecterror',)
	try:
		result = store.execute('SELECT * FROM products')
	except Exception:
		return 'nodberror', database, store
	return 'success', database, store

