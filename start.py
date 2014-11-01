#!/usr/bin/env python2.7

'''	
=================================================
Copyright 2011 Kulverstukas, Factionwars

	This file is part of D0xBase.

	D0xBase is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation version 3

	D0xBase is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with D0xBase.  If not, see http://www.gnu.org/licenses/
=================================================

Shouts: Evilzone.org
You can contact us at: kulverstukas@kaime.lt
--------
Description:
  This module is part of "D0xBase" project.
  Any modification without knowing what you are doing will result
  in unwanted behavior and can stop working.

  This module is the front-end of D0xBase to give
  graphical interface.
--------
'''

import urwid
import D0xText # 
import D0xDBManager # 
import D0xConfigWizard # REFACTORED
import D0xScreens # 
import D0xCallbacks # 
import D0xImport # 

import os
import sys
import ConfigParser
from optparse import OptionParser


# TODO: somebody needs to refactor this, I'm unfamiliar with urwid but if somebody wants 
# they can take it on themeselves.  Just file a github issue and say you're doing it 
class FrontEnd:
	def __init__(self):
		self.texts = D0xText.D0xText()
		self.palette = self.texts.getPalette()
		self.interfaces = D0xScreens.D0xScreens()

	def begin(self, whichScreen, importFile=''):
		'''Start everything'''

		if (whichScreen == 'main'):
			try:
				self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithBanner(), self.texts.getVersion(), callbacks.importFromXMLCallback, callbacks.importCancelCallback)
				self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=callbacks.mainScreenMenu)
				self.loop.run()
			except UnicodeEncodeError:
				self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithoutBanner(), self.texts.getVersion(), callbacks.importFromXMLCallback, callbacks.importCancelCallback)
				self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=callbacks.mainScreenMenu)
				self.loop.run()
		elif (whichScreen == 'add'):
			self.mainScreen, self.exit, self.success, self.confirmCancel, self.reallyAdd, editFieldsList = self.interfaces.showAdd(self.texts.getVersion(), gap)
			self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=callbacks.addEditMenu)
			self.loop.run()
		elif (whichScreen == 'search'):
			self.mainScreen, self.empty, self.gotLetter, self.noRecord = self.interfaces.showSearch(self.texts.getVersion())
			self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=callbacks.searchScreenMenu)
			self.loop.run()
		elif (whichScreen == 'import'):
			print 'Importing "%s"...' % os.path.basename(importFile)
			if (os.path.exists(importFile) and os.path.isfile(importFile)):
				d0xImport = D0xImport.Import()
				wasOk = d0xImport.importFromXML(importFile, database)
				if (wasOk):
					print 'Import succeeded'
				else:
					print 'Import failed. Not a d0xbase export file?'
			else:
				print '"%s" does\'t seem to exist or is not a file' % importFile

parser = OptionParser()
parser.add_option('-s', '--screen', help='Which homescreen to use when D0xbase begins', metavar='main')
parser.add_option('-i', '--import', help='For importing a record from XML', metavar='file.xml')

(options, args) = parser.parse_args()
options = vars(options)

#Check if appropriate version is being used
if urwid.__version__ == '1.0.2':
	sucess = True
	config = ConfigParser.RawConfigParser()
	
	wizard = D0xConfigWizard.ConfigWizard(config)
	wizard.check_config()
	try:
		wizard.interactive_setup()
	except KeyboardInterrupt as e:
		print '\n\n<ctrl>+c was pressed\n'.format(e)
		sys.exit(1)
	
	database =  D0xDBManager.DBManager(config.get('main', 'database_path'))	
	database.connect()
	gap = database.getNearestGap()
	callbacks = D0xCallbacks.Callbacks(database, gap, config)
	frontend = FrontEnd()

	if (options['screen'] == 'add'): frontend.begin('add')
	elif (options['screen'] == 'search'): frontend.begin('search')
	elif ((options['import'] != None) and (options['import'].strip() != '')):
		frontend.begin('import', options['import'].strip())
	else: frontend.begin(config.get('main', 'default_screen'))
else:
	print 'Urwid version must be 1.0.2; Exiting.'
