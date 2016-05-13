from AStarSeries import *
from tickettoride import *

class TreeNode:
	def __init__(self, game, pnum, parent, move):
		self.state = game
		self.pnum = pnum
		self.numerator = self.rollout(pnum, state)
		self.denominator = 1
		self.children = []
		self.parent = parent
		self.move = move

	def expand(self):
		randomAgent = Agent()
		g = self.state.copy()
		move = randomAgent.decide(g, g.current_player)
		g.make_move(move.function, move.args)
		expanded = Treenode(g, self.pnum, self, move)
		children.append(expanded)
		self.propagate(expanded.numerator)

	def expand(self, move):
		randomAgent = Agent()
		g = self.state.copy()
		g.make_move(move.function, move.args)
		expanded = Treenode(g, self.pnum, self, move)
		children.append(expanded)
		self.propagate(expanded.numerator)

	def rollout(self, pnum, node):
		self.state.players_choosing_destination_cards = False
		g = self.state.copy()
		randomAgent = Agent()
		while g.game_over != True:
			rmove = Agent.decide(g, g.current_player)
			g.make_move(rmove.function, rmove.args)
		pmax = -1
		smax = -1000
		for player in g.players:
			if player.points > smax:
				pmax = g.players.index(player)
				smax = player.points

		if pmax == pnum:
			return 1

	def propagate(self, winint):
		self.denominator = self.denominator + 1
		self.numerator = self.numerator + winint
		if self.parent != None:
			self.parent.propagate(winint)


	def getUCTSelect(self):
		return (numerator / denominator) + sqrt(2) * sqrt(log(self.parent.denominator) / denominator)

	def __int__(self):
		return getUCTSelect()



class MCTSAgent():
	def __init__(self):
		pass

	def decide(self, game, pnum):
		g = game.copy()
		root = TreeNode(g, pnum, None, None)
		#selection
		pmoves = g.get_possible_moves(pnum)
		for move in pmoves:
			root.expand(move)

		

