#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2 as mdb
import re

class Database:    #our server info
    host = 'db-new.doc.ic.ac.uk'
    user = 'ng1513'
    password = 'MalariaTeam2014'
    data_base = 'ng1513'
    main_table = 'malariamain'
    byte_table = 'malariaimage'

    def __init__(self):
        self.connection = mdb.connect(host = self.host, user = self.user, password = self.password, dbname = self.data_base)
        self.cursor = self.connection.cursor()
    


    def insert(self, query):
        try:
            cursor = self.connection.cursor()
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except:
            self.connection.rollback()
            return False

    def query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()


    def insert_create(self, variables, byte_array):
        if self.array_check_insert(variables) == False:
            return "Invalid Parameters Passed"
        q = "INSERT INTO malariamain (date, lab, class, species, strain, count, zoom, slideid, comments) VALUES ("
        for i in range(0,9):
            if (i < 5 or i > 6):
                q += "'" + variables[i] + "'"
            else:
                q += variables[i]
            if i < 8:
                q += ", "
                    
        q += ");"
        q_2 = "INSERT INTO malariaimage VALUES ((SELECT MAX(id) FROM malariamain), '" + byte_array +"');"
        if self.insert(q) and self.insert(q_2):
            return "Success"
        else:
            return "Something went wrong..."
        
    
         
    def query_create(self, variables):
         if self.array_check_query(variables) == False:
            return [], "Invalid Parameters Passed"
                
         q = "SELECT * FROM malariamain JOIN malariaimage ON malariamain.id = malariaimage.id WHERE "
         places = ["date", "lab", "class", "species", "strain", "count", "zoom", "slideid",  "comments"]
         
         for i in range(0, 9):
             if variables[i] != "NULL":
                 if i == 0:
                     between = variables[i].split(";")
                     q += places[i] + " >= " + "'" + between[0] + "'" + " AND " + places[i] + " <= " + "'" + between[1] + "'"
                 elif ((i < 5 and i > 0) or i > 6):
                     q += places[i] + " = " + "'" + variables[i] + "'"
                 elif i == 5 or i == 6:
                     between = variables[i].split(";")
                     q += places[i] + " >= " + between[0] + " AND " + places[i] + " <= " + between[1]
                
                 q += " AND "
    
         q += "1=1;"
         return self.query(q), "Success"


    def array_check_insert(self, variables):
        if len(variables) != 9:
            return False
        for i in range(0,9):
            if (i == 0 or i == 5 or i == 6) and re.search('[a-zA-Z]',variables[i]) and variables[i]!="NULL":
                return False
            elif i == 2 and (variables[i] != "positive" and variables[i] != "negative"):
                return False
            elif ((i > 0 and i <5) or i>6) and variables[i].find(';')!=-1:
                return False
        return True

    def array_check_query(self, variables):
        if len(variables) != 9:
            return False
        for i in range(0,9):
            if (i == 0 or i == 5 or i == 6) and (re.search('[a-zA-Z]', variables[i]) or variables[i].find(';')==-1):
                return False
            elif i == 2 and (variables[i] != "positive" and variables[i] != "negative" and variables[i] != "NULL"):
                return False
            elif ((i > 0 and i <5) or i>6) and variables[i].find(';')!=-1:
                return False
        return True


'''
def array_check_insert(variables, byte_array):
    if len(variables) != 9:
        return False
    if byte_array.find(';')!=-1:
        return False
    for i in range(0,9):
        if (i == 0 or i == 5 or i == 6) and re.search('[a-zA-Z]',variables[i]) and variables[i]!="NULL":
            return False
        elif ((i > 0 and i <5) or i>6) and variables[i].find(';')!=-1:
            return False
    return True

def array_check_query(variables):
    if len(variables) != 9:
        return False
    for i in range(0,9):
        if (i == 0 or i == 5 or i == 6) and (re.search('[a-zA-Z]', variables[i]) or variables[i].find(';')==-1):
            return False
        elif ((i > 0 and i <5) or i>6) and variables[i].find(';')!=-1:
            return False
    return True

'''
'''
testdb = Database()
list = ["1999-11-11", "Jamestest", "positive","test","test","0","0","test","test"]
if testdb.insert_create(list, "011"):
    print("success")
else:
    print("failure")
newlist = ["1999-11-11;2014-03-10", "Jamestest", "positive","test","test","0;100","0;100","test","test"]
print(testdb.query_create(newlist))
'''
'''
if array_check_insert(["1999-11-11", "Jamestest", "positive","test","test","0","0","test","test"], '01') == True:
    print "fine"
else:
    print "not ok"

if array_check_query(["1999-11-11;1999-11-11", "Jamestest", "positive","test","test","0;0","0;0","test","test"]) == True:
    print "fine"
else:
    print "not ok"

string = "0;0"
if re.search('[a-zA-Z]',string) or string.find(';')==-1:
    print "bad"
'''

