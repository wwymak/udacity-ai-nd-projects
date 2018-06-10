import random
import numpy as np
from sample_players import DataPlayer



class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only *required* method. You can modify
    the interface for get_action by adding named parameters with default
    values, but the function MUST remain compatible with the default
    interface.

    **********************************************************************
    NOTES:
    - You should **ONLY** call methods defined on your agent class during
      search; do **NOT** add or call functions outside the player class.
      The isolation library wraps each method of this class to interrupt
      search when the time limit expires, but the wrapper only affects
      methods defined on this class.

    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.
    **********************************************************************
    """
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
        self.queue.put(self.uct_search(state, depth=3))

    #reward function
    def get_score(self, node, uct_const):
        Q = node.value / node.visits
        # U = np.sqrt(node.parent.visits)/ node.visits
        U = uct_const * np.sqrt(2 * np.log(node.parent.number_visits) / (1 + node.number_visits))

        return Q + U
    #
    # def value_estimate(self, state):
    #     own_loc = state.locs[self.player_id]
    #     opp_loc = state.locs[1 - self.player_id]
    #     own_liberties = state.liberties(own_loc)
    #     opp_liberties = state.liberties(opp_loc)
    #     return len(own_liberties) - len(opp_liberties)

    def add_child(self, move, node):
        node.children[move] = self.create_node(node.state, node)
        pass

    def uct_search(self, state, depth):
        root_node = self.create_node(state)  #root node
        for step in range(depth):
            leaf_node = self.tree_policy(root_node)
            reward = self.default_policy(leaf_node.state)
            self.backup(leaf_node, reward)
        best_root_child, move = max(root_node, lambda node: node.visits)
        # best_root_child, move = self.best_child(root_node, 0)
        return move



    def create_node(self,state, parent=None, move=None):
        node = {}
        node['move'] = move
        node['state'] = state
        node['parent'] = parent
        node['children'] = {}
        node['value'] = 0
        node['visits'] = 0
        node['expanded'] = False
        return node

    # return the best child from the node and the action that lead to it
    def best_child(self, node, uct_const = 1):

        move_max = max(node.children.keys(), key=lambda node: self.get_score(node, uct_const))

        return node.children[move_max], move_max
        # child_values = []
        # for move, child_node in node.children.items():
        #     child_val = child_node.value / child_node.visits + np.sqrt(2 * np.log(node.visits)/ child_node.visits)
        #     child_values.append(child_val)
        # return node.children[np.argmax(node.children.wins)]


    def tree_policy(self, node):
        while not node['state'].terminal_test():
            if node['expanded'] == False:
                return self.expand(node)
            else:
                node = self.best_child(node)
        return node

    def default_policy(self, state):
        while not state.terminal_test():
            next_action = random.choice(state.actions())
            state = state.result(next_action)
            # reward = self.value_estimate(state)
        if state.utility > 0:
            return 1
        else:
            return 0

    def expand(self, node):
        node.expanded = True
        for move in node.state.actions():
            self.add_child(move, node)

    # negamax
    def backup(self, node, reward_value):
        curr_node = node
        while curr_node is not None:
            curr_node.visits += 1
            curr_node.value += reward_value
            reward_value = -reward_value
            curr_node = curr_node.parent

