# game.py
# marc, marc@gruita.ro

from random import randint
from src.board import Board
from src.ship import Ship, ShipType
from src.utils import ShotResult, Players


class Game:
    def __init__(self, player_board: Board, ai_board: Board):
        self._player_board = player_board
        self._ai_board = ai_board
        self._playing = False
        self._winner = None
        self._ai_moves = []
        self.__ships = [
            Ship(ShipType.CARRIER),
            Ship(ShipType.BATTLESHIP),
            Ship(ShipType.DESTROYER),
            Ship(ShipType.SUBMARINE),
            Ship(ShipType.PATROL_BOAT)
        ]

    @property
    def playing(self):
        return self._playing and self._winner is None

    def start(self):
        self._place_ai_ships()
        self._playing = True

    def _place_ai_ships(self):
        while len(self._ai_board.ships) != len(self.__ships):
            o = randint(0, 1)
            x = randint(0, 10)
            y = randint(0, 10)
            try:
                self._ai_board.place_ship(Ship(self.__ships[len(self._ai_board.ships) - len(self.__ships)].type, o, x, y))
            except Exception:
                pass

    def __ai_shoot(self):
        x = randint(0, 9)
        y = randint(0, 9)
        while (x, y) in self._ai_moves:
            x = randint(0, 9)
            y = randint(0, 9)

        self._ai_moves.append((x, y))
        self._player_board.shoot(x, y)

    def get_player_ships(self):
        while len(self._player_board.ships) != len(self.__ships):
            yield self.__ships[len(self._player_board.ships) - len(self.__ships)]

    def place_ship(self, ship_type: ShipType, orientation: int, x: int, y: int):
        self._player_board.place_ship(Ship(ship_type, orientation, x, y))

    def shoot(self, x, y):
        response = self._ai_board.shoot(x, y)
        self.__ai_shoot()

        return response if self.__check_game_won() is None else (ShotResult.WON, self.__check_game_won())

    def __check_game_won(self):
        if all(s.sunk for s in self._player_board.ships):
            self._winner = Players.AI
        elif all(s.sunk for s in self._ai_board.ships):
            self._winner = Players.HUMAN
        return self._winner
