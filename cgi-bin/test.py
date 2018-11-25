#!/usr/bin/env python3

from SimpleSPL import SimpleSPLparse
from fileTree import fileTree
import sqlite3
from basicQuery import basicQuery

#conn = sqlite3.connect('../data/test.db')
#c = conn.cursor()
#pt = SimpleSPLparse(conn, 'ftstest')

conn = sqlite3.connect('../data/fileTree.db')
c = conn.cursor()
pt = SimpleSPLparse(conn, "filesysdata")

def test1():
	pt.getColumns()
	print(pt.columns)

def test2():
	pt.parseQuery("stan")
	execandfetch()
		
def execandfetch():
	#print(pt.SQLStatement)
	#print(pt.paramDict)
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
	pt.parseQuery("first_name=mike")
	execandfetch()
	pt.parseQuery("first_name!=mike")
	execandfetch()	
	pt.parseQuery("first_name>mike")
	execandfetch()
	pt.parseQuery("first_name<mike")
	execandfetch()
	pt.parseQuery("first_name>=mike")
	execandfetch()		

def test6():
	pt.parseQuery("given_name=mike")
	execandfetch()
	
def test7():
	ft = fileTree(".", "../data/fileTree.db")
	ft.makedb()
	
def test8():
	pt.parseQuery(".py")
	execandfetch()
	
def test9():
	bq = basicQuery('../data/fileTree.db', "filesysdata")
	result = bq.query("")
	print(result)

def test10():
	bq = basicQuery('../data/fileTree.db', "filesysdata", 3)
	result = bq.query("")
	print(result)	
	
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
test10()


print("done")
