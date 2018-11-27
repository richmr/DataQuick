#!/usr/bin/env python3
import subprocess

def ownerTest():
	powerShellPath = r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe'
	powerShellCmd = "(get-childitem fileTree.py).GetAccessControl().Owner"

	p = subprocess.Popen([powerShellPath, powerShellCmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = p.communicate()
	rc = p.returncode
	print("Return code given to Python script is: " + str(rc))
	print("stdout: " + output.decode("utf-8"))
	print("stderr: " + error.decode("utf-8"))
	
ownerTest()

