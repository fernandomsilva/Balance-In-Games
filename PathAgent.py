import networkx as nx
import Queue

class PathAgent:
	def __init__(self):
		pass

	def decide(self, game, pnum):
		p_queue = Queue.PriorityQueue()

		list_of_destinations = self.destinations_not_complete(game.players[pnum].hand_destination_cards, game.player_graph(pnum))

		free_connections_graph = self.free_routes_graph(game.board.graph, game.number_of_players)
		player_edges = game.player_graph(pnum).edges()
		
		joint_graph = free_connections_graph
		for edge in player_edges:
			joint_graph.add_edge(edge[0], edge[1], weight=0, color='none')
		
		#print joint_graph.edges()
		
		paths_to_take = []
		for destination in list_of_destinations:
			temp = nx.shortest_path(joint_graph, destination['city1'], destination['city2'])

			for i in range(0, len(temp)-1):
				if (temp[i], temp[i+1]) not in player_edges and (temp[i+1], temp[i]) not in player_edges:
					if (temp[i], temp[i+1]) not in paths_to_take and (temp[i+1], temp[i]) not in paths_to_take:
						weight = 0
						try:
							weight = game.board.graph[temp[i]][temp[i+1]][0]['weight']
						except:
							weight = game.board.graph[temp[i]][temp[i+1]][0]['weight']

						if weight < game.players[pnum].number_of_trains:
							paths_to_take.append(((-1) * (weight + 2 * destination['points']), temp[i], temp[i+1]))
		
		for path in paths_to_take:
			p_queue.put(path)
		
		#while not p_queue.empty():
		if not p_queue.empty():
			move = p_queue.get()
			print move
			color = []
			try:
				edges = game.board.graph[move[1]][move[2]]
				for key in edges:
					color.append(game.board.graph[move[1]][move[2]][key]['color'])
			except:
				edges = game.board.graph[move[2]][move[1]]
				for key in edges:
					color.append(game.board.graph[move[2]][move[1]][key]['color'])

			print color
		#for (city1, city2) in paths_to_take:
		#	try:
		#		p_queue.
		#	except:

		#print player_edges
		print paths_to_take
		#print game.board.get_free_connection(paths_to_take[0][0], paths_to_take[0][1], 'GRAY')
		#print game.board.get_free_connection(paths_to_take[0][0], paths_to_take[0][1], 'BLACK')
		#print game.board.get_free_connection(paths_to_take[0][0], paths_to_take[0][1], 'BLUE')
		#print game.board.get_free_connection(paths_to_take[0][0], paths_to_take[0][1], 'GREEN')
		#print game.board.get_free_connection(paths_to_take[0][0], paths_to_take[0][1], 'RED')
		#print game.board.get_free_connection(paths_to_take[0][0], paths_to_take[0][1], 'ORANGE')
		#print game.board.get_free_connection(paths_to_take[0][0], paths_to_take[0][1], 'YELLOW')
		#print game.board.get_free_connection(paths_to_take[0][0], paths_to_take[0][1], 'PINK')
		#print game.board.get_free_connection(paths_to_take[0][0], paths_to_take[0][1], 'WHITE')
		
	def destinations_not_complete(self, destination_cards, graph):
		result = []

		for card in destination_cards:
			city1, city2 = card.destinations
			solved = False
			try:
				nx.shortest_path(graph, city1, city2)
				solved = True
			except:
				solved = False

			if not solved:
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
						if number_of_players < 3:
							if graph[node1][node2][edge]['owner'] != -1:
								locked = True

					if not locked:
						for edge in graph[node1][node2]:
							G.add_edge(node1, node2, weight=graph[node1][node2][edge]['weight'], color=graph[node1][node2][edge]['color'])

			visited_nodes.append(node1)
		
		return G
