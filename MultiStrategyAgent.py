from ttroptimized import *
from HungryAgent import *
from PathAgent import *

import random

class MultiStrategyAgent:
	def __init__(self):
		self.pa = PathAgent()
		self.ha = HungryAgent()
		self.turn_count = 0
		self.choice = 0

	def decide(self, game, pnum):
		if (self.turn_count % 6) == 0:
			self.choice = random.randint(0, 1)

		if self.choice > 0:
			return self.pa.decide(game, pnum)
		else:
			return self.ha.decide(game, pnum)

		self.turn_count += 1