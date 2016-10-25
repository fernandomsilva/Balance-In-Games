class HungryAgent():
	def __init__(self):
		pass

	def decide(self, game, pnum):
		possible_moves = game.get_possible_moves(pnum)

		free_connections_graph = self.free_routes_graph(game.board.graph, game.number_of_players)
		player_edges = game.player_graph(pnum).edges()
		
		joint_graph = free_connections_graph
		for edge in player_edges:
			joint_graph.add_edge(edge[0], edge[1], weight=0, color='none')



		if possible_moves[0].function == 'chooseDestinationCards' and game.players_choosing_destination_cards:
			for m in possible_moves:
				if len(m.args[1]) == game.destination_deck_draw_rules[0]:
					return m

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