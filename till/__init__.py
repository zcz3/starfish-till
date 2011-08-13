
import sys
import os.path

sys.path.append(os.path.join(
	os.path.dirname(__file__),
	'lib/'
))

from till import config

config.load()

from till import db

db.load()

