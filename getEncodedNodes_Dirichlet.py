#!/usr/bin/python
from mrjob.protocol import JSONProtocol
def encode_node(node_id, links=None, score=1):
	node = {}
	if links:
		node['links'] = sorted(links.items())
	node['score'] = score
	x=JSONProtocol()
	return x.write(node_id, node) + '\n'
	
if __name__=='__main__':
	from random import choice
	from sys import argv
	from numpy import ones,random
	d={}
	with open(argv[1],'r') as fi:
		for line in fi:
			link=line.split()
			d[link[0]]=d.get(link[0],[])+[link[2]]

	with open ('result.txt','w') as fo:
		for key in d:
			temp={}
			randValues=random.dirichlet(ones(len(d[key])),size=1).tolist()[0]
			for val in d[key]:
				elem=choice(randValues)
				temp[val]=(val,elem)
				randValues.remove(elem)
			fo.write(encode_node(key,temp))
	

