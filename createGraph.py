#!/usr/bin/python
import community
import networkx as nx
import matplotlib.pyplot as plt

graph={}
topic_words={}

def readGraph():
	f=open('../aan/release/2013/acl.txt', 'r')
	lines=f.readlines()
	for line in lines:
		line=line.rstrip('\n')
		ids=line.split(" ==> ")
		if ids[0] in graph:
			graph[ids[0]].append(ids[1])
		else:
			graph[ids[0]]=[]
			graph[ids[0]].append(ids[1])

		if ids[1] in graph:
			graph[ids[1]].append(ids[0])
		else:
			graph[ids[1]]=[]
			graph[ids[1]].append(ids[0])


def detectComm(G):
	partition = community.best_partition(G)
	size = float(len(set(partition.values())))
	pos = nx.spring_layout(G)
	count = 0.
	for com in set(partition.values()) :
	    count = count + 1.
	    list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
	    print "*********"
	    print "Community ",com
	    print list_nodes
	    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20, node_color = str(count / size))

	nx.draw_networkx_edges(G,pos, alpha=0.5)
	plt.show()


def createCommunityGraph(nodes):
	l2=nodes
	commGraph={}
	for node in nodes:
		if node in graph:
			l1=graph[node]
			adjList=list(set(l1)&set(l2))
			commGraph[node]=adjList
	G=nx.Graph()
	G.add_nodes_from(commGraph.keys())
	for node in commGraph.items():
		vertex,nodeList=node
		for n in nodeList:
			G.add_edge(vertex, n);

	detectComm(G)

def loadTopics():
	f=open('topic_names.txt','r')
	lines=f.readlines()
	i=0
	for line in lines:
		line=line.rstrip('\n')
		if i==92 or i==88 or i==72:
			i+=1
			continue
		topic_words[i]=line
		i+=1

def print_topic():

	print
	print "######################\t Topic Top word table\t#############################"
		

	for k,v in topic_words.items():
		print "| topic ",k,": ",v 

	print "##########################################################################################"
	print	



def listTopics():
	loadTopics()
	while 1:

		print "1. List Topic top words"
		print "2. Select topic number"
		print "3. exit"

		option = input()

		if option == 1:
			print_topic()

		elif option == 2: 
			print "Enter Topic number: "
			ntopic=raw_input()
			createCommunityGraph(subfield_map[int(ntopic)])

		else:
			print "Thank you"
			break




readGraph()

f=open('lda_res1.txt','r')
fdata=f.readlines()
f.close()
unwanted = [92,88,44]
subfield_map = {}
for data in fdata:
	#print data
	tlist=data.strip('\n').split('|')
	doc_name=tlist[0].split('.')[0]
	#print len(tlist)
	if len(tlist) <= 2:
		continue 

	prob=0
	subfield=-1
	#print maxdoc,prob
	for i in range(1,len(tlist)):
		curlist=tlist[i].strip('(').strip(')').split(',')
		cur_subfield=int(curlist[0])
		if cur_subfield in unwanted:
			continue

		cur_prob=float(curlist[1])
		if cur_prob > prob:
			prob=cur_prob
			subfield=cur_subfield
	#print subfield,doc_name	

	if subfield in subfield_map:
		subfield_map[subfield].append(doc_name)
	else:
		dlist = []
		dlist.append(doc_name)
		subfield_map[subfield]=dlist

listTopics()