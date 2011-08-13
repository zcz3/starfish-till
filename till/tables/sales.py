
from till.lib.storm.locals import *
from till.tables.users import User
from till.tables.locations import Location


class Sale(object):
	
	__storm_table__ = 'sales'
	
	id = Int(primary=True)
	receipt_number = Unicode()
	total = Decimal()
	vat = Decimal()
	date = DateTime()
	user_id = Int()
	location_id = Int()
	payment_method = Int()
	# Payment methods:
	# 1 - cash
	# 2 - card
	# 3 - cheque
	cash_paid = Decimal()
	
	user_o = Reference(user_id, User.id)
	location_o = Reference(location_id, Location.id)

