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
  
  This module defines various utilify functions
--------
'''
import urwid
import string
import datetime
import os

class Utilities:
#=====================================
    def checkForChars(self, item):
        '''Checks a string if it contains a letter.
           This is a part of the search method'''
        for char in (string.lowercase+string.uppercase+' '):
            if item.find(char) != -1:
                return True
        return False
#=====================================
    def getResults(self, listWithIDs, database):
        '''Receives a list of tuples with IDs
           and returns relevant data in array
           of tuples'''
        result = []
        tmp = []
        finalResult = []
        for item in listWithIDs:
            people = database.getPerson(item[0])
            result.append(people[0]) # ID
            for i in people[1].split('\n'):
                for j in ('name', 'lastname', 'nickname'):
                    index = i.strip().lower().find(j)
                    if ((index != -1) and (index == 0)):
                        tmp.append(i.lower().replace(j+':', '').strip())
            result.append(tmp[0])     # Name
            result.append(tmp[1])     # Lastname
            result.append(tmp[2])     # Nickname
            finalResult.append(result)
            result = []
            tmp = []
        return finalResult
#=====================================
    def formatViewOutput(self, rawInfo):
        '''Formats the rawInfo into two columns with proper
           alignment and outputs a table of information'''
        parsedInfo = [
            urwid.Divider(top=1),
            urwid.Text([
                ('LastModifiedField', 'Last modified: '),
                ('LastModifiedDate', self.calculateRecordModDays(rawInfo[2])+'\n\n')
                       ], align='center'),
            urwid.Padding(urwid.Text([('Info', rawInfo[1])]), left=10, right=10, align='center')
                     ]
        return urwid.ListBox(urwid.SimpleListWalker([urwid.Pile(parsedInfo)]))
        #return urwid.Filler(urwid.Pile(parsedInfo))
#=====================================
    def calculateRecordModDays(self, date):
        '''Calculates number of days the record was not modified
           to display in the results'''
        returnStr = ''
        try:
            date = date.split('.')
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            today = datetime.date.today()
            daysSince = today - date
            returnStr = '%d.%d.%d, days since then: %d' % (date.year, date.month, date.day, daysSince.days)
        except:
             returnStr = 'Wrong date format was given'
        return returnStr
#=====================================
    def listFiles(self, path):
        files = []
        for f in os.listdir(path):
            if f.endswith(".xml"):
                files.append(f)
        return files
#=====================================
