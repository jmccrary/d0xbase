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
  
  This module defines callbacks/menus for the screens
--------
'''
import urwid

import datetime
import os
import random
import sys
import ConfigParser

import D0xDBManager
import D0xConfigWizard
import D0xScreens
import D0xUtils
import D0xText
import D0xExport
import D0xImport

class Callbacks:
    def __init__(self, database, gap, config):
        self.information = []
        self.INPUT = []
        self.cameToEdit = False
        self.interfaces = D0xScreens.D0xScreens()
        self.utils = D0xUtils.Utilities()
        self.texts = D0xText.D0xText()
        self.database = database
        self.gap = gap
        self.palette = self.texts.getPalette()
        self.config = config
        self.d0xExport = D0xExport.Export()
        self.d0xImport = D0xImport.Import()
        try:  # all self.N vars must be initialized here as well for use in the main screen
              # else it will throw "reference before assignment" type error
            self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
        except UnicodeEncodeError:
            self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithoutBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
#===================================
    def mainScreenMenu(self, key):
        '''Main screen menu'''
        
        if ((self.loop.widget == self.importSuccess) or (self.loop.widget == self.importFail)):
            if key in ('esc', 'enter'):
                self.loop.widget = self.mainScreen
                return
        
        elif key == 'esc':  #Quit
            if (self.loop.widget == self.importDialog):
                self.loop.widget = self.mainScreen
            else:
                sys.exit("You have quit D0xBase %s. Have a nice day!\n".rjust(50) % self.texts.getVersion())
        elif key in ('s', 'S'):  #Search
            self.mainScreen, self.empty, self.gotLetter, self.noRecord = self.interfaces.showSearch(self.texts.getVersion())
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.searchScreenMenu)
            self.loop.run()
        elif key in ('a', 'A'):  #Adding screen
            self.mainScreen, self.exit, self.success, self.confirmCancel, self.reallyAdd = self.interfaces.showAdd(self.texts.getVersion(), self.gap)
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.addEditMenu)
            self.loop.run()
        elif key in ('i', 'I'):
            self.loop.widget = self.importDialog
            self.loop.run()
#===================================
    def searchScreenMenu(self, key):
        '''Menu for the search screen'''

        if (self.loop.widget == self.empty) or (self.loop.widget == self.gotLetter) or (self.loop.widget == self.noRecord):
            if key in ('esc', 'enter'):
                self.loop.widget = self.mainScreen
                return
        elif key == 'esc':
            try:
                self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
                self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                self.loop.run()
            except UnicodeEncodeError:
                self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithoutBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
                self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                self.loop.run()
        elif key == 'enter':
            Hurr = self.interfaces.getSearchField().edit_text.strip()
            #Lets check if the field is empty, k?
            if (Hurr == ''): #oh shi- it is!?
                self.loop.widget = self.empty #Display an error...
                return
            else:
                #Search by ID starts here
                if (self.interfaces.getRadioButtons()[0].state == True):
                    if (self.utils.checkForChars(Hurr) == True): #search by ID received a letter!?
                        self.loop.widget = self.gotLetter #show an error
                        return
                    #Get some data from the self.database
                    self.INPUT = self.database.getPerson(Hurr)
                    if (self.INPUT is None):
                        self.loop.widget = self.noRecord
                        return
                    self.mainScreen, self.deletionPopup, self.noMoreRecords, self.export, self.successExport = self.interfaces.showInfo(self.texts.getVersion(), self.INPUT,
                                                                    self.exportAsTextCallback,
                                                                    self.exportAsXMLCallback,
                                                                    self.exportCancelCallback)
                    self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.viewScreenMenu)
                    self.loop.run()

                elif (self.interfaces.getRadioButtons()[1].state): #search by name
                    searchIDs = self.database.search('name', Hurr)

                elif (self.interfaces.getRadioButtons()[2].state): #search by last name
                    searchIDs = self.database.search('lastname', Hurr)

                elif (self.interfaces.getRadioButtons()[3].state): #search by nickname
                    searchIDs = self.database.search('nickname', Hurr)
                    
                searchIDs = self.utils.getResults(searchIDs, self.database)
                self.mainScreen, self.noRecord = self.interfaces.showSearchResultScreen(searchIDs, self.texts.getVersion())
                self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.searchResultMenu)
                self.loop.run()
#===================================
    def searchResultMenu(self, key):
        '''Menu for the found results'''
        
        if (self.loop.widget == self.noRecord):
            if key in 'esc':
                self.loop.widget = self.mainScreen
                return
        elif key == 'esc':  #Get back to the search screen bish!
            try:
                self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
                self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                self.loop.run()
            except UnicodeEncodeError:
                self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithoutBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
                self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                self.loop.run()
        elif key == 'enter':
            if (self.interfaces.getIntEditField().edit_text == ''): return #nothing is entered...
            self.INPUT = self.database.getPerson(self.interfaces.getIntEditField().edit_text)
            if (self.INPUT is None):
                self.loop.widget = self.noRecord
                return
            self.mainScreen, self.deletionPopup, self.noMoreRecords, self.export, self.successExport = self.interfaces.showInfo(self.texts.getVersion(), self.INPUT,
                                                                    self.exportAsTextCallback,
                                                                    self.exportAsXMLCallback,
                                                                    self.exportCancelCallback)
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.viewScreenMenu)
            self.loop.run()
        elif key in ('s', 'S'):  #Search
            self.mainScreen, self.empty, self.gotLetter, self.noRecord = self.interfaces.showSearch(self.texts.getVersion())
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.searchScreenMenu)
            self.loop.run()
        elif key in ('a', 'A'):  #Adding screen
            self.mainScreen, self.exit, self.success, self.confirmCancel, self.reallyAdd = self.interfaces.showAdd(self.texts.getVersion(), self.gap)
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.addEditMenu)
            self.loop.run()
#===================================
    def viewScreenMenu(self, key):
        '''This menu is for when viewing a record'''

        if (self.loop.widget == self.noMoreRecords):
            if key in ('esc', 'enter'):
                try:
                    self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithBanner(), self.texts.getVersion(), importFromXMLCallback, importCancelCallback)
                    self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                    self.loop.run()
                except UnicodeEncodeError:
                    self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithoutBanner(), self.texts.getVersion(), importFromXMLCallback, importCancelCallback)
                    self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                    self.loop.run()
        elif (self.loop.widget == self.export):
            if key == 'esc':
                self.loop.widget = self.mainScreen
                return
        elif (self.loop.widget == self.successExport):
            if key in ('esc', 'enter'):
                self.loop.widget = self.mainScreen
                return
        elif (self.loop.widget == self.deletionPopup):
            if key in ('y', 'Y'):
                #If confirmed, delete him and show the next one
                #or the previous one, if deleted person was the last in DB
                self.database.deletePerson(self.INPUT[0])
                self.loop.widget = self.mainScreen
                lastPerson = self.database.getLastID();
                oldIndex = self.INPUT[0]
                self.INPUT = None
                if (lastPerson == 0):
                    self.loop.widget = self.noMoreRecords
                    return
                elif ((oldIndex >= lastPerson) and (oldIndex >= 1)):
                    while (self.INPUT is None):
                        oldIndex -= 1
                        self.INPUT = self.database.getPerson(oldIndex)
                elif (oldIndex < lastPerson):
                    while (self.INPUT is None):
                        oldIndex += 1
                        self.INPUT = self.database.getPerson(oldIndex)
                self.gap = self.database.getNearestGap();
                self.mainScreen, self.deletionPopup, self.noMoreRecords, self.export, self.successExport = self.interfaces.showInfo(self.texts.getVersion(), self.INPUT,
                                                                    self.exportAsTextCallback,
                                                                    self.exportAsXMLCallback,
                                                                    self.exportCancelCallback)
                self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.viewScreenMenu)
                self.loop.run()
            elif key in ('n', 'N'):
                self.loop.widget = self.mainScreen
                return
        elif key in ('e', 'E'): #Edit screen
            self.cameToEdit = True
            self.gap = self.INPUT[0]
            self.mainScreen, self.exit, self.success, self.confirmCancel, self.reallyAdd = self.interfaces.showEditor(self.texts.getVersion(), self.INPUT)
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.addEditMenu)
            self.loop.run()
        elif key in ('a', 'A'): #Add screen
            self.gap = self.database.getNearestGap()
            self.mainScreen, self.exit, self.success, self.confirmCancel, self.reallyAdd = self.interfaces.showAdd(self.texts.getVersion(), self.gap)
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.addEditMenu)
            self.loop.run()
        elif key in ('d', 'D'): #Deletion of a record popup
            self.loop.widget = self.deletionPopup
            return
        elif key in ('s', 'S'):  #Search screen
            self.mainScreen, self.empty, self.gotLetter, self.noRecord = self.interfaces.showSearch(self.texts.getVersion())
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.searchScreenMenu)
            self.loop.run()
        elif key in ('x', 'X'): #Export dialog
            self.loop.widget = self.export
            return
        elif key == 'esc':
            try:
                self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
                self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                self.loop.run()
            except UnicodeEncodeError:
                self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithoutBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
                self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                self.loop.run()
        elif key == 'right':  # record browsing when the RIGHT arrow key was pressed
            lastPerson = self.database.getLastID()
            idCounter = self.INPUT[0]
            previousID = idCounter
            if (self.INPUT[0] != lastPerson):
                while (self.INPUT[0] == previousID):
                    idCounter += 1
                    self.INPUT = self.database.getPerson(idCounter)
            elif (self.INPUT[0] == lastPerson):
                return
            self.mainScreen, self.deletionPopup, self.noMoreRecords, self.export, self.successExport = self.interfaces.showInfo(self.texts.getVersion(), self.INPUT,
                                                                self.exportAsTextCallback,
                                                                self.exportAsXMLCallback,
                                                                self.exportCancelCallback)
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.viewScreenMenu)
            self.loop.run()
        elif key == 'left':
            firstPerson = self.database.getFirstID()
            idCounter = self.INPUT[0]
            previousID = idCounter
            if (self.INPUT[0] != firstPerson):
                while (self.INPUT[0] == previousID):
                    idCounter -= 1
                    self.INPUT = self.database.getPerson(idCounter)
            elif (self.INPUT[0] == firstPerson):
                return
            self.mainScreen, self.deletionPopup, self.noMoreRecords, self.export, self.successExport = self.interfaces.showInfo(self.texts.getVersion(), self.INPUT,
                                                                self.exportAsTextCallback,
                                                                self.exportAsXMLCallback,
                                                                self.exportCancelCallback)
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.viewScreenMenu)
            self.loop.run()
#===================================
    def addEditMenu(self, key):
        '''Adding and editing screen menu'''
        
        if (self.loop.widget == self.exit):
            if key in ('esc', 'enter'):
                self.loop.widget = self.mainScreen
                return
        elif (self.loop.widget == self.confirmCancel):
            if key in ('y', 'Y'):
                try:
                    self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
                    self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                    self.loop.run()
                except UnicodeEncodeError:
                    self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithoutBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
                    self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                    self.loop.run()
            elif key in ('n', 'N'):
                self.loop.widget = self.mainScreen
                return
        elif (self.loop.widget == self.reallyAdd):
            #if a record is to be modified, "self.cameToEdit" will be true
            if key in ('y', 'Y'):
                if (self.cameToEdit == True):
                    self.database.editPerson(self.information)
                else:
                    #Let's add that ish, finally!
                    self.database.addPerson(self.information)
                self.loop.widget = self.success
                return
            elif key in ('n', 'N'):
                self.loop.widget = self.mainScreen
                return
        elif key in ('esc', 'enter'):
            if (self.loop.widget == self.success):
                if (self.cameToEdit == True):
                    self.INPUT = self.information
                    self.cameToEdit = False
                else:
                    self.INPUT = self.database.getPerson(self.gap)
                    self.gap = self.database.getNearestGap() #get next position where to insert a record
                self.information = []
                self.mainScreen, self.deletionPopup, self.noMoreRecords, self.export, self.successExport = self.interfaces.showInfo(self.texts.getVersion(), self.INPUT,
                                                                    self.exportAsTextCallback,
                                                                    self.exportAsXMLCallback,
                                                                    self.exportCancelCallback)
                self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.viewScreenMenu)
                self.loop.run()
            else:
                if (self.config.get('main', 'confirm_add_cancel') == 'y'):
                    self.loop.widget = self.confirmCancel
                    return
                else:
                    try:
                        self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
                        self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                        self.loop.run()
                    except UnicodeEncodeError:
                        self.mainScreen, self.importDialog, self.importSuccess, self.importFail = self.interfaces.showMain(self.texts.getMainScreenTextWithoutBanner(), self.texts.getVersion(), self.importFromXMLCallback, self.importCancelCallback)
                        self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.mainScreenMenu)
                        self.loop.run()
        elif key == 'f2':
            #Check if anything was entered
            if (self.interfaces.getEditField().get_edit_text().strip() == ''):
                self.loop.widget = self.exit
                return
            self.information = []
            self.information.append(self.gap) # first is the ID
            self.information.append(self.interfaces.getEditField().get_edit_text()) # second comes the test
            #add the last modification time at the end
            Date = datetime.date.today()
            self.information.append('%d.%d.%d' % (Date.year, Date.month, Date.day)) # last is the modification date
            #Ask if you really reall want to add it :D
            self.loop.widget = self.reallyAdd
            return
#===================================
    def exportAsTextCallback(self, button):
        self.d0xExport.exportAsText(self.texts.getVersion(), self.INPUT)
        self.loop.widget = self.successExport
#===================================
    def exportAsXMLCallback(self, button):
        self.d0xExport.exportAsXML(self.texts.getVersion(), self.INPUT)
        self.loop.widget = self.successExport
#===================================
    def exportCancelCallback(self, button):
        self.loop.widget = self.mainScreen
#===================================
    def importFromXMLCallback(self, button, user_data):
        wasOk = self.d0xImport.importFromXML(D0xImport.IMPORT_PATH+'/'+user_data, self.database)
        if (wasOk):
            self.loop.widget = self.importSuccess
        else:
            self.loop.widget = self.importFail
        self.gap = self.database.getNearestGap()
#===================================
    def importCancelCallback(self, button):
        self.loop.widget = self.mainScreen
#===================================
