def make_train_deck(number_of_color_cards, number_of_wildcards):
	result = []
	cards = ["red", "orange", "blue", "pink", "white", "yellow", "black", "green"]
	result = [card for card in cards for x in range(0, number_of_color_cards)]
	result.extend(["wild" for x in range(0, number_of_wildcards)])

def point_table():
	return {1: 1, 2:2, 3:4, 4:7, 5:10, 6:15}

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

	def discard(self, card):
		self.discard_pile.append(card)

	def reshuffle(self):
		self.deck = copy.copy(discard_pile)
		self.discard_pile = []

class Game:
	def __init__(self, board, point_table, destination_deck, train_deck, number_of_players, players, current_player):
		self.board = board
		self.point_table = point_table
		self.destination_deck = CardManager(destination_deck)
		self.train_deck = CardManager(train_deck)
		self.number_of_players = number_of_players
		self.players = players
		self.current_player = current_player
		self.players_choosing_destination_cards = False

	def setup(self):
		for i in range (0, self.number_of_players):
			for j in range(0, 4):
				self.players[i].hand.append(draw_card(self.train_deck))
			for j in range(0, 3):
				self.players[i].hand.append(draw_card(self.destination_deck))

			self.players[i].choosing_destination_cards = True

		self.current_player = random.choice([x for x in range(0, self.number_of_players)])
		self.players_choosing_destination_cards = True

	def draw_card(self, deck):
		card = random.choice(deck)
		deck.remove(card)

		return card

	def choose_destination_cards(self, player, cards):
		min_num_cards = 2 if self.players_choosing_destination_cards else 1

		if len(cards) >= min_num_cards:
			for card in cards:
				self.players[player].hand.remove(card)
				self.players[player].hand_destination_cards.append(card)

			self.players[player].choosing_destination_cards = False

			for i in range(0, self.number_of_players):
				if self.players[i].choosing_destination_cards == True:
					break
			if i == self.number_of_players - 1:
				self.players_choosing_destination_cards = False

	