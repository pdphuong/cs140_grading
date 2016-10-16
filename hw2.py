#!/bin/python

################################################################
#To use this script:
# 1. Prepare 3 folders referred to by variables turnin_dir, given_stuffs, extract_dir
# 2. Set executing permission for the tester scripts.
# 3. Set the list of students to be graded by setting start_name, stop_name variables.
# 4. Ignore submissions (e.g. from instructor, TA) by setting variable ignore_names
# 5. Run script by issue: python hw2.py
# 6. Optional: If you want to print the list of students to be graded, change the entry point from __main__() to print_turnins()
#	at the bottom of this file.
	
#MODIFY ME!!
start_name="student_a"
stop_name="student_z"
ignore_names = ['instructor', 'ta']

#Folder consists of students' submissions
turnin_dir="/cs140a/grading/turnin_dir"
#This folder has a special structure. It consists of:
#	+ folder student_a which consists of:
#		+ file: student_a.tar.gz

#Folder consists of given test cases, makefile, tester script, etc.
#This folder has a special structure:
#For HW2, this folder consists of:
#	+ partXX folder: contains Makefile, tXXX.e, tXXX.correct, tXXX.correctStatus.
#	+ File: tester, testerAddendum, HWDesc	
given_stuffs="/cs140a/grading/given"

#Folder to which a student's submission is extracted
extract_dir="/cs140a/grading/extract_dir"
################################################################

import os
from sys import stdin

def run_cmd(cmd):
	print cmd
	if(os.system(cmd)):
		print "Error"
		return 1
	return 0

def testpart(student_name,partname):
	src_dir = os.path.join(given_stuffs, partname)
	dst_dir = os.path.join(extract_dir, student_name,partname)
	cmd="/bin/cp  --remove-destination " + src_dir + "/* " + dst_dir +"/"

	current_dir = os.getcwd()
	try:		
		if run_cmd(cmd) \
			or run_cmd("make -C %s remake"%dst_dir) \
			or os.chdir(dst_dir) \
			or run_cmd("cd %s; ../tester -m %s"%(dst_dir, partname)):

			print "%s failed"%partname
	finally:
		os.chdir(current_dir)

def getinput(prompt,expected,default):
	while(True):
		print prompt
		input=stdin.readline()
		input=input[0]
		if input =="\n": return default
		if input not in expected:
			print "Enter your choice: %s"%expected
		else:
			return input

def print_turnins():
	for dirname,subdirs, filenames in os.walk(turnin_dir):
		if dirname != turnin_dir:
			continue
		for subdir in sorted(subdirs):
			print subdir

def __main__():
	for dirname,subdirs, filenames in os.walk(turnin_dir):
		if dirname != turnin_dir:
			continue
		for subdir in sorted([subdir for subdir in subdirs if subdir >= start_name and subdir <=stop_name]):
			if subdir in ignore_names:
				continue
			#NOTE THAT subdir is also student kerberos account
			input=getinput("Grade this student y/n/c? %s"%subdir, "ync", "y")
			if input=="c": return
			if input=="n": continue

			cmd="rm -rf " + os.path.join(extract_dir) +"/*"
			run_cmd(cmd)

			os.system("touch %s"%os.path.join(extract_dir,"__"+subdir+"__"))
			cmd="mkdir " + os.path.join(extract_dir,subdir)
			run_cmd(cmd)

			#cmd="unzip -q " + os.path.join(turnin_dir,subdir, subdir + "tar.gz") + " -d " + os.path.join(extract_dir,subdir)
			cmd="tar -xzf " + os.path.join(turnin_dir,subdir, subdir + ".tar.gz") + " -C " + os.path.join(extract_dir,subdir)
			run_cmd(cmd)

			#copy tester stuffs to extracted dir
			run_cmd("cp --remove-destination " + given_stuffs + "/tester " + os.path.join(extract_dir,subdir))
			run_cmd("cp --remove-destination " + given_stuffs + "/testerAddendum " + os.path.join(extract_dir,subdir))
			run_cmd("cp --remove-destination " + given_stuffs + "/HWDesc " + os.path.join(extract_dir,subdir))
			
			test_names = ['part10','part11','part12','part13','part14','part15','part16','part17','part18','part19']
			for t in test_names:				
				input=getinput("Grade %s? y(default)/n/c? %s"%(t,subdir), "ync", "y")
				if input=="c": break
				if input=="y": testpart(subdir,t)
if __name__ == '__main__':
	__main__()
	#print_turnins()
