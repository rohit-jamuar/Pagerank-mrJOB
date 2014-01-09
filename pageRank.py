#!/usr/bin/python
from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

class MRPageRank(MRJob):

    INPUT_PROTOCOL = JSONProtocol  # read the same format we write

    def configure_options(self):
        super(MRPageRank, self).configure_options()

        self.add_passthrough_option(
            '--iterations', dest='iterations', default=10, type='int',
            help='number of iterations to run')

        self.add_passthrough_option(
            '--damping-factor', dest='damping_factor', default=0.85,
            type='float',
            help='probability a web surfer will continue clicking on links')

    def map_task(self, node_id, node):
        
        yield node_id, ('node', node)
	
	if 'links' in node:
	        for dest_id, weight in node.get('links'):
	        	if type(weight)==list:
		        	yield dest_id, ('score', node['score'] * weight[1])
		        else:
		        	yield dest_id, ('score', node['score'] * weight)

    def reduce_task(self, node_id, typed_values):
       
        node = {}
        total_score = 0
	prevScoreSet=False
        for value_type, value in typed_values:
            if value_type == 'node':
                node = value
                if not prevScoreSet:
	                node['prev_score'] = node['score']
	                prevScoreSet=True
            elif value_type == 'score':
		total_score += value
	    else:
	    	raise Excpetion("Fishy business!!")
		
        d = self.options.damping_factor
        node['score'] = 1 - d + d * total_score
	
        yield node_id, node

    def steps(self):
        return ([self.mr(mapper=self.map_task, reducer=self.reduce_task)] *
                self.options.iterations)


if __name__ == '__main__':
   	MRPageRank.run()

