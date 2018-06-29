import numpy as np
import random
from sample_players import DataPlayer, BasePlayer
from datetime import datetime

VALID_MOVES_PER_NODE = 8
UCT_CONST = 1.4

inf = 1000000
epsilon = 0.001
win_score = 10000
lose_score = -10000


class CustomPlayer1(DataPlayer):
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE:
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)

        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            print(self.uct_search(state, 10000)[0])
            self.queue.put(self.uct_search(state, 10)[0])

    def create_node(self, state, parent=None, prior=0):
        node = {

        }
        pass



    def uct_search(self, state, max_iters):
        root = CustomPlayer.MCTSNode(state)
        for i in range(max_iters):
            leaf = root.selection()
            reward = self.evaluate(state)
            leaf.expand()
            leaf.backup(reward)
        print('uct search out', max(root.children.items(), lambda item: item[1].sum_visits))
        # tuple of (move, node)
        return max(root.children.items(), lambda item: item[1].sum_visits)[0]

    def evaluate(self, state):
        own_loc = state.locs[state.player()]
        opp_loc = state.locs[1 - state.player()]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

    class MCTSNode(object):
        def __init__(self, state, parent=None, prior=0):
            self.state = state
            self.parent = parent
            # self.move = move
            self.expanded = False
            self.children = {}
            self.prior = prior
            self.sum_value = 0
            self.sum_visits = 0

        def Q(self):
            return self.sum_value / (1 + self.sum_visits)

        def U(self):
            return UCT_CONST * np.sqrt(1 + self.sum_visits) * self.prior / (1 + self.sum_visits)

        def best_child(self):
            if not self.children.values():
                return self
            return max(self.children.values(), key=lambda node: node.Q() + node.U())

        def add_node(self, move, state, prior):
            self.children[move] = CustomPlayer.MCTSNode(state.result(move), parent=self, prior=prior)

        def selection(self):
            node = self
            while node.expanded:
                node = node.best_child()
            return node

        def expand(self):
            self.expanded = True
            for move in self.state.actions():
                self.add_node(move, self.state, np.random.random())

        def backup(self, estimate_reward):
            node = self
            while node is not None:
                node.sum_visits += 1
                node.sum_value += estimate_reward

                # estimate_reward = - estimate_reward #flip for opposin g player (negamax)

                node = node.parent


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
            # self.transposition_table = {}

            # self.queue.put(self.iterative_deepeningTT(state, depth=5000))

            self.iterative_deepening(state, depth=15000, timelimit=5000)

    def iterative_deepening(self, state, depth=15000000, timelimit=500):
        start = datetime.now()
        # action = random.choice(state.actions())
        action = None
        alpha = -inf
        beta = inf
        maxdepth = 0
        f = open('./logs/maxdepth_AB_sortedNodes_score1.txt', 'a')
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
        start = datetime.now()
        # action = random.choice(state.actions())
        action = None
        for depth in range(1, depth):
            # action = self.alphabeta(state, depth)
            action = self.alphabetaTT(state, depth)
            self.queue.put(action)
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
            # return self.score3(state, depth), alpha
            return self.score(state), alpha
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
