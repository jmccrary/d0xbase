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
You can contact me at: kulverstukas@kaime.lt
--------
Description:
  This module is part of "D0xBase" project.
  Any modification without knowing what you are doing will result
  in unwanted behavior and can stop working.
  
  This module is for back-end work with D0xBase,
  managing database processes.
--------
'''
import sys
import sqlite3

class DBManager:
#============================================
    def __init__(self, dbname):
        global conn, curs
        conn =  sqlite3.connect(dbname)
        curs = conn.cursor()
#============================================
    def install(self):
        '''Here we add the tables to the database'''
        curs.execute('CREATE TABLE person (id INTEGER PRIMARY KEY, information TEXT, lastModDate TEXT)')
        conn.commit();
#============================================
    def connect(self):
        '''Here we try some statements and see if the database
        is already filled with tables'''
        try:
           curs.execute("SELECT id FROM person")
        except:
            self.install()
#============================================
    def getPerson(self, id):
        '''id == row id, and it return a list:)'''
        conn.row_factory = sqlite3.Row
        for person in curs.execute('SELECT * FROM person WHERE id=:id',{"id" : id}):
            return list(person)
#============================================
    def addPerson(self, infoList):
        '''We calculate the last id by counting all the records in the database.
        ID calculation only gets done if given ID == 0'''
        curs.execute("SELECT * FROM person")
        people = 0
        for row in curs:
           people += 1
        if (infoList[0] == 0):
            infoList[0] = people + 1
        curs.execute("INSERT INTO person VALUES (:id, :information, :lastModDate)",
        {"id":infoList[0], "information":infoList[1], "lastModDate":infoList[2]})
        conn.commit()
#============================================
    def editPerson(self, infoList):
        try:
            curs.execute("REPLACE INTO person VALUES (:id, :information, :lastModDate)",
            {"id":infoList[0], "information":infoList[1], "lastModDate":infoList[2]})
            conn.commit()
        except:
            raise Exception('\n\nCannot edit. Database seems to be locked. Someone else uses it?\n')
#============================================
    def deletePerson(self, id):
        try:
            curs.execute("DELETE FROM person WHERE id=:id", {"id":id})
            conn.commit()
        except:
            raise Exception('\n\nCannot delete. Database seems to be locked. Someone else uses it?\n')
#============================================
    def search(self, criteria, statement):
        conn.row_factory = sqlite3.Row
        sql = "%"+criteria+"__"+statement+"%"
        curs.execute('SELECT id FROM person WHERE information LIKE ?',(sql,))
        idList = curs.fetchall()
        return list(idList)
#============================================
    def getNearestGap(self):
        '''Returns an integer representing first
        gap in the database where record can be put'''
        curs.execute("SELECT * FROM person")
        id = 0
        tempRec = ()
        while (tempRec is not None):
            id += 1
            tempRec = self.getPerson(id)
        return id
#============================================
    def getNumberOfPeople(self):
        '''Returns an integer representing
        number of people in the database'''
        curs.execute("SELECT * FROM person")
        people = 0
        for row in curs:
           people += 1
        return people
#============================================
    def getLastID(self):
        '''Returns an integer representing
        ID of the very last record'''
        curs.execute("SELECT * FROM person")
        lastID = 0
        for row in curs:
            lastID = row[0]
        return lastID
#============================================
    def getFirstID(self):
        '''Returns an integer representins
        ID of the very first record'''
        curs.execute("SELECT * FROM person")
        return curs.fetchone()[0]
#============================================
