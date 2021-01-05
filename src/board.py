# board.py
# marc, marc@gruita.ro

from src.utils import anything, ShotResult


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
        for i in range(ship.size):
            x, y = ship.coords.x - i*ship.orientation, ship.coords.y + i*(not ship.orientation)
            self._board[x][y] = 1
            ship.add_piece(x, y)

        self._ships.append(ship)

    def __check(self, ship):
        for i in range(ship.size):
            if self._board[ship.coords.x - i * ship.orientation][ship.coords.y + i * (not ship.orientation)] == 1 or \
                (not 0 <= ship.coords.x - i * ship.orientation <= self._size) or \
                    (not 0 <= ship.coords.y + i * (not ship.orientation) <= self._size):
                raise Exception

    def shoot(self, x, y):
        if not ((0 <= x <= self._size) and
                (0 <= y <= self._size)):
            raise Exception

        self.board[x][y] = 2
        # for s in self.ships:
        #     for p in s.pieces:
        #         if p == [anything, x, y]:
        #             p[0] = False
        #             response = all(p[0] is False for p in s.pieces)
        #             return response if not response else s.type
        # return -1  #miss

        for s in self.ships:
            hit = s.check_hit(x, y)
            if hit != ShotResult.MISS:
                return hit
        return ShotResult.MISS





