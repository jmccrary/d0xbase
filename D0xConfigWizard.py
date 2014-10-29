#!/usr/bin/env python2.7

'''
=================================================
Copyright 2011 Kulverstukas

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
You can contact me at: kulverstukas@kaime.lt
--------
Description:
  This module is part of "D0xBase" project.
  Any modification without knowing what you are doing will result
  in unwanted behavior and can stop working.
  
  This module is for generating a configuration file for the program.
--------
'''

import ConfigParser
import os

#=====================================================
class ConfigWizard:
    def checkAns(self, answer):
        if (answer in ('y', 'Y', 'n', 'N')):
            return True
        else:
            return False
#=====================================================
    def checkAns1(self, answer):
        if (answer.lower() in ('id', 'name', 'lastname', 'nickname')):
            return True
        else:
            return False
#=====================================================
    def checkAns2(self, answer):
        if (answer.lower() in ('main', 'add', 'search')):
            return True
        else:
            return False
#=====================================================
    def checkIfCorrupt(self, config):
        if (os.path.exists('resources/d0xconfig.ini') == False):
            #If file does not exist then set default options, k
            config = self.setDefaults(config)
        else:
            #Well if it does then read it
            config.read('resources/d0xconfig.ini')
            #Lets check integrity if the config file has the right
            #options and if not then set default for them
            if (config.has_section('main') == False): #oh snap! no section holding our options!?
                config = self.setDefaults(config)
            else: #ok so it does exist, huh
                if ((config.has_option('main', 'program_version') == False) or
                    (self.checkAns(config.get('main', 'program_version') == False))):
                    config.set('main', '# Whether or not to display program', '')
                    config.set('main', '# version in all the screens, except main', '')
                    config.set('main', 'program_version', 'y')
                    
                if ((config.has_option('main', 'display_id_adding') == False) or
                    (self.checkAns(config.get('main', 'display_id_adding')) == False)):
                    config.set('main', '# a record that will be assigned to the new record', '')
                    config.set('main', '# This will also affect the editing screen', '')
                    config.set('main', 'display_id_adding', 'y')
                    
                if ((config.has_option('main', 'display_id_viewing') == False) or
                    (self.checkAns(config.get('main', 'display_id_viewing')) == False)):
                    config.set('main', '\n# Display or not the ID of a record when viewing', '')
                    config.set('main', 'display_id_adding', 'y')
    
                if ((config.has_option('main', 'confirm_add_cancel') == False) or
                    (self.checkAns(config.get('main', 'confirm_add_cancel')) == False)):
                    config.set('main', '\n# Display or not a confirmation dialog when you', '')
                    config.set('main', '# want to quit adding a record', '')
                    config.set('main', 'confirm_add_cancel', 'y')
    
                if ((config.has_option('main', 'default_search_method') == False) or
                    (self.checkAns1(config.get('main', 'default_search_method')) == False)):
                    config.set('main', '\n# Set the default search option', '')
                    config.set('main', 'default_search_method', 'name')
    
                if ((config.has_option('main', 'default_screen') == False) or
                    (self.checkAns2(config.get('main', 'default_screen')) == False)):
                    config.set('main', '\n# Set the default screen to show on startup', '')
                    config.set('main', 'default_screen', 'main')
                    
                if (config.has_option('main', 'database_path') == False):
                    config.set('main', '\n# Path where database is located.', '')
                    config.set('main', '# Leave dox.db to have it in the same folder', '')
                    config.set('main', 'database_path', 'dox.db')
        self.writeToFile(config)
        return config
#=====================================================
    def setDefaults(self, config):
        config.add_section('main')
        config.set('main', '# Whether or not to display program', '')
        config.set('main', '# version in all the screens', '')
        config.set('main', 'program_version', 'y')

        config.set('main', '\n# Determine to display or not an ID of', '')
        config.set('main', '# a record that will be assigned to the new record', '')
        config.set('main', 'display_id_adding', 'y')

        config.set('main', '\n# Display or not the ID of a record when viewing', '')
        config.set('main', 'display_id_viewing', 'y')

        config.set('main', '\n# Display or not a confirmation dialog when you', '')
        config.set('main', '# want to quit adding a record', '')
        config.set('main', 'confirm_add_cancel', 'y')

        config.set('main', '\n# Set the default search option', '')
        config.set('main', 'default_search_method', 'name')

        config.set('main', '\n# Set the default screen to show on startup', '')
        config.set('main', 'default_screen', 'main')
        
        config.set('main', '\n# Path where database is located.', '')
        config.set('main', '# Leave dox.db to have it in the same folder', '')
        config.set('main', 'database_path', 'dox.db')
        
        return config
#=====================================================
    def writeToFile(self, config):
        #Information is collected, let's write it to a file
        with open('resources/d0xconfig.ini', 'w') as configfile: config.write(configfile)

        #Now strip "=" from comment lines and write again
        lineStr = '#####################################################\r'\
                  '#           These are settings for D0xBase          #\r'\
                  '#  You should use the wizard to generate this file  #\r'\
                  '#       You can change these settings manualy       #\r'\
                  '#     only if you know how. See reference below     #\r'\
                  '#####################################################\r'\
                  '# Reference:    n == NO / FALSE                     #\r'\
                  '#               y == YES / TRUE                     #\r'\
                  '#       Everything else is self-explainatory        #\r'\
                  '#####################################################\r'
        configfile = open('resources/d0xconfig.ini', 'r')
        line = configfile.readline()
        while line:
            if line.startswith('#'):
                lineStr += line.replace(' = ', '')
            else:
                lineStr += line
            line = configfile.readline()
        #Replace line-feed with line-feed+new-line so that MSNotepad can display
        lineStr = lineStr.replace('\r', '\r\n')
        configfile.close()
        configfile = open('resources/d0xconfig.ini', 'w')
        configfile.write(lineStr)
        configfile.close()
#=====================================================
if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    tempVar = ''

    print ' _____   ___         ____                  \n'\
          '|  __ \ / _ \       |  _ \                 \n'\
          '| |  | | | | |__  __| |_) | __ _ ___  ___  \n'\
          '| |  | | | | |\ \/ /|  _ < / _` / __|/ _ \ \n'\
          '| |__| | |_| | >  < | |_) | (_| \__ \  __/ \n'\
          '|_____/ \___/ /_/\_\|____/ \__,_|___/\___| \n'\
          '                                           \n'\
          '            Configuration wizard           \n'

    #Lets ask if the user wants to set default settings
    while (ConfigWizard().checkAns(tempVar) == False):
        tempVar = raw_input('Would you like to load default settings [Y/N]? ')
    tempVar = ''
    if (tempVar.lower() == 'y'): #If he wants then...
        config = ConfigWizard().setDefaults(config)
    else:
    #if the user doesn't want to...
        config.add_section('main')
        while (ConfigWizard().checkAns(tempVar) == False):
            tempVar = raw_input('Display program version in header [Y/N]? ')
        config.set('main', '# Whether or not to display program', '')
        config.set('main', '# version in all the screens, except main', '')
        config.set('main', 'program_version', tempVar)
        tempVar = ''

        while (ConfigWizard().checkAns(tempVar) == False):
            tempVar = raw_input('Display ID in adding screen [Y/N]? ')
        config.set('main', '\n# Determine to display or not an ID of', '')
        config.set('main', '# a record that will be assigned to the new record', '')
        config.set('main', '# This will also affect the editing screen', '')
        config.set('main', 'display_id_adding', tempVar)
        tempVar = ''

        while (ConfigWizard().checkAns(tempVar) == False):
            tempVar = raw_input('Display ID in viewing screen [Y/N]? ')
        config.set('main', '\n# Display or not the ID of a record when viewing', '')
        config.set('main', 'display_id_viewing', tempVar)
        tempVar = ''

        while (ConfigWizard().checkAns(tempVar) == False):
            tempVar = raw_input('Display confirmation before quitting adding [Y/N]? ')
        config.set('main', '\n# Display or not a confirmation dialog when you', '')
        config.set('main', '# want to quit adding a record', '')
        config.set('main', 'confirm_add_cancel', tempVar)
        tempVar = ''

        while (ConfigWizard().checkAns1(tempVar) == False):
            tempVar = raw_input('Enter default search method [ID/Name/Lastname/Nickname]? ')
        config.set('main', '\n# Set the default search option', '')
        config.set('main', 'default_search_method', tempVar)
        tempVar = ''

        while (ConfigWizard().checkAns2(tempVar) == False):
            tempVar = raw_input('Enter default screen to show on startup [Main/Add/Search]? ')
        config.set('main', '\n# Set the default screen to show on startup', '')
        config.set('main', 'default_screen', tempVar)
        tempVar = ''
        
        tempVar = raw_input('Enter the path of your database? ')
        config.set('main', '\n# Path where database is located.', '')
        config.set('main', '# Leave dox.db to have it in the same folder', '')
        config.set('main', 'database_path', tempVar)
        tempVar = ''

        print '\nWizard has completed collecting the information.\n'
    ConfigWizard().writeToFile(config)
    print 'Configuration has been written to "d0xconfig" file\n'
