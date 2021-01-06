# tests.py
# marc, marc@gruita.ro
from random import randint
from unittest import TestCase

from src.board import Board
from src.game import Game
from src.ship import Ship, ShipType
from src.utils import Players, IllegalMove


class TestBattleship(TestCase):
    def setUp(self):
        pass

    def test_ai(self):
        """
        Test that the ai can beat a random shooting player in 5 random games
        The ai offset is set to the value which gives us the best results - 42
        Value obtained from 1000s of game simulations
        """
        total = 0
        for _ in range(5):
            self.game = Game(10)
            for ship in self.game.get_player_ships():
                o = randint(0, 1)
                x = randint(0, 9)
                y = randint(0, 9)
                try:
                    self.game.place_ship(ship.type, o, x, y)
                except Exception:
                    pass

            self.game.start()
            while self.game.playing:
                self.game.shoot(randint(0, 9), randint(0, 9))
            self.assertEqual(self.game._winner, Players.AI)

    def test_board(self):
        self.board = Board(2)

        self.assertEqual(self.board.board, [[0, 0], [0, 0]])
        self.assertEqual(str(self.board), "0 0 \n0 0 ")
        with self.assertRaises(IllegalMove):
            self.board.place_ship(Ship(ShipType.SUBMARINE, 0, 0, 0))
        with self.assertRaises(IllegalMove):
            self.board.shoot(-1, -1)

    def test_game(self):
        game = Game(10)
        for ship in game._ai_board.ships:
            ship._sunk = True

        game._Game__check_game_won()
        self.assertEqual(game._winner, Players.HUMAN)

        game._Game__ai_shoot()
        total_shots = 0
        for row in game.player_board.board:
            for elem in row:
                if elem == 2:
                    total_shots += 1
        self.assertEqual(total_shots, 1)
        del game

        game = Game(2)
        self.assertEqual(game.shots_board.board, [[0, 0], [0, 0]])
        self.assertEqual(game.player_board.board, [[0, 0], [0, 0]])

