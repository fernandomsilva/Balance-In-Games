from AStarSeries import *
from ttroptimized import *
from PathAgent import *
import math

class TreeNode:
	def __init__(self, game, pnum, parent, move, max_num):
		self.state = game
		self.pnum = pnum
		self.denominator = 1
		self.numerator = self.rollout(pnum, game)
		self.children = []
		self.parent = parent
		self.move = move
		self.max_num = max_num

	def expand(self):
		g = self.state.copy()
		#try:
		#	randomAgent = PathAgent()
		#	move = randomAgent.decide(g, g.current_player)
		#	g.make_move(move.function, move.args)
		#except:
		randomAgent = PathAgent()
		move = randomAgent.decide(g, g.current_player)
		if move == None:
			self.denominator = self.denominator + 1
			self.propagate(0, self.max_num)
		else:
			g.make_move(move.function, move.args)
			expanded = TreeNode(g, self.pnum, self, move, 0)
			self.children.append(expanded)
			self.propagate(expanded.numerator, self.max_num)

	def expand2(self, move):
		g = self.state.copy()
		g.make_move(move.function, move.args)
		expanded = TreeNode(g, self.pnum, self, move, 0)
		self.children.append(expanded)
		self.propagate(expanded.numerator, self.max_num)

	def rollout(self, pnum, node):
		self.state.players_choosing_destination_cards = False
		g = self.state.copy()
		randomAgent = CopyAgent()#PathAgent()
		count = 0
		while g.game_over != True:
			#try:
			#	pmove = pathAgent.decide(g, g.current_player)
			#	g.make_move(pmove.function, pmove.args)
			#except:
			try:
				rmove = randomAgent.decide(g, g.current_player)
				count = count + 1
				if count >= 35:
					break
				if rmove == None:
					return 0
			except:
				return 0
			g.make_move(rmove.function, rmove.args)
		pmax = -1
		smax = -1000
		for player in g.players:
			if player.points > smax:
				pmax = g.players.index(player)
				smax = player.points

		if count >= 35:
			if pmax == pnum:
				return 0.5
			else:
				return -0.5	

		if pmax == pnum:
			return 1.0
		else:
			return 0.0

	def propagate(self, winint, max_num):
		#print winint
		if winint != None:
			self.numerator = self.numerator + winint
		self.denominator = self.denominator + 1
		#print winint
		if max_num > self.max_num:
			self.max_num = max_num
		if (self.numerator / self.denominator) > self.max_num:
			self.max_num = self.numerator / self.denominator
		if self.parent != None:
			self.parent.propagate(winint, self.max_num)


	def getUCTSelect(self):
		#return self.numerator/self.denominator + math.sqrt(2) * math.sqrt(math.log(self.parent.denominator) / self.denominator)
		max_child = self.max_num
		Q = 0.125
		return (Q * max_child + (1.0 - Q) * (self.numerator/self.denominator)) + math.sqrt(2) * math.sqrt(math.log(self.parent.denominator) / self.denominator)

	def getPartialExpansion(self, k=0.5):
		return k * math.sqrt(2) * math.sqrt(math.log(self.parent.denominator) / (1 + len(self.children)))

	def __float__(self):
		return self.getUCTSelect()




class MCTSAgent():
	def __init__(self):
		pass

	def decide(self, game, pnum):
		g = game.copy()
		root = TreeNode(g, pnum, None, None, 0)
		#selection
		pmoves = g.get_possible_moves(pnum)
		for move in pmoves:
			root.expand2(move)
		start = time.time()

		while time.time() - start < 20:
			#print time.time() - start
			#selection
			cNode = []
			maxuct = -10000
			for node in root.children:
				if float(node) > maxuct:
					cNode = [node]
					maxuct = float(node)
				elif float(node) == maxuct:
					cNode.append(node)

			explore = random.choice(cNode)

			while True:
				if len(explore.children) == 0:
					explore.expand()
					break
				else:
					cNode = [explore]
					maxuct = float(explore)
					partialExpansion = explore.getPartialExpansion()
					PE_exceeded = False

					for node in explore.children:
						if float(node) < partialExpansion:
							PE_exceeded = True
						if float(node) > maxuct:
							cNode = [node]
							maxuct = float(node)
						elif float(node) == maxuct:
							cNode.append(node)

					if PE_exceeded:
						expexplore = explore
					else:
						expexplore = random.choice(cNode)

					if expexplore == explore:
						explore.expand()
						break
					else:
						explore = expexplore

		cNode = []
		maxuct = -10000
		for node in root.children:
			if float(node) > maxuct:
				cNode = [node]
				maxuct = float(node)
			elif float(node) == maxuct:
				cNode.append(node)

		return random.choice(cNode).move

		

