from ttroptimized import *
import random

class HastyAgent:
	def __init__(self):
		pass

	def decide(self, game, pnum):
		possible_moves = game.get_possible_moves(pnum)

		if possible_moves[0].function == 'chooseDestinationCards':
			min_points = None
			move = None
			for m in possible_moves:
				total = 0
				for d in m.args[1]:
					if isinstance(d.points, int):
						total += d.points
					else:
						total += min(d.points)
				if min_points == None or min_points > total:
					min_points = total
					move = m

			return move

		m_claim_routes = []
		m_draw_cards = []

		for move in possible_moves:
			if move.function == 'drawTrainCard':
				m_draw_cards.append(move)
			if move.function == 'claimRoute':
				m_claim_routes.append(move)

		max_weight = 0
		max_move = None
		for route in m_claim_routes:
			edge = game.board.get_free_connection(route.args[0], route.args[1], route.args[2], game.number_of_players, game.switzerland_variant or game.nordic_countries_variant)
			if edge['weight'] > max_weight:
				max_weight = edge['weight']
				max_move = route

		if len(m_claim_routes) > 0:
			return max_move

		return random.choice(m_draw_cards)
