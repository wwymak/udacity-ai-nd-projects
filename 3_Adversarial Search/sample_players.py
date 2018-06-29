###############################################################################
#     YOU CAN MODIFY THIS FILE, BUT CHANGES WILL NOT APPLY DURING GRADING     #
###############################################################################
import logging
import pickle
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
class BasePlayer:
    def __init__(self, player_id):
        self.player_id = player_id
        self.timer = None
        self.queue = None
        self.context = None
        self.data = None

    def get_action(self, state):
        """ Implement a function that calls self.queue.put(ACTION) within the allowed time limit 

        See RandomPlayer and GreedyPlayer for examples.
        """
        raise NotImplementedError


class DataPlayer(BasePlayer):
    def __init__(self, player_id):
        super().__init__(player_id)
        try:
            with open("data.pickle", "rb") as f:
                self.data = pickle.load(f)
        except (IOError, TypeError) as e:
            logger.error(str(e))
            self.data = None


class RandomPlayer(BasePlayer):
    def get_action(self, state):
        """ Randomly select a move from the available legal moves.

        Parameters
        ----------
        state : `isolation.Isolation`
            An instance of `isolation.Isolation` encoding the current state of the
            game (e.g., player locations and blocked cells)
        """
        self.queue.put(random.choice(state.actions()))


class GreedyPlayer(BasePlayer):
    """ Player that chooses next move to maximize heuristic score. This is
    equivalent to a minimax search agent with a search depth of one.
    """
    def score(self, state):
        own_loc = state.locs[self.player_id]
        own_liberties = state.liberties(own_loc)
        return len(own_liberties)

    def get_action(self, state):
        """Select the move from the available legal moves with the highest
        heuristic score.

        Parameters
        ----------
        state : `isolation.Isolation`
            An instance of `isolation.Isolation` encoding the current state of the
            game (e.g., player locations and blocked cells)
        """
        self.queue.put(max(state.actions(), key=lambda x: self.score(state.result(x))))

class AlphaBetaPlayer(BasePlayer):
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
            # self.transposition_table = {}

            # self.queue.put(self.iterative_deepeningTT(state, depth=5000))

            # self.iterative_deepening(state, depth=15000, timelimit=5000)
            self.iterative_deepeningTT(state, depth=15000, timelimit=5000)


    def iterative_deepening(self, state, depth=15000000, timelimit=500):
        start = datetime.now()
        # action = random.choice(state.actions())
        action = None
        alpha = -inf
        beta = inf
        maxdepth = 0
        f = open('./logs/maxdepth.txt', 'a')
        for depth in range(1, depth):
            if depth > maxdepth:
                maxdepth = depth
            bestmove = None
            tempscore = -inf
            for action in state.actions():
                val, tempAlpha = self.AlphaBetaSortedNodesV2(state.result(action), depth, alpha, beta,False)
                if val > tempscore:
                    tempscore = val
                    bestmove = action
                if tempAlpha > alpha:
                    alpha = tempAlpha
            beta = tempscore
            self.queue.put(bestmove)
            f.write("{},{}\n".format(state.ply_count, maxdepth))
            if (datetime.now() - start).microseconds > timelimit * 1000:
                print('break', depth)
                break
        return action

    def iterative_deepeningTT(self, state, depth=1000, timelimit=300):
        maxdepth = 0
        f = open('./logs/maxdepth_alphabetaTT_score1.txt', 'a')
        start = datetime.now()
        # action = random.choice(state.actions())
        action = None
        for depth in range(1, depth):
            if depth > maxdepth:
                maxdepth = depth
            action = self.alphabetaTT(state, depth)
            self.queue.put(action)
            f.write("{},{}\n".format(state.ply_count, maxdepth))
            if (datetime.now() - start).microseconds > timelimit * 1000:
                print('break', depth)
                break
        return action

    def alphabeta(self, state, depth):


        def min_value(state, alpha, beta, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), alpha, beta, depth - 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        def max_value(state, alpha, beta, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), alpha, beta, depth - 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

        alpha = float("-inf")
        beta = float("inf")

        return max(state.actions(), key=lambda x: min_value(state.result(x), alpha, beta, depth - 1))

    def alphabetaTT(self, state, depth):

        def min_value(state, alpha, beta, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)

            if state in self.transposition_table:
                ttEntry = self.transposition_table[state]
                if ttEntry.depth >= depth:
                    if ttEntry.type == 'EXACT':
                        return ttEntry.value
                    # elif ttEntry.type == 'LOWER':
                    #     alpha = max(alpha, ttEntry.value)
                    elif ttEntry.type == 'UPPER':
                        beta = min(beta, ttEntry.value)
                    if alpha >= beta:
                        return ttEntry.value

            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), alpha, beta, depth - 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)

            entry = EntryAB(depth, value, 'UPPER')
            self.transposition_table[state] = entry
            return value

        def max_value(state, alpha, beta, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score2(state)

            if state in self.transposition_table:
                ttEntry = self.transposition_table[state]
                if ttEntry.depth >= depth:
                    if ttEntry.type == 'EXACT':
                        return ttEntry.value
                    elif ttEntry.type == 'LOWER':
                        alpha = max(alpha, ttEntry.value)
                    # elif ttEntry.type == 'UPPER':
                    #     beta = min(beta, ttEntry.value)
                    if alpha >= beta:
                        return ttEntry.value

            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), alpha, beta, depth - 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)

            entry = EntryAB(depth, value, 'LOWER')
            self.transposition_table[state] = entry

            return value

        alpha = float("-inf")
        beta = float("inf")


        return max(state.actions(), key=lambda x: min_value(state.result(x), alpha, beta, depth - 1))

    def sort_states(self,state):
        sortedNodes = []
        for action in state.actions():
            nextstate = state.result(action)
            sortedNodes.append((nextstate, action, self.score2(nextstate)))
        sortedNodes = sorted(sortedNodes, key=lambda node: node[2], reverse=True)
        sortedNodes = [node[0] for node in sortedNodes]
        return sortedNodes

    def AlphaBetaSortedNodes(self, state, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or state.terminal_test():
            return self.score2(state)
        sortedStates = self.sort_states(state)
        if maximizingPlayer:
            v = -inf
            for state in sortedStates:
                v = max(v, self.AlphaBetaSortedNodes(state, depth - 1, alpha, beta, False))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break  # beta cut-off
            return v
        else:  # minimizingPlayer
            v = inf
            for state in sortedStates:
                v = min(v, self.AlphaBetaSortedNodes(state, depth - 1, alpha, beta, True))
                beta = min(beta, v)
                if beta <= alpha:
                    break  # alpha cut-off
            return v

    def AlphaBetaSortedNodesV2(self, state, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or state.terminal_test():
            return self.score3(state, depth), alpha
            # return self.score2(state), alpha
        sortedStates = self.sort_states(state)
        if maximizingPlayer:
            v = -inf
            for state in sortedStates:
                tempval, _ = self.AlphaBetaSortedNodesV2(state, depth - 1, alpha, beta, False)
                v = max(v, tempval)
                alpha = max(alpha, v)
                if beta <= alpha:
                    break  # beta cut-off
            return v, alpha
        else:  # minimizingPlayer
            v = inf
            for state in sortedStates:
                tempval, _ = self.AlphaBetaSortedNodesV2(state, depth - 1, alpha, beta, True)
                v = min(v, tempval)
                beta = min(beta, v)
                if beta <= alpha:
                    break  # alpha cut-off
            return v, alpha

    def negascout(self, state, depth, alpha, beta, player_id):
        if state.terminal_test() or depth == 0:
            evalute = self.score(state)
            # if state.player() != player_id:
            #     return -evalute, None
            # else:
            return evalute, None
        player = deepcopy(player_id)
        best_action = state.actions()[0]
        for idx, action in enumerate(state.actions()):

            curr_player =( player + 1 )% 2
            if idx == 0:
                print('here', self.negascout(state.result(action), depth -1, -beta, -alpha, curr_player))
                alpha, _ = self.negascout(state.result(action), depth -1, -beta, -alpha, curr_player)
            else:
                alpha, _ = self.negascout(state.result(action), depth -1, -alpha-1, -alpha, curr_player)
            score = -score
            print(score)
            alpha = max(alpha, score)
            if alpha >= beta:
                best_action = action
                break
        return alpha, best_action

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
        return (len(own_liberties) - len(opp_liberties) -manhattan_own  + manhattan_opp) * pow(0.8, depth-1)



class MinimaxPlayer(BasePlayer):
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
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.minimax(state, depth=3))

    def minimax(self, state, depth):

        def min_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1))
            return value

        def max_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1))
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)


class MTDPlayer(BasePlayer):
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
            self.queue.put(self.mtdf(state, 0, depth=4)[0])
            # self.queue.put(self.iterative_deepening(state, depth=10, timelimit=280))

    def mtdf(self, state, guess, depth):
        upperbound = float("inf")
        lowerbound = float("-inf")
        while lowerbound < upperbound:
            if guess == lowerbound:
                beta = guess + 1
            else:
                beta = guess
            guess, action = self.alphaBetaWithMemory(state, beta - 1, beta, depth)
            if guess < beta:
                upperbound = guess
            else:
                lowerbound = guess
        return action, guess


    def mtdf_with_id(self, state, guess, depth):
        upperbound = float("inf")
        lowerbound = float("-inf")
        while lowerbound < upperbound:
            if guess == lowerbound:
                beta = guess + 1
            else:
                beta = guess
            guess, action, state = self.alphaBetaWithMemory(state, beta - 1, beta, depth)
            if guess < beta:
                upperbound = guess
            else:
                lowerbound = guess
        return action, guess

    def iterative_deepening(self, state, guess=0, depth=10, timelimit=280):
        guess = guess
        start = datetime.now()
        for depth in range(1, depth):
            action, guess = self.mtdf(state, guess, depth)
            if (datetime.now() - start).microseconds > timelimit * 1000:
                break
        return action

    def alphaBetaWithMemory1(self, state, alpha, beta, depth):
        # if state in self.context:
        if state in self.transposition_table:
            stored_alpha = self.transposition_table[state][0]
            stored_beta = self.transposition_table[state][1]
            stored_move = self.transposition_table[state][2]
            # stored_alpha = self.context[state][0]
            # stored_beta = self.context[state][1]
            # stored_move = self.context[state][2]

            if stored_alpha >= beta:
                return stored_alpha, stored_move
            if stored_beta <= alpha:
                return stored_beta, stored_move

        def min_value(state, alpha, beta, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), alpha, beta, depth - 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        def max_value(state, alpha, beta, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), alpha, beta, depth - 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

        action = max(state.actions(), key=lambda x: min_value(state.result(x), alpha, beta, depth - 1))
        value = min_value(state.result(action), alpha, beta, depth - 1)

        self.transposition_table[state] = alpha, beta, action
        # self.context[state] = alpha, beta, action

        return value, max(state.actions(), key=lambda x: min_value(state.result(x), alpha, beta, depth - 1))

    def alphaBetaWithMemory(self, state, alpha, beta, depth):
        a = deepcopy(alpha)
        b = deepcopy(beta)
        # if state in self.context:
        if state in self.transposition_table and self.transposition_table[state]['depth'] >= depth:
            stored_alpha = self.transposition_table[state]['lower']
            stored_beta = self.transposition_table[state]['upper']
            stored_value = self.transposition_table[state]['value']
            stored_move = self.transposition_table[state]['move']
            stored_type = self.transposition_table[state]['type']

            if stored_type == 'EXACT': # stored value is exact
                return stored_value

            if stored_type == 'LOWERBOUND' and stored_value > a:
                alpha = stored_value
            elif stored_type == 'UPPERBOUND' and stored_value <b:
                beta = stored_value # update upperbound beta if needed
                if alpha >= beta:
                    return stored_value # if lowerbound surpasses upperbound
        if depth == 0 or state.terminal_test():
            value = self.score(state)
            if value <= alpha:
                self.transposition_table[state]['value'] = value
                self.transposition_table[state]['depth'] = depth
                self.transposition_table[state]['type'] = 'LOWERBOUND'
            elif value >= beta: # an upperbound value
                self.transposition_table[state]['value'] = value
                self.transposition_table[state]['depth'] = depth
                self.transposition_table[state]['type'] = 'UPPERBOUND'
            else: # a true minimax value
                self.transposition_table[state]['value'] = value
                self.transposition_table[state]['depth'] = depth
                self.transposition_table[state]['type'] = 'EXACT'
            return value


        elif state.player() == state.player_id:
            value = float("-inf")
            sorted(state.actions(), key=lambda x: self.score(state.result(x)))

            while (value < beta):
                for action in state.actions():
                    c = state.result(action)
                    value = max(value,self.alphaBetaWithMemory(c, a, beta, depth - 1))
                    a = max(a, value)

        elif state.player() != state.player_id:
            value = float("inf")
            sorted(state.actions(), key=lambda x: -self.score(state.result(x)))

            while (value > alpha):
                for action in state.actions():
                    c = state.result(action)
                    value = min(value, self.alphaBetaWithMemory(c, a, beta, depth - 1))
                    b = min(b, value)



        def min_value(state, alpha, beta, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), alpha, beta, depth - 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        def max_value(state, alpha, beta, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            """
            g: = -INFINITY;
            a: = alpha; 
            c: = firstchild(n);
            while (g < beta) and (c != NOCHILD) do
            g: = max(g, AlphaBetaWithMemory(c, a, beta, d - 1));
            a: = max(a, g);
            c: = nextbrother(c);
            """

            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), alpha, beta, depth - 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

        action = max(state.actions(), key=lambda x: min_value(state.result(x), alpha, beta, depth - 1))
        value = min_value(state.result(action), alpha, beta, depth - 1)

        # if value <= alpha:
        #     self.transposition_table[state][0] = alpha
        #
        #     if g <= alpha then n.upperbound:=
        #     g;
        #     store
        #     n.upperbound;
        #     / *Found
        #     an
        #     accurate
        #     minimax
        #     value - will
        #     not occur if called
        #     with zero window * /
        #     if g > alpha and g < beta then
        #     n.lowerbound: = g;
        #     n.upperbound: = g;
        #     store
        #     n.lowerbound, n.upperbound;
        #     / *Fail
        #     high
        #     result
        #     implies
        #     a
        #     lower
        #     bound * /
        #     if g >= beta then n.lowerbound:=
        #     g;
        #     store
        #     n.lowerbound;
        #     return g;

        self.transposition_table[state] = (alpha, beta, action)
        # self.context[state] = alpha, beta, action

        return value#, max(state.actions(), key=lambda x: min_value(state.result(x), alpha, beta, depth - 1))

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return 20 * len(own_liberties) - len(opp_liberties)

