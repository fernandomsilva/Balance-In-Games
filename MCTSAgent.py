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
    def __init__(self, game, actions, pnum):
        self.actions = []
        for action in actions:
            self.actions.append(tickettorideAction(action))
        self.state = game
        self.pnum = pnum

    def perform(self, action):
        print("performing " + action.getFunction())
        #game = self.state.copy()
        self.state.make_move(action.getFunction(), action.getArgs())
        if (action.getFunction() == "drawTrainCard"):
            print("game getting set to game over")
            self.state.game_over = True
        self.state.players_choosing_destination_cards = False
        self.state.current_player = self.pnum
        return tickettorideState(self.state, self.state.get_possible_moves(self.pnum), self.pnum)

    def reward(self, parent, action):
        points = self.state.players[self.pnum].points * -1 - self.state.getDCardScore(self.pnum)
        return points

    def is_terminal(self):
        if(self.state.players[self.pnum].number_of_trains <= 2):
            print("Game over reached!")
            self.state.game_over = True
        return self.state.game_over

    def __eq__(self, other):
        return self.action == other.action

class MCTSAgent:
    def __init__(self):
        pass

    def decide(self, game, pnum):
        mcts = MCTS(tree_policy=UCB1(c=1.41),
                    default_policy=random_terminal_roll_out,
                    backup=monte_carlo)

        root = StateNode(None, tickettorideState(game, game.get_possible_moves(pnum), pnum))
        best_action = mcts(root)
        print("the best action was: " + best_action.function)
        return best_action