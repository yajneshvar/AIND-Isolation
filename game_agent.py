"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Quantifies a player move where a move in the center of square is weighted higher
    while the center space is not crowded

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float("+inf")
    elif game.is_loser(player):
        return float("-inf")

    opponent = game.get_opponent(player)
    opponent_moves = game.get_legal_moves(opponent)
    my_moves = game.get_legal_moves(player)
    my_weighted_score = calculate_weigthed_score(my_moves, game.height, game.width)
    opponent_weighted_score = calculate_weigthed_score(opponent_moves, game.height, game.width)

    open_moves = len(game.get_blank_spaces())
    total_space = game.height*game.width
    if center_space_ratio(game) > 0.6:
        return my_weighted_score - opponent_weighted_score
    else:
        return float(len(my_moves) - len(opponent_moves))


def custom_score_2(game, player):
    """ while the center of board is empty game is scored on the distance between players
        when the center of board becomes crowded evaluate the number of moves available

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float("+inf")
    elif game.is_loser(player):
        return float("-inf")

    moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    if center_space_ratio(game) > 0.6:
        return distance_between_player(game)
    return float(len(moves) - len(opponent_moves))


def custom_score_3(game, player):
    """Calculates a weighted sum of the possible moves for the player
        When the board is less crowded it assigns more weight to moves far from the board
        When the board is crowded assigns more priority to greater number of moves


    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float("+inf")
    elif game.is_loser(player):
        return float("-inf")

    free_ratio = free_space_ratio(game)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    my_moves = game.get_legal_moves(player)
    return free_ratio*(distance_from_center(game, player)) + (1-free_ratio)*(float(len(my_moves) - len(opponent_moves)))


def free_space_ratio(game):
    """ Calculates the ratio of blank space to board spaces

    Parameters
    ----------
    game: `isolation.Board`
        An instance of `isolation.Board`

    Returns
    -------
    float
        Ratio of available spaces
    """
    free_space_count = len(game.get_blank_spaces())
    total_space = game.height * game.width
    return free_space_count/total_space


def center_space_ratio(game):
    """ Calculates the ratio of center space to board spaces

    Parameters
    ----------
    game: `isolation.Board`
        An instance of `isolation.Board`

    Returns
    -------
    float
        Ratio of available center spaces
    """
    def center_filter(move, h, w):
        return 0 + 2 < move[0] < w - 2 and 0 + 2 < move[1] < h - 2
    center_spaces = list(filter(lambda mov: center_filter(mov,game.height, game.width), game.get_blank_spaces()))
    return float(len(center_spaces)/(game.width*game.height))


def distance_between_player(game):
    """ Calculates the distance between players

    Parameters
    ----------
    game: `isolation.Board`
        An instance of `isolation.Board`

    Returns
    -------
    float
        distance between players
    """
    loc = game.get_player_location(game.active_player)
    loc_oppponent = game.get_player_location(game.inactive_player)
    distance_between = math.sqrt((loc[0] - loc_oppponent[0])**2 + (loc[1] - loc_oppponent[1])**2)
    return distance_between


def distance_from_center(game, player):
    """ Calculates the distance between player and center of board

    Parameters
    ----------
    game: `isolation.Board`
        An instance of `isolation.Board`

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        distance between player and center of board
    """
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    return float((h - y)**2 + (w - x)**2)


def calculate_weigthed_score(list_moves, height, width):
    """
    Weighted score of possible moves
    Parameters
    ----------
    list_moves: List
    height: integer
    width: integer

    Returns
    -------
    float
        Weighted sum of moves
    """

    scores = map(lambda move: assign_weight(move, height, width), list_moves)
    return sum(scores)


def assign_weight(move, h, w):
    """
    Weighted score of possible moves
    Parameters
    ----------
    move: (integer, integer)
        Possible move in a board (x,y)
    h: integer
        height of board
    w: integer
        width of board

    Returns
    -------
    float
        Weighted value of a move
    """

    x_cor = [0,w-1]
    y_cor = [0,h-1]

    corner_pieces = [(x,y) for x in x_cor for y in y_cor]
    if 0 + 2 < move[0] < w - 2 and 0 + 2 < move[1] < h - 2:
        return 2.0
    elif move in corner_pieces:
        return 0.5
    return 1.0


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score_2, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        if len(moves) == 0:
            return -1, -1

        result = max([(self.minvalue(game.forecast_move(move), game.active_player, depth-1), move)for move in moves],key=lambda x: x[0])
        return result[1]

    def minvalue(self, game, activeplayer, depth):
        """ Implements the min value function of the minimax algorithm

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        activeplayer: object
            Tracks the existing player for the intial move

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        int
            returns the move that results in smallest score

        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if game.utility(activeplayer) != 0:
            return game.utility(activeplayer)
        elif depth == 0:
            return self.score(game, activeplayer)

        moves = game.get_legal_moves()
        return min([self.maxvalue(game.forecast_move(move), activeplayer, depth-1) for move in moves])

    def maxvalue(self, game, activeplayer, depth):
        """ Implements the max value function for the minimax algorithm

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        activeplayer: object
            Tracks the existing player for the intial move

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
         int
            returns the move that results in the largest value
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if game.utility(activeplayer) != 0:
            return game.utility(activeplayer)
        elif depth == 0:
            return self.score(game, activeplayer)

        return max([self.minvalue(game.forecast_move(move), activeplayer, depth-1) for move in game.get_legal_moves()])


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 0
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        result = self.maxvalue(game, depth)
        return result[1]

    def minvalue(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """ Implements the min value function of the minimax algorithm with cutoff

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, (int, int))
            A tuple consisting of score, board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if game.utility(self) != 0:
            return game.utility(self), (-1, -1)
        elif depth == 0:
            return self.score(game, self), (-1, -1)

        v = float("+inf")
        best_move = (-1, -1)
        list_of_moves = []
        for move in game.get_legal_moves():
            list_of_moves.append(move)
            v_branch, tmp_move = self.maxvalue(game.forecast_move(move), depth-1, alpha, beta)
            v, best_move = min((v, best_move), (v_branch, move), key=lambda x: x[0])
            if v <= alpha:
                return v, best_move
            beta = min(v, beta)
        return v, best_move

    def maxvalue(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """ Implements the max value function for the minimax algorithm with cutoff

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers


        Returns
        -------
        (int, (int, int))
            A tuple consisting of score, board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if game.utility(self) != 0:
            return game.utility(self), (-1, -1)
        elif depth == 0:
            return self.score(game, self), (-1, -1)

        v = float("-inf")
        best_move = (-1,-1)
        for move in game.get_legal_moves():
            v_branch, tmp_move = self.minvalue(game.forecast_move(move), depth-1, alpha, beta)
            v, best_move = max((v, best_move), (v_branch, move), key=lambda x: x[0])
            if v >= beta:
                return v, best_move
            alpha = max(v, alpha)
        return v, best_move


