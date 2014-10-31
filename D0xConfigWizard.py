#!/usr/bin/env python2.7


import ConfigParser
import os

class ConfigWizard:
	def __init__(self, config):
		self.config = config
		self.filepath = 'resources/d0xconfig.ini'
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
		if os.path.isfile('resources/d0xconfig.ini'):
			os.remove('resources/d0xconfig.ini')
	
	def check_for_conf(self):
		if os.path.isfile('resources/d0xconfig.ini'):
			with open('resources/d0xconfig.ini', 'r+') as conf_file:
				# what do?? halp pls
				pass

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
