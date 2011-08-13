
from till.lib.storm.locals import *


class Vat(object):
	
	__storm_table__ = 'vat'
	
	id = Int(primary=True)
	name = Unicode()
	rate = Decimal()

