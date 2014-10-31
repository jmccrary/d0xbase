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
  
  This module defines methods for importing a record to
  the database from XML format
--------
'''

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import xml.etree.ElementTree as ET
import sys

IMPORT_PATH = 'resources/imports'

class Import:
#=============================================
    def checkForPath(self):
        '''Checks if a folder named "imports" exists.'''
        success = True
        if ((os.path.exists(IMPORT_PATH) == False) or (os.path.isdir(IMPORT_PATH) == False)):
            success = False
        return success
#=============================================
    def checkIfValid(self, importFile):
        isValid = True
        
        # here we check if the file is in a valid XML format
        try:
            parser = make_parser()
            parser.setContentHandler(ContentHandler())
            parser.parse(importFile)
        except:
            isValid = False
            return isValid  # doesn't seem like a valid format
        
        return isValid
#=============================================
    def importFromXML(self, importFile, database):
        success = self.checkIfValid(importFile)
        if (success):
            xmlData = ET.parse(importFile)
            root = xmlData.getroot()
            recordInfo = root.find('record')
            data = []
            for child in recordInfo:
                data.append(child.text)
            try:
                database.addPerson(data)
            except:
                # if it comes here then the ID exists in the database
                data[0] = database.getNearestGap()
                database.addPerson(data)
            
        return success
#=============================================

