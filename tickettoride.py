def make_train_deck(number_of_color_cards, number_of_wildcards):
	result = []
	cards = ["red", "orange", "blue", "pink", "white", "yellow", "black", "green"]
	result = [card for card in cards for x in range(0, number_of_color_cards)]
	result.extend(["wild" for x in range(0, number_of_wildcards)])

def point_table():
	return {1: 1, 2:2, 3:4, 4:7, 5:10, 6:15}

class Player:
	def __init__(self, hand, number_of_trains, points):
		self.hand = hand
		self.number_of_trains = number_of_trains
		self.points = points

class Game:
	def __init__(self, board, point_table, destination_deck, train_deck, number_of_players, players, current_player):
		self.board = board
		self.point_table = point_table
		self.destination_deck = destination_deck
		self.train_deck = train_deck
		self.number_of_players = number_of_players
		self.players = players
		self.current_player = current_player

