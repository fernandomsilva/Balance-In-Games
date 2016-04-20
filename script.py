from tickettoride import *
from loadgraphfile import *
from loaddestinationdeck import *
from Visualization import *

if __name__ == '__main__':
	game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), loaddestinationdeckfromfile('usa_destinations.txt'), make_train_deck(12, 14), [Player([], 45, 0), Player([], 45, 0), Player([], 45, 0)], 0)
	game_object.setup()

	gh = GameHandler(game_object, [AStarAgent(), RAStarAgent(), Agent()])

	gh.play()
	show_graph(game_object.board.graph)
