import numpy as np
from sample_players import DataPlayer, BasePlayer
import logging
import random
from datetime import datetime
from copy import deepcopy
from collections import namedtuple

Entry = namedtuple('Entry', 'move depth value type')
EntryAB = namedtuple('Entry', 'depth value type')

logger = logging.getLogger(__name__)


inf = 1000000
epsilon = 0.001
win_score = 10000
lose_score = -10000

score3_pow = 2.5

class CustomPlayer(BasePlayer):
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
        self.score_func = self.score3

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
        # return the optimal minimax move at a fixed search depth of 3 plies
        if state.ply_count < 2:
            if 57 in state.actions():
                self.queue.put(57)
            else:
                self.queue.put(random.choice(state.actions()))

        else:
            self.iterative_deepening(state)

    def iterative_deepening(self, state, depth=15000000, timelimit=500):
        start = datetime.now()
        # action = random.choice(state.actions())
        action = None
        alpha = -inf
        beta = inf
        maxdepth = 0
        for depth in range(1, depth):
            if depth > maxdepth:
                maxdepth = depth
            bestmove = None
            tempscore = -inf
            for action in state.actions():
                val = self.AlphaBetaSortedNodesTT(state.result(action), depth, alpha, beta,False)
                if val > tempscore:
                    tempscore = val
                    bestmove = action

            self.queue.put(bestmove)

            if (datetime.now() - start).microseconds > timelimit * 1000:
                print('break', depth)
                break
        return action

    def sort_states(self,state, depth, should_sort=True):
        sortedNodes = []
        for action in state.actions():
            nextstate = state.result(action)
            sortedNodes.append((nextstate, action, self.score_func(nextstate, depth)))
        if should_sort:
            sortedNodes = sorted(sortedNodes, key=lambda node: node[2], reverse=True)
        sortedNodes = [node[0] for node in sortedNodes]
        return sortedNodes

    def AlphaBetaSortedNodesTT(self, state, depth, alpha, beta, maximizingPlayer):
        sortedStates = self.sort_states(state, depth, True)

        if state in self.transposition_table:
            ttEntry = self.transposition_table[state]
            if ttEntry.depth >= depth:
                if ttEntry.type == 'EXACT':
                    self.f2.write(
                        "{},{},{},{},{},{}\n".format(state.ply_count, depth, state.terminal_test(), state.player(),
                                                  self.player_id, 'EXACT'))
                    return ttEntry.value
                elif ttEntry.type == 'LOWER' and not maximizingPlayer:
                    alpha = max(alpha, ttEntry.value)
                elif ttEntry.type == 'UPPER' and maximizingPlayer:
                    beta = min(beta, ttEntry.value)
                if alpha >= beta:
                    return ttEntry.value

        if depth == 0 or state.terminal_test():
            return self.score_func(state, depth)
        if maximizingPlayer:
            v = -inf
            for state in sortedStates:
                tempval = self.AlphaBetaSortedNodesTT(state, depth - 1, alpha, beta, False)
                v = max(v, tempval)
                alpha = max(alpha, v)
                if beta <= alpha:
                    break  # beta cut-off

            # return v, alpha
        else:  # minimizingPlayer
            v = inf
            for state in sortedStates:
                tempval = self.AlphaBetaSortedNodesTT(state, depth - 1, alpha, beta, True)
                v = min(v, tempval)
                beta = min(beta, v)
                if beta <= alpha:
                    break  # alpha cut-off

        if v <= alpha:
            entry = EntryAB(depth, v, 'UPPER')
            self.transposition_table[state] = entry
        elif v >=beta:
            entry = EntryAB(depth, v, 'LOWER')
            self.transposition_table[state] = entry

        else:
            entry = EntryAB(depth, v, 'EXACT')
            self.transposition_table[state] = entry
        return v

    def ind2xy(self, i):
        return i % 13, i // 13

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

    def score2(self, state):
        if state.terminal_test():
            if state.utility(self.player_id) > 0:
                return win_score
            elif state.utility(self.player_id) < 0:
                return lose_score

        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_loc_xy = self.ind2xy(own_loc)
        opp_loc_xy = self.ind2xy(opp_loc)
        manhattan_own = abs(5-own_loc_xy[0]) + abs(4 - own_loc_xy[1])
        manhattan_opp = abs(5-opp_loc_xy[0]) + abs(4 - opp_loc_xy[1])
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) -manhattan_own - len(opp_liberties) + manhattan_opp

    def score3(self, state, depth):
        if state.terminal_test():
            if state.utility(self.player_id) > 0:
                return win_score
            elif state.utility(self.player_id) < 0:
                return lose_score

        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_loc_xy = self.ind2xy(own_loc)
        opp_loc_xy = self.ind2xy(opp_loc)
        manhattan_own = abs(5-own_loc_xy[0]) + abs(4 - own_loc_xy[1])
        manhattan_opp = abs(5-opp_loc_xy[0]) + abs(4 - opp_loc_xy[1])
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return (len(own_liberties) - len(opp_liberties) -manhattan_own  + manhattan_opp) * pow(score3_pow, depth-1)

