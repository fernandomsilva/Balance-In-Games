from tickettoride import *
from mcts import *
import numpy as np
import networkx as nx

class tickettorideAction(object):
    def __init__(self, action):
        self.action = action

    def __eq__(self, other):
        return self.action == other.action

class tickettorideState(object):
    def __init__(self, game, actions, pnum):
        self.actions = []
        for action in actions:
            self.actions.append(tickettorideAction(action))
        self.state = game
        self.pnum = pnum

    def perform(self, action):
        game = self.game.copy()
        game.make_move(action.function, action.args)
        return tickettorideState(game)

    def reward(self, parent, action):
        destpoints = 0
        opengraph = self.state.player_plus_free_graph(self.pnum)
        dcards = self.state.players[self.pnum].hand_destination_cards
        for destcard in dcards:
            try:
                spath = nx.shortest_path(opengraph, destcard.destinations[0], destcard.destinations[1])
                for i in range(0, len(spath) - 1):
                    for edge in opengraph[destcard.destinations[0]][destcard.destinations[1]]:
                        if self.state.board.graph[destcard.destinations[0]][destcard.destinations[1]][edge]['owner'] == self.pnum:
                            destpoints = destpoints + 50
            except:
                pass
        return (destpoints + self.state.players[self.pnum].points) * -1

    def is_terminal(self):
        return False

    def __eq__(self, other):
        return self.action == other.action

class MCTSAgent:
    def __init__(self):
        pass

    def decide(self, game, pnum):
        mcts = MCTS(tree_policy=UCB1(c=1.41),
                    default_policy=random_terminal_roll_out,
                    backup=monte_carlo)
        root = StateNode(tickettorideState(game, game.get_possible_moves(pnum), pnum))
        return mcts(root)