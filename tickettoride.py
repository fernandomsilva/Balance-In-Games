import collections

def make_train_deck(number_of_color_cards, number_of_wildcards):
	result = []
	cards = ["red", "orange", "blue", "pink", "white", "yellow", "black", "green"]
	result = [card for card in cards for x in range(0, number_of_color_cards)]
	result.extend(["wild" for x in range(0, number_of_wildcards)])

def point_table():
	return {1:1, 2:2, 3:4, 4:7, 5:10, 6:15}

class DestinationCard:
	def __init__(self, dest1, dest2, points):
		self.destinations = [dest1, dest2]
		self.points = points

class Player:
	def __init__(self, hand, number_of_trains, points):
		self.hand = hand
		self.hand_destination_cards = []
		self.number_of_trains = number_of_trains
		self.points = points
		self.choosing_destination_cards = False

class CardManager:
	def __init__(self, deck):
		self.deck = deck
		self.discard_pile = []

	def draw_card(self):
		card = random.choice(self.deck)
		self.deck.remove(card)

		return card

	def discard(self, card):
		self.discard_pile.append(card)

	def reshuffle(self):
		self.deck = copy.copy(discard_pile)
		self.discard_pile = []

class Board:
	def __init__(self, board_graph):
		self.graph = board_graph

	def get_connection(self, city1, city2):
		if city1 in self.graph:
			if city2 in self.graph[city1]:
				return self.graph[city1][city2]

		if city2 in self.graph:
			if city1 in self.graph[city2]:
				return self.graph[city2][city1]

		return None

class Game:
	def __init__(self, board, point_table, destination_deck, train_deck, number_of_players, players, current_player):
		self.board = board
		self.point_table = point_table
		self.destination_deck = CardManager(destination_deck)
		self.train_deck = CardManager(train_deck)
		self.train_cards_face_up = []
		self.number_of_players = number_of_players
		self.players = players
		self.current_player = current_player
		self.players_choosing_destination_cards = False
		self.last_turn_player = -1

	def setup(self):
		for i in range (0, self.number_of_players):
			for j in range(0, 4):
				self.players[i].hand.append(draw_card(self.train_deck))
			for j in range(0, 3):
				self.players[i].hand.append(draw_card(self.destination_deck))

			self.players[i].choosing_destination_cards = True

		self.current_player = random.choice([x for x in range(0, self.number_of_players)])
		self.players_choosing_destination_cards = True

		for i in range(0, 5):
			self.addFaceUpTrainCard()

	def draw_card(self, deck):
		card = deck.draw_card()

		if deck == self.train_deck and len(self.train_deck.deck) == 0:
			self.train_deck.reshuffle()

		return card

	def discard_cards(self, player_index, cards):
		for card in cards:
			self.train_deck.discard(card)
			self.players[player_index].hand.remove(card)

	def addFaceUpTrainCard(self):
		card = self.draw_card(self.train_deck)

		self.train_cards_face_up.append(card)

		if len(self.train_cards_face_up) == 5:
			card_count = collections.Count(self.train_deck)

			if 'wild' in card_count:
				if card_count['wild'] >= 3:
					self.train_deck.discard(self.train_cards_face_up)
					self.train_cards_face_up = []

					x = 5 if len(self.train_deck.deck) + len(self.train_deck.discard) >= 5 else len(self.train_deck.deck) + len(self.train_deck.discard)
					for i in range(0, x):
						self.addFaceUpTrainCard()

	def next_players_turn(self):
		self.current_player = self.current_player + 1

	def choose_destination_cards(self, args):
		return choosing_destination_cards(args[0], args[1])

	def choose_destination_cards(self, player, cards):
		min_num_cards = 2 if self.players_choosing_destination_cards else 1

		if len(cards) >= min_num_cards:
			for card in cards:
				self.players[player].hand.remove(card)
				self.players[player].hand_destination_cards.append(card)

			self.players[player].choosing_destination_cards = False

			if self.players_choosing_destination_cards:
				for i in range(0, self.number_of_players):
					if self.players[i].choosing_destination_cards == True:
						break
				if i == self.number_of_players - 1:
					self.players_choosing_destination_cards = False

		if min_num_cards == 1:
			self.next_players_turn()

	def checkPlayerHandRequirements(self, player_index, number_of_cards, color):
		if len(self.players[player_index].hand) < number_of_cards:
			return False

		card_count = collections.Counter(self.players[player_index].hand)
		total = 0

		if color in card_count:
			total = total + card_count[color]
		if color != 'wild' and 'wild' in card_count:
			total = total + card_count['wild']
		if color not in card_count and color != 'wild':
			color = 'wild'

		if total < number_of_cards:
			return False

		cards_to_use = []
		if color in card_count:
			x = number_of_cards if card_count[color] >= number_of_cards else card_count[color]
			for i in range(0, x):
				cards_to_use.append(color)

		if len(cards_to_use) < number_of_cards:
			x = number_of_cards - len(cards_to_use)
			for i in range(0, x):
				cards_to_use.append('wild')

		return cards_to_use

	def claimRoute(self, args):
		if len(args) == 2:
			return claimRoute(args[0], args[1])
		return claimRoute(args[0], args[1], args[2])		

	def claimRoute(self, city1, city2, color=None):
		edge = self.board.get_connection(city1, city2)

		if edge['owner'] == -1:
			route_color = edge['color'] if edge['color'] != 'GRAY' else color
			cards_needed = checkPlayerHandRequirements(self.current_player, edge['weight'], route_color)

			if cards_needed and self.players[current_player].trains >= edge['weight']:
				self.discard_cards(current_player, cards_needed)
				self.players[current_player].trains = self.players[current_player].trains - edge['weight']
				edge['owner'] = current_player
				self.players[current_player].points = self.players[current_player].points + self.point_table[edge['weight']]
			else:
				return False

			if self.players[current_player].trains <= 2:
				self.last_turn_player = current_player

			self.next_players_turn()

			return True

		return False

	def drawDestinationCards(self, args):
		return drawDestinationCards()

	def drawDestinationCards(self):
		if len(self.destination_deck) == 0:
			return False

		x = 3 if len(self.destination_deck) >= 3 else len(self.destination_deck)
		for i in range(0, x):
			self.players[current_player].hand.append(self.draw_card(self.destination_deck))

		self.players[current_player].choosing_destination_cards = True

		return True

	#def make_move(self, move, args):
	#	last_turn = False
	#	if self.current_player == self.last_turn_player:
	#		last_turn = True
	#	if not self.players[current_player].choosing_destination_cards or (self.players[current_player].choosing_destination_cards and move == choose_destination_cards):
	#		move(args)
