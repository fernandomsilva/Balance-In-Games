import networkx as nx
import Queue
import collections

class SpeedRacerMove:
	def __init__(self, game, move, pnum, lnum):
		self.state = game
		self.basemove = move
		self.pnum = pnum
		self.lnum = lnum

	def __int__(self):
		return self.state.players[self.pnum].number_of_trains 

	def __cmp__(self, other):
		return cmp(int(self), int(other))

class SpeedRacerAgent:
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
			prioq.put(SpeedRacerMove(g, move, pnum, 0))
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
				miniprioq.put(SpeedRacerMove(g, ATuple.basemove, pnum, ATuple.lnum + 1))
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