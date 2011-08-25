
import sys
import os.path

sys.path.append(os.path.join(
	os.path.dirname(__file__),
	'lib/'
))

datadirs = (
	os.path.join(os.getcwd(), 'data'),
	'/opt/till/data',
	'/usr/local/share/till',
)
for dir in datadirs:
	if os.path.exists(dir):
		os.environ['TILLFILES'] = dir

