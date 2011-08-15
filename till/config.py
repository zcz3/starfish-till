"""
Allows reading and writing to the configuration file.
The path to the configuration file may exist in an environment
variable 'TILLCONFIG'. Otherwise, it will be read (or created in) the home
directory.
"""

import os
import os.path
import ConfigParser


config = None
configpath = None

defaults = {
	'database': 'sqlite',
	'dbuser': '',
	'dbpass': '',
	'dbhost': '',
	'dbname': '~/.tilldb.sqlite',
	'tillid': 1,
	'tillname': 'till1',
	'nextid': 1,
}


class ConfigPathNotFound(Exception):
	pass

def load():
	"""Load the configuration file. This is done by till/__init__.py and should not need to be called anywhere else."""
	global config, configpath
	
	if 'TILLCONFIG' in os.environ.keys():
		configpath = os.environ['TILLCONFIG']
	elif 'HOME' in os.environ.keys():
		configpath = os.path.join(os.environ['HOME'], 'tillconfig.ini')
	elif 'USERPROFILE' in os.environ.keys():
		configpath = os.path.join(os.environ['USERPROFILE'], 'tillconfig.ini')
	else:
		raise ConfigPathNotFound()
	config = ConfigParser.RawConfigParser(defaults)
	if not os.path.isfile(configpath):
		config.add_section('Till')
		for key in defaults.keys():
			config.set('Till', key, defaults[key])
		config.write(open(configpath, 'w'))
	else:
		config.readfp(open(configpath, 'r'))

def get(name):
	"""Get the value of an option."""
	return config.get('Till', name)

def set(name, value):
	"""Set an option value."""
	config.set('Till', name, value)
	config.write(open(configpath, 'w'))

