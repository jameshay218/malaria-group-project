#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2 as mdb
import sys

try:
    con = mdb.connect(database = 'jah113', host = 'db.doc.ic.ac.uk', password = 'raA2ngaDjf', user = 'jah113');

    cur = con.cursor()
    cur.execute("CREATE TABLE cars(id INT PRIMARY KEY, name VARCHAR(20), price INT)")
    cur.execute("INSERT INTO cars VALUES(1,'Audi',52642)")
    cur.execute("INSERT INTO cars VALUES(2,'Mercedes',57127)")
    cur.execute("INSERT INTO cars VALUES(3,'Skoda',9000)")
    cur.execute("INSERT INTO cars VALUES(4,'Volvo',29000)")
    cur.execute("INSERT INTO cars VALUES(5,'Bentley',350000)")
    cur.execute("INSERT INTO cars VALUES(6,'Citroen',21000)")
    cur.execute("INSERT INTO cars VALUES(7,'Hummer',41400)")
    cur.execute("INSERT INTO cars VALUES(8,'Volkswagen',21600)")

    con.commit()

except mdb.DatabaseError, e:

    if con:
        con.rollback()
        
    print 'Error %s' % e
    sys.exit(1)

finally:
    if con:
        con.close()
