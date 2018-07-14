import networkx as nx
import matplotlib.pyplot as plt
import pylab
def visualize(PageRank,G,nodes,graph_pos,node_color='red', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):
	#size of node is propotional to PageRank
	node_size=[]
	for n in nodes:
		node_size.append(int(PageRank[0][n]*28200000))
	
	#Normalizing Node Sizes if they are too big 
	if max(node_size)>2000:
		x=max(node_size)
		x=x//500 + 1
		for i in range(len(node_size)):
			node_size[i]=(node_size[i]*1.0)/x  
	print "Node Sizes are", node_size
	#Drawing Graph
	nx.draw_networkx_nodes(G,graph_pos,node_size=node_size,alpha=node_alpha, node_color=node_color)
	nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,alpha=edge_alpha,edge_color=edge_color,arrows=True)
	#nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,font_family=text_font)
	return 