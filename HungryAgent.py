class HungryAgent():
	def __init__(self):
		self.players_previous_points = 0
		self.colors_needed = {}
		self.routes_by_color = {}
		self.current_threshold = 0
		self.ready = False

	def decide(self, game, pnum):
		possible_moves = game.get_possible_moves(pnum)

		free_connections_graph = self.free_routes_graph(game.board.graph, game.number_of_players)
		player_edges = game.player_graph(pnum).edges()
		
		joint_graph = free_connections_graph
		for edge in player_edges:
			joint_graph.add_edge(edge[0], edge[1], weight=0, color='none', underground=False, ferries=0)
		
		list_of_cities = []
		d_points = 0
		for d in game.players[pnum].hand_destination_cards:
			list_of_cities.extend(d.destinations)
			d_points += d.points

		if possible_moves[0].function == 'chooseDestinationCards':
			best_ratio = 0
			min_over_train_requirements = game.players[pnum].number_of_trains
			best_move = None
			min_points = None
			for m in possible_moves:
				destinations = list(list_of_cities)
				temp = []
				points = d_points
				for d in m.args[1]:
					destinations.extend(d.destinations)
					points += d.points
				if min_points == None or points < min_points:
					min_points = points
					min_move = m
				destinations = list(set(destinations))
				x = generate_game_plan(destinations, joint_graph)
				fitness = float((points + x[0])) / float(x[1])
				if x[1] <= game.players[pnum].number_of_trains - 5:
					if fitness > best_ratio:
						best_ratio = fitness
						best_move = m
						croutes = x[2]
						cneeded = x[3]
				elif x[1] <= game.players[pnum].number_of_trains:
					if x[1] < min_over_train_requirements:
						min_over_train_requirements = x[1]
						best_move = m
						croutes = x[2]
						cneeded = x[3]
			if best_move == None:
				return min_move
			
			self.colors_needed = cneeded
			self.routes_by_color = croutes
			self.current_threshold = x[1]
			for i in range(0, len(game.players)):
				if i != pnum:
					self.players_previous_points += game.players[i].points

			return best_move

	def generate_game_plan(self, dkey_nodes, G):
		longest_route = None
		size_longest_route = 0

		result = {'start': set(), 'end':set()}

		for x in range(0, len(dkey_nodes)-1):
			for y in range(x+1, len(dkey_nodes)):
				temp_route_size = nx.dijkstra_path_length(G, dkey_nodes[x], dkey_nodes[y])
				if temp_route_size > size_longest_route:
					size_longest_route = temp_route_size
					#longest_route = nx.dijkstra_path(G, key_nodes[x], key_nodes[y])
					result['start'] = set([dkey_nodes[x]])
					result['end'] = set([dkey_nodes[y]])

		key_nodes = list((set(dkey_nodes) - result['start']) - result['end'])
		
		where = ''
		size_shortest_route = None

		which = []

		#routes = []
		routes_dict = {}

		total_points_from_routes = 0

		#if len(dkey_nodes) > 2:
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
		
		size_shortest_route = None
		for x in result['start']:
			for y in result['end']:
				temp_route_size = nx.dijkstra_path_length(G, x, y)
				if size_shortest_route == None or temp_route_size < size_shortest_route:
					size_shortest_route = temp_route_size
					which = [x, y]
		
		temp_path = nx.dijkstra_path(G, which[0], which[1])

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
					owned = False
					for y in G[key][x]:
						edge = G[key][x][y]
						if edge['weight'] == 0:
							owned = True
							break
						temp.append((edge['color'], edge['weight'], edge['ferries'], key, x))
					if not owned:
						double_opt.append(temp)

				else:
					if edge['weight'] > 0:
						edge = G[key][x][0]
						colors_needed[edge['color']] += edge['weight']
						colors_needed['WILD'] += edge['ferries']
						color_routes[edge['color']].append([key, x])
						total_points_from_routes += point_dict[edge['weight']]

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

		return [total_points_from_routes, sum(colors_needed.itervalues()), color_routes, colors_needed]

					
	def destinations_not_complete(self, destination_cards, graph, switzerland=False):
		result = []
		
		country_reference = {"FRANCE": ['FRANCEA', 'FRANCEB', 'FRANCEC', 'FRANCED'], "ITALIA": ['ITALIAA', 'ITALIAB', 'ITALIAC', 'ITALIAD', 'ITALIAE'], "OSTERREICH": ['OSTERREICHA', 'OSTERREICHB','OSTERREICHC'], "DEUTSCHLAND": ['DEUTSCHLANDA', 'DEUTSCHLANDB', 'DEUTSCHLANDC', 'DEUTSCHLANDD', 'DEUTSCHLANDE']}

		for card in destination_cards:
			city1, city2 = card.destinations
			solved = False
			try:
				if card.type == "city":
					if city1 in graph.nodes():
						for country in city2:
							for d in country_reference[country]:
								if d in graph.nodes():
									if nx.has_path(graph, city1, d):
										solved = True
										break
						if solved:
							break

				elif card.type == "country":
					for d1 in country_reference[city1]:
						if d1 in graph.nodes():
							for country2 in city2:
								for d2 in country_reference[country2]:
									if d2 in graph.nodes():
										if nx.has_path(graph, d1, d2):
											solved = True
											break
							if solved:
								break
					if solved:
						break
			except:
				try:
					nx.shortest_path(graph, city1, city2)
					solved = True
				except:
					solved = False

			if not solved:
				try:
					result.append({'city1': city1, 'city2': city2, 'points': card.points, 'type': card.type})
				except:
					result.append({'city1': city1, 'city2': city2, 'points': card.points})

		return result

	def free_routes_graph(self, graph, number_of_players):
		G = nx.MultiGraph()

		visited_nodes = []
		
		for node1 in graph:
			for node2 in graph[node1]:
				if node2 not in visited_nodes:
					locked = False
					for edge in graph[node1][node2]:
						if number_of_players < 4:
							if graph[node1][node2][edge]['owner'] != -1:
								locked = True

					if not locked:
						for edge in graph[node1][node2]:
							if graph[node1][node2][edge]['owner'] == -1:
								G.add_edge(node1, node2, weight=graph[node1][node2][edge]['weight'], color=graph[node1][node2][edge]['color'])

			visited_nodes.append(node1)
		
		return G