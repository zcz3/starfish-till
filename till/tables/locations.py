
from till.lib.storm.locals import *


class Location(object):
	
	__storm_table__ = 'locations'
	
	id = Int(primary=True)
	name = Unicode()

