# tests.py
# marc, marc@gruita.ro
from random import randint
from unittest import TestCase

from src.board import Board
from src.game import Game
from src.ship import Ship, ShipType
from src.utils import Players, IllegalMove, ShotResult


class TestBattleship(TestCase):
    def setUp(self):
        pass

    def test_ai(self):
        """
        Test that the ai can beat a random shooting player in 5 random games
        The ai offset is set to the value which gives us the best results
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
        self.assertEqual(self.board.size, 2)

        self.assertEqual(self.board.board, [[0, 0], [0, 0]])
        self.assertEqual(str(self.board), "o o \no o ")
        with self.assertRaises(IllegalMove):
            self.board.place_ship(Ship(ShipType.SUBMARINE, 0, 0, 0))
        with self.assertRaises(IllegalMove):
            self.board.shoot(-1, -1)

        self.assertEqual(self.board.all_sunk(), True)
        self.board.place_ship(Ship(ShipType.PATROL_BOAT, 0, 0, 0))
        self.assertEqual(self.board.all_sunk(), False)

        self.assertEqual(self.board.shoot(0, 0), ShotResult.HIT)
        self.assertEqual(self.board.shoot(0, 0), ShotResult.ALREADY_HIT)
        self.assertEqual(self.board.shoot(0, 1), (ShotResult.SUNK, ShipType.PATROL_BOAT))
        self.assertEqual(self.board.shoot(1, 0), ShotResult.MISS)

    def test_game(self):
        game = Game(10)

        self.assertEqual(game.playing, False)
        game.start()
        self.assertEqual(game.playing, True)

        pos = 0
        for s in game.get_player_ships():
            self.assertEqual(type(s), Ship)
            game.place_ship(s.type, 0, pos, pos)  # will always fit
            pos += 1
        self.assertEqual(pos, len(game._Game__ships))

        del game
        game = Game(10)
        s = Ship(ShipType.PATROL_BOAT, 0, 0, 0)
        s1 = Ship(ShipType.PATROL_BOAT, 0, 0, 0)
        s2 = Ship(ShipType.PATROL_BOAT, 1, 9, 9)

        game._player_board.place_ship(s)  # so the ai doesn't automatically win
        game._ai_board.place_ship(s1)
        game._ai_board.place_ship(s2)

        self.assertEqual(game.shoot(0, 0), ShotResult.HIT)
        self.assertEqual(game.shoot(0, 0), ShotResult.ALREADY_HIT)
        self.assertEqual(game.shoot(0, 1), (ShotResult.SUNK, ShipType.PATROL_BOAT))

        game.shoot(9, 9)
        self.assertEqual(game.shoot(8, 9), (ShotResult.WON, Players.HUMAN))

        del game
        game = Game(10)
        game._ai_board.place_ship(Ship(ShipType.CARRIER, 0, 0, 0))
        for ship in game._ai_board.ships:
            ship._sunk = True

        game._Game__get_winner()
        self.assertEqual(game.winner, Players.HUMAN)

        game._Game__ai_shoot()
        game._Game__ai_shoot(1, 1)
        game._Game__ai_shoot(1, 1)
        game._Game__cool_ai_shoot()
        total_shots = 0

        for row in game.player_board.board:
            for elem in row:
                if elem == 2:
                    total_shots += 1
        self.assertEqual(total_shots, 4)
        del game

        game = Game(2)
        self.assertEqual(game.shots_board.board, [[0, 0], [0, 0]])
        self.assertEqual(game.player_board.board, [[0, 0], [0, 0]])

    def test_ship(self):
        self.assertEqual(Ship(ShipType.DESTROYER, 0, 1, 2), Ship(ShipType.DESTROYER, 1, 2, 4))

        ship = Ship(ShipType.CARRIER, 0, 1, 1)
        ship.add_piece(1, 1)
        ship.add_piece(1, 2)

        self.assertEqual(ship.check_hit(1, 1), ShotResult.HIT)
        self.assertEqual(ship.sunk, False)

        self.assertEqual(ship.check_hit(0, 1), ShotResult.MISS)
        self.assertEqual(ship.check_hit(1, 2), (ShotResult.SUNK, ShipType.CARRIER))

        self.assertEqual(ship.sunk, True)

