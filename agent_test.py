"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2, 9, 9)
        self.game.setstate([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 57, 41])

    def test_minimax_interface(self):
        print(self.game.to_string())
        alpha_player = game_agent.AlphaBetaPlayer()
        alpha_move = alpha_player.alphabeta(self.game.copy(), 3)
        print(self.game.to_string())
        print(alpha_move)
        player = game_agent.MinimaxPlayer()
        move = player.minimax(self.game.copy(), 3)
        print(self.game.to_string())
        print(move)
        assert (alpha_move == move)




if __name__ == '__main__':
    unittest.main()
