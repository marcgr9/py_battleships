# ship.py
# marc, marc@gruita.ro

from enum import Enum
from coords import Coords


class Ship:
    def __init__(self, ship_type, orientation=-1, x=-1, y=-1):
        self._type: ShipType = ship_type
        self._orientation = orientation
        self._coords = Coords(x, y)
        self._sunk = False

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


class ShipType(Enum):
    DESTROYER = 5
    BARCA = 3
    SUBMARIN = 2

    @property
    def size(self):
        return self.value
