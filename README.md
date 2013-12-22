PageRank implementation using mrJOB
===================================
##What is [Pagerank](http://en.wikipedia.org/wiki/PageRank)?
PageRank algorithm was created by the founders of Google and it serves as the backbone (underlying algorithm) of the Google search engine. It allocates a weight (a.k.a. pagerank) to every page that is crawled by the search engine. This weight is directly proportionate to the relevance given (to the associated page) by Google search - a page with a higher pagerank value is considered to be more relevant and is ranked higher in the searches. These weights are computed by iterations and each iteration's completion is contingent upon the number of pages involved - this bit would be more palpable from running the provided code. With the exceptionally large amount of data that needs to be crunched in order for this algorithm to work as desired, it is necessary to adopt a system which enables to do just that, in a time-efficient manner - [Hadoop](http://strata.oreilly.com/2011/01/what-is-hadoop.html) based implementation.

[Really nice explanation of PageRank](http://pr.efactory.de/e-pagerank-algorithm.shtml)

##What is [mrJOB](https://github.com/Yelp/mrjob)?
mrJOB is a Python package (created by Yelp) which can be used for writing [Hadoop streaming](http://hadoop.apache.org/docs/r1.1.2/streaming.html) jobs. It's a really neat / simple tool for writing map / reduce jobs in Python. I suppose you ought to have Python 2.5 and above to run this package. One can go about running tasks locally (i.e. on your machine) / on Hadoop (in pseudo-distributed mode / clustered mode) / on [Amazon's Elastic MapReduce](http://aws.amazon.com/elasticmapreduce/) very conveniently - by just changing couple of command line arguments!

##Dataset
Data used for this experiment has been derived from [DBpedia](http://dbpedia.org/About). Wikipedia pages can be thought of as a rich source for modeling a networked structure from - each page has multiple outbound links (e.g. **See Also**,**References**,**Notes** sections).

[[Download sample dataset]](http://downloads.dbpedia.org/3.9/id/page_links_id.nt.bz2)

##Setup
1. Python 2.7 ([Get Python](http://www.python.org/download/releases/2.7/))
2. pip ([Get pip](https://pypi.python.org/pypi/pip))
3. Open **Terminal**. *Run* `sudo pip install mrjob`
4. If you intend for the outbound links (of pages) to have a Dirichlet distribution: [Get numpy](http://www.scipy.org/install.html)

##Experiment
###Running pagerank algorithm on wikipedia's dataset

1. Move the extracted dataset, \*.py files to a new folder.
2. Open **Terminal**, change the *cwd* to the newly created folder. *Run* `python getEncodedNodes.py <dataset_name>`

	If you intend your outbound links to have Dirichlet distribution, *Run* `python getEncodedNodes_Dirichlet.py <dataset_name>`


**To run experiment locally -**

1. From **Terminal**, *Run* `python pagerank.py path_of_'result.txt'`

**To run experiment on Hadoop -**

1. Ensure that Hadoop (pseudo-distributed mode / clustered mode) is setup on your system. If not,

	1. I'd suggest you download [Hadoop 1.2.1](http://mirror.cc.columbia.edu/pub/software/apache/hadoop/common/hadoop-1.2.1/hadoop-1.2.1-bin.tar.gz).
	2. Setup Hadoop in desired mode - [Pseudo-distributed setup](http://hadoop.apache.org/docs/r1.2.1/single_node_setup.html),[Cluster setup](http://hadoop.apache.org/docs/r1.2.1/cluster_setup.html)

2. Before running the code, you would have to transfer the extracted dataset to HDFS. 

	For pseudo-distributed setup, From **Terminal**, run `~/hadoop-1.2.1/bin/hadoop dfs -copyFromLocal path_of_'result.txt' /input`

3. From **Terminal**, run `python pageRank.py -r hadoop hdfs:////input >out`

**To run code on Elastic MapReduce -**

1. Ensure that you have the following : an AWS account setup, signed up for EMR service, EMR configuration file (on your system). [If not](http://pythonhosted.org/mrjob/guides/emr-quickstart.html#configuring-aws-credentials).

2. If your input file is:

	In HDFS: From **Terminal**, run `python pageRank.py -r emr hdfs:////input >out`

	Stored locally: From **Terminal**, run `python pageRank.py -r emr path_of_'result.txt' >out`

The output of the experiment will be stored in a file named *out*.


####To find out the page with the highest pageRank score :

From **Terminal**, run `python getMaxNode.py out`


####To change number of iterations / mappers-reducers :

1.	python pageRank.py -r hadoop hdfs:////input --jobconf **mapred.map.tasks=numberOfMappers** --jobconf **mapred.reduce.tasks=numberOfReducers** > out
	
**e.g.** `python pageRank.py -r hadoop hdfs:////input --jobconf mapred.map.tasks=5 --jobconf mapred.reduce.tasks=10 > out`
	
2. python pageRank.py -r hadoop hdfs:////input **--iterations=numberOfIterations** > out
	
**e.g.** `python pageRank.py -r hadoop hdfs:////input --iterations=5 > out`