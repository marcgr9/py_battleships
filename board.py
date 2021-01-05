# board.py
# marc, marc@gruita.ro

from ship import Ship
from array import *


class Board:
    def __init__(self, size):
        self._size = size
        self._board = [[0 for _ in range(size)] for _ in range(10)]
        self._ships = []

    def __str__(self):
        msg = ""
        for row in self._board:
            msg += str(row) + "\n"
        msg = msg[:-1]
        return msg

    @property
    def board(self):
        return self._board

    @property
    def ships(self):
        return self._ships

    def place_ship(self, ship):
        self.__check(ship)
        self._ships.append(ship)
        for i in range(ship.size):
            self._board[ship.coords.x - i*ship.orientation][ship.coords.y + i*(not ship.orientation)] = 1

    def __check(self, ship):
        for i in range(ship.size):
            if self._board[ship.coords.x - i * ship.orientation][ship.coords.y + i * (not ship.orientation)] == 1 or \
                (not 0 <= ship.coords.x - i * ship.orientation <= self._size) or \
                    (not 0 <= ship.coords.y + i * (not ship.orientation) <= self._size):
                raise Exception
        return True
