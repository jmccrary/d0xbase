#!/usr/bin/env python2.7


import ConfigParser
import os
import hashlib

# I'm going to try something bold here... Writing a ew class named ConfigFile
# should help eliminate some of these awful variable name redundancies.
class ConfigFile:
	def __init__(self):
		self.name = 'd0xconfig.ini'
		self.default_path = 'resources/d0xconfig.ini'
		

class ConfigWizard:
	def __init__(self, conf_object):
		self.conf_object = conf_object
		# We need to run this wizard through some kind of urwid interface.
		self.def_conf_desc = [
			'Would you like see the program version printed onscreen? [y/n]: ',
			'Want to display the entry ID when adding a new record? [y/n]: ',
			'Want to display the ID of the record while viewing it? [y/n]: ',
			'Confirm on close while adding a new entry? [y/n]: ',
			'Set the default search paramater [id, name, last_name, nick_name]: ',
			'Set the "home screen" for d0xbase [main]: ',
			'Enter custom path to create a database:  '
		]
		self.def_conf_keys = [
			'program_version',
			'display_id_adding',
			'display_id_viewing',
			'confirm_add_cancel',
			'default_search_method',
			'default_screen',
			'database_path'
		]
		self.def_conf_values = [
			'y',
			'y',
			'y',
			'y',
			'name',
			'main',
			'resources/database/dox.db'
		]
		self.def_conf = dict(zip(self.def_conf_keys, self.def_conf_values))
		self.user_conf_keys = self.def_conf_keys
		self.user_conf_values = []

	def write_config(self, user_conf):
		self.config.add_section('main')
		for key, value in user_conf.iteritems():
			self.config.set('main', key, value)
		with open(self.filepath, 'wb') as configfile:
			self.config.write(configfile)

	def interactive_setup(self):
		for x in range(0, len(self.def_conf_values)):
			self.user_conf_values.append(raw_input(self.def_conf_desc[x]))
		self.user_conf = dict(zip(self.user_conf_keys, self.def_conf_values))
		self.write_config(self.user_conf)

	def keep_defaults(self):
		self.config.add_section('main')
		for key, value in self.def_conf.iteritems():
			self.config.set('main', key, value)
		with open('resources/d0xconfig.ini', 'wb') as default_config_file:
			self.config.write(default_config_file)
	
	def remove_conf():
		if os.path.isfile(self.filepath):
			os.remove(self.filepath)
	
	def check_for_conf(self):
		file_integrity = ''
		if os.path.isfile(self.filepath):
			file_hash = hashlib.md5()
			with open(self.filename "r+b") as f:
				file_hash = hashlib.md5(f.read()).hexdigest
			if file_hash == '6fa8f4cc592d2739146a1664ba25a522':
				return file_integrity = 'good'
			else:
				return file_integrity = 'bad'

if __name__ == '__main__':
	print '''
  _____   ___         ____                  
 |  __ \ / _ \       |  _ \                 
 | |  | | | | |__  __| |_) | __ _ ___  ___  
 | |  | | | | |\ \/ /|  _ < / _` / __|/ _ \ 
 | |__| | |_| | >  < | |_) | (_| \__ \  __/ 
 |_____/ \___/ /_/\_\|____/ \__,_|___/\___| 
                                            
           Configuration wizard             
'''
	config = ConfigParser.RawConfigParser()
	decision = raw_input('Would you like to load default settings [Y/N]? ')
	wizard = ConfigWizard(config)
	if (decision.lower() == 'y'):
		wizard.keep_defaults()
		print 'Configuration has been written to "d0xconfig" file\n'
	else:
		wizard.interactive_setup()
