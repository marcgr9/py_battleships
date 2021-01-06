# utils.py
# marc, marc@gruita.ro
from enum import Enum, unique
import warnings


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
    ALREADY_HIT = 3


@unique
class Players(Enum):
    HUMAN = 0
    AI = 1


class IllegalMove(Exception):
    def __init__(self, msg=""):
        super().__init__(msg)


def deprecated(message):
    def deprecated_decorator(func):
        def deprecated_func(*args, **kwargs):
            warnings.warn("{} is a deprecated function. {}".format(func.__name__, message),
                          category=DeprecationWarning,
                          stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)

        return deprecated_func

    return deprecated_decorator
