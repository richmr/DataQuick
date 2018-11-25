#!/usr/bin/env python3
"""
Copyright 2018 Michael R Rich (mike@tofet.net)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions 
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""
This is a basic query module for DataQuick
Called by other modules and returns a JSON object with the results of the query, as well as error codes, etc.
	{
		Error:True|False,
		ErrorMsg:"message here",
		Warning:True|False,
		WarningMsg: "warning here",
		Results: [
							// full scope objects returned in the sort order specified by query, or no particular order
							{
								field1:val1,
								field2:val2,
								...
								fieldN:valN
							},
							...,
							{
								objectN							
							}
						]
		FieldStats: {
									// This will be a list of the top 5 unique values present in that field, ordered by count
									// I've always found this super useful for exploring data
									// DocID will be ignored
									field1: [
														{TopVal1:countofVal},
														{TopVal2:countofVal},
														etc
												]
									field2: etc..
							}				
	
	}

"""

import sqlite3
from SimpleSPL import SimpleSPLparse
import json

class basicQuery:
	
	def __init__(self, sourcedb, tablename, retLimit = 500):
		# Aimed at sqlite so "sourcedb" is the filename
		self.sourcedb = sourcedb
		self.tablename = tablename
		
		# retLimit limits the number of values that are returned
		# set to False to prevent return limiting
		self.retLimit = retLimit

	def query(self, querystr):
		"""
		Accepts the query, gets the SQL statement from parser, gets the results, packages in json and returns.
		"""
		resultsDict = {}
		try:
			# initial set up			
			conn = sqlite3.connect(self.sourcedb)		
			c = conn.cursor()
			parser = SimpleSPLparse(conn, self.tablename)
			
			# parse the query
			parser.parseQuery(querystr)
			
			# run the query
			if len(parser.paramDict):
				c.execute(parser.SQLStatement, parser.paramDict)
			else:
				c.execute(parser.SQLStatement)
			
			results_raw = c.fetchall()
			if (self.retLimit):
				if (len(results_raw) > self.retLimit):
					resultsDict["Warning"] = True
					resultsDict["WarningMsg"] = 'This query found {} records but only {} have been returned.  Please change the Return Limit in settings, or add more search terms to your query.'.format(len(results_raw), self.retLimit)
					results_raw = results_raw[:self.retLimit]
			
			results = []
			# zip the results up
			column_keys = parser.getColumns()
			# PRAGMA does not return the hidden docid for a FTS
			column_keys = ["docid"]+column_keys
			for raw_result in results_raw:
				aResult = dict(zip(column_keys, raw_result))
				results.append(aResult)
				
			resultsDict["Results"] = results
		except Exception as err:
			#print("****ERROR: {}".format(err))
			resultsDict["Error"] = True
			resultsDict["ErrorMsg"] = "{}".format(err)
			
		return json.dumps(resultsDict)
		
		