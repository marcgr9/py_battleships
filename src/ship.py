# ship.py
# marc, marc@gruita.ro

from enum import Enum
from typing import List

from src.utils import Coords, anything


class Ship:
    def __init__(self, ship_type, orientation=-1, x=-1, y=-1):
        self._type: ShipType = ship_type
        self._orientation = orientation
        self._coords = Coords(x, y)
        self._sunk = False
        self._pieces: List[List[bool, int, int]] = []

    def __eq__(self, other):
        return type(other) == Ship and other.type == self.type

    @property
    def type(self):
        return self._type

    @property
    def size(self):
        return self._type.size

    @property
    def orientation(self):
        return self._orientation

    @property
    def coords(self):
        return self._coords

    @property
    def pieces(self):
        return self._pieces

    @property
    def sunk(self):
        return self._sunk

    def add_piece(self, x, y):
        self._pieces.append([True, x, y])

    def check_hit(self, x, y):
        for p in self.pieces:
            if p == [anything, x, y]:
                p[0] = False
                sunk = all(p[0] is False for p in self.pieces)
                if sunk:
                    self._sunk = True
                return sunk if not sunk else self.type
        return -1


class ShipType(Enum):
    DESTROYER = 5
    BARCA = 3
    SUBMARIN = 2

    @property
    def size(self):
        return self.value
