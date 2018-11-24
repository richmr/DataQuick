#!/usr/bin/env python3

from SimpleSPL import SimpleSPLparse
import sqlite3

conn = sqlite3.connect('../data/test.db')
c = conn.cursor()
pt = SimpleSPLparse(conn, 'ftstest')

def test1():
	pt.getColumns()
	print(pt.columns)

def test2():
	pt.parseQuery("stan")
	execandfetch()
		
def execandfetch():
	print(pt.SQLStatement)
	print(pt.paramDict)
	if len(pt.paramDict):
		c.execute(pt.SQLStatement, pt.paramDict)
	else:
		c.execute(pt.SQLStatement)
	
	print(c.fetchall())

def test3():
	pt.parseQuery("")
	execandfetch()	

def test4():
	pt.parseQuery("stan -mike")
	execandfetch()				

def test5():
	pt.parseQuery("first_name:mike")
	execandfetch()		

def test6():
	pt.parseQuery("given_name:mike")
	execandfetch()
#------------- Tests ---------------------
#print(test.columnLimiter("bobyouruncle", Mode.SELECT))
#print(test.ANDORNOT("bobyouruncle", Mode.SELECT))
#print(test.ANDORNOT("and", Mode.SELECT))
#print(test.ANDORNOT("NOT", Mode.SELECT))
#test.parseQuery("");
#test.parseQuery("Windows -temp")
#test.parseQuery("Windows -temp name:bob AND occupation:plumber house:apartment")
#pt.parseQuery("name:bob AND occupation:plumber NOT house:apartment")
#pt.parseQuery("Windows -temp")
#print(pt.SQLStatement)
#print(pt.paramDict)
test6()


print("done")
