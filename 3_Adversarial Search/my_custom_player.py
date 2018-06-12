import numpy as np
import random
from sample_players import DataPlayer

VALID_MOVES_PER_NODE = 9
UCT_CONST = 1.4

#  action value Q(s, a), visit count N(s, a),
# and prior probability P(s, a). The tree is traversed by simulation (that
# is, descending the tree in complete games without backup), starting
# from the root state. At each time step t of each simulation, an action at
# is selected from state st
# a Q t = ( argmax ( ) s a, , + ( u s a))

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

        self.queue.put(random.choice(state.actions()))

    class MCTSNode(object):
        def __init__(self, state, parent=None, move=None):
            self.parent = parent
            self.move = move
            self.state = state
            self.num_visits = 0
            self.children = {}
            self.children_value = np.zeros([VALID_MOVES_PER_NODE], dtype=np.float32)
            self.children_visits = np.zeros([VALID_MOVES_PER_NODE], dtype=np.float32)
            self.children_prior = np.zeros([VALID_MOVES_PER_NODE], dtype=np.float32)
            self.expanded = False

        # using np broadcasting to calc all the q values of the children
        def child_Q(self):
            return self.children_value / (1 + self.children_visits)

        def child_U (self):
            return UCT_CONST * np.sqrt(1 + self.num_visits) * self.children_prior / (1 + self.children_visits)







