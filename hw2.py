#!/bin/python

start_name="mlhe" #"acdt93"
stop_name="mlhe" #"zijianch"
ignore_names = ['olsson']

turnin_dir='/home/pdphuong/pl/F2016/grading_hw2/hw_dir' #"/home/pdphuong/ecs140a/hw2/ecs140a_hw2/"
extract_dir="/home/pdphuong/pl/F2016/grading_hw2/sample_dir"
given_stuffs="/home/pdphuong/pl/F2016/grading_hw2/tests_dir"


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
