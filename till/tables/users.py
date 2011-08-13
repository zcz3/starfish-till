
from till.lib.storm.locals import *


class User(object):
	
	__storm_table__ = 'users'
	
	id = Int(primary=True)
	title = Unicode()
	name = Unicode()
	password = Unicode()
	role = Int()
	# Roles:
	# 1 - administrator
	# 2 - staff

