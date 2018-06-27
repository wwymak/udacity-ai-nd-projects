import numpy as np
import random
from sample_players import DataPlayer, BasePlayer
from datetime import datetime
inf = 1000000
epsilon = 0.001
win_score = 10000
lose_score = -10000

class PVSPlayer(BasePlayer):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.transposition_table = {}
        self.score_func = self.score

    def ind2xy(self, i):
        return (i % 13, i // 13)

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
            # self.transposition_table = {}

            self.queue.put(self.iterative_deepeningTT(state, depth=5000))
            # self.queue.put(self.iterative_deepening(state, depth=5000))

    def iterative_deepeningTT(self, state, depth=1000, timelimit=300):
        start = datetime.now()
        # action = random.choice(state.actions())
        action = None
        for depth in range(1, depth):
            action, _ = self.pvs(state, depth, -inf, inf)
            self.queue.put(action)
            if (datetime.now() - start).microseconds > timelimit * 1000:
                print('break', depth)
                break
        return action

    def pvs(self, state, depth, alpha, beta, ply=1):
        if state.terminal_test():
            return [], state.utility(self.player_id)
        if depth <= 0:
            return [], self.score_func(state)

        best_move = []
        best_value = alpha

        for idx, move in enumerate(state.actions()):
            if idx == 0 or depth == 1 or (beta-alpha) == 1:
                nextmoves, score = self.pvs(state.result(move), depth - 1,
                                               -beta, -best_value, (ply + 1) %2)
            else:
                _, score = self.pvs(state.result(move), depth - 1,
                                            -best_value - 1, -best_value, (ply + 1) %2)

                score = -score
                if score > best_value:
                    nextmoves, score = self.pvs(state.result(move), depth - 1,
                                               -beta, -best_value, (ply + 1) %2)
                else:
                    continue

            score = -score
            if score > best_value:
                best_value = score
                best_move = [move] + nextmoves
            elif not best_move:
                best_move = [move] + nextmoves

            if best_value >= beta:
                break

        return best_move, best_value