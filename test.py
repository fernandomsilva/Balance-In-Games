import networkx as nx

def func(G, source, list_of_visited_edges):
	temp_edges = [e for e in G.edges() if e not in list_of_visited_edges and source in e]
	if len(temp_edges) == 0:
		return 0
	else:
		result = []
		result.extend([(func(G, x, list_of_visited_edges+[(x,y)]) + G[x][y]['weight']) for (x,y) in temp_edges if source == y])
		result.extend([(func(G, y, list_of_visited_edges+[(x,y)]) + G[y][x]['weight']) for (x,y) in temp_edges if source == x])
		return max(result)

G = nx.Graph()

G.add_edge('A', 'B', weight=3)
G.add_edge('B', 'E', weight=1)
G.add_edge('B', 'G', weight=2)
G.add_edge('B', 'C', weight=4)
G.add_edge('B', 'F', weight=4)
G.add_edge('E', 'D', weight=2)
G.add_edge('E', 'G', weight=1)
G.add_edge('G', 'D', weight=1)
G.add_edge('G', 'C', weight=3)
G.add_edge('C', 'D', weight=2)

print func(G, 'A', [])
print func(G, 'B', [])
print func(G, 'C', [])
print func(G, 'D', [])
print func(G, 'E', [])
print func(G, 'F', [])
print func(G, 'G', [])