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
        self.player1 = game_agent.AlphaBetaPlayer()
        self.player2 = "Player2"
        self.game1 = isolation.Board(self.player1, self.player2, 9, 9)
        self.game1.setstate([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 57, 41])
        self.player_game1 = game_agent.MinimaxPlayer()
        self.player_game2 = "Player2"
        self.game2 = isolation.Board(self.player_game1, self.player_game2, 9, 9)
        self.game2.setstate([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 57, 41])

    def test_minimax_interface(self):
        print(self.game1.to_string())
        alpha_player = self.game1.active_player;
        alpha_move = alpha_player.alphabeta(self.game1.copy(), 3)
        print(self.game1.to_string())
        print(alpha_move)
        print(self.game2.to_string())
        player = self.game2.active_player
        move = player.minimax(self.game2.copy(), 3)
        print(self.game2.to_string())
        print(move)
        assert (alpha_move == move)


if __name__ == '__main__':
    unittest.main()
