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
This is the cgi-callable pipe for basicQuery

Called by a post call with a json payload:
	{
		sourcedb:"filename",
		tablename:"tablename",
		returnlimit:500 // Optional
		query:""	
	}

Responds with a json type response from basicQuery
"""

from basicQuery import basicQuery
import sys
import json

import cgitb
import cgi

cgitb.enable()

def processPostJson():
	#print("basicQuerySite.processPostJson: Running..", file=sys.stderr)

	#query_string = sys.stdin.read()
		
	
	#querydict = json.loads(query_string)
	form = cgi.FieldStorage()
	#print("basicQuerySite.processPostJson: Read complete", file=sys.stderr)
	
	querydict = {}
	if not "sourcedb" in form:
		raise Exception("POST data missing required key 'sourcedb'")
	else:
		querydict["sourcedb"] = form["sourcedb"].value
	if not "tablename" in form:
		raise Exception("POST data missing required key 'tablename'")
	else:
		querydict["tablename"] = form["tablename"].value
	if not "query" in form:
		querydict["query"] = ""
	else:
		querydict["query"] = form["query"].value
	if not "returnlimit" in form:
		querydict["returnlimit"] = 500
	else:
		querydict["returnlimit"] = form["returnlimit"].value
	
	# add the ../data/ to the sourcedb
	querydict["sourcedb"] = "data/" + querydict["sourcedb"]
	
	#print("basicQuerySite.processPostJson: Done.", file=sys.stderr)
	return querydict
	
def queryAndResult(queryDict):
	#print("basicQuerySite.processPostJson: {}".format(queryDict), file=sys.stderr)
	
	bq = basicQuery(queryDict["sourcedb"], queryDict["tablename"], queryDict["returnlimit"])
	result = bq.query(queryDict["query"])
	return result


#print("basicQuerySite: Running..", file=sys.stderr)
response = ""
try:
	queryDict = processPostJson()
	response = queryAndResult(queryDict)
except Exception as err:
	responseDict = {}
	responseDict["Error"] = True
	responseDict["ErrorMessage"] = "{}".format(err)
	response = json.dumps(responseDict)
	
print("Content-Type: application/json")    # HTML is following
print()      
print(response)
print()
#print("basicQuerySite: Done", file=sys.stderr)

		
		 


