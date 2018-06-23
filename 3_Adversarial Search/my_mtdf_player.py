import numpy as np
import random
from collections import namedtuple
from sample_players import DataPlayer
from copy import deepcopy
from datetime import datetime

Entry = namedtuple('Entry', 'move depth value state upperbound lowerbound')

inf = 1000000
epsilon = 0.001
win_score = 10000
lose_score = -10000


class MTDfPlayer(DataPlayer):
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
        print(player_id, 'my player id')

        self.transposition_table = {}
        self.move = None

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
            # self.queue.put(self.mtdf(state, 0, depth=4)[0])
            self.queue.put(self.iterative_deepening(state, guess=0, depth=10, timelimit=1000))

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
        value = -inf
        upperbound = inf
        lowerbound = -inf
        if state in self.transposition_table and self.transposition_table[state].depth >= depth:
            # print('yes')
            if self.transposition_table[state].lowerbound > gamma:
                if depth == game_depth:
                    self.move = self.transposition_table[state].move
                return self.transposition_table[state].lowerbound, self.transposition_table[state].move
            if self.transposition_table[state].upperbound < gamma:
                if depth == game_depth:
                    self.move = self.transposition_table[state].move
                return self.transposition_table[state].upperbound, self.transposition_table[state].move

        if state.terminal_test() or depth == 0:
            lowerbound = upperbound = value = self.score(state)
        else:
            moves = state.actions()
            best_move = moves[0]
            self.move = best_move

            for move in moves:
                if value >= gamma:
                    break
                statecopy = deepcopy(state)
                nextstate = statecopy.result(move)

                # move_val =  1 * self.MT(nextstate, gamma, depth -1, game_depth )[0]
                move_val =  -1 * self.MT(nextstate, -gamma, depth -1, game_depth )[0]
                if value < move_val:
                    value = move_val
                    best_move = move

            if value < gamma:
                upperbound = value
            else:
                if depth == game_depth:
                    self.move = best_move
                lowerbound = value

        if depth > 0 and not state.terminal_test():
            entry = Entry(best_move, depth, value, state, upperbound, lowerbound)
            self.transposition_table[state] = entry

        return value, best_move

    def MTDriver(self, first, nextfunc, state, depth):
        upperbound = inf
        lowerbound = -inf
        bound = value = first

        while True:
            bound = nextfunc(bound, value)
            # print('bound', bound)
            value, best_move = self.MT(state, bound - epsilon, depth, depth)
            # depth = depth -1
            # print(value, best_move, bound)
            if value < bound:
                upperbound = value
            else:
                lowerbound = value
            if lowerbound >= upperbound:
                break
        return value, best_move

    def MTDf(self, state, guess, depth):
        def nextfunc(bound, guess):
            # print('guess', guess)
            # print('nextufn', bound)
            if guess < bound:
                return guess
            else:
                return guess + 1

        value, best_move = self.MTDriver(guess, nextfunc, state, depth)

        return best_move, value

    def iterative_deepening(self, state, guess=0, depth=35, timelimit=300):
        guess = guess
        start = datetime.now()
        # action = random.choice(state.actions())
        action = None
        for depth in range(1, depth):
            a = datetime.now()
            action, guess = self.MTDf(state, guess, depth)
            self.queue.put(action)
            # self.queue.put(self.move)
            if not action:
                print('action err!!')
            # print((datetime.now() - a).microseconds / 1000)
            # print('cf time', (datetime.now() - start).microseconds)
            if (datetime.now() - start).microseconds > timelimit * 1000:
                break
        return action



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