#!/usr/bin/python

from sys import argv
maxR,maxS='',0.0
with open(argv[1]) as fi:
	for line in fi:
		temp=line.split()
		if float(temp[2][:-1])>maxS:
			maxS=float(temp[2][:-1])
			maxR=temp[0]
print 'Resource with maximum score = %s (score = %f)'%(maxR,maxS)
