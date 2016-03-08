from tickettoride import *
from loadgraphfile import *

g = Game(Board(loadgraphfromfile('usa.txt')), point_table(), [1,2,3,4,5,6], make_train_deck(12, 14), [Player([], 45, 0), Player([], 45, 0)], 0)
g.setup()
