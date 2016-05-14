import networkx as nx
import Queue
import collections
import random
import time

class CopyAgent:
	def __init__(self):
		pass

	def decide(self, game, pnum):
		pmoves = game.get_possible_moves(pnum)
		for move in pmoves:
			g = game.copy()
			g.players_choosing_destination_cards = False
			g.make_move(move.function, move.args)
			g.current_player = pnum
		return random.choice(pmoves)


class Agent:
	def __init__(self):
		pass

	def decide(self, game, pnum):
		pmoves = game.get_possible_moves(pnum)
		if len(pmoves) == 0:
			f1 = open('disaster' + '.go', 'wb')
			pickle.dump(game, f1)
			f1.close()
		return random.choice(pmoves)



class AStarMove:
	def __init__(self, game, move, pnum, lnum):
		self.state = game
		self.basemove = move
		self.pnum = pnum
		self.lnum = lnum

	def __int__(self):
		return (-1) * (self.state.players[self.pnum].points + ((20 - len(self.state.players[self.pnum].hand) if len(self.state.players[self.pnum].hand) > 20 else len(self.state.players[self.pnum].hand))) + self.getDCardScore())
		#return (self.state.players[self.pnum].points * -1) - self.state.getDCardScore(self.pnum) - self.weightPath()
		#return (self.state.players[self.pnum].points * -1) - self.state.getDCardScore(self.pnum) - self.weightPath()

	def __cmp__(self, other):
		return cmp(int(self), int(other))

	def getDCardScore(self):
		rscore = 0
		player = self.state.players[self.pnum]
		player_graph = self.state.player_graph(self.pnum)
		min_dest_number_of_trains = 0

		for destination in player.hand_destination_cards:
			try:
				if nx.has_path(player_graph, destination.destinations[0], destination.destinations[1]):
					#print "Finished " + str(destination.destinations) + "!  +" + str(destination.points)
					rscore = rscore + destination.points
				else:
					#print "Did not finish " + str(destination.destinations) + "!  -" + str(destination.points)
					min_dest_number_of_trains = min_dest_number_of_trains + destination.points
					rscore = rscore - destination.points
			except:
				#print "Did not finish " + str(destination.destinations) + "!  -" + str(destination.points)
				rscore = rscore - destination.points

		if player.number_of_trains < min_dest_number_of_trains:
			rscore = rscore - 2 * (min_dest_number_of_trains - player.number_of_trains)

		return rscore


	def weightPath(self):
		incomplete_dest = []
		player_graph = self.state.player_graph(self.pnum)
		free_routes = self.free_routes_graph(self.state.board.graph, self.state.number_of_players)
		result = 0

		joint_graph = free_routes
		for edge in player_graph.edges():
			joint_graph.add_edge(edge[0], edge[1], weight=0, color='none', owner=self.pnum)

		for destination in self.state.players[self.pnum].hand_destination_cards:
			try:
				if not nx.has_path(player_graph, destination.destinations[0], destination.destinations[1]):
					incomplete_dest.append(destination)
			except:
				incomplete_dest.append(destination)

		for destination in incomplete_dest:
			try:
				temp = nx.shortest_path(joint_graph, destination.destinations[0], destination.destinations[1])
			except:
				temp = None

			if temp != None:
				for i in range(0, len(temp) - 1):
					try:
						if nx.has_path(player_graph, temp[i], temp[i+1]):
							#print temp[i] + " : " + temp[i+1]
							result = result + (destination.points * 2)
					except:
						pass

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
							G.add_edge(node1, node2, weight=graph[node1][node2][edge]['weight'], color=graph[node1][node2][edge]['color'], owner=-1)

			visited_nodes.append(node1)
		
		return G


class RAStarAgent:
	def __init__(self):
		pass

	def decide(self,game,pnum):
		adversary = Agent()
		count = 0
		prioq = Queue.PriorityQueue()
		pmoves = game.get_possible_moves(pnum)
		max_iterations = 500
		for move in pmoves:
			count = count + 1
			g = game.copy()
			#game.players[pnum].print_destination_cards()
			g.make_move(move.function, move.args)
			g.current_player = pnum
			prioq.put(AStarMove(g, move, pnum, 0))
			g.players_choosing_destination_cards = False
		i = 0
		while True:
			i = i + 1
			print i
			#print str(i) + ", " + str(prioq.qsize())
			miniprioq = Queue.PriorityQueue()
			ATuple = prioq.get()
			#print (str(ATuple.lnum) + ", " + str(ATuple.state.players[pnum].points) + ", " + str(ATuple.state.players[pnum].number_of_trains) + ", " + str(len(ATuple.state.players[pnum].hand)))
			nstat = ATuple.state

			#print nstat.players[pnum].number_of_trains
			print 'a'
			if nstat.game_over == True:
				print "Endgame found after " + str(i) + " iterations with " + str(nstat.players[pnum].points) + " points" 
				return ATuple.basemove
			pmoves = nstat.get_possible_moves(pnum)
			for move in pmoves:
				print 'b'
				#print str(i) + ", " + str(miniprioq.qsize())
				g = nstat.copy()
				#endflag = False
				#if(g.players[pnum].number_of_trains <= 2):
				#	endflag = True
				g.make_move(move.function, move.args)
				#if(endflag == True):
				#	g.calculatePoints();
				#	g.game_over = True
				while g.current_player != pnum:
					#print g.current_player
					admove = adversary.decide(g, g.current_player)
					#print admove.function
					g.make_move(admove.function, admove.args)
				miniprioq.put(AStarMove(g, ATuple.basemove, pnum, ATuple.lnum + 1))
				print 'c'
			index = 10
			if miniprioq.qsize() < 10:
				index = miniprioq.qsize()
			for x in range(0, index):
				prioq.put(miniprioq.get())
				count = count + 1
				print 'd'
			if i > max_iterations:
				break

			#print i
		lastmove = prioq.get()
		print "Search ended at layer: " + str(lastmove.lnum) + " with " + str(lastmove.state.players[pnum].points) + " points"
		return lastmove.basemove

class AStarAgent:
	def __init__(self):
		pass

	def decide(self,game,pnum):
		start = time.time()
		count = 0
		prioq = Queue.PriorityQueue()
		pmoves = game.get_possible_moves(pnum)
		max_iterations = 500
		for move in pmoves:
			count = count + 1
			g = game.copy()
			#game.players[pnum].print_destination_cards()
			g.make_move(move.function, move.args)
			g.current_player = pnum
			prioq.put(AStarMove(g, move, pnum, 0))
			g.players_choosing_destination_cards = False
		i = 0
		while True:
			i = i + 1
			#print str(i) + ", " + str(prioq.qsize())
			miniprioq = Queue.PriorityQueue()
			ATuple = prioq.get()
			#print (str(ATuple.lnum) + ", " + str(ATuple.state.players[pnum].points) + ", " + str(ATuple.state.players[pnum].number_of_trains) + ", " + str(len(ATuple.state.players[pnum].hand)))
			nstat = ATuple.state
			#print nstat.players[pnum].number_of_trains
			#print 'a'
			if nstat.game_over == True:
				print "Endgame found after " + str(i) + " iterations with " + str(nstat.players[pnum].points) + " points in " + str(time.time() - start)  
				return ATuple.basemove
			pmoves = nstat.get_possible_moves(pnum)
			for move in pmoves: 
				#print 'b'
				#print str(i) + ", " + str(miniprioq.qsize())
				g = nstat.copy()
				endflag = False
				if(g.players[pnum].number_of_trains <= 2):
					endflag = True
				g.make_move(move.function, move.args)
				if(endflag == True):
					g.calculatePoints();
					g.game_over = True
				g.current_player = pnum
				miniprioq.put(AStarMove(g, ATuple.basemove, pnum, ATuple.lnum + 1))
				#print 'c'
			index = 10
			if miniprioq.qsize() < 10:
				index = miniprioq.qsize()
			for x in range(0, index):
				prioq.put(miniprioq.get())
				count = count + 1
				#print 'd'
			if i > max_iterations:
				break

			#print i
		lastmove = prioq.get()
		print "Search ended at layer: " + str(lastmove.lnum) + " with " + str(lastmove.state.players[pnum].points) + " points in " + str(time.time() - start) 
		return lastmove.basemove

class EAStarMove:
	def __init__(self, game, move, pnum, lnum):
		self.state = game
		self.basemove = move
		self.pnum = pnum
		self.lnum = lnum

	def __int__(self):
		return self.state.pseudoCalculatePoints(self.pnum) * -1

	def __cmp__(self, other):
		return cmp(int(self), int(other))


class EAStarAgent:
	def __init__(self):
		pass

	def decide(self,game,pnum):
		count = 0
		prioq = Queue.PriorityQueue()
		pmoves = game.get_possible_moves(pnum)
		max_iterations = 500
		for move in pmoves:
			count = count + 1
			g = game.copy()
			#game.players[pnum].print_destination_cards()
			g.make_move(move.function, move.args)
			g.current_player = pnum
			prioq.put(EAStarMove(g, move, pnum, 0))
			g.players_choosing_destination_cards = False
		i = 0
		while True:
			i = i + 1
			#print str(i) + ", " + str(prioq.qsize())
			miniprioq = Queue.PriorityQueue()
			ATuple = prioq.get()
			#print (str(ATuple.lnum) + ", " + str(ATuple.state.players[pnum].points) + ", " + str(ATuple.state.players[pnum].number_of_trains) + ", " + str(len(ATuple.state.players[pnum].hand)))
			nstat = ATuple.state
			#print nstat.players[pnum].number_of_trains
			#print 'a'
			if nstat.game_over == True:
				print "Endgame found after " + str(i) + " iterations with " + str(nstat.players[pnum].points) + " points" 
				return ATuple.basemove
			pmoves = nstat.get_possible_moves(pnum)
			for move in pmoves: 
				#print 'b'
				#print str(i) + ", " + str(miniprioq.qsize())
				g = nstat.copy()
				endflag = False
				if(g.players[pnum].number_of_trains <= 2):
					endflag = True
				g.make_move(move.function, move.args)
				if(endflag == True):
					g.calculatePoints();
					g.game_over = True
				g.current_player = pnum
				miniprioq.put(EAStarMove(g, ATuple.basemove, pnum, ATuple.lnum + 1))
				#print 'c'
			index = 10
			if miniprioq.qsize() < 10:
				index = miniprioq.qsize()
			for x in range(0, index):
				prioq.put(miniprioq.get())
				count = count + 1
				#print 'd'
			if i > max_iterations:
				break

			#print i
		lastmove = prioq.get()
		print "Search ended at layer: " + str(lastmove.lnum) + " with " + str(lastmove.state.players[pnum].points) + " points"
		return lastmove.basemove

class TrollStarMove:
	def __init__(self, game, move, pnum, lnum):
		self.state = game
		self.basemove = move
		self.pnum = pnum
		self.lnum = lnum

	def __int__(self):
		trollscore = 0
		for i in range(self.state.number_of_players):
			if i != self.pnum:
				pgraph = self.state.player_graph(i)
				for city1 in pgraph:
					for city2 in self.state.board.graph[city1]:
						for edge in self.state.board.graph[city1][city2]:
							if self.state.board.graph[city1][city2][edge]['owner'] == self.pnum:
								trollscore = trollscore + 30

		return (self.state.players[self.pnum].points + self.state.getDCardScore(self.pnum) + trollscore) * -1

	def __cmp__(self, other):
		return cmp(int(self), int(other))

class TrollStarAgent:
	def __init__(self):
		pass

	def decide(self,game,pnum):
		count = 0
		prioq = Queue.PriorityQueue()
		pmoves = game.get_possible_moves(pnum)
		max_iterations = 500
		for move in pmoves:
			count = count + 1
			g = game.copy()
			#game.players[pnum].print_destination_cards()
			g.make_move(move.function, move.args)
			g.current_player = pnum
			prioq.put(TrollStarMove(g, move, pnum, 0))
			g.players_choosing_destination_cards = False
		i = 0
		while True:
			i = i + 1
			#print i
			#print str(i) + ", " + str(prioq.qsize())
			miniprioq = Queue.PriorityQueue()
			ATuple = prioq.get()
			#print (str(ATuple.lnum) + ", " + str(ATuple.state.players[pnum].points) + ", " + str(ATuple.state.players[pnum].number_of_trains) + ", " + str(len(ATuple.state.players[pnum].hand)))
			nstat = ATuple.state
			#print nstat.players[pnum].number_of_trains
			#print 'a'
			if nstat.game_over == True:
				print "Endgame found after " + str(i) + " iterations with " + str(nstat.players[pnum].points) + " points" 
				return ATuple.basemove
			pmoves = nstat.get_possible_moves(pnum)
			for move in pmoves: 
				#print 'b'
				#print str(i) + ", " + str(miniprioq.qsize())
				g = nstat.copy()
				endflag = False
				if(g.players[pnum].number_of_trains <= 2):
					endflag = True
				g.make_move(move.function, move.args)
				if(endflag == True):
					g.calculatePoints();
					g.game_over = True
				g.current_player = pnum
				miniprioq.put(TrollStarMove(g, ATuple.basemove, pnum, ATuple.lnum + 1))
				#print 'c'
			index = 10
			if miniprioq.qsize() < 10:
				index = miniprioq.qsize()
			for x in range(0, index):
				prioq.put(miniprioq.get())
				count = count + 1
				#print 'd'
			if i > max_iterations:
				break

			#print i
		lastmove = prioq.get()
		print "Search ended at layer: " + str(lastmove.lnum) + " with " + str(lastmove.state.players[pnum].points) + " points"
		return lastmove.basemove

class PAStarMove:
	def __init__(self, game, move, pnum, lnum):
		self.state = game
		self.basemove = move
		self.pnum = pnum
		self.lnum = lnum

	def __int__(self):
		destpoints = 0
		opengraph = self.state.player_plus_free_graph(self.pnum)
		dcards = self.state.players[self.pnum].hand_destination_cards
		for destcard in dcards:
			try:
				spath = nx.shortest_path(opengraph, destcard.destinations[0], destcard.destinations[1])
				for i in range(0, len(spath) - 1):
					for edge in opengraph[destcard.destinations[0]][destcard.destinations[1]]:
						if self.state.board.graph[destcard.destinations[0]][destcard.destinations[1]][edge]['owner'] == self.pnum:
							destpoints = destpoints + 50
			except:
				pass
		return (destpoints + self.state.players[self.pnum].points) * -1

	def __cmp__(self, other):
		return cmp(int(self), int(other))

class PAStarAgent:
	def __init__(self):
		pass

	def decide(self,game,pnum):
		count = 0
		prioq = Queue.PriorityQueue()
		pmoves = game.get_possible_moves(pnum)
		max_iterations = 500
		for move in pmoves:
			count = count + 1
			g = game.copy()
			#game.players[pnum].print_destination_cards()
			g.make_move(move.function, move.args)
			g.current_player = pnum
			prioq.put(PAStarMove(g, move, pnum, 0))
			g.players_choosing_destination_cards = False
		i = 0
		while True:
			i = i + 1
			#print i
			#print str(i) + ", " + str(prioq.qsize())
			miniprioq = Queue.PriorityQueue()
			ATuple = prioq.get()
			#print (str(ATuple.lnum) + ", " + str(ATuple.state.players[pnum].points) + ", " + str(ATuple.state.players[pnum].number_of_trains) + ", " + str(len(ATuple.state.players[pnum].hand)))
			nstat = ATuple.state
			#print nstat.players[pnum].number_of_trains
			#print 'a'
			if nstat.game_over == True:
				print "Endgame found after " + str(i) + " iterations with " + str(nstat.players[pnum].points) + " points" 
				return ATuple.basemove
			pmoves = nstat.get_possible_moves(pnum)
			for move in pmoves: 
				#print 'b'
				#print str(i) + ", " + str(miniprioq.qsize())
				g = nstat.copy()
				endflag = False
				if(g.players[pnum].number_of_trains <= 2):
					endflag = True
				g.make_move(move.function, move.args)
				if(endflag == True):
					g.calculatePoints();
					g.game_over = True
				g.current_player = pnum
				miniprioq.put(PAStarMove(g, ATuple.basemove, pnum, ATuple.lnum + 1))
				#print 'c'
			index = 10
			if miniprioq.qsize() < 10:
				index = miniprioq.qsize()
			for x in range(0, index):
				prioq.put(miniprioq.get())
				count = count + 1
				#print 'd'
			if i > max_iterations:
				break

			#print i
		lastmove = prioq.get()
		print "Search ended at layer: " + str(lastmove.lnum) + " with " + str(lastmove.state.players[pnum].points) + " points"
		return lastmove.basemove


class TAStarMove:
	def __init__(self, game, move, pnum, lnum):
		self.state = game
		self.basemove = move
		self.pnum = pnum
		self.lnum = lnum
		self.score = 0
		if self.state.game_over == False:
			self.score =  (-1) * (self.state.players[self.pnum].points + ((20 - len(self.state.players[self.pnum].hand) if len(self.state.players[self.pnum].hand) > 20 else len(self.state.players[self.pnum].hand))) + self.getDCardScore())
		else:	
			self.score =  (-1) * (self.state.players[self.pnum].points + ((20 - len(self.state.players[self.pnum].hand) if len(self.state.players[self.pnum].hand) > 20 else len(self.state.players[self.pnum].hand))))
		


	def __int__(self):
		return self.score
		#return (self.state.players[self.pnum].points * -1) - self.state.getDCardScore(self.pnum) - self.weightPath()
		#return (self.state.players[self.pnum].points * -1) - self.state.getDCardScore(self.pnum) - self.weightPath()

	def __cmp__(self, other):
		return cmp(int(self), int(other))

	def getDCardScore(self):
		rscore = 0
		player = self.state.players[self.pnum]
		player_graph = self.state.player_graph(self.pnum)
		min_dest_number_of_trains = 0

		for destination in player.hand_destination_cards:
			try:
				if nx.has_path(player_graph, destination.destinations[0], destination.destinations[1]):
					#print "Finished " + str(destination.destinations) + "!  +" + str(destination.points)
					rscore = rscore + destination.points
				else:
					#print "Did not finish " + str(destination.destinations) + "!  -" + str(destination.points)
					min_dest_number_of_trains = min_dest_number_of_trains + destination.points
					rscore = rscore - destination.points
			except:
				#print "Did not finish " + str(destination.destinations) + "!  -" + str(destination.points)
				rscore = rscore - destination.points

		if player.number_of_trains < min_dest_number_of_trains:
			rscore = rscore - 2 * (min_dest_number_of_trains - player.number_of_trains)

		return rscore


	def weightPath(self):
		incomplete_dest = []
		player_graph = self.state.player_graph(self.pnum)
		free_routes = self.free_routes_graph(self.state.board.graph, self.state.number_of_players)
		result = 0

		joint_graph = free_routes
		for edge in player_graph.edges():
			joint_graph.add_edge(edge[0], edge[1], weight=0, color='none', owner=self.pnum)

		for destination in self.state.players[self.pnum].hand_destination_cards:
			try:
				if not nx.has_path(player_graph, destination.destinations[0], destination.destinations[1]):
					incomplete_dest.append(destination)
			except:
				incomplete_dest.append(destination)

		for destination in incomplete_dest:
			try:
				temp = nx.shortest_path(joint_graph, destination.destinations[0], destination.destinations[1])
			except:
				temp = None

			if temp != None:
				for i in range(0, len(temp) - 1):
					try:
						if nx.has_path(player_graph, temp[i], temp[i+1]):
							#print temp[i] + " : " + temp[i+1]
							result = result + (destination.points * 2)
					except:
						pass

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
							G.add_edge(node1, node2, weight=graph[node1][node2][edge]['weight'], color=graph[node1][node2][edge]['color'], owner=-1)

			visited_nodes.append(node1)
		
		return G

class TAStarAgent:
	def __init__(self):
		pass

	def decide(self,game,pnum):
		start = time.time()
		count = 0
		prioq = Queue.PriorityQueue()
		pmoves = game.get_possible_moves(pnum)
		max_iterations = 500
		for move in pmoves:
			count = count + 1
			g = game.copy()
			#game.players[pnum].print_destination_cards()
			g.make_move(move.function, move.args)
			g.current_player = pnum
			prioq.put(TAStarMove(g, move, pnum, 0))
			g.players_choosing_destination_cards = False
		i = 0
		while True:
			i = i + 1
			print i
			#print str(i) + ", " + str(prioq.qsize())
			miniprioq = Queue.PriorityQueue()
			ATuple = prioq.get()
			#print (str(ATuple.lnum) + ", " + str(ATuple.state.players[pnum].points) + ", " + str(ATuple.state.players[pnum].number_of_trains) + ", " + str(len(ATuple.state.players[pnum].hand)))
			nstat = ATuple.state
			#print nstat.players[pnum].number_of_trains
			#print 'a'
			if nstat.game_over == True:
				print "Endgame found after " + str(i) + " iterations with " + str(nstat.players[pnum].points) + " points in " + str(time.time() - start) 
				return ATuple.basemove
			pmoves = nstat.get_possible_moves(pnum)
			for move in pmoves: 
				#print 'b'
				#print str(i) + ", " + str(miniprioq.qsize())
				g = nstat.copy()
				endflag = False
				if(g.players[pnum].number_of_trains <= 2):
					endflag = True
				g.make_move(move.function, move.args)
				if(endflag == True):
					g.calculatePoints();
					g.game_over = True
				g.current_player = pnum
				miniprioq.put(TAStarMove(g, ATuple.basemove, pnum, ATuple.lnum + 1))
				#print 'c'
			index = 10
			if miniprioq.qsize() < 10:
				index = miniprioq.qsize()
			for x in range(0, index):
				prioq.put(miniprioq.get())
				count = count + 1
				#print 'd'
			if i > max_iterations:
				break

			#print i
		lastmove = prioq.get()
		print "Search ended at layer: " + str(lastmove.lnum) + " with " + str(lastmove.state.players[pnum].points) + " points in " + str(time.time() - start) 
		return lastmove.basemove