import networkx as nx
import Queue

class PathAgent:
	def __init__(self):
		pass

	def decide(self, game, pnum):
		p_queue = Queue.PriorityQueue()

		list_of_destinations = self.destinations_not_complete(game.players[pnum].hand_destination_cards, game.player_graph(pnum))

		#path_to_take = []
		#for destination in list_of_destinations:
		free_connections_graph = self.free_routes_graph(game.board.graph, game.number_of_players)
		print free_connections_graph.edges()

		#print list_of_destinations

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

		for node1 in graph:
			for node2 in graph[node1]:
				locked = False
				for edge in graph[node1][node2]:
					print edge
					if number_of_players < 3:
						if graph[node1][node2][edge]['owner'] != -1:
							locked = True

				if not locked:
					for edge in graph[node1][node2]:
						G.add_edge(node1, node2, weight=graph[node1][node2][edge]['weight'], color=graph[node1][node2][edge]['color'])

		return G
