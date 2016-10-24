from AStarSeries import *
from ttroptimized import *
from PathAgent import *
import math

class TreeNode:
	def __init__(self, game, pnum, parent, move):
		self.state = game
		self.pnum = pnum
		self.denominator = 1
		self.numerator = self.rollout(pnum, game)
		self.children = []
		self.parent = parent
		self.move = move

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
			self.propagate(0)
		else:
			g.make_move(move.function, move.args)
			expanded = TreeNode(g, self.pnum, self, move)
			self.children.append(expanded)
			self.propagate(expanded.numerator)

	def expand2(self, move):
		g = self.state.copy()
		g.make_move(move.function, move.args)
		expanded = TreeNode(g, self.pnum, self, move)
		self.children.append(expanded)
		self.propagate(expanded.numerator)

	def rollout(self, pnum, node):
		
		self.state.players_choosing_destination_cards = False
		g = self.state.copy()
		pathAgent = PathAgent()
		count = 0
		while g.game_over != True:
			#try:
			#	pmove = pathAgent.decide(g, g.current_player)
			#	g.make_move(pmove.function, pmove.args)
			#except:
			try:
				rmove = pathAgent.decide(g, g.current_player)
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

		if pmax == pnum:
			return 1
		else:
			return 0

	def propagate(self, winint):
		#print winint
		if winint != None:
			self.numerator = self.numerator + winint
		self.denominator = self.denominator + 1
		#print winint
		if self.parent != None:
			self.parent.propagate(winint)


	def getUCTSelect(self):
		return (self.numerator / self.denominator) + math.sqrt(2) * math.sqrt(math.log(self.parent.denominator) / self.denominator)

	def __float__(self):
		return self.getUCTSelect()




class MCTSAgent():
	def __init__(self):
		pass

	def decide(self, game, pnum):
		g = game.copy()
		root = TreeNode(g, pnum, None, None)
		#selection
		pmoves = g.get_possible_moves(pnum)
		for move in pmoves:
			root.expand2(move)
		start = time.time()

		while time.time() - start < 5:
			print time.time() - start
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
					for node in explore.children:
						if float(node) > maxuct:
							cNode = [node]
							maxuct = float(node)
						elif float(node) == maxuct:
							cNode.append(node)
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

		

