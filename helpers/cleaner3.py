#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys,re

# Setting, for program won't search for dependencies inside non_dig_type files. 
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

	global ext_set,file_set,protect_rule,counter
	relation_tree={}
	
	file=open(rootname, 'r')
	counter=counter+1
	print "Digging", str(counter),"  files \r",

	for line in file:
		for each in file_set.keys():
			if file_set[each][1]+file_set[each][2] in line:
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
def main(argv):
	global ext_set,file_set,protect_rule

	#Simple parser, should be replaced with getopt
	treeroot=argv[0]
	index='index'
	try:
		option=argv[1]
	except:
		option=''
	#Simple parser ends.

	#Do a little fix for the inputing path in order to perform the following string operation  
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

	if option=='-e':
		print ext_set
	else:
		result=recur_trace(index)
		print result
		for k in file_set.keys():
			os.remove(k)

if __name__ == "__main__":
    main(sys.argv[1:])

