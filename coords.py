class Coords:
    def __init__(self, x=-1, y=-1, pair=(-1, -1)):
        if pair is not (-1, -1):
            self.__x = pair[0]
            self.__y = pair[1]
            return

        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
