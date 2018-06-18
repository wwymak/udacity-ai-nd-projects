import numpy as np
import random
from sample_players import DataPlayer

VALID_MOVES_PER_NODE = 8
UCT_CONST = 1.4

#  action value Q(s, a), visit count N(s, a),
# and prior probability P(s, a). The tree is traversed by simulation (that
# is, descending the tree in complete games without backup), starting
# from the root state. At each time step t of each simulation, an action at
# is selected from state st
# a Q t = ( argmax ( ) s a, , + ( u s a))

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


class CustomPlayer(DataPlayer):
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
            self.queue.put(self.mtdf(state, 0, depth=5)[0])
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

            alpha = max(stored_alpha, alpha)
            beta = min(beta, stored_beta)

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

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)
