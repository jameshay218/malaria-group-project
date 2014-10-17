#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2 as mdb
con = mdb.connect(host = 'db-new.doc.ic.ac.uk', database = 'ng1513', user = 'ng1513', password = 'MalariaTeam2014')
print 'Connected'
cur = con.cursor()
cur.execute("SELECT * FROM malariamain;")

rows = cur.fetchall()

for row in rows:    
    print row
