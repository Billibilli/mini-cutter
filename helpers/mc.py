#!/usr/bin/python
# -*- coding: utf-8 -*-

# Minimal Cleaner v0.1 - BETA
# By Yigao Shao
#
# Usage: python mc.py [PATH]
# Example: python mc.py /home/yiago/mh2go
# 
# This is a script to clean up a website folder. 
# WARNING: ALWAYS back up your directory before performing the cleaning!
#          The safety of the script is not throughoutly verified.
#
# Idea: Delete unesscesary files by anlyzing the dependencies to index.*.
# 1) It first recurssively acquire all the file names inside PATH.
# 2) Next it would find a file in PATH begins with "index" and read it, 
#    looking for patterns matching the acquired file names. If it find some, then 
#    it will go to these files and check accordingly.
# 3) Recurssion  
# 4) File-to-be-deleted set is the complement.So just delete the remaining files in the set. 
# 5) Recursively delete the empty folders.
#
# Notice:
# 1) To prevent cyclic refenrencing, it deletes the traversed entry in the 
#    global file  storage after one trail of recurssion. 
# 2) To prevent repeated referencing, dictionary data structure are used extensively  
#
# Statics:
#      Takes 2 mins go through 1800 files and reserve 900 files.
#
# Drawbacks:
#      1) There are no built-in parser so it couldn't distinguish between comments and codes. 


import os,sys,re,time

# Setting, program won't search for dependencies with extensions matching the patterns inside non_dig_type files. 
# A possible bug exists for dependencies of inside compiled executables.  
non_dig_type=['.png','.gif','.swf','.ico','.jpg']

#----To be implemented feature in the futre
# Enable rich configuration to define the protect_rule 
#      1) If a key exists and content is not empty,then follow the rules. 
#      2) If the key exists and the content is empty, then default to protect EVERY files
#               a) type:[] means protect EVERY files so the script does nothing. 
#               b) filename:[] means protect EVERY files so the script does nothing. Same to a) 
#               c) directory:[] means protect EVERY directory even they are empty. 
#      3) If a key doesn't exist, then default behavior is to reserve minimal necessary files
#
# Example:
# protect_rule={'type':['.sh','.md','.lic','.sql','.bat','.TXT',''],'filename':['LICENSE.lic'],'directory':[phpadmin]}


#Globals

ext_set=[]
file_set={}
protect_rule={}
counter=0

def recur_trace(rootname):
	'''This is a function finding dependencies and remove them from the set list'''
	global ext_set,file_set,protect_rule,counter
	relation_tree={}
	
	file=open(rootname, 'r')
	counter=counter+1
	print "Digging ", str(counter),"  files \r",

	for line in file:
		for each in file_set.keys():
			if file_set[each][1] in line:
				relation_tree[each]={}
				file_set.pop(each, None)
	file.close()

	if relation_tree=={}:
		return {}
	else:
		for k in relation_tree.keys():
			(kfnamedummy,kfnameext)=os.path.splitext(k)
			if not (kfnameext in non_dig_type): 
				relation_tree[k]=recur_trace(k)
		return relation_tree

def removeEmptyFolders(path):
	'''This function is found online on the blog of Eneko Alonso'''
  	# remove empty subfolders
	files = os.listdir(path)
  	if len(files):
    		for f in files:
      			fullpath = os.path.join(path, f)
      			if os.path.isdir(fullpath):
        			removeEmptyFolders(fullpath)

  	# if folder empty, delete it
  	files = os.listdir(path)
  	if len(files) == 0:
    		print "Removing folders...", path
    		os.rmdir(path)

def main(argv):
	global ext_set,file_set,protect_rule,counter
	#Begin counting 
	start_time = time.time()
	#Simple parser, should be replaced with getopt
	treeroot=argv[0]
	index=''
	try:
		option=argv[1]
	except:
		option=''
	#Simple parser ends.

	#Do a little fix in order to perform the following string operation  
	if treeroot[len(treeroot)-1]!=r'/':
		treeroot=treeroot+'/'

	for (path, dirs, files) in os.walk(treeroot):
		for f in files:
			fname=os.path.join(path,f)
			(fnamepath,_fnametrunk)=os.path.split(fname)
			(fnametrunk,fnameext)=os.path.splitext(_fnametrunk)
			file_set[fname]=[fnamepath,fnametrunk,fnameext]
			if fname[0:len(treeroot+'index')]==treeroot+'index':
				index=fname
			if not (fnameext in ext_set):
				ext_set.append(fnameext)

	number_total=len(file_set)

	if option=='-e':
		print ext_set
	else:
		assert index!=''
		result=recur_trace(index)
		#print result
		for k in file_set.keys():
			print "Removing files...",k
			os.remove(k)
		removeEmptyFolders(treeroot)

	elapsed_time = time.time() - start_time 
	number_deleted=len(file_set.keys())
	print "-----------Report-----------"
	print "Time elapsed:",elapsed_time
	print "Number of files deleted:",number_deleted
	print "Number of files traversed:",counter
	print "Number of files reservered:",number_total-number_deleted
	print "Original total number of files:",number_total
	print "----------------------------"




if __name__ == "__main__":
    main(sys.argv[1:])

