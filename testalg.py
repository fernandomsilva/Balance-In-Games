import networkx as nx
from loadgraphfile import *

G = loadgraphfromfile('usa.txt')
key_nodes = ['KANSAS CITY', 'HOUSTON', 'DULUTH', 'SAULT ST. MARIE', 'OKLAHOMA CITY', 'WINNIPEG', 'LITTLE ROCK', 'CHICAGO', 'NEW ORLEANS', 'NASHVILLE', 'SANTA FE']

longest_route = None
size_longest_route = 0

result = {'start': set(), 'end':set()}

for x in range(0, len(key_nodes)-1):
	for y in range(x+1, len(key_nodes)):
		temp_route_size = nx.dijkstra_path_length(G, key_nodes[x], key_nodes[y])
		if temp_route_size > size_longest_route:
			size_longest_route = temp_route_size
			#longest_route = nx.dijkstra_path(G, key_nodes[x], key_nodes[y])
			result['start'] = set([key_nodes[x]])
			result['end'] = set([key_nodes[y]])

key_nodes = list((set(key_nodes) - result['start']) - result['end'])

where = ''
size_shortest_route = None

which = []

routes = []
routes_dict = {}

for x in key_nodes:
	for y in result['start']:
		temp_route_size = nx.dijkstra_path_length(G, x, y)
		if size_shortest_route == None or temp_route_size < size_shortest_route:
			size_shortest_route = temp_route_size
			which = [x, y]
			where = 'start'

	for y in result['end']:
		temp_route_size = nx.dijkstra_path_length(G, x, y)
		if size_shortest_route == None or temp_route_size < size_shortest_route:
			size_shortest_route = temp_route_size
			which = [x, y]
			where = 'end'

	result[where] = result[where] | set([x])
	temp_path = nx.dijkstra_path(G, x, y)
	routes.append(temp_path)

	for i in range(0, len(temp_path)-1):
		if temp_path[i] > temp_path[i+1]:
			temp1 = temp_path[i+1]
			temp2 = temp_path[i]
		else:
			temp1 = temp_path[i]
			temp2 = temp_path[i+1]

		if (temp1 not in routes_dict) and (temp2 not in routes_dict):
			routes_dict[temp1] = [temp2]

		elif (temp1 in routes_dict):
			if temp2 not in routes_dict[temp1]:
				routes_dict[temp1].append(temp2)
		else:
			if temp1 not in routes_dict[temp2]:
				routes_dict[temp2].append(temp1)


print routes_dict
#print result
#print result['start'] & result['end']
#print routes