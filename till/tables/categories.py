
from till.lib.storm.locals import *


class Category(object):
	
	__storm_table__ = 'categories'
	
	id = Int(primary=True)
	name = Unicode()
	image = RawStr()

