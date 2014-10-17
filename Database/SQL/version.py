#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2 as mdb
import sys

con = None

con = mdb.connect(host = 'db-new.doc.ic.ac.uk', database = 'ng1513', user = 'ng1513', password = 'MalariaTeam2014')
cur = con.cursor()
cur.execute("SELECT VERSION()")

ver = cur.fetchone()

print "Database version : %s " % ver
    
