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
Parses a simplified verion of SPL into SQL select statements, currently set for sqlite use.

Search terms are space-delimited and assumed OR, next term can be restricted with an AND or a NOT
Terms pre-pended by (-) are interpreted as "NOT"
Terms that are joined by standard logic operators (=, >=, <=, !=, >, <) are limiters for a specific field (and fields = columns)

"""

import sqlite3
from enum import Enum
import re

class Mode(Enum):
	SELECT = 1
	SORT = 2
	PIPE = 3
	STATS = 4

class SimpleSPLparse:
	
	def __init__(self, dbconn, tablename = "ftsdata"):
		"""
		Since this is designed with DataQuick in mind, all searches are made against a single table name, embedded
		in a single sqlite db file
		
		The db connection (sqlite3 connection instance) is required to build the generic search query against all column names
		"""
		self.tablename = tablename
		self.dbconn = dbconn
		
		# pIndex is the current parameter index, used for named parameters		
		self.pIndex = 0
		self.columns = []
				
	def getColumns(self):
		"""
		Builds and sets a list of all column names in the subject table
		This is needed to ensure field limiters (i.e. first_name:mike) don't generate sql errors by asking for columns that don't exist
		"""
		self.columns = []
		query = 'PRAGMA table_info('+self.tablename+')'
		c = self.dbconn.cursor()
		c.execute(query)
		result = c.fetchall()
		# Going to assume sqlite keeps its PRAGMA return format and column order, this could clearly cause problems later
		name_col = 1
		type_col = 2
		pk_col = 5
		self.columns = []
		for column in result:
			 self.columns.append(column[name_col])
			 
		return self.columns
		
	def checkColumn(self, column):
		"""
		returns true if the column is in the table
		"""
		# does column name exist in the table?
		if (len(self.columns) == 0):
			# Need to load the columns up
			self.getColumns()
		return (column in self.columns)
			
		
	def nextNamedParameter(self):
		# returns the text of the next named parameter and then increments
		base = "p"
		nextParameter = base + str(self.pIndex)
		self.pIndex += 1
		return nextParameter

	def logicJoin(self, theList, newElement):
		"""
		Mutates theList with the newElement appended to it.  If the element is the first then the nextLogicJoin term is ignored,
		if the element is not the first, the nextLogicJoin is appended first.  nextLogicJoin is reset to 'OR' by default
		
		"""
		if (len(theList)):
			theList.append(self.nextLogicJoin)
			theList.append(newElement)
			self.nextLogicJoin = 'OR'
			return
		
		theList.append(newElement)
		self.nextLogicJoin = 'OR'
		
	def getParamDict(self):
		# mainly for testing purposes, returns the paramDict raw
		return self.getParamDict
					
	def parseQuery(self, query):
		"""
		Select statements are structured like:
			SELECT
				docID, *  -> This returns the specific docID and all other columns for this table.  Notice assumes native sqlite FTS usage
			FROM
				tablename -> Set on init
			WHERE
				column=val
				AND/OR/NOT  -> A logical joiner, assumed to be OR unless otherwise set
											-> if there aren't any column limiters, then this section is ignored
			AND
				tablename
				MATCH
				'term1 AND term2 OR term3 ..'  -> if there are no FTS terms then this whole section is ignored (starting at the AND)
			ORDER BY
				column ASC|DESC,
				column ASC|DESC
			;
				
		This function takes the SimpleSPL and build the select statement
		"""
		self.selectList = ['SELECT', 'docID, *']
		self.fromList = ['FROM', self.tablename]
		self.whereList = []
		self.ftsStart = [self.tablename, 'MATCH']
		self.ftsTermList = []
		self.paramDict = {}
		self.orderByList = []
		# TODO: group by
		
		# Initial States
		self.nextLogicJoin = 'OR'
		self.currentMode = Mode.SELECT
		
		# begin parse
		tokens = query.split()
		for token in tokens:
			# I tried a ternary shortcut here [continue if self.columnLimiter(token) else pass] but syntax error after the continue
			if (self.columnLimiter(token)):
				continue
			if (self.ANDORNOT(token)):
				continue
			if (self.pipe(token)):
				continue
			if (self.sort(token)):
				continue
			if (self.ASCDESC(token)):
				continue
			if (self.ftsSearchTerm(token)):
				continue
					
		# Build the SQL statement
		self.SQLStatement = '\n'.join(self.selectList)
		self.SQLStatement += '\n'+'\n'.join(self.fromList)
		if (len(self.whereList) or len(self.ftsTermList)):
			self.SQLStatement += '\nWHERE\n'
			self.SQLStatement += '\n'.join(self.whereList)+'\n'
		if (len(self.ftsTermList)):
			ftsTermParam = self.nextNamedParameter()
			self.ftsStart.append(':'+ftsTermParam)
			# need an additional AND if there were column search terms
			if (len(self.whereList)):
				self.SQLStatement += 'AND\n'
			self.SQLStatement += '\n'.join(self.ftsStart)
			# The parameters from fts form a long string parameter, not direct into the SQL statement
			ftsSearchTermStr = " ".join(self.ftsTermList)
			self.paramDict = {**self.paramDict, **{ftsTermParam:ftsSearchTermStr}}
		if (len(self.orderByList)):
			# pop the last trailing , off
			self.orderByList.pop()
			self.SQLStatement += '\nORDER BY\n'
			self.SQLStatement += '\n'.join(self.orderByList)+'\n'
		self.SQLStatement += ';'
			
		#Parse done, data stored in class variables
		return
		

			
#------------- Parsing functions ------------
# These should all take a token and return a boolean value if the token was processed
# If processed, the proper values are stored in the proper select statement groups, with the proper logical joins

	def columnLimiter(self, token):
		# Column limiter only active in select mode
		if (self.currentMode != Mode.SELECT):
			return False
			
		regex = r"(\w+)(>=|<=|!=|>|<|=)(\w+)"
		found = re.findall(regex, token)
		if (len(found)):
			paramStr = self.nextNamedParameter()
			column = found[0][0]
			operator = found[0][1]
			value = found[0][2]
			
			if not self.checkColumn(column):
				raise NameError('select: There is no field named "'+column+'" in this database.')
				
			retString = column + operator + ":" + paramStr
			self.logicJoin(self.whereList, retString)
			retDict = {paramStr:value}
			self.paramDict = {**self.paramDict, **retDict}
			return True
			
		return False
		
	def ANDORNOT(self, token):
		regex = r"(^AND$|^OR$|^NOT$)"
		found = re.findall(regex, token, re.IGNORECASE)
		if (len(found)):
			self.nextLogicJoin = found[0].upper()
			return True
		
		return False
		
	def ftsSearchTerm(self, token):
		# Column limiter only active in select mode
		if (self.currentMode != Mode.SELECT):
			return False
		# check for the ignore symbol ("-" prepended to the term)
		regex = r"-(.+)"
		found = re.findall(regex, token)
		if (len(found)):
			self.nextLogicJoin = 'NOT'
			token = found[0]
		self.logicJoin(self.ftsTermList, token)
		return True

	def pipe(self, token):
		if (token == '|'):
			self.currentMode = Mode.PIPE
			return True
		return False
		
	def sort(self, token):
		# sort token needs to be preceded immediately by a pipe
		if (self.currentMode == Mode.PIPE):
			regex = r"sort\((.+)\)"
			found = re.findall(regex, token, re.IGNORECASE)
			if (len(found)):
				column = found[0]
				if not self.checkColumn(column):
					raise NameError('sort: There is no field named "'+column+'" in this database.')
				self.orderByList.append(column)
				self.orderByList.append(",")
				self.currentMode = Mode.SORT
				return True
		
		return False
		
	def ASCDESC(self, token):
		if (self.currentMode == Mode.SORT):
			regex = r"(^asc$|^desc$)"
			found = re.findall(regex, token, re.IGNORECASE)
			if (len(found)):
				# remove the last trailing comma
				self.orderByList.pop()
				self.orderByList.append(found[0].upper())
				self.orderByList.append(",")
				self.currentMode = Mode.PIPE
				return True
		
		return False


		
			
			

