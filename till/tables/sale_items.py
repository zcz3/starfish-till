
from till.lib.storm.locals import *
from till.tables.sales import Sale
from till.tables.products import Product


class SaleItem(object):
	
	__storm_table__ = 'sale_items'
	
	id = Int(primary=True)
	sale_id = Int()
	product_id = Int()
	name = Unicode()
	barcode = Unicode()
	price_each = Decimal()
	vat_each = Decimal()
	quantity = Int()
	total_price = Decimal()
	total_vat = Decimal()
	is_discount = Bool()
	
	sale_o = Reference(sale_id, Sale.id)
	product_o = Reference(product_id, Product.id)

