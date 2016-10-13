from ttroptimized import *
from loadgraphfile import *
from loaddestinationdeck import *
from Visualization import *
import multiprocessing as mp
from PathAgent import *
from AStarSeries import *
from mcts2 import *

def run(i, mode="usa"):
	if mode == "usa":
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa_destinations.txt')), make_train_deck(12, 14), [Player(emptyCardDict(), 45, 0), Player(emptyCardDict(), 45, 0)], 0)
	if mode == "usa1910":
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa1910_destinations.txt')), make_train_deck(12, 14), [Player(emptyCardDict(), 45, 0), Player(emptyCardDict(), 45, 0)], 0, [3, 2, 3, 1, False, True, False])
	if mode == "usa_megagame":
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa_megagame_destinations.txt')), make_train_deck(12, 14), [Player(emptyCardDict(), 45, 0), Player(emptyCardDict(), 45, 0)], 0, [5, 3, 4, 1, True, True, False])
	if mode == "usa_bigcities":
		game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('usa_bigcities_destinations.txt')), make_train_deck(12, 14), [Player(emptyCardDict(), 45, 0), Player(emptyCardDict(), 45, 0)], 0, [4, 2, 4, 1, False, False, False])
	if mode == "europe":
		game_object = Game(Board(loadgraphfromfile('europe.txt')), point_table(), destinationdeckdict(loaddestinationdeckfromfile('europe_destinations.txt'), "europe"), make_train_deck(12, 14), [Player(emptyCardDict(), 45, 0), Player(emptyCardDict(), 45, 0)], 0, [3, 2, 3, 1, True, False, True])

	game_object.setup()

	gh = GameHandler(game_object, [TAStarAgent(), PathAgent()], 'data3/AvM')

	#gh.play(i, True)
	gh.play(i)
	return game_object

#if __name__ == '__main__':
#	pool = mp.Pool(20)

#	anything = range(0, 10000)

#	pool.map(run, anything)

#	pool.terminate()
#i = 0
#while(True):
#	run(i)
#	i = i + 1

t = run(0, "europe")
#t = run(0, "usa_megagame")

#game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), loaddestinationdeckfromfile('usa_destinations.txt'), make_train_deck(12, 14), [Player([], 45, 0),Player([], 45, 0),Player([], 45, 0), Player([], 45, 0), Player([], 45, 0)], 0)


#gh = GameHandler(game_object, [AStarAgent(), TrollStarAgent(), EAStarAgent(), PAStarAgent(), Agent()], 'data/testdata')
#gh.play(0)
#gh = GameHandler(game_object, [PathAgent(), PathAgent()], 'data/testdata')

#pa = PathAgent()
#print pa.decide(game_object, 0)

#show_graph(game_object.board.graph)
