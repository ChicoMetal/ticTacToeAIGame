import unittest

from tictactoe import initial_state, player, X, O, actions
from tictactoe import EMPTY as _, result, winner, terminal, utility, minimax


class TestPlayer(unittest.TestCase):
    def test_x_play(self):
        start = initial_state()
        self.assertEqual(X, player(start))

    def test_o_play(self):
        board = initial_state()
        board[0][0] = X
        self.assertEqual(O, player(board))

    def test_all_players(self):
        board = initial_state()
        next_player = player(board)
        for i in range(9):
            board[i % 3][i // 3] = next_player
            if next_player == "The game is already over":
                self.assertEqual(0,0)
            elif i % 2 == 0:
                self.assertEqual(X, next_player)
            else:
                self.assertEqual(O, next_player)
            next_player = player(board)


class TestPossibleActions(unittest.TestCase):
    def test_empty(self):
        empty_board = initial_state()
        self.assertEqual(9, len(actions(empty_board)))

    def test_two_left(self):
        almost_full_board = [[X, O, X], [_, O, _], [O, X, X]]
        self.assertEqual(2, len(actions(almost_full_board)))
        self.assertEqual({(1, 0), (1, 2)}, actions(almost_full_board))

    def test_full(self):
        full_board = [[X, O, X], [O, X, O], [X, O, X]]
        # self.assertEqual(0, len(actions(full_board)))
        self.assertEqual("The game is already over", actions(full_board))


class TestResult(unittest.TestCase):
    def test_from_empty(self):
        empty_board = initial_state()
        new_board = result(empty_board, (1, 0))
        self.assertEqual(9, len(actions(empty_board)))
        self.assertEqual(empty_board, initial_state())
        self.assertEqual(8, len(actions(new_board)))
        self.assertEqual(new_board, [[_]*3, [X, _, _], [_]*3])

    def test_not_allowed(self):
        empty_board = initial_state()
        self.assertRaisesRegex(ValueError, "The action is not valid",
                                result, empty_board, (3, 7))
    def test_not_allowed_negative(self):
        empty_board = initial_state()
        self.assertRaisesRegex(ValueError, "The action is not valid",
                                result, empty_board, (-1, 0))


class TestWinner(unittest.TestCase):
    def test_empty(self):
        empty_board = initial_state()
        self.assertIsNone(winner(empty_board))

    def test_full(self):
        full_board = [[X, O, X], [O, X, O], [X, O, X]]
        self.assertEqual(X, winner(full_board))
        full_board = [[X, O, X],
                        [O, O, X],
                        [X, X, O]]
        self.assertIsNone(winner(full_board))

    def test_row(self):
        fake_board = [[_]*3, [_]*3, [O]*3]
        self.assertEqual(O, winner(fake_board))

    def test_column(self):
        fake_board = [[O, _, _]]*3
        self.assertEqual(O, winner(fake_board))

    def test_diagonal(self):
        fake_board = [[X, _, _], [_, X, _], [_, _, X]]
        self.assertEqual(X, winner(fake_board))
        fake_board = [[_, _, O], [_, O, _], [O, _, _]]
        self.assertEqual(O, winner(fake_board))


class TestTerminal(unittest.TestCase):
    def test_empty(self):
        empty_board = initial_state()
        self.assertFalse(terminal(empty_board))

    def test_full(self):
        full_board = [[X, O, X], [O, X, O], [X, O, X]]
        self.assertTrue(terminal(full_board))
        full_board = [[X, O, X],
                        [O, O, X],
                        [X, X, O]]
        self.assertTrue(terminal(full_board))

    def test_row(self):
        fake_board = [[_]*3, [_]*3, [O]*3]
        self.assertTrue(terminal(fake_board))

    def test_almost_full(self):
        almost_full_board = [[X, O, X], [_, O, _], [O, X, X]]
        self.assertFalse(terminal(almost_full_board))


class TestUtility(unittest.TestCase):
    def test_full(self):
        full_board = [[X, O, X], [O, X, O], [X, O, X]]
        self.assertEqual(1, utility(full_board))
        full_board = [[X, O, X],
                        [O, O, X],
                        [X, X, O]]
        self.assertEqual(0, utility(full_board))

    def test_row(self):
        fake_board = [[_]*3, [_]*3, [O]*3]
        self.assertEqual(-1, utility(fake_board))

    def test_column(self):
        fake_board = [[O, _, _]]*3
        self.assertEqual(-1, utility(fake_board))

    def test_diagonal(self):
        fake_board = [[X, _, _], [_, X, _], [_, _, X]]
        self.assertEqual(1, utility(fake_board))
        fake_board = [[_, _, O], [_, O, _], [O, _, _]]
        self.assertEqual(-1, utility(fake_board))


class TestMinMax(unittest.TestCase):
    # def test_tictactoe_is_a_draw(self):
    #     board = initial_state()
    #     self.assertEqual(0, score(board))

    def test_almost_finished(self):
        board = [[_, X, O],
                    [O, X, X],
                    [X, _, O]]
        self.assertEqual((2, 1), minimax(board))
        # self.assertEqual(0, score(board))

    def test_middle(self):
        board = [[X, X, O],
                    [_, _, _],
                    [O, _, _]]
        self.assertEqual((1, 1), minimax(board))
        # self.assertEqual(1, score(board))

    def test_still_a_draw(self):
        board = [[X, _, _],
                    [_, _, _],
                    [_, _, _]]
        self.assertEqual((1, 1), minimax(board))
        # self.assertEqual(0, score(board))

    # def test_bad_start(self):
    #     board = [[X, _, O],
    #                 [_, _, _],
    #                 [_, _, _]]
    #     self.assertEqual(1, score(board))

    def test_fork(self):
        board = [[_, X, O],
                    [_, O, _],
                    [X, X, _]]
        self.assertEqual((2, 2), minimax(board))
        # self.assertEqual(-1, score(board))

    def test_lost(self):
        board = [[_, X, _],
                    [_, _, O],
                    [_, _, _]]
        self.assertEqual((0, 2), minimax(board))
        # self.assertEqual(1, score(board))

    def test_full_board(self):
        full_board = [[X, O, X],
                        [O, O, X],
                        [X, X, O]]
        self.assertIsNone(minimax(full_board))
        # self.assertEqual(0, score(full_board))


if __name__ == '__main__':
    unittest.main()