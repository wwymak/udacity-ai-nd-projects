import random
import numpy as np
from sample_players import DataPlayer

# node instance for each part of the MCTree
# count the wins/visits to see how favorable a node is
class Node():
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = set()
        self.wins = 0
        self.visits = 0
        self.expanded = False


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
    def get_score(self, node):
        Q = node.value / node.visits
        U = np.sqrt(node.parent.visits)/ node.visits
        return Q + U

    # def get_score(self, state):
    #     own_loc = state.locs[self.player_id]
    #     opp_loc = state.locs[1 - self.player_id]
    #     own_liberties = state.liberties(own_loc)
    #     opp_liberties = state.liberties(opp_loc)
    #     return len(own_liberties) - len(opp_liberties)

    def add_child(self, move, node):
        node.children[move] =

    def uct_search(self, state, depth):
        root_node = self.create_node(state)  #root node
        for step in range(depth):
            leaf_node = self.tree_policy(root_node)
            reward = self.default_policy(state)
            self.backup(leaf_node, reward)
        return self.action_from_node(self.best_child(root_node, 0))

    def action_from_node(self, node):
        pass


    def create_node(self,state, parent=None):
        node = {}
        node.state = state
        node.parent = parent
        node.children = {}
        node.value = 0
        node.visits = 0
        node.expanded = False
        return node

    def best_child(self, node):
        child_values = []
        for child_node in node.children:
            child_val = child_node.value / child_node.visits + np.sqrt(2 * np.log(node.visits)/ child_node.visits)
            child_values.append(child_val)
        return node.children[np.argmax(node.children.wins)]


    def tree_policy(self, node, state):
        while not state.terminal_test():
            if node.expanded == False:
                return self.expand(node)
            else:
                node = self.best_child(node)
        return node

    def default_policy(self, state):
        while not state.terminal_test():
            next_action = random.choice(state.actions())
            state = state.result(next_action)
            reward = self.get_score(state)

        return reward

    def expand(self, node):
        node.expanded = True


    def backup(self, node, reward_value):
        curr_node = node
        while curr_node.parent is not None:
            curr_node.visits += 1
            curr_node.value += reward_value
            curr_node = curr_node.parent

