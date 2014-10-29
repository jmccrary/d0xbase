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
  
  This module is part of front-end. Here is stored the text
  for D0xBase front-end.
--------
'''

import urwid
import random
import D0xUtils

class D0xText:
#======================================
    def RandomColor(self):
        '''Pick a random color for the main menu text'''
        listOfColors = ['dark red', 'dark green', 'brown', 'dark blue',
                        'dark magenta', 'dark cyan', 'light gray',
                        'dark gray', 'light red', 'light green', 'yellow',
                        'light blue', 'light magenta', 'light cyan', 'default']
        color = listOfColors[random.randint(0, 14)]
        return color
#======================================
    def getHeaderText(self, version):
        '''Accept version as an argument
        return header text'''
        return 'D0xBase version %s' % version
#======================================
    def getFooterViewText(self):
        '''Returns Footer text for record viewing screen'''
        return ('InfoFooterText',['Press ', ('InfoFooterHotkey', '"ESC"'), ' for main screen, ', ('InfoFooterHotkey', '"E"'), ' to edit, ', ('InfoFooterHotkey', '"A"'), ' to add, ', ('InfoFooterHotkey', '"D"'), ' to delete, ', ('InfoFooterHotkey', '"S"'), ' to search, ', ('InfoFooterHotkey', '"X"'), ' to export'])
#======================================
    def getFooterAddingText(self):
        '''Returns Footer text for record adding screen'''
        return ('InfoFooterText', ['Press ', ('InfoFooterHotkey', '"ESC"'), ' to Cancel, ', ('InfoFooterHotkey', '"F2"'), ' to add'])
#======================================
    def getFooterMainText(self):
        '''Returns text for the main screen'''
        return ('InfoFooterText', ['Press ', ('InfoFooterHotkey', '"ESC"'), ' to Quit, ', ('InfoFooterHotkey', '"A"'), ' to add, ', ('InfoFooterHotkey', '"S"'), ' to search, ', ('InfoFooterHotkey', '"I"'), ' to Import'])
#======================================
    def getFooterSearchText(self):
        '''Returns text for the search screen'''
        return ('InfoFooterText', ['Press ', ('InfoFooterHotkey', '"ESC"'), ' for main screen'])
#======================================
    def getFooterSearchResultText(self):
        '''Returns text for the search result screen'''
        return ('InfoFooterText', ['Press ', ('InfoFooterHotkey', '"ESC"'), ' for main screen, ', ('InfoFooterHotkey', '"A"'), ' to add, ', ('InfoFooterHotkey', '"S"'), ' to search again'])
#======================================
    def getPalette(self):
        '''Returns a palette used for coloring the text'''
        return [
                ('Field', 'dark green, bold', 'black'), # information fields, Search: etc.
                ('Info', 'dark green', 'black'), # information in fields
                ('Bg', 'black', 'black'), # screen background
                ('InfoFooterText', 'white', 'dark blue'), # footer text
                ('InfoFooterHotkey', 'dark cyan, bold', 'dark blue'), # hotkeys in footer text
                ('InfoFooter', 'black', 'dark blue'),  # footer background
                ('InfoHeaderText', 'white, bold', 'dark blue'), # header text
                ('InfoHeader', 'black', 'dark blue'), # header background
                ('BigText', self.RandomColor(), 'black'), # main menu banner text
                ('GeneralInfo', 'brown', 'black'), # main menu text
                ('LastModifiedField', 'dark cyan, bold', 'black'), # Last modified:
                ('LastModifiedDate', 'dark cyan', 'black'), # info in Last modified:
                ('PopupMessageText', 'black', 'dark cyan'), # popup message text
                ('PopupMessageBg', 'black', 'dark cyan'), # popup message background
                ('SearchBoxHeaderText', 'light gray, bold', 'dark cyan'), # field names in the search box
                ('SearchBoxHeaderBg', 'black', 'dark cyan'), # field name background in the search box
                ('OnFocusBg', 'white', 'dark magenta') # background when a widget is focused
               ]
#======================================
# Adding/editing screen warning/tips texts
    def getAddTips(self):
        '''Returns the information when adding a record'''
        return urwid.SimpleListWalker([
                urwid.Padding(urwid.Text(('GeneralInfo', '\n Tips and tricks filling this form:\n\n'\
                                          '  1. Use the supplied template to fill in your '\
                                          'information. Stick to the defined format to use '\
                                          'the program efficiently.\n\n'\
                                          '  2. The template is given to utilize the search '\
                                          'efficiently. Do not alter the format. Not everything '\
                                          'must be filled in, input either name, lastname or nickname '\
                                          'for the record to appear in the search results.\n\n'\
                                          '  3. You can add your desired info in free-form, but stick '\
                                          'to the format.\n\n'\
                                          '  4. Use arrow keys to navigate and buttons PAGEUP '\
                                          'to get to the first line, use PAGEDOWN to get to the '\
                                          'last line. HOME key gets to the start of the line and '\
                                          'END key gets to the end of the line.'\
                                          'TAB key insert multiple spaces.')), left=2)
                                        ])

    def getEmptyWarning(self):
        '''Returns a text for a warning if Name field is emty'''
        return urwid.Text(('PopupMessageText', 'Cannot add to the database.\nData field is empty.\n\nPress "ESC" or "ENTER" to return'), align='center')
    
    def getAddedMessage(self):
        '''Returns a text for a notice if record was added'''
        return urwid.Text(('PopupMessageText', 'Successfully added to the database!\n\nPress "ESC" or "ENTER" to return'), align='center')
    
    def getReallyCancelMessage(self):
        '''Returns a text for a confirmation message to cancel adding'''
        return urwid.Text(('PopupMessageText', 'Are you sure you want to cancel?\n[Y/N]'), align='center')
    
    def getReallyAddMessage(self):
        '''Returns a text for a confirmation message to add a record'''
        return urwid.Text(('PopupMessageText', 'Are you sure you want to add?\n[Y/N]'), align='center')
#======================================
# Search screen warning/tips texts
    def getSearchTips(self):
        '''Returns the information for searching screen'''
        return urwid.SimpleListWalker([
                        urwid.Padding(urwid.Text(('GeneralInfo', '\n Tips and tricks for searching:\n\n'\
                                                                 '  1. Searching by ID, you only need to enter '\
                                                                 'the ID of the person in the Database. '\
                                                                 'So, if you would enter "1337", you would get '\
                                                                 'a person whose ID is "1337"\n\n'\
                                                                 '  2. Searching by "Name", "Lastname" or "Nickname", '\
                                                                 'only enter one of the above to get a list '\
                                                                 'of records matching that criteria\n\n'\
                                                                 '  3. To select how to search, use the arrow keys, '\
                                                                 'UP and DOWN, when the cursor is on a wanted box '\
                                                                 'press ENTER or SPACE to select it\n\n')), left=2),
                                              ])
                                              
    def getEmptyFieldMessage(self):
        '''Returns a text for a warning if the search field is empty'''
        return urwid.Text(('PopupMessageText', 'Cannot proceed with the search.\nNothing given as search criteria!\n\nPress "ESC" or "ENTER" to return'), align='center')

    def getGotLetterMessage(self):
        '''Returns a text for a warning if letter was received searching by ID'''
        return urwid.Text(('PopupMessageText', 'Cannot proceed with the search\nSearch by ID received a letter!\nMust only be numbers.\n\nPress "ESC" or "ENTER" to return'), align='center')

    def getNoRecordMessage(self):
        '''Returns a text for a warning that a record does not exist'''
        return urwid.Text(('PopupMessageText', 'Cannot proceed with the search\nRecord does not seem to exist\n\nPress "ESC" or "ENTER" to return'), align='center')
#======================================
    def getMainPageText(self, Banner):
        '''Returns a text for the main page'''
        
        return urwid.LineBox(urwid.AttrWrap(
                urwid.Overlay(
                urwid.LineBox(
                urwid.Padding(
                urwid.Text(('GeneralInfo', 'In case of any bugs, suggestions or '\
                            'just to say Thanks, please email me at kulverstukas@kaime.lt\n'\
                            'You can get a copy of this application by going to '\
                            'http://9v.lt/projects/python/d0xbase/\nYou can also reach '\
                            'us on IRC at irc.evilzone.org #evilzone - we lurk there every day!'),
                            align='center'), align='center', left=3, right=3)), Banner, 'center', 150, 'middle', None),
                'GeneralInfo'))
#======================================
    def getNoRecordsWarning(self):
        '''Returns a warning when last person is deleted
        from the database before returning to the main screen'''
        return urwid.Text(('PopupMessageText', 'The database is empty\n\nPress "ESC" or "ENTER" to return'), align='center')
#======================================
    def getVersion(self):
        return "0.3"
#======================================
    def getMainScreenTextWithBanner(self):
        return urwid.AttrWrap(urwid.Overlay(urwid.BigText('D0xBase %s' % self.getVersion(), urwid.font.HalfBlock7x7Font()), urwid.SolidFill(' '), 'center', None, 'top', None), 'BigText')
#======================================
    def getMainScreenTextWithoutBanner(self):
        return urwid.AttrMap(urwid.SolidFill(' '), 'BigText')
#======================================
    def getRecordTemplate(self):
        template = "Name: \n\n"\
                   "Lastname: \n\n"\
                   "Nickname: \n\n"
        return template
#======================================
    def getDeletionText(self):
        return urwid.Text(('PopupMessageText', 'Are you sure you want to delete it?\n[Y/N]'), align='center')
#======================================
    def getExportText(self, textBtn, xmlBtn, cancelBtn):
        exportDialog = [
                        urwid.AttrWrap(urwid.Button(label='Export as Plain text', on_press=textBtn), 'PopupMessageBg', 'OnFocusBg'),
                        urwid.AttrWrap(urwid.Button(label='Export as XML', on_press=xmlBtn), 'PopupMessageBg', 'OnFocusBg'),
                        urwid.Divider(),
                        urwid.AttrWrap(urwid.Button(label='Cancel', on_press=cancelBtn), 'PopupMessageBg', 'OnFocusBg')
                       ]
        return urwid.BoxAdapter(urwid.ListBox(urwid.SimpleListWalker([urwid.Pile(exportDialog)])), height=4)
#======================================
    def getExportSuccessText(self):
        return urwid.Text(('PopupMessageText', 'Successfully exported\n\nPress "ESC" or "ENTER" to return'), align='center')
#======================================
    def getImportText(self, fileList, importBtn, cancelBtn):
        buttons = []
        for f in fileList:
            buttons.append(urwid.AttrWrap(urwid.Button(label=f, on_press=importBtn, user_data=f), 'PopupMessageBg', 'OnFocusBg'))
            
        importDialog = buttons+[
                       urwid.Divider(),
                       urwid.AttrWrap(urwid.Button(label='Cancel', on_press=cancelBtn), 'PopupMessageBg', 'OnFocusBg')
                               ]

        lines = len(importDialog)
        if (lines >= 8):
            lines = 8
        return urwid.BoxAdapter(urwid.ListBox(urwid.SimpleListWalker([urwid.Pile(importDialog)])), height=lines)
#======================================
    def getImportSuccessText(self):
        return urwid.Text(('PopupMessageText', 'Successfully imported\n\nPress "ESC" or "ENTER" to return'), align='center')
#======================================
    def getImportFailedText(self):
        return urwid.Text(('PopupMessageText', 'Something went wrong. Not a D0x export?\n\nPress "ESC" or "ENTER" to return'), align='center')
#======================================
