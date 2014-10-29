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
  
  This module is for constructing different interface screens
--------
'''
import urwid
import D0xText
import D0xUtils
import D0xImport
import ConfigParser

class D0xScreens:
    def __init__(self):
        self.texts = D0xText.D0xText()
        self.utils = D0xUtils.Utilities()
        self.config = ConfigParser.RawConfigParser()
        self.config.read('resources/d0xconfig.ini')
        self.editField = urwid.Edit
        self.intEdit = urwid.IntEdit
        self.searchField = urwid.Edit
        self.radioButtons = []
#======================================
    def getEditField(self):
        return self.editField
#======================================
    def getIntEditField(self):
        return self.intEdit
#======================================
    def getRadioButtons(self):
        return self.radioButtons
#======================================
    def getSearchField(self):
        return self.searchField
#======================================
    def showAdd(self, version, gap):
        '''This is the adding screen'''
        
        #footer
        footer = urwid.AttrMap(urwid.Text(self.texts.getFooterAddingText(), align='center'), 'InfoFooter')

        #header
        headerTxt = ''
        if (self.config.get('main', 'program_version') == 'y'):
            headerTxt += self.texts.getHeaderText(version)+' / '
        headerTxt += 'Adding'
        if (self.config.get('main', 'display_id_adding') == 'y'):
            headerTxt += ' ID: [%s]' % (gap)
        header = urwid.AttrMap(urwid.Text(('InfoHeaderText', headerTxt), align='center'), 'InfoHeader')

        self.editField = urwid.Edit(('Field', ''),
                                    multiline=True,
                                    edit_text=self.texts.getRecordTemplate(),
                                    edit_pos=len(self.texts.getRecordTemplate().split('\n')[0]),
                                    allow_tab=True)
        editField = urwid.ListBox(urwid.SimpleListWalker([
                            urwid.Divider(top=1),
                            urwid.AttrWrap(self.editField,
                            'Info', 'OnFocusBg')
                                                              ]))
        explanation = self.texts.getAddTips()
        explanation = urwid.ListBox(explanation)

        vline = urwid.AttrWrap(urwid.SolidFill('|'), 'Info')

        bodyWithInfo = urwid.Columns([('fixed', 40, explanation),('fixed', 1, vline), editField], dividechars=3, focus_column=2)
        headBodyFootFrame = urwid.Frame(footer=footer, header=header, body=bodyWithInfo)

        #Background
        bkg = urwid.AttrWrap(headBodyFootFrame, 'Bg')

        #empty Name field dialog
        empty = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getEmptyWarning(), title='|** Error **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        #Message to show when person is added
        added = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getAddedMessage(), title='|** Success **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        #Message to show when canceling adding
        reallyCancel = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getReallyCancelMessage(), title='|** Confirm **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        #Message to show when adding a record
        reallyAdd = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getReallyAddMessage(), title='|** Confirm **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        return bkg, empty, added, reallyCancel, reallyAdd
#======================================
    def showInfo(self, version, rawInput, textFunc, xmlFunc, cancelFunc):
        '''Part of the Search method.
           Search calls this method to display selected data'''
           
        #footer
        footer = urwid.AttrMap(urwid.Text(self.texts.getFooterViewText(), align='center'), 'InfoFooter')

        #header
        headerTxt = ''
        if  (self.config.get('main', 'program_version') == 'y'):
            headerTxt += self.texts.getHeaderText(version)+' / '
        headerTxt += 'Viewing'
        if (self.config.get('main', 'display_id_viewing') == 'y'):
            headerTxt += ' ID: [%s]' % rawInput[0]
        header = urwid.AttrWrap(urwid.Text(('InfoHeaderText', headerTxt), align='center'), 'InfoHeader')

        paddedBody = self.utils.formatViewOutput(rawInput)
        headBodyFootFrame = urwid.Frame(body=paddedBody, header=header, footer=footer)

        #Background
        bkg = urwid.AttrWrap(headBodyFootFrame, 'Bg')

        #Deletion popup
        delete = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getDeletionText(), title='|** Confirm **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')
        
        #No more records warning
        noRecord = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getNoRecordsWarning(), title='|** Information **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')
        
        #Exporting dialog
        export = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getExportText(textFunc, xmlFunc, cancelFunc), title='|** Export **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')
        
        #Popup after export was successfull
        success = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getExportSuccessText(), title='|** Information **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        return  bkg, delete, noRecord, export, success
#======================================
    def showEditor(self, version, rawInput):
        '''This is the editing screen'''
        
        #footer
        footer = urwid.AttrMap(urwid.Text(self.texts.getFooterAddingText(), align='center'), 'InfoFooter')

        #header
        headerTxt = ''
        if (self.config.get('main', 'program_version') == 'y'):
            headerTxt += self.texts.getHeaderText(version)+' / '
        headerTxt += 'Editing'
        if (self.config.get('main', 'display_id_adding') == 'y'):
            headerTxt += ' ID: [%s]' % rawInput[0]
        header = urwid.AttrMap(urwid.Text(('InfoHeaderText', headerTxt), align='center'), 'InfoHeader')

        self.editField = urwid.Edit(('Field', ''),
                                    multiline=True,
                                    edit_text=rawInput[1],
                                    edit_pos=len(rawInput[1].split('\n')[0]),
                                    allow_tab=True)
        editField = urwid.ListBox(urwid.SimpleListWalker([
                            urwid.Divider(top=1),
                            urwid.AttrWrap(self.editField,
                            'Info', 'OnFocusBg')
                                                              ]))
        explanation = self.texts.getAddTips()
        explanation = urwid.ListBox(explanation)

        vline = urwid.AttrWrap(urwid.SolidFill('|'), 'Info')

        bodyWithInfo = urwid.Columns([('fixed', 40, explanation),('fixed', 1, vline), editField], dividechars=3, focus_column=2)
        headBodyFootFrame = urwid.Frame(footer=footer, header=header, body=bodyWithInfo)

        #Background
        bkg = urwid.AttrWrap(headBodyFootFrame, 'Bg')

        #empty Name field dialog
        empty = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getEmptyWarning(), title='|** Error **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        #Message to show when person is added
        added = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getAddedMessage(), title='|** Success **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        #Message to show when canceling
        reallyCancel = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getReallyCancelMessage(), title='|** Confirm **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        #Message to show when adding a record
        reallyAdd = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getReallyAddMessage(), title='|** Confirm **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        return bkg, empty, added, reallyCancel, reallyAdd
#======================================
    def showSearch(self, version):
        '''This is the main search screen'''
        
        #footer
        footer = urwid.AttrMap(urwid.Text(self.texts.getFooterSearchText(), align='center'), 'InfoFooter')

        #header
        header = urwid.AttrMap(urwid.Text(('InfoHeaderText', '%s %s Searching' % (self.texts.getHeaderText(version), '/')), align='center'), 'InfoHeader')

        radioGroup = []
        self.radioButtons = []
        tmpDict = {'id':'ID','name':'Name','lastname':'Last name','nickname':'Nickname'}
        for i in ('id','name','lastname','nickname'):
            if (self.config.get('main', 'default_search_method') == i):
                self.radioButtons.append(urwid.AttrWrap(urwid.RadioButton(radioGroup, tmpDict[i], state=True), 'Info', 'OnFocusBg'))
            else: 
                self.radioButtons.append(urwid.AttrWrap(urwid.RadioButton(radioGroup, tmpDict[i], state=False), 'Info', 'OnFocusBg'))
        
        self.searchField = urwid.AttrWrap(urwid.Edit(('Field', 'Search: ')), 'Info', 'OnFocusBg')

        bodeh = urwid.Pile([urwid.ListBox(urwid.SimpleListWalker([
                     urwid.Divider(top=2),
                     self.searchField,
                     urwid.Divider(),
                     urwid.AttrWrap(urwid.Text(('Field', 'Select search criteria:')), 'Bg'),
                     self.radioButtons[0],
                     self.radioButtons[1],
                     self.radioButtons[2],
                     self.radioButtons[3]]))
                           ])

        explanation = urwid.ListBox(self.texts.getSearchTips())

        bodyWithInfo = urwid.Columns([('fixed', 40, explanation), ('fixed', 1, urwid.AttrWrap(urwid.SolidFill('|'), 'Info')), bodeh], dividechars=3, focus_column=2)
        headBodyFootFrame = urwid.Frame(footer=footer, header=header, body=bodyWithInfo)

        #Background
        bkg = urwid.AttrWrap(headBodyFootFrame, 'Bg')

        #empty field popup
        empty = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getEmptyFieldMessage(), title='|** Error **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        #Search by ID received a letter. We are doomed!
        gotLetter = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getGotLetterMessage(), title='|** Error **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        #Record does not exist
        noRecord = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getNoRecordMessage(), title='|** Error **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        return bkg, empty, gotLetter, noRecord
#======================================
    def showSearchResultScreen(self, listOfResults, version):
        '''This is the search result screen when searching by name/nickname/lastname'''

        resultBoxColumns = [
                    urwid.AttrWrap(urwid.Text(('SearchBoxHeaderText', 'ID'), align='center'), 'SearchBoxHeaderBg'),
                    urwid.AttrWrap(urwid.Text(('SearchBoxHeaderText', 'Name'), align='center'), 'SearchBoxHeaderBg'),
                    urwid.AttrWrap(urwid.Text(('SearchBoxHeaderText', 'Lastname'), align='center'), 'SearchBoxHeaderBg'),
                    urwid.AttrWrap(urwid.Text(('SearchBoxHeaderText', 'Nickname'), align='center'), 'SearchBoxHeaderBg')
                           ]

        #Let's put all the results in columns, k?
        resTmp = []
        resultToShow = []
        for List in listOfResults:
            for Item in List:
                resTmp.append(urwid.AttrWrap(urwid.Text(('Info', '%s' % Item), align='center'), 'Bg'))
            resultToShow.append(urwid.Columns(resTmp, 1))
            resTmp = []

        self.intEdit = urwid.AttrWrap(urwid.IntEdit(caption='Enter ID: '.rjust(15)), 'Field')
        resultBox = urwid.ListBox(urwid.SimpleListWalker([
                                        urwid.Divider(),
                                        self.intEdit,
                                        urwid.Divider(),
                                        urwid.Columns(resultBoxColumns, 1),
                                                         ]+resultToShow))

        #footer
        footer = urwid.AttrMap(urwid.Text(self.texts.getFooterSearchResultText(), align='center'), 'InfoFooter')

        #header
        header = urwid.AttrMap(urwid.Text(('InfoHeaderText', '%s / Search results / Found records: %d' % (self.texts.getHeaderText(version), len(resultToShow))), align='center'), 'InfoHeader')

        headBodyFootFrame = urwid.Frame(footer=footer, header=header, body=resultBox)

        #Background
        bkg = urwid.AttrWrap(headBodyFootFrame, 'Bg')

        #Record does not exist
        noRecord = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getNoRecordMessage(), title='|** Error **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')

        return bkg, noRecord
#======================================
    def showMain(self, Banner, version, importBtn, cancelBtn):
        '''The main screen'''
        
        #footer
        footer = urwid.AttrMap(urwid.Text(self.texts.getFooterMainText(), align='center'), 'InfoFooter')

        #header
        header = urwid.AttrMap(urwid.Text(('InfoHeaderText', '%s / Kulverstukas @ Evilzone.org' % (self.texts.getHeaderText(version))), align='center'), 'InfoHeader')

        #Message below the banner
        headBodyFootFrame = urwid.Frame(header=header, body=self.texts.getMainPageText(Banner), footer=footer)
        bkg = urwid.AttrWrap(headBodyFootFrame, 'Bg')
        
        #Import dialog
        importDialog = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getImportText(self.utils.listFiles(D0xImport.IMPORT_PATH), importBtn, cancelBtn), title='|** Import **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')
        
        #Popup after import was successfull
        success = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getImportSuccessText(), title='|** Information **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')
        
        #Popup if the file is invalid
        fail = urwid.AttrWrap(urwid.Overlay(urwid.LineBox(self.texts.getImportFailedText(), title='|** Information **|'), bkg, 'center', 40, 'middle', None), 'PopupMessageBg')
        
        return bkg, importDialog, success, fail
#======================================
