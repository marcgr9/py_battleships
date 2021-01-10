# utils.py
# marc, marc@gruita.ro
from abc import abstractmethod, ABC
from enum import unique
import warnings

from aenum import Enum, NoAlias


class Anything:
    def __eq__(self, other):
        return True


anything = Anything()


class Coords:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


class ShipType(Enum):
    _settings_ = NoAlias

    CARRIER = 5
    BATTLESHIP = 4
    DESTROYER = 3
    SUBMARINE = 3
    PATROL_BOAT = 2

    @property
    def size(self):
        return self.value


@unique
class ShotResult(Enum):
    MISS = -1
    HIT = 0
    SUNK = 1
    WON = 2
    ALREADY_HIT = 3


@unique
class Players(Enum):
    HUMAN = 0
    AI = 1


class IllegalMove(Exception):
    def __init__(self, msg=""):
        super().__init__(msg)
