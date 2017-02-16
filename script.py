from ttroptimized import *
from loadgraphfile import *
from loaddestinationdeck import *
from Visualization import *
from configLoader import *
import multiprocessing as mp
from PathAgent import *
from AStarSeries import *
from mcts2 import *
from HastyAgent import *
from HungryAgent import *

#def run(i, mode="usa", num_of_players=2):
def run(configFile):

	#Loads configuration settings relevant to game setup
	configuration = getGameConfiguration(configFile)
	i = configuration['run_num']
	num_of_players = configuration['num_players']
	mode = configuration['board']
	game_point_table = point_table()
	if 'point_table' in configuration:
		game_point_table = configuration['point_table']
	train_deck = (12, 14)
	if 'train_deck' in configuration:
		train_deck = configuration['train_deck']

	player = []
	if mode == "usa":
		trainCount = 45
		variants = [3, 2, 3, 1, True, False, False, False, False, False]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa_destinations.txt')), make_train_deck(12, 14), player, 0)
		"""
	if mode == "usa1910":
		trainCount = 45
		variants = [3, 2, 3, 1, False, True, False, False, False, False]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa1910_destinations.txt')), make_train_deck(12, 14), player, 0, [3, 2, 3, 1, False, True, False, False, False, False])
		"""
	if mode == "usa_megagame":
		trainCount = 45
		variants = [5, 3, 4, 1, True, True, False, False, False, False]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa_megagame_destinations.txt')), make_train_deck(12, 14), player, 0, [5, 3, 4, 1, True, True, False, False, False, False])
		"""
	if mode == "usa_bigcities":
		trainCount = 45
		variants = [4, 2, 4, 1, False, False, False, False, False, False]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa_bigcities_destinations.txt')), make_train_deck(12, 14), player, 0, [4, 2, 4, 1, False, False, False, False, False, False])
		"""
	if mode == "europe":
		trainCount = 45
		variants = [3, 2, 3, 1, True, False, True, False, False, False]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('europe.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('europe_destinations.txt'), "europe"), make_train_deck(12, 14), player, 0, [3, 2, 3, 1, True, False, True, False, False, False])
		"""
	if mode == "switzerland":
		trainCount = 40
		variants = [5, 2, 3, 1, True, False, False, True, False, False]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 40, 0))
		game_object = Game(Board(loadgraphfromfile('switzerland.txt')), point_table(), loadswitzerlanddestinationdeck('switzerland_destinations.txt', 'switzerland_country_country_destinations.txt', 'switzerland_city_country_destinations.txt'), make_train_deck(12, 14), player, 0, [5, 2, 3, 1, True, False, False, True, False, False])
		"""
	if mode == "nordic_countries":
		trainCount = 40
		variants = [5, 2, 3, 1, False, True, False, False, True, False]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 40, 0))
		game_object = Game(Board(loadgraphfromfile('nordic_countries.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('nordic_countries_destinations.txt')), make_train_deck(12, 14), player, 0, [5, 2, 3, 1, False, True, False, False, True, False])
		"""
	if mode == "india":
		trainCount = 45
		variants = [4, 2, 3, 1, True, False, False, False, False, True]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('india.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('india_destinations.txt')), make_train_deck(12, 14), player, 0, [4, 2, 3, 1, True, False, False, False, False, True])
		"""

	for j in range(0, num_of_players):
		player.append(Player(emptyCardDict(), trainCount, 0))

	game_object = Game(Board(loadgraphfromfile(mode + '.txt')), game_point_table, destinationdeckdict(loaddestinationdeckfromfile(mode + '_destinations.txt')), make_train_deck(train_deck[0], train_deck[1]), player, 0, variants)

	game_object.setup()

	#gh = GameHandler(game_object, [AStarAgent(), PathAgent()], 'data3/AvP')
	gh = GameHandler(game_object, [HungryAgent(), PathAgent(), HastyAgent()], 'data3/HvPvHa')

	#gh.play(i, True)
	gh.play(i)
	return [game_object, gh]

#if __name__ == '__main__':
#	pool = mp.Pool(20)

#	anything = range(0, 10000)

#	pool.map(run, anything)

#	pool.terminate()
#i = 0
#while(True):
#	run(i)
#	i = i + 1

#results = [0, 0, 0]
#total_points = [0, 0, 0]

#num_of_games = 100

#for i in range(0,num_of_games):
#t = run(0, "usa", 3)
t = run("config.txt")	
#	total_points[0] += t.players[0].points
#	total_points[1] += t.players[1].points
#	total_points[2] += t.players[2].points
	
#	index = [t.players[0].points, t.players[1].points, t.players[2].points]
#	index = index.index(max(index))
	
#	results[index] += 1

#print [x / num_of_games for x in total_points]
#print results

#t = run(0, "usa_megagame")

#game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), loaddestinationdeckfromfile('usa_destinations.txt'), make_train_deck(12, 14), [Player([], 45, 0),Player([], 45, 0),Player([], 45, 0), Player([], 45, 0), Player([], 45, 0)], 0)


#gh = GameHandler(game_object, [AStarAgent(), TrollStarAgent(), EAStarAgent(), PAStarAgent(), Agent()], 'data/testdata')
#gh.play(0)
#gh = GameHandler(game_object, [PathAgent(), PathAgent()], 'data/testdata')

#pa = PathAgent()
#print pa.decide(game_object, 0)

#show_graph(game_object.board.graph)
