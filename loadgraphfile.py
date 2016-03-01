import networkx as nx
import re

import matplotlib.pyplot as plt

def loadgraphfromfile(filename):
	file = open(filename, 'r')
	line = file.readline()

	G = nx.Graph()

	while len(line.strip()) > 0:
		G.add_node(line.strip())
		line = file.readline()

	line = file.readline()
	while len(line.strip()) > 0:
		index = re.search('\d', line).start()
		index_space = line[index+2:].index(' ')
		color = line[index+2:index+2+index_space]
		#print line[index+2:index+2+index_space]]
		node1 = line[:index].strip() if (line[:index].strip())[-1] != ' ' else line[:index-1].strip()
		node2 = line[index+2+index_space:].strip() if (line[index+2+index_space:].strip())[-1] != ' ' else (line[index+2+index_space:].strip())[:-1]
		G.add_edge(node1, node2, weight=int(line[index]), color=color)
		line = file.readline()

	for e in G.edges():
		G[e[0]][e[1]]['owner'] = -1
		#e['owner'] = -1

	#print G.edges()

	nx.draw(G, with_labels=True)
	plt.show()

	return G

	#for node in G.nodes():
	#	print node

	#print(G.nodes())
	#print(G.edges())
#loadgraphfromfile('usa.txt')