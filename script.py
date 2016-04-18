from tickettoride import *
from loadgraphfile import *
from loaddestinationdeck import *



game_object = Game(Board(loadgraphfromfile('usa.txt')), point_table(), loaddestinationdeckfromfile('usa_destinations.txt'), make_train_deck(12, 14), [Player([], 45, 0), Player([], 45, 0), Player([], 45, 0)], 0)
game_object.setup()
gh = GameHandler(game_object, [AStarAgent(), RAStarAgent(), Agent()])
gh.play()
#g.choose_destination_cards(0, [g.players[0].hand[-1], g.players[0].hand[-2]])
#g.choose_destination_cards(1, [g.players[1].hand[-1], g.players[1].hand[-2]])
