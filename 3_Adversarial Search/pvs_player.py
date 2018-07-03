import numpy as np
import random
from sample_players import DataPlayer, BasePlayer
from datetime import datetime
inf = 1000000
epsilon = 0.001
win_score = 10000
lose_score = -10000



class PVSPlayer(BasePlayer):
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
        self.score_func = self.score

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

            # self.queue.put(self.iterative_deepeningTT(state, depth=5000))
            self.queue.put(self.iterative_deepening(state, depth=15000, timelimit=5000))


    def iterative_deepening(self, state, depth=15000000, timelimit=500):
        start = datetime.now()
        # action = random.choice(state.actions())
        action = None
        alpha = -inf
        beta = inf
        for depth in range(1, depth):
            bestmove = None
            # alpha = inf
            for action in state.actions():
                # val, tempAlpha = self.AlphaBetaSortedNodesV2(state.result(action), depth, alpha, beta,False)
                val = self.negascout(state.result(action), depth, alpha, beta,True)
                if val > alpha:
                    alpha = val
                    bestmove = action
                # if tempAlpha > alpha:
                #     alpha = tempAlpha
            # beta = tempscore
            self.queue.put(bestmove)
            if (datetime.now() - start).microseconds > timelimit * 1000:
                print('break', depth)
                break
        return action


    def sort_states(self,state):
        sortedNodes = []
        for action in state.actions():
            nextstate = state.result(action)
            sortedNodes.append((nextstate, action, self.score2(nextstate)))
        sortedNodes = sorted(sortedNodes, key=lambda node: node[2], reverse=True)
        sortedNodes = [node[0] for node in sortedNodes]
        return sortedNodes

    def negascout(self, state, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or state.terminal_test():
            score = self.score(state)
            if maximizingPlayer:
                return score
            else:
                return -score
        # b = copy(beta)
        b =beta
        bestscore = -inf

        sortedNodes = self.sort_states(state)
        firstChild = True
        for state in sortedNodes:
            score = -self.negascout(state, -b, -alpha, depth -1, not maximizingPlayer)
            if(score > alpha and score < beta and not firstChild):
                score = -self.negascout(state, -beta, -score, depth -1, not maximizingPlayer)
            bestscore = max(bestscore, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                return alpha
            b = alpha + 1
        return bestscore

        for state in sortedNodes:
            if not firstChild:
                score = -self.negascout(state, depth - 1, -alpha - 1, -alpha, False)
                if alpha < score and score < beta:
                    score = -self.negascout(state, depth - 1, -beta, -score, False)
            else:
                firstChild = False
                score = -self.negascout(state, depth - 1, -beta, -alpha, False)
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return alpha



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
        return len(own_liberties) - len(opp_liberties) -manhattan_own + 0.1 * depth
