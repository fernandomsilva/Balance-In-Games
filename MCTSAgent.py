from tickettoride import *
from mcts import *
import networkx as nx
from mcts.mcts import *
from mcts.graph import *
from mcts.tree_policies import *
from mcts.default_policies import *
from mcts.backups import *

class tickettorideAction(object):
    def __init__(self, action):
        self.action = action

    def __eq__(self, other):
        return self.action == other.action

    def getFunction(self):
        return self.action.function

    def getArgs(self):
        return self.action.args

class tickettorideState(object):
    def __init__(self, game, actions, pnum, parent = None):
        self.actions = []
        for action in actions:
            self.actions.append(tickettorideAction(action))
        self.state = game
        self.pnum = pnum
        self.parent = parent
        self.n = 0
        self.q = 0

    def perform(self, action):
        print("performing " + action.getFunction())
        game = self.state
        game.make_move(action.getFunction(), action.getArgs())
        #if (action.getFunction() == "drawTrainCard"):
            #print("game getting set to game over")
            #game.game_over = True
        game.players_choosing_destination_cards = False
        # print("possible moves at this point: ")
        # stuff = game.get_possible_moves(self.pnum)
        # for s in stuff:
        #     print(s.function)
        return tickettorideState(game, game.get_possible_moves(self.pnum), self.pnum, self)

    def reward(self, parent, action):
        return self.state.players[self.pnum].points * -1 - self.state.getDCardScore(self.pnum)

    def is_terminal(self):
        if(self.state.players[self.pnum].number_of_trains <= 2):
            print("Game over reached!")
            self.state.game_over = True
        return self.state.game_over

    def __eq__(self, other):
        return (self.game == other.game)

    def __str__(self):
        return "tis a state node"

class MCTSAgent:
    def __init__(self):
        pass

    def decide(self, game, pnum):
        mcts = MCTS(tree_policy=UCB1(c=1.41),
                    default_policy=random_terminal_roll_out,
                    backup=monte_carlo)
        root = tickettorideState(game, game.get_possible_moves(pnum), pnum)
        next_state = StateNode(None, root)
        best_action = mcts(next_state)
        print("the best action was: " + best_action.function)
        return best_action