# utils.py
# marc, marc@gruita.ro
from enum import Enum, unique


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


@unique
class ShotResult(Enum):
    MISS = -1
    HIT = 0
    SUNK = 1
    WON = 2


@unique
class Players(Enum):
    HUMAN = 0
    AI = 1
