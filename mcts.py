import tickettoride.py
from __future__ import division
import datetime
import random
from math import log, sqrt

class MonteCarlo(object):
    def __init__(self, game, player, **kwargs):
        #inits game state list, statistics tables, etc.
        self.game = game.copy()
        self.player = player
        self.states = []
        #arbitrary number
        self.max_moves = 100
        self.wins = {}
        self.plays = {}
        seconds = kwargs.get('time', 60)
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.C = kwargs.get('C', 1.4)

    def update(self, state):
        #appends game state to history
        self.states.append(state)

    def get_play(self):
        #calculate best move from current game state
        self.max_depth = 0
        state = self.states[-1]
        player = self.game.current_player
        possible_plays = self.game.get_possible_moves(player)
        if not possible_plays:
            return
        if len(possible_plays) == 1:
            return possible_plays[0]
        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.simulate()
            games += 1
        moves_states = [(p, self.make_move(p.function, p.args)) for p in possible_plays]
        print games, datetime.datetime.utcnow() - begin

        #need to fix this part for sure...
        percent_wins, move = max((self.wins.get((player, S), 0) / self.plays.get((player, S), 1), p) for p, S in moves_states)
        for x in sorted(
                ((100 * self.wins.get((player, S), 0) /
                  self.plays.get((player, S), 1),
                  self.wins.get((player, S), 0),
                  self.plays.get((player, S), 0), p)
                 for p, S in moves_states),
            reverse=True
        ):
            print "{3}: {0:.2f}% ({1} / {2})".format(*x)
        print "Maximum depth searched:", self.max_depth
        return move

    def simulate(self):
        # actually implement the decision making of mcts
        # visited = set()
        # statesCopy = self.states[:]
        # state = statesCopy[-1]
        # expand = True
        # for i in xrange(self.maxMoves):
        #     choices = self.game.get_possible_moves(self.player)
        #     play = random.choice(choices)
        #     state = self.game.make_move(play.function, play.args)
        #     self.game.current_player = self.player
        #     statesCopy.append(state)
        #     if expand and (self.player, state) not in self.plays:
        #         expand = False
        #         self.plays[(self.player, state)]
        #         self.wins[(self.player, state)]
        #     visited.add((self.player, state))
        #
        #     if self.game.last_turn_player >= -1:
        #         break
        # # need to fix this part too
        # for player, state in visited:
        #     if (player, state) not in self.plays:
        #         continue
        #     self.plays[(player, state)] += 1
        #     if player == self.game.last_turn_player:
        #         self.wins[(player, state)] += 1

        #vers. 2
        plays, wins = self.plays, self.wins
        visited = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = self.game.current_player

        expand = True
        for t in xrange(1, self.max_moves + 1):
            plays = self.game.get_possible_moves(self.player)
            moves_states = [(p, self.game.make_move(p.function, p.args)) for p in plays]

            if all(plays.get((player, S)) for p, S in moves_states):
                log_total = log(sum(plays[(player, S)] for p, S in moves_states))
                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.C * sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                move, state = random.choice(moves_states)

            states_copy.append(state)

            #this needs work
            if expand and (player, state) not in plays:
                expand = False
                plays[(player, state)] = 0
                wins[(player, state)] = 0
                if t > self.max_depth:
                    self.max_depth = t
            visited.add((player, state))
            player = self.game.current_player
            if self.game.last_turn_player >= -1:
                break

            for player, state in visited:
                if (player, state) not in plays:
                    continue

                plays[(player, state)] += 1

                #needs work in deciding how to deal with what nodes are "winners" in tickettoride context
                if player == self.game.last_turn_player:
                    wins[(player, state)] += 1
