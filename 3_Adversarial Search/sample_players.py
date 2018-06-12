###############################################################################
#     YOU CAN MODIFY THIS FILE, BUT CHANGES WILL NOT APPLY DURING GRADING     #
###############################################################################
import logging
import pickle
import random
import datetime
from copy import deepcopy

logger = logging.getLogger(__name__)


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


class MCTSPlayer(BasePlayer):
    def __init__(self, timelimit=2):
        self.states = [] #history of game state
        self.max_moves_sim = 50 #max number of moves per simulation
        self.c = 1.5 # exploratory const
        self.timelimit = datetime.timedelta(seconds=timelimit)

        self.win = {}
        self.moves = {}

    def update(self, state):
        self.states.append(state)

    def play(self):
        start = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - start < self.timelimit:
            self.simulation()

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
        if state.ply_count < 2: self.queue.put(random.choice(state.actions()))
        self.queue.put(self.minimax(state, depth=3))



    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)


    def simulation(self, state):
        state_list = [state]
        active_player = state.player()
        visited_states = set()

        expand = True

        for iter in self.max_moves_sim:
            actions = state.actions()
            move = random.choice(actions)
            state = state.result(move)
            state_list.append(state)

            if expand and (active_player, state) not in self.moves:
                expand = False
                self.moves[(active_player, state)] = 0
                self.win[(active_player, state)] = 0

            visited_states.add((active_player, state))

            active_player = state.player()

            if state.terminal_test():
                if state.utility(active_player) > 0:
                    winner = active_player
                elif state.utility(active_player) < 0:
                    winner = abs(1 - active_player)
                break

        for player, state in visited_states:
            if (player, state) not in self.moves:
                continue
            self.moves[(player, state)] += 1
            if player == winner:
                self.win[(player, state)] += 1



        pass

    def backpropagation(self):

        pass