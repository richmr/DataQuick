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
Builds a file tree and stores it in a sqlite db for additional work
Includes:
	- filename
	- full path
	- file size
	- access date
	- creation date
	- modification date
	- owner

"""

import sqlite3
import os
if os.name != 'nt':
	import pwd
else:
	import subprocess


class fileTree:
	
	def __init__(self, rootStart="/", dbname="fileTree.db"):
		self.rootStart = rootStart
		self.dbname = dbname
	
	def winOwner(self, fullpath):
		# Returns the owner of an object using Windows Powershell
		# obviously this only works on Windows
		if (os.name != 'nt'):
			return "N/A"
		
		powerShellPath = r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe'
		powerShellCmd = "(get-childitem {}).GetAccessControl().Owner".format(fullpath)

		p = subprocess.Popen([powerShellPath, powerShellCmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output, error = p.communicate()
		rc = p.returncode
		#print("Return code given to Python script is: " + str(rc))
		#print("stdout: " + output.decode("utf-8"))
		#print("stderr: " + error.decode("utf-8"))
		return output.decode("utf-8").strip()
	
	def makedb(self):
		# Open db in the current working directory
		conn = sqlite3.connect(self.dbname)
		c = conn.cursor()
		
		# Make the table
		createStatement = "CREATE VIRTUAL TABLE filesysdata USING fts3(filename, path, filesize, access_time, mod_time, create_time, owner);" # size, creation_date, creation_time, modification_date, modification_time, owner);"
		c.execute(createStatement)
		
		# Populate it
		insertStatement = "INSERT INTO filesysdata(filename, path, filesize, access_time, mod_time, create_time, owner) VALUES (:filename, :path, :filesize, :access_time, :mod_time, :create_time, :owner)"
		
		filecount = 0
		
		# for efficiently converting uid to usernames in an environment with lots of users
		userDict = {}
		
		for root, dirs, files in os.walk(self.rootStart):
			for filename in files:
				# start with clear paramDict
				paramDict = {}
				paramDict["filename"] = filename
				
				fullpath = os.path.join(root, filename)
				paramDict["path"] = root
				
				filestats = os.stat(fullpath)
				
				# Owner
				if (os.name != 'nt'):
					if not filestats.st_uid in userDict:
						userDict[filestats.st_uid] = pwd.getpwuid(filestats.st_uid).pw_name
					paramDict["owner"] = userDict[filestats.st_uid]
				else:
					paramDict["owner"] = self.winOwner(fullpath)
				
				# filesize
				paramDict["filesize"] = filestats.st_size
				
				# access_time
				paramDict["access_time"] = filestats.st_atime
				
				# mod_time
				paramDict["mod_time"] = filestats.st_mtime
				
				# create time
				paramDict["create_time"] = filestats.st_ctime
				
				c.execute(insertStatement, paramDict)
				filecount += 1
				conn.commit()
		
				
		# print("{} files inserted into database".format(filecount))
		
		
		