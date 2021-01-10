# ship.py
# marc, marc@gruita.ro
from aenum import Enum, NoAlias
from typing import List

from src.utils.utils import Coords, anything, ShotResult, ShipType


class Ship:
    def __init__(self, ship_type: ShipType, orientation: int = -1, x: int = -1, y: int = -1):
        self._type = ship_type
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

    def add_piece(self, x: int, y: int):
        """
        Adds spot at (x, y) as part of the ship
        """
        self._pieces.append([True, x, y])

    def check_hit(self, x, y):
        """
        Check if spot at (x, y) is part of the ship
        :return:
            ShotResult.MISS: if the ship doesn't contain spot (x, y)
            ShotResult.HIT: if the ship does contain spot (x, y)

            (ShotResult.SUNK, type: ShipType): if the shot does contain spot (x, y) and all other pieces were hit
        """
        for p in self.pieces:
            if p == [anything, x, y]:
                p[0] = False  # marks spot (x, y) as hit
                sunk = all(p[0] is False for p in self.pieces)
                if sunk:
                    self._sunk = True
                    return ShotResult.SUNK, self.type
                return ShotResult.HIT
        return ShotResult.MISS
