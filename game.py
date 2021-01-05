# game.py
# marc, marc@gruita.ro

from random import randint
from board import Board
from ship import Ship, ShipType


class Game:
    def __init__(self, player_board: Board, ai_board: Board):
        self._player_board = player_board
        self._ai_board = ai_board
        self._playing = False
        self._winner = None
        self._moving_player = 0  # todo
        self._moves = []
        self.__ships = [
            Ship(ShipType.BARCA),
            Ship(ShipType.SUBMARIN),
            Ship(ShipType.DESTROYER)
        ]

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

    def get_player_ships(self):
        while len(self._player_board.ships) != len(self.__ships):
            yield self.__ships[len(self._player_board.ships) - len(self.__ships)]

    def place_ship(self, ship_type: ShipType, orientation: int, x: int, y: int):
        self._player_board.place_ship(Ship(ship_type, orientation, x, y))
