from visualize import visualize
import networkx as nx
import matplotlib.pyplot as plt
from random import *
import pylab
import time
#storing the start time 
start_time = time.time()
#enabling interactive mode in pylab
pylab.ion()									
#function to display and keep the image on screen till refreshing
pylab.show()


def initialize_graph(outLinks,layout="xNotAsCentre"):
	''' This Function initializes all the parameters for a networkx graph to draw
	'''
	#creating a networkx graph
	G=nx.DiGraph()
	nodes_set=set()

 	#adding edges to graph
	x=randint(1,DATASIZE+1)
	print "Random node",x
	# Some Nodes with Good graph representations are 
	#x=56224
	#x=161658
	#x=11433
	#x=8144
	x=132517
	print "inlinks to the Random Node", len(inLinks[x])
	print "outlinks to the Random Node", len(outLinks[x])
	if layout=="xNotAsCentre":
		for i in outLinks[x]:
			for j in range(min(3,len(outLinks[i]))):
				G.add_edge(i,int(outLinks[i][j]))
				nodes_set.update([i,outLinks[i][j]])
	elif layout=="xInCentre" :
		nodes_set.add(x)
		for i in outLinks[x]:
			G.add_edge(x,i)
			nodes_set.add(i)
		for j in inLinks[x]:
			G.add_edge(j,x)	
			nodes_set.add(j)
	nodes=[int(a) for a in nodes_set]
	G.add_nodes_from(nodes)
	#layout 
	graph_pos=nx.spring_layout(G)
	return G,nodes,graph_pos


#Main driver 

#Taking input from file 
filename = "./web-Stanford.txt"
graph = []
nodeCount=set()
with open(filename, "r") as file:
	for line in file:
		graph.append(map(int,line.split()))
		nodeCount.update(map(int,line.split()))
#closing File
file.close()

#initializing DATASIZE variable according to imput file 
DATASIZE=len(nodeCount)
print "There are " + str(DATASIZE) + " nodes in the system" 
#Declaring and Initializing lists to store links 
outLinks=[[] for _ in range(DATASIZE+1)]
inLinks=[[] for _ in range(DATASIZE+1)]
for p,q in graph:
	outLinks[p].append(q)
	inLinks[q].append(p)

#Declaring and Initializing PageRank
PageRank=[[1.0/DATASIZE]*(DATASIZE+1),[[]]*(DATASIZE+1)];

#List to store DeadEnds
DeadEnds=[]
for i in range(1,DATASIZE+1):
	if len(outLinks[i])==0:
		DeadEnds.append(i)

#initializing graph		
G,nodes,graph_pos=initialize_graph(outLinks,)#"xInCentre")
print "number of nodes in the created graph", len(nodes)
print "The nodes are ", nodes

#Declaring and Initializing variables
flag=1
i=0
count=0
while flag:
	count+=1
	delta=0.0
	const_Dead=0.0;
	#Handling DeadEnds
	for k in DeadEnds:
		const_Dead+=PageRank[i][k]/DATASIZE
	for j in range(1,DATASIZE+1):
		c=0.0
		for k in inLinks[j]:
			c+= PageRank[i][k]/len(outLinks[k])\
		#Handling spidertraps	
		PageRank[1-i][j]=(c+const_Dead) * 0.85 + (0.15/DATASIZE)	
		delta+=abs(PageRank[0][j]-PageRank[1][j]) 
	i=1-i
#Displaying graph every second iteration
	if count%2 == 1:
		visualize(PageRank,G,nodes,graph_pos)
		print count
		pylab.draw()
		plt.pause(0.01)
#Checking convergence		
	flag = (delta > 0.000005)
#Final Display for 5 sec
visualize(PageRank,G,nodes,graph_pos)	
print count

print "Time of Program " + str(time.time()-start_time)

plt.pause(5)
