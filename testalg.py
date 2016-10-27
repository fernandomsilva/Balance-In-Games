import networkx as nx
from loadgraphfile import *
from loaddestinationdeck import *
import random
import itertools

def generate_game_plan(key_nodes, G):
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

	#routes = []
	routes_dict = {}

	total_points_from_routes = 0

	if len(key_nodes) > 2:
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
			temp_path = nx.dijkstra_path(G, x, which[1])
			#routes.append(temp_path)

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

		lost = None
		if len(result['start']) == 1:
			lost = list(result['start'])[0]
		elif len(result['end']) == 1:
			lost = list(result['end'])[0]

		if lost != None:
			size_shortest_route = None

			for x in key_nodes:
				if x != lost:
					temp_route_size = nx.dijkstra_path_length(G, lost, x)
					if size_shortest_route == None or temp_route_size < size_shortest_route:
						size_shortest_route = temp_route_size
						which = x

			temp_path = nx.dijkstra_path(G, lost, which)

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
	else:
		temp_path = nx.dijkstra_path(G, list(result['start'])[0], list(result['end'])[0])

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

	colors_needed = {"BLUE": 0, "GREEN": 0, "RED": 0, "PINK": 0, "ORANGE": 0, "BLACK": 0, "YELLOW": 0, "WHITE": 0, "GRAY": 0, "WILD": 0}
	color_routes = {"BLUE": [], "GREEN": [], "RED": [], "PINK": [], "ORANGE": [], "BLACK": [], "YELLOW": [], "WHITE": [], "GRAY": []}
	double_opt = []
	point_dict = {1:1, 2:2, 3:4, 4:7, 5:10, 6:15, 8:21, 9:27}

	for key in routes_dict:
		for x in routes_dict[key]:
			if len(G[key][x].keys()) > 1:
				temp = []
				for y in G[key][x]:
					edge = G[key][x][y]
					temp.append((edge['color'], edge['weight'], edge['ferries'], key, x))
				double_opt.append(temp)

			else:
				edge = G[key][x][0]
				colors_needed[edge['color']] += edge['weight']
				colors_needed['WILD'] += edge['ferries']
				color_routes[edge['color']].append([key, x])
				total_points_from_routes += point_dict[edge['weight']]

	#print colors_needed

	for edge_list in double_opt:
		min_val = 0
		max_color = None
		temp = None
		flag = False
		for (color, weight, ferries, city1, city2) in edge_list:
			if colors_needed[color] == 0:
				colors_needed[color] += weight
				colors_needed['WILD'] += ferries
				color_routes[color].append([city1, city2])
				total_points_from_routes += point_dict[weight]
				flag = True
				break
			else:
				if max_color == None or colors_needed[color] < min_val:
					max_color = color
					min_val = colors_needed[color]
					temp = (color, weight, ferries, city1, city2)

		if not flag:
			colors_needed[temp[0]] += temp[1]
			colors_needed['WILD'] += temp[2]
			color_routes[temp[0]].append([temp[3], temp[4]])
			total_points_from_routes += point_dict[weight]


	#print total_points_from_routes
	#print sum(colors_needed.itervalues())

	return [total_points_from_routes, sum(colors_needed.itervalues()), color_routes, colors_needed]

	#print routes_dict
	#print result
	#print result['start'] & result['end']
	#print routes

dest_deck = loaddestinationdeckfromfile('usa_destinations.txt')
G = loadgraphfromfile('usa.txt')

list_dest = []

for i in range(0, 3):
	card = random.choice(dest_deck)
	dest_deck.remove(card)
	list_dest.append(card)

combinations = []

for i in range(1, 4):
	comb = itertools.combinations(list_dest, i)
	for c in comb:
		combinations.append(c)

best_ratio = 0
best_dest = None
croutes = None
cneeded = None

for c in combinations:
	destinations = []
	temp = []
	points = 0
	for d in c:
		temp.append(d)
		destinations.extend(d.destinations)
		points += d.points
	destinations = list(set(destinations))
	x = generate_game_plan(destinations, G)
	fitness = float((points + x[0])) / float(x[1])
	if fitness > best_ratio:
		best_ratio = fitness
		best_dest = temp
		croutes = x[2]
		cneeded = x[3]

for d in best_dest:
	print d.destinations

print croutes


#key_nodes = ['KANSAS CITY', 'HOUSTON', 'DULUTH', 'SAULT ST. MARIE', 'OKLAHOMA CITY', 'WINNIPEG', 'LITTLE ROCK', 'CHICAGO', 'NEW ORLEANS', 'NASHVILLE', 'SANTA FE']
