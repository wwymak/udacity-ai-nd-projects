import numpy as np
import random
from collections import namedtuple
from sample_players import DataPlayer, BasePlayer
from copy import deepcopy
from datetime import datetime

Entry = namedtuple('Entry', 'move depth value state upperbound lowerbound')

inf = 1000000
epsilon = 0.001
win_score = 10000
lose_score = -10000


class MTDfPlayer(BasePlayer):
    """ Implement an agent using any combination of techniques discussed
    in lecture (or that you find online on your own) that can beat
    sample_players.GreedyPlayer in >80% of "fair" matches (see tournament.py
    or readme for definition of fair matches).

    Implementing get_action() is the only required method, but you can add any
    other methods you want to perform minimax/alpha-beta/monte-carlo tree search,
    etc.

    **********************************************************************
    NOTE: The test cases will NOT be run on a machine with GPU access, or
          be suitable for using any other machine learning techniques.
    **********************************************************************
    """
    def __init__(self, player_id):
        super().__init__(player_id)

        self.transposition_table = {}

    def get_action(self, state):
        """ Choose an action available in the current state

        See RandomPlayer and GreedyPlayer for examples.

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired.

        **********************************************************************
        NOTE: since the caller is responsible for cutting off search, calling
              get_action() from your own code will create an infinite loop!
              See (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # randomly select a move as player 1 or 2 on an empty board, otherwise
        # return the optimal mtdf move at a fixed search depth
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.iterative_deepening(state, depth=100000, timelimit=1000)
            # self.queue.put(self.iterative_deepening(state, guess=0, depth=100000, timelimit=1000))


    def MT(self, state, gamma, depth, game_depth):
        """
        MT, a memory-enhanced version of Pearl’s Test from https://arxiv.org/ftp/arxiv/papers/1404/1404.1515.pdf
        :param state:
        :param gamma:
        :param depth:
        :param game_depth:
        :return:
        """
        best_move = None
        best_value = -inf
        upperbound = inf
        lowerbound = -inf
        if state in self.transposition_table and self.transposition_table[state].depth >= depth:
            ttLookup = self.transposition_table[state]
            lowerbound = ttLookup.lowerbound
            upperbound = ttLookup.upperbound

            if lowerbound > gamma:
                if depth == game_depth:
                    self.queue.put(ttLookup.move)
                return lowerbound
            if upperbound < gamma:
                if depth == game_depth:
                    self.queue.put(ttLookup.move)
                return self.transposition_table[state].upperbound

        if state.terminal_test() or (depth == 0):
            score = self.score(state)

            if score != 0:
                score = (score - 0.99 * depth * abs(score) / score)
            lowerbound = upperbound = best_value = score

        else:
            moves = state.actions()
            best_move = moves[0]

            for move in moves:
                if best_value >= gamma:
                    break
                nextstate = state.result(move)

                move_val =  -1 * self.MT(nextstate, -gamma, depth -1, game_depth )
                if best_value < move_val:
                    best_value = move_val
                    best_move = move

            if best_value < gamma:
                upperbound = best_value
            else:
                if depth == game_depth:
                    self.queue.put(best_move)
                lowerbound = best_value

        if depth > 0 and not state.terminal_test() and best_move in state.actions():
            entry = Entry(best_move, depth, best_value, state, upperbound, lowerbound)
            self.transposition_table[state] = entry
        # if best_move is not None:
        #     self.queue.put(best_move)
        return best_value

    def MTDriver(self, first, nextfunc, state, depth):
        upperbound = inf
        lowerbound = -inf
        bound = best_value = first

        while True:
            bound = nextfunc(lowerbound, upperbound, best_value)
            best_value = self.MT(state, bound - epsilon, depth, depth)
            if best_value < bound:
                upperbound = best_value
            else:
                lowerbound = best_value
            if lowerbound >= upperbound:
                break
        return best_value

    def SSS(self, state, depth):
        def nextfunc(lowerbound, upperbound, bestValue):
            return bestValue
        val = self.MTDriver(inf, nextfunc, state, depth)
        return val

    # def MTDf(self, state, guess, depth):
    #
    #     first = win_score
    #
    #
    #     self.alpha = self.MTDriver(state, first, nextfunc,depth)
    #
    #     return

    def iterative_deepening(self, state, depth=5000, timelimit=300):
        guess = 0
        start = datetime.now()
        for depth in range(1, depth):
            guess = self.SSS(state, depth)

            if (datetime.now() - start).microseconds > timelimit * 1000:
                print(depth, 'break at')
                break
        return


    def score(self, state):
        if state.terminal_test():
            if state.utility(self.player_id) > 0:
                return win_score
            elif state.utility(self.player_id) < 0:
                return lose_score
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)