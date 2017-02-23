from ttroptimized import *
import networkx as nx
import operator

class OneStepThinkerAgent:
	def __init__(self):
		self.current_objective_route = #
		self.current_objective_color = #
		self.current_grand_objective = {}
		self.players_previous_points = 0

	def decide(self, game, pnum):
		possible_moves = game.get_possible_moves(pnum)

		if possible_moves[0].function == 'chooseDestinationCards':
			for m in possible_moves:
				#if len(m.args[1]) == 3:
				if len(m.args[1]) == game.destination_deck_draw_rules[0]:
					#print 'd'
					return m

		total_current_points = 0
		for i in range(0, len(game.players)):
			total_current_points += game.players[i].points

		if self.players_previous_points < total_current_points:
			#x = self.generate_game_plan(list_of_cities, joint_graph)
			#self.colors_needed = x[3]
			#self.routes_by_color = x[2]
			self.players_previous_points = total_current_points


	def generate_game_plan(self, game, pnum):
		#shortest path between destinations - 1 destination at a time
		#connect destination edges
		#get long routes
		joint_graph = self.joint_graph(game, pnum)
		city1 = None
		city2 = None
		color = None

		dict_of_destinations = destinations_not_completed(game, pnum)
		if dict_of_destinations:
			most_valuable_route = max(dict_of_destinations.iteritems(), key=operator.itemgetter(2))[0]
			result = self.chooseNextRouteTarget(self, game, graph, most_valuable_route['city1'], most_valuable_route['city2'])
			if result != False:
				city1, city2, color = result
		if city1 == None:
			if #connect destination edges


	def destinations_not_completed(self, game, pnum)
		result = {}
		graph = game.player_graph(pnum)

		destination_cards = game.players[pnum].hand_destination_cards
		for card in destination_cards:
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

	def joint_graph(self, game, pnum):
		free_connections_graph = self.free_routes_graph(game.board.graph, game.number_of_players)
		player_edges = game.player_graph(pnum).edges()
		
		joint_graph = free_connections_graph
		for edge in player_edges:
			joint_graph.add_edge(edge[0], edge[1], weight=0, color='none')

		return joint_graph

	def chooseNextRouteTarget(self, game, graph, city1, city2):
		try:
			list_of_route_nodes = nx.shortest_path(graph, city1, city2)
		except:
			return False

		list_of_colors = set()
		cities = []
		for i in range(0, len(list_of_route_nodes)-1):
			for j in range(i+1, len(list_of_route_nodes)):
				cities = [i, j]
				for key in graph[i][j]:
					edge = graph[i][j][key]

					if edge['owner'] != -1:
						list_of_colors = []
						cities = []
						break

					list_of_colors.add(edge['color'])
				if len(cities) != 0:
					break
			if len(cities) != 0:
				break

		color_weight = []
		for color in list_of_colors:
			color_weight.append(game.players[pnum].hand[color])

		max_weight = color_weight.index(max(color_weight))
		desired_color = color_weight[max_weight]

		return [cities[0], cities[1], desired_color]
