
def test1():
	import till.printers.maxatec
	import decimal
	p = till.printers.maxatec.MaxatecPrinter('/dev/ttyUSB0')
	p.text('Hello.')
	p.text('Line 2.', 'c')
	p.text('Line 3.', 'r')
	p.text('Line 4.')
	p.line()
	p.price('Example', decimal.Decimal('2.99'))
	p.price('Test product with a really long product description.', decimal.Decimal('23.00'))
	p.price('Discount.', decimal.Decimal('-123.99'))
	p.line()
	p.price('Total', decimal.Decimal('6.00'), 'h')
	p.barcode('Test.', 'code128', 'c')
	p.part_cut()

def test2():
	import decimal
	import till.tables
	import till.db
	till.db.load()
	my = till.tables.Product()
	my.name = u'Test'
	my.price = decimal.Decimal('2.00')
	my.vat_o = till.db.store.find(till.tables.Vat, till.tables.Vat.name == u'Standard').one()
	my.set_vat()
	my.available = True
	till.db.store.add(my)
	till.db.store.flush()

def test3():
	import till.config
	till.config.load()
	print till.config.get('database')

def test4():
	import till.gui.config_editor
	app = till.gui.config_editor.ConfigEditor()
	app.mainloop()

def test5():
	import till.gui.base
	import till.gui.login
	base = till.gui.base.Base()
	login = till.gui.login.Login(base.frame_main)
	base.attach_frame(login, None)
	base.mainloop()

test5()

