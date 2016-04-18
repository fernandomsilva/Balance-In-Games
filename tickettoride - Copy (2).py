import collections
import random
import networkx as nx
import itertools
import random
import copy
import Queue


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
		return random.choice(pmoves)



class AStarMove:
	def __init__(self, game, move, pnum, lnum):
		self.state = game
		self.basemove = move
		self.pnum = pnum
		self.lnum = lnum

	def __int__(self):
		return self.state.players[self.pnum].points * -1 - self.state.getDCardScore(self.pnum)

	def __cmp__(self, other):
		return cmp(int(self), int(other))

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
				#endflag = False
				#if(g.players[pnum].number_of_trains <= 2):
				#	endflag = True
				g.make_move(move.function, move.args)
				#if(endflag == True):
				#	g.calculatePoints();
				#	g.game_over = True
				while g.current_player != pnum:
					admove = adversary.decide(g, g.current_player)
					g.make_move(admove.function, admove.args)
				miniprioq.put(AStarMove(g, ATuple.basemove, pnum, ATuple.lnum + 1))
				#print 'c'
			index = 10
			if miniprioq.qsize() < 10:
				index = miniprioq.qsize()
			for x in range(0, index):
				prioq.put(miniprioq.get())
				count = count + 1
				# print 'd'
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
				miniprioq.put(AStarMove(g, ATuple.basemove, pnum, ATuple.lnum + 1))
				#print 'c'
			index = 10
			if miniprioq.qsize() < 10:
				index = miniprioq.qsize()
			for x in range(0, index):
				prioq.put(miniprioq.get())
				count = count + 1
				# print 'd'
			if i > max_iterations:
				break

			#print i
		lastmove = prioq.get()
		print "Search ended at layer: " + str(lastmove.lnum) + " with " + str(lastmove.state.players[pnum].points) + " points"
		return lastmove.basemove

class GameHandler:
	def __init__(self, game, agents):
		self.game = game
		self.agents = agents

	def play(self):
		for i in range(0, self.game.number_of_players):
			print(i)
			move = self.agents[i].decide(self.game.copy(), i)
			print(move.function)
			self.game.make_move(move.function, move.args)
		
		print (self.game.players_choosing_destination_cards)

		while self.game.game_over == False:
			print("Current Player: " + str(self.game.current_player) + ", " + str(self.game.players[self.game.current_player].number_of_trains)) + ', ' + str(self.game.players[self.game.current_player].points)
			move = self.agents[self.game.current_player].decide(self.game, self.game.current_player)
			print(move.function)
			#print self.game.players[self.game.current_player].hand
			self.game.make_move(move.function, move.args)
		#move = self.agents[self.game.current_player].decide(self.game, self.game.current_player)
		#self.game.make_move(move.function, move.args)

		print("Player 1: " + str(self.game.players[0].points))
		print("Player 2: "+ str(self.game.players[1].points))

#returns the train deck (a list of strings)
#number_of_color_cards => an integer that defines the number of each of the non-wild cards in the deck
#number_of_wildcards => an integer that defines the number of wild cards in the deck
#default values (following the rulebook) should be 12 color cards and 14 wilds
def make_train_deck(number_of_color_cards, number_of_wildcards):
	result = []
	cards = ["red", "orange", "blue", "pink", "white", "yellow", "black", "green"]
	result = [card for card in cards for x in range(0, number_of_color_cards)]
	result.extend(["wild" for x in range(0, number_of_wildcards)])
	return result

#returns a dict that relates the number of trains on a route to how many points that is worth
# 1 train route is worth 1 point
# 2 train route is worth 2 points
# 3 train route is worth 4 points
def point_table():
	return {1:1, 2:2, 3:4, 4:7, 5:10, 6:15}

def comparePlayerKey(p1):
	return p1.points

#class to encapsulate the destination cards
#dest1 and dest2 => strings for the two destinations
#points => integer for how many points the player wins by completing that conection
class DestinationCard:
	def __init__(self, dest1, dest2, points):
		self.destinations = [dest1, dest2]
		self.points = points
	
	def __str__(self):
		return str(self.destinations) + " " + str(self.points)

#class to encapsulate the player
#hand => list of train cards (strings) in the player's hand
#number_of_trains => integer of how many trains the player has left (players start with 45 trains)
#points => integer of the number of points the player currently has
#choosing_destination_cards => boolean to indicate if the player is picking destination cards to keep
#drawing_train_cards => boolean to indicate that the player drew 1 train cards and needs to draw 1 more
class Player:
	def __init__(self, hand, number_of_trains, points):
		self.hand = hand
		self.hand_destination_cards = []
		self.number_of_trains = number_of_trains
		self.points = points
		self.choosing_destination_cards = False
		self.drawing_train_cards = False

	def copy(self):
		p = Player(list(self.hand), self.number_of_trains, self.points)
		p.hand_destination_cards = copy.copy(self.hand_destination_cards)
		p.choosing_destination_cards = self.choosing_destination_cards
		p.drawing_train_cards = self.drawing_train_cards
		return p

	def print_destination_cards(self):
		for card in self.hand_destination_cards:
			print(card)






#Data structure to store move data
class Move:
	def __init__(self, fref, args):
		self.function = fref
		self.args = args


#class to encapsulate decks (train card deck and destination deck)
#deck => list of cards (strings for train deck, DestinationCard class for destination deck) of the deck 
class CardManager:
	def __init__(self, cardlist):
		self.deck = cardlist
		self.discard_pile = []

	def __len__(self):
		return len(self.deck)

	def copy(self):
		c = CardManager(copy.copy(self.deck))
		c.discard_pile = copy.copy(self.discard_pile)
		return c

	#returns a randomly picked card from the list (deck)
	def draw_card(self):
		card = random.choice(self.deck)
		self.deck.remove(card)

		return card

	#puts a card in the discard pile
	def discard(self, card):
		if type(card) == type([]):
			for c in card:
				self.discard_pile.append(c)
		else:
			self.discard_pile.append(card)

	#assumes an empty deck. Puts all cards from the discard pile back in the deck. Empties the discard_pile
	def reshuffle(self):
		self.deck = copy.copy(self.discard_pile)
		self.discard_pile = []

#class to encapsulate the Board (represented by a graph from the library networkx)
#board_graph => graph that represents the board (a graph in networkx is represented by a dictionary)
class Board:
	def __init__(self, board_graph):
		self.graph = board_graph

	def copy(self):
		b = Board(copy.deepcopy(self.graph))
		return b

	#returns a route (edge) of a specific color that connect two cities
	#if color is None, return a list of all routes between the two cities
	#city1 => string of one of the cities in the route
	#city2 => string of the other city in the route
	#color => string of color of the route
	def get_connection(self, city1, city2, color=None):
		edge = None

		if city1 in self.graph:
			if city2 in self.graph[city1]:
				edge = self.graph[city1][city2]

		if city2 in self.graph:
			if city1 in self.graph[city2]:
				edge = self.graph[city2][city1]

		if edge != None:
			if color == None:
				return edge
			else:
				for opt in edge:
					if edge[opt]['color'] == color:
						return edge[opt]

		return None

	#returns a route (edge) with a specific color that has not been claimed
	#if number_of players <= 3, only 1 route can be claimed between the same two cities
	#city1 and city2 => string of the two cities that make up the route
	#color => the color of the route
	#number_of_players => the number of players in the current game
	def get_free_connection(self, city1, city2, color, number_of_players=2):
		connections = self.get_connection(city1, city2)

		if number_of_players < 4:
			locked = False
			for c in connections:
				if connections[c]['owner'] != -1:
					locked = True

		if not locked:
			for c in connections:
				if (connections[c]['color'] == color or connections[c]['color'] == "GRAY") and connections[c]['owner'] == -1:
					return connections[c]

		return None

#class that encapsulate the game itself
#board => object of the Board class (defined above)
#point_table => dictionary (use function point_table above)
#destination_deck => list of all destination cards in the game (cards should be of class DestinationCard [defined above])
#train_deck => list of all train cards in the game (use function make_train_deck above)
#player => list of all players (objects of class Player [defined above]) in the game
#current_player => index of the player in the list of players who should make the next move
#------------------------
#train_deck_face_up => list of train cards that are currently face up on the table (always has length of 5 after setup)
#players_choosing_destination_cards => boolean that is true while all players are choosing the destination cards they want at the beginning of the game (only at the beginning of the game)
#last_turn_player => index of the player who has the last turn. After it has a value > -1, the next time this player makes a move, the game will end


####################
#   MAKING MOVES   #
####################

#always use the funciton make_move(self, move, args)
#move is the reference to a move function. All possible move functions are:
#move_choose_destination_cards(self, args), move_claimRoute(self, args), move_drawDestinationCards(self, args), move_drawTrainCard(self, args)
#all of them are expecting a list as an argument. Look at their 'sister' functions to know what should be on the list, for example:
#if I wanted to claim a route, I have the function move_claimRoute and:
#claimRoute(self, city1, city2, color)
#to claim a route, you would call:
#game.make_move(game.move_claimRoute, [city1, city2, color])
#so, if the AI wants to claim the blue route between NEW YORK and BOSTON, the call should be:
#game.make_move(game.move_claimRoute, ['NEW YORK', 'BOSTON', 'blue'])
#the same concept is applied to all other move. If a move function has no parameters just pass an empty list, for example:
#game.make_move(game.move_drawDestinationCards, [])

######### REMEMBER: the first move every player makes should be to choose which destination cards they want to keep (they need to keep 2 or 3 out of the 3 they get at the setup)
class Game:
	def __init__(self, board, point_table, destination_deck, train_deck, players, current_player):
		self.board = board
		self.point_table = point_table
		self.destination_deck = CardManager(destination_deck)
		self.train_deck = CardManager(train_deck)
		self.train_cards_face_up = []
		self.number_of_players = len(players)
		self.players = players
		self.current_player = current_player
		self.players_choosing_destination_cards = False
		self.last_turn_player = -1
		self.moves_reference = {}
		self.game_over = False

	def set_moves_reference(self):
		self.moves_reference['chooseDestinationCards'] = self.move_choose_destination_cards
		self.moves_reference['claimRoute'] = self.move_claimRoute
		self.moves_reference['drawDestinationCards'] = self.move_drawDestinationCards
		self.moves_reference['drawTrainCard'] = self.move_drawTrainCard
		
	def copy(self):
		copy_players = []
		for p in self.players:
			copy_players.append(p.copy())
		g = Game(self.board.copy(), self.point_table, copy.copy(self.destination_deck), copy.copy(self.train_deck), copy_players, self.current_player)
		g.set_moves_reference()
		g.destination_deck = self.destination_deck.copy()
		g.train_deck = self.train_deck.copy()
		g.players_choosing_destination_cards = self.players_choosing_destination_cards
		return g

	#sets up the initial state of the players hands, face up cards and etc
	#remember, the first move of every player should be to choose the destination cards they want to keep
	def setup(self):
		self.set_moves_reference()
	
		for i in range (0, self.number_of_players):
			for j in range(0, 4):
				self.players[i].hand.append(self.draw_card(self.train_deck))
			for j in range(0, 3):
				self.players[i].hand.append(self.draw_card(self.destination_deck))

			self.players[i].choosing_destination_cards = True

		self.current_player = random.choice([x for x in range(0, self.number_of_players)])
		self.players_choosing_destination_cards = True

		for i in range(0, 5):
			self.addFaceUpTrainCard()

	#draws a card from a deck
	#deck => the deck (list) to be drawn from
	def draw_card(self, deck):
		card = deck.draw_card()

		if deck == self.train_deck and len(self.train_deck.deck) == 0:
			self.train_deck.reshuffle()

		return card

	#discards train cards to the discard pile
	#used be the function claim route
	def discard_cards(self, player_index, cards):
		for card in cards:
			self.train_deck.discard(card)
			self.players[player_index].hand.remove(card)

	#adds a new face up train cards
	#makes sure to never have 3 wild cards face up at the same time (rulebook)
	def addFaceUpTrainCard(self):
		if len(self.train_deck.deck) > 0:
			card = self.draw_card(self.train_deck)

			self.train_cards_face_up.append(card)

			if len(self.train_cards_face_up) == 5:
				card_count = collections.Counter(self.train_cards_face_up)

				if 'wild' in card_count:
					if card_count['wild'] >= 3:
						self.train_deck.discard(self.train_cards_face_up)
						self.train_cards_face_up = []

						x = 5 if len(self.train_deck.deck) + len(self.train_deck.discard_pile) >= 5 else len(self.train_deck.deck) + len(self.train_deck.discard_pile)
						for i in range(0, x):
							self.addFaceUpTrainCard()

	#passes the turn to the next player
	def next_players_turn(self):
		self.current_player = (self.current_player + 1) % self.number_of_players

	#lists all the destination cards pending the player choice of which to keep
	#player_index => index of the player
	def list_pending_destination_cards(self, player_index):
		result = []
		for card in self.players[player_index].hand:
			if type(card) != str:
				result.append(card)

		return result

	#makes the move of choosing the destination cards to keep
	def move_choose_destination_cards(self, args):
		#for card in args[1]:
			#print card
		self.choose_destination_cards(args[0], args[1])

	#chooses which destination cards to keep
	#player => index of the player choosing the cards
	#cards => list of destination cards (objects of class DestinationCard) to keep. All the other destiantion cards not in the list that the player currently has will be removed from the game
	#PS: Destination cards get added to the players hand of train cards until he decides which ones to keep
	def choose_destination_cards(self, player, cards):
		min_num_cards = 2 if self.players_choosing_destination_cards else 1

		#print "cards:" + str(cards)
		
		if len(cards) >= min_num_cards:
			#print self.players[player].hand
			for card in cards:
				self.players[player].hand.remove(card)
				self.players[player].hand_destination_cards.append(card)

			self.players[player].choosing_destination_cards = False

			if self.players_choosing_destination_cards:
				for i in range(0, self.number_of_players):
					if self.players[i].choosing_destination_cards == True:
						i = i - 1
						break
				if i == self.number_of_players - 1:
					self.players_choosing_destination_cards = False

			cards_to_remove = []
			for card in self.players[player].hand:
				if type(card) != str:
					cards_to_remove.append(card)

			for card in cards_to_remove:
				self.players[player].hand.remove(card)

			#print (self.players[player].hand)
			#raw_input('wait')

		if min_num_cards == 1 and len(cards) >= min_num_cards:
			self.next_players_turn()

	#tests whether the player has the cards needed to claim a route
	#player_index => index of the player
	#number_of_cards => integer of the number of cards needed to claim that route
	#color => string of the color the cards need to be to claim the route
	#returns False if the player doesn't have the cards needed
	#returns the list of cards he needs to use to claim the route
	#if the player doesn't have enough of the color, it will try to complete the requirements with wild cards
	def checkPlayerHandRequirements(self, player_index, number_of_cards, color):
		if len(self.players[player_index].hand) < number_of_cards:
			return False

		color = color.lower()

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

	#makes the move of claiming a route
	def move_claimRoute(self, args):
		#if len(args) == 2:
		#	return self.claimRoute(args[0], args[1])
		return self.claimRoute(args[0], args[1], args[2])		

	#claims a route of a specific color between two cities
	#city1 and city2 => strings of the two cities that form the route
	#color => string of the color of the route to claim
	#if the route is a gray route, pass color as the color you want to use to claim that route, for example:
	#if you want to claim a gray route with blue cards, pass 'blue' as the color
	def claimRoute(self, city1, city2, color):
		edge = self.board.get_free_connection(city1, city2, color, self.number_of_players)

		if edge != None and edge['owner'] == -1:
			route_color = edge['color'] if edge['color'] != 'GRAY' else color
			cards_needed = self.checkPlayerHandRequirements(self.current_player, edge['weight'], route_color)

			if cards_needed and self.players[self.current_player].number_of_trains >= edge['weight']:
				self.discard_cards(self.current_player, cards_needed)
				self.players[self.current_player].number_of_trains = self.players[self.current_player].number_of_trains - edge['weight']
				edge['owner'] = self.current_player
				self.players[self.current_player].points = self.players[self.current_player].points + self.point_table[edge['weight']]
			else:
				return False

			if self.players[self.current_player].number_of_trains <= 2:
				self.last_turn_player = self.current_player

			self.next_players_turn()

			return True

		return False

	#makes the move of drawing new destination cards
	def move_drawDestinationCards(self, args):
		return self.drawDestinationCards()

	#draws 3 new destination cards of which the player is required to keep at least 1 (rulebook)
	#the player that does this move needs to call the choose destination cards moves right after.
	def drawDestinationCards(self):
		if len(self.destination_deck.deck) == 0:
			return False

		x = 3 if len(self.destination_deck.deck) >= 3 else len(self.destination_deck.deck)
		for i in range(0, x):
			self.players[self.current_player].hand.append(self.draw_card(self.destination_deck))

		self.players[self.current_player].choosing_destination_cards = True

		return True

	#makes the move of drawing new train cards
	def move_drawTrainCard(self, card):

		return self.drawTrainCard(card)

	#draws a new train card either from the ones face up on the table or from the top of the deck
	#card => string of the card to draw. If value is 'top', draws a card from the top of the deck
	#to draw from the face up cards, just pass the string of the color of the card to draw as the parameter
	def drawTrainCard(self, card):
		if card == 'wild' and card in self.train_cards_face_up and self.players[self.current_player].drawing_train_cards == False:
			self.players[self.current_player].hand.append('wild')
			self.train_cards_face_up.remove('wild')
			self.addFaceUpTrainCard()
			self.next_players_turn()
			
			return True
		
		drawn = False
		
		if card == 'top':
			self.players[self.current_player].hand.append(self.draw_card(self.train_deck))
			drawn = True
			
		elif card in self.train_cards_face_up:
			self.players[self.current_player].hand.append(card)
			self.train_cards_face_up.remove(card)
			self.addFaceUpTrainCard()
			
			drawn = True
		
		if drawn:
			if card == 'top' and len(self.train_deck.deck) == 0:
				self.next_players_turn()
				return True

			elif len(self.train_deck.deck) == 0 and len(self.train_cards_face_up) == 0:
				self.next_players_turn()
				return True

			if self.players[self.current_player].drawing_train_cards:
				self.players[self.current_player].drawing_train_cards = False
				self.next_players_turn()
			
			else:
				self.players[self.current_player].drawing_train_cards = True
			
			return True
		
		return False
		
	#makes a move as the current player
	#read the description of how to use on the Game Class description
	def make_move(self, move, args):
		#print("args: " + str(args))
		#print(len(self.train_deck.deck))
		#print "Move made!  " + str(move)
		last_turn = False
		if self.current_player == self.last_turn_player:
			last_turn = True
		if not self.players[self.current_player].choosing_destination_cards or (self.players[self.current_player].choosing_destination_cards) and move == 'chooseDestinationCards':

			if move == 'chooseDestinationCards':
				self.move_choose_destination_cards(args)
			elif move == 'claimRoute':
				self.move_claimRoute(args)
			elif move == 'drawDestinationCards':
				self.move_drawDestinationCards(args)
			elif move == 'drawTrainCard':
				self.move_drawTrainCard(args)
			else:
				move(args)
		if last_turn:
			self.calculatePoints()
			self.game_over = True
			return sorted([x for x in self.players], key=comparePlayerKey)


	#returns a graph of all routes (edges) claimed by a player
	#player => index of the player
	def player_graph(self, player):
		G = nx.Graph()
		
		for node1 in self.board.graph:
			for node2 in self.board.graph[node1]:
				for edge in self.board.graph[node1][node2]:
					if self.board.graph[node1][node2][edge]['owner'] == player:
						G.add_edge(node1, node2, weight=self.board.graph[node1][node2][edge]['weight'])
		
		return G

	#calculates the points of all players at the end of the game
	def calculatePoints(self):
		longest_route_value = None
		longest_route_player = []
	
		for player in self.players:
			#print "This player has " + str(player.points) + " points from building routes"
			player_graph = self.player_graph(self.players.index(player))
		
			for destination in player.hand_destination_cards:
				try:
					if nx.has_path(player_graph, destination.destinations[0], destination.destinations[1]):
						#print "Finished " + str(destination.destinations) + "!  +" + str(destination.points)
						player.points = player.points + destination.points
					else:
						#print "Did not finish " + str(destination.destinations) + "!  -" + str(destination.points)
						player.points = player.points - destination.points
				except:
					#print "Did not finish " + str(destination.destinations) + "!  -" + str(destination.points)
					player.points = player.points - destination.points

			temparr = [self.findMaxWeightSumForNode(player_graph, v, []) for v in player_graph.nodes()]
			temp = 0
			if len(temparr) > 0:
				temp = max(temparr)
			
			if longest_route_value == None or temp >= longest_route_value:
				if temp > longest_route_value:
					longest_route_player = [self.players.index(player)]
				else:
					longest_route_player.append(self.players.index(player))

				longest_route_value = temp
		
		for player in longest_route_player:
			self.players[player].points = self.players[player].points + 10
	
	#calculates the longest route of a player
	#G => the graph from which to calculate (use a graph return by the function player_graph above)
	#source => the node from which to start
	#list_of_visited_edges => the list of the edges visited already
	#the function calculates the longest route in the calculatePoints function above by recursively calling this function updating the list of visited edges, for every node in the graph
	def findMaxWeightSumForNode(self, G, source, list_of_visited_edges):
		temp_edges = [e for e in G.edges() if e not in list_of_visited_edges and source in e]
		if len(temp_edges) == 0:
			return 0
		else:
			result = []
			result.extend([(self.findMaxWeightSumForNode(G, x, list_of_visited_edges+[(x,y)]) + G[x][y]['weight']) for (x,y) in temp_edges if source == y])
			result.extend([(self.findMaxWeightSumForNode(G, y, list_of_visited_edges+[(x,y)]) + G[y][x]['weight']) for (x,y) in temp_edges if source == x])
			return max(result)

	def get_possible_moves(self, player_index):
		pmoves = []
		if self.players_choosing_destination_cards == True:
			dest_card_set = self.list_pending_destination_cards(player_index)
			for x in range(2, len(dest_card_set) + 1):
				comb = itertools.combinations(dest_card_set, x)
				for cardset in comb:
					pmoves.append(Move('chooseDestinationCards', [player_index, list(cardset)]))
					#pmoves.append(Move(self.move_choose_destination_cards, [player_index, list(cardset)]))
		elif self.players[player_index].choosing_destination_cards == True:
			dest_card_set = self.list_pending_destination_cards(player_index)
			for x in range(1, len(dest_card_set) + 1):
				comb = itertools.combinations(dest_card_set, x)
				for cardset in comb:
					pmoves.append(Move('chooseDestinationCards', [player_index, list(cardset)]))
					#pmoves.append(Move(self.move_choose_destination_cards, [player_index, list(cardset)]))
		elif self.players[player_index].drawing_train_cards == True:
			pmoves.append(Move('drawTrainCard', 'top'))
			for card in self.train_cards_face_up:
				pmoves.append(Move('drawTrainCard', card))
				#pmoves.append(Move(self.move_drawTrainCard, card))				
		else:
			colors = ["RED", "ORANGE", "BLUE", "PINK", "WHITE", "YELLOW", "BLACK", "GREEN"]
			edges = self.board.graph.edges()
			#for city1 in self.board.graph:
			#	for city2 in self.board.graph:
			visited = []
			for (city1, city2) in edges:
				if (city1, city2) not in visited:
					visited.append((city1, city2))

					for color in colors:
						edge = self.board.get_free_connection(city1, city2, color, self.number_of_players)

						if edge != None:
							if self.checkPlayerHandRequirements(player_index, edge['weight'], color) != False:
								pmoves.append(Move('claimRoute', [city1, city2, color]))
								#pmoves.append(Move(self.move_claimRoute, [city1, city2, color]))
			if len(self.destination_deck.deck) > 0:
				pmoves.append(Move('drawDestinationCards',[]))
				#pmoves.append(Move(self.move_drawDestinationCards,[]))
			if len(self.train_deck.deck) > 0:
				pmoves.append(Move('drawTrainCard', 'top'))
				#pmoves.append(Move(self.move_drawTrainCard, 'top'))
			if len(self.train_cards_face_up) > 0:
				for card in self.train_cards_face_up:
					pmoves.append(Move('drawTrainCard', card))
					#pmoves.append(Move(self.move_drawTrainCard, card))
		return pmoves

	def printScoring(self, pnum):
		longest_route_player = []
	
		player = self.players[pnum]
		player_graph = self.player_graph(pnum)
	
		for destination in player.hand_destination_cards:
			try:
				if nx.has_path(player_graph, destination.destinations[0], destination.destinations[1]):
					print str(destination.destinations) + ' was completed! +' + str(destination.points)
				else:
					print str(destination.destinations) + ' was not completed! -' + str(destination.points)
			except:
				print str(destination.destinations) + ' was not completed! -' + str(destination.points)

		visited = []
		for node1 in self.board.graph:
			for node2 in self.board.graph[node1]:
				for edge in self.board.graph[node1][node2]:
					if self.board.graph[node1][node2][edge]['owner'] == pnum:
						visited.append((node1, node2))
						if not (node2, node1) in visited:
							print node1 + ", " + node2 + ": +" + str(self.point_table[self.board.graph[node1][node2][edge]['weight']])
		
	def getDCardScore(self, pnum):
		rscore = 0
		player = self.players[pnum]
		player_graph = self.player_graph(pnum)
		
		for destination in player.hand_destination_cards:
			try:
				if nx.has_path(player_graph, destination.destinations[0], destination.destinations[1]):
					#print "Finished " + str(destination.destinations) + "!  +" + str(destination.points)
					rscore = rscore + destination.points
				else:
					#print "Did not finish " + str(destination.destinations) + "!  -" + str(destination.points)
					rscore = rscore - destination.points
			except:
				#print "Did not finish " + str(destination.destinations) + "!  -" + str(destination.points)
				rscore = rscore - destination.points
		return rscore

