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
            self.uct_search(state, 100)[0]
            print(self.uct_search(state, 10000)[0])
            # self.queue.put(self.uct_search(state, 10)[0])

    def uct_search(self, state, max_iters):
        root = CustomPlayer.MCTSNode(state)
        root.expand()
        print('uct')
        for i in range(max_iters):
            leaf = root.selection()
            print('getreward')
            reward = self.evaluate(state)
            print(reward)
            leaf.expand()
            leaf.backup(reward)
        print('uct search out', max(root.children.items(), lambda item: item[1].sum_visits))
        #tuple of (move, node)
        return max(root.children.items(), lambda item: item[1].sum_visits)[0]



    def evaluate(self, state):
        print('here')
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

        def U (self):
            return UCT_CONST * np.sqrt(1 + self.sum_visits) * self.prior / (1 + self.sum_visits)

        def best_child(self):
            if not self.children.values():
                return self
            return max(self.children.values(), key=lambda node : node.Q() + node.U())

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









