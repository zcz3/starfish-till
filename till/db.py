"""
Conencts to the database.
"""

from till.lib.storm.locals import *
from till import config


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

database = None
store = None

def load():
	global database, store
	database = create_database(uri)
	store = Store(database)


