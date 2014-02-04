#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys,re

phprule=["src\s*=\s*'(.*)'",
	 'src\s*=\s*"(.*)"',
         "href\s*=\s*'(.*)'",
         'href\s*=\s*"(.*)"',
         "require\s*\(\s*'(.*)'\s*\)",
         'require\s*\(\s*"(.*)"\s*\)',
	 "require_once\s*\(\s*'(.*)'",
         'require_once\s*\(\s*"(.*)"',
	 "include\s*\(\s*'(.*)'",
	 'include\s*\(\s*"(.*)"',
         "include_once\s*\(\s*'(.*)'",
         'include_once\s*\(\s*"(.*)"']

htmlrule=phprule
jsrule=phprule

digset={'php':phprule,'js':jsrule,'html':htmlrule,'htm':htmlrule}
protectset=['sh','txt','lic']


def main(argv):
	treeroot=argv[0]
	outputdir=argv[1]
	print treeroot,outputdir
	file=open(treeroot, 'r')
	for line in file:
		for eachrule in phprule:
			child=re.findall(eachrule,line)
			if child:
				print child 
	file.close()

if __name__ == "__main__":
    main(sys.argv[1:])

