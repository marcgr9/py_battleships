# ship.py
# marc, marc@gruita.ro

from enum import Enum
from typing import List, Tuple

from coords import Coords


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

    def add_piece(self, x, y):
        self._pieces.append([True, x, y])


class ShipType(Enum):
    DESTROYER = 5
    BARCA = 3
    SUBMARIN = 2

    @property
    def size(self):
        return self.value
