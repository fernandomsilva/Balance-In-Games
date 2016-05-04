from tickettoride import *
from loadgraphfile import *
from loaddestinationdeck import *
from Visualization import *
import multiprocessing as mp
from PathAgent import *

def run(i):
	game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), loaddestinationdeckfromfile('usa_destinations.txt'), make_train_deck(12, 14), [Player([], 45, 0),Player([], 45, 0),Player([], 45, 0), Player([], 45, 0), Player([], 45, 0)], 0)
	game_object.setup()

	gh = GameHandler(game_object, [AStarAgent(), RAStarAgent(), TrollStarAgent(), PAStarAgent(), Agent()], 'data/testdata')

	#gh.play(i)
	return game_object

#if __name__ == '__main__':
#	pool = mp.Pool()
#
#	anything = range(0, 20)
#
#	pool.map(run, anything)
#
#	pool.terminate()
#t = run(0)

#game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), loaddestinationdeckfromfile('usa_destinations.txt'), make_train_deck(12, 14), [Player([], 45, 0),Player([], 45, 0),Player([], 45, 0), Player([], 45, 0), Player([], 45, 0)], 0)
game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), loaddestinationdeckfromfile('usa_destinations.txt'), make_train_deck(12, 14), [Player([], 45, 0),Player([], 45, 0)], 0)
game_object.setup()

#gh = GameHandler(game_object, [AStarAgent(), TrollStarAgent(), EAStarAgent(), PAStarAgent(), Agent()], 'data/testdata')
#gh.play(0)
gh = GameHandler(game_object, [Agent(), Agent()], 'data/testdata')
gh.play(0)

pa = PathAgent()
pa.decide(game_object, 0)

#show_graph(game_object.board.graph)
