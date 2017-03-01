from ttroptimized import *
from loadgraphfile import *
from loaddestinationdeck import *
#from Visualization import *
from configLoader import *
import multiprocessing as mp
from PathAgent import *
from AStarSeries import *
from mcts2 import *
from HastyAgent import *
from HungryAgent import *
from MultiStrategyAgent import *
from OneStepThinkerAgent import *
from LongRouteJunkieAgent import *

def evaluate(params, number_of_players, n=100):
	game_obj, game_handler = runGenectic(params)
	results = [0 for i in range(0, number_of_players)]
	num_of_games = n

	hungry_agent_index = 0
	path_agent_index = 1

	for i in range(0, num_of_games):
		t = runGenectic(params)

		#for j in range(0, number_of_players):
		#	total_points[j] += t[0].players[j].points

		index = [t[0].players[k].points for k in range(0, number_of_players)]
		
		index = index.index(max(index))
		
		results[index] += 1

	return results[path_agent_index] / num_of_games


def runGenectic(params):
	#Loads configuration settings relevant to game setup
	num_of_players = 2
	mode = "usa"
	trainCount = 45 #params
	game_point_table = point_table() #params
	train_deck = (12, 14) #params

	player = []
	variants = [3, 2, 3, 1, True, False, False, False, False, False, 4, 5, 2, 3, 2, 10, 15, 2]

	for j in range(0, num_of_players):
		player.append(Player(emptyCardDict(), trainCount, 0))

	game_graph = loadgraphfromfile(mode + '.txt')
	destination_deck = loaddestinationdeckfromfile(mode + '_destinations.txt')

	game_object = Game(Board(game_graph), game_point_table, destinationdeckdict(destination_deck, mode), make_train_deck(train_deck[0], train_deck[1]), player, 0, variants)
	game_object.setup()

	#gh = GameHandler(game_object, [AStarAgent(), PathAgent()], 'data3/AvP')
	#gh = GameHandler(game_object, [HungryAgent(), PathAgent(), MultiStrategyAgent()], 'data3/HvPvHa')
	#gh = GameHandler(game_object, [HungryAgent(), PathAgent(), OneStepThinkerAgent()], 'data3/HvPvHa')
	#gh = GameHandler(game_object, [HungryAgent(), OneStepThinkerAgent()], 'data3/HvPvHa')
	gh = GameHandler(game_object, [HungryAgent(), PathAgent(), OneStepThinkerAgent(), LongRouteJunkieAgent()], 'data3/HvPvHa')

	#gh.play(i, True)
	gh.play(i)
	return [game_object, gh]

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
	num_remove_routes = configuration['random_remove_routes']

	player = []
	if mode == "usa":
		trainCount = 45
		variants = [3, 2, 3, 1, True, False, False, False, False, False, 4, 5, 2, 3, 2, 10, 15, 2]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa_destinations.txt')), make_train_deck(12, 14), player, 0)
		"""
	if mode == "usa1910":
		trainCount = 45
		variants = [3, 2, 3, 1, False, True, False, False, False, False, 4, 5, 2, 3, 2, 10, 15, 2]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa1910_destinations.txt')), make_train_deck(12, 14), player, 0, [3, 2, 3, 1, False, True, False, False, False, False])
		"""
	if mode == "usa_megagame":
		trainCount = 45
		variants = [5, 3, 4, 1, True, True, False, False, False, False, 4, 5, 2, 3, 2, 10, 15, 2]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa_megagame_destinations.txt')), make_train_deck(12, 14), player, 0, [5, 3, 4, 1, True, True, False, False, False, False])
		"""
	if mode == "usa_bigcities":
		trainCount = 45
		variants = [4, 2, 4, 1, False, False, False, False, False, False, 4, 5, 2, 3, 2, 10, 15, 2]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa_bigcities_destinations.txt')), make_train_deck(12, 14), player, 0, [4, 2, 4, 1, False, False, False, False, False, False])
		"""
	if mode == "europe":
		trainCount = 45
		variants = [3, 2, 3, 1, True, False, True, False, False, False, 4, 5, 2, 3, 2, 10, 15, 2]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('europe.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('europe_destinations.txt'), "europe"), make_train_deck(12, 14), player, 0, [3, 2, 3, 1, True, False, True, False, False, False])
		"""
	if mode == "switzerland":
		trainCount = 40
		variants = [5, 2, 3, 1, True, False, False, True, False, False, 4, 5, 2, 3, 2, 10, 15, 2]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 40, 0))
		game_object = Game(Board(loadgraphfromfile('switzerland.txt')), point_table(), loadswitzerlanddestinationdeck('switzerland_destinations.txt', 'switzerland_country_country_destinations.txt', 'switzerland_city_country_destinations.txt'), make_train_deck(12, 14), player, 0, [5, 2, 3, 1, True, False, False, True, False, False])
		"""
	if mode == "nordic_countries":
		trainCount = 40
		variants = [5, 2, 3, 1, False, True, False, False, True, False, 4, 5, 2, 3, 2, 10, 15, 2]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 40, 0))
		game_object = Game(Board(loadgraphfromfile('nordic_countries.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('nordic_countries_destinations.txt')), make_train_deck(12, 14), player, 0, [5, 2, 3, 1, False, True, False, False, True, False])
		"""
	if mode == "india":
		trainCount = 45
		variants = [4, 2, 3, 1, True, False, False, False, False, True, 4, 5, 2, 3, 2, 10, 15, 2]
		"""
		for j in range(0, num_of_players):
			player.append(Player(emptyCardDict(), 45, 0))
		game_object = Game(Board(loadgraphfromfile('india.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('india_destinations.txt')), make_train_deck(12, 14), player, 0, [4, 2, 3, 1, True, False, False, False, False, True])
		"""

	for j in range(0, num_of_players):
		player.append(Player(emptyCardDict(), trainCount, 0))

	game_graph = loadgraphfromfile(mode + '.txt')
	destination_deck = loaddestinationdeckfromfile(mode + '_destinations.txt')

	for j in range(0, num_remove_routes):
		target = random.choice(game_graph.edges())
		game_graph.remove_edge(target[0], target[1])
		if target[1] in game_graph[target[0]]:
			if 1 in game_graph[target[0]][target[1]]:
				game_graph[target[0]][target[1]][0] = game_graph[target[0]][target[1]][1]
				game_graph.remove_edge(target[0], target[1], key = 1)


	isolated_cities = nx.isolates(game_graph)
	game_graph.remove_nodes_from(isolated_cities)
	remove_destination_cards = []

	for destination_card in destination_deck:
		if destination_card.destinations[0] in isolated_cities or destination_card.destinations[1] in isolated_cities:
			remove_destination_cards.append(destination_card)

	for destination_card in remove_destination_cards:
		destination_deck.remove(destination_card)

	game_object = Game(Board(game_graph), game_point_table, destinationdeckdict(destination_deck, mode), make_train_deck(train_deck[0], train_deck[1]), player, 0, variants)
	game_object.setup()

	#gh = GameHandler(game_object, [AStarAgent(), PathAgent()], 'data3/AvP')
	#gh = GameHandler(game_object, [HungryAgent(), PathAgent(), MultiStrategyAgent()], 'data3/HvPvHa')
	#gh = GameHandler(game_object, [HungryAgent(), PathAgent(), OneStepThinkerAgent()], 'data3/HvPvHa')
	#gh = GameHandler(game_object, [HungryAgent(), OneStepThinkerAgent()], 'data3/HvPvHa')
	gh = GameHandler(game_object, [HungryAgent(), PathAgent(), OneStepThinkerAgent(), LongRouteJunkieAgent()], 'data3/HvPvHa')

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

number_of_players = 4

results = [0 for i in range(0, number_of_players)]
total_points = [0 for i in range(0, number_of_players)]

num_of_games = 500
#t = run("config.txt")
for i in range(0,num_of_games):
	t = run("config.txt")

	for j in range(0, number_of_players):
		total_points[j] += t[0].players[j].points

	index = [t[0].players[k].points for k in range(0, number_of_players)]

	#total_points[0] += t[0].players[0].points
	#total_points[1] += t[0].players[1].points
	#if t[0].number_of_players > 2:
	#	total_points[2] += t[0].players[2].points
	#	index = [t[0].players[0].points, t[0].players[1].points, t[0].players[2].points]
	#else:
	#	index = [t[0].players[0].points, t[0].players[1].points]
	
	
	index = index.index(max(index))
	
	results[index] += 1

print [x / num_of_games for x in total_points]
print results

#t = run(0, "usa_megagame")

#game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), loaddestinationdeckfromfile('usa_destinations.txt'), make_train_deck(12, 14), [Player([], 45, 0),Player([], 45, 0),Player([], 45, 0), Player([], 45, 0), Player([], 45, 0)], 0)


#gh = GameHandler(game_object, [AStarAgent(), TrollStarAgent(), EAStarAgent(), PAStarAgent(), Agent()], 'data/testdata')
#gh.play(0)
#gh = GameHandler(game_object, [PathAgent(), PathAgent()], 'data/testdata')

#pa = PathAgent()
#print pa.decide(game_object, 0)

#show_graph(game_object.board.graph)
