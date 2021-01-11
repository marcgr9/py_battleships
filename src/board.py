# board.py
# marc, marc@gruita.ro
from src.ship import Ship
from src.utils.utils import ShotResult, IllegalMove


class Board:
    """
    Stores individual battleship boards
    """
    nums_to_chars = {
        3: '~',
        2: 'x',
        1: '+',
        0: 'o'
    }

    def __init__(self, size: int):
        """
        :param size: size of board
        """
        self._size = size
        self._board = [[0 for _ in range(size)] for _ in range(size)]
        self._ships = []

    def __str__(self):
        msg = ""
        for row in self._board:
            for n in row:
                msg += self.nums_to_chars[n] if n > -500 else '-'
                msg += "  "
            msg += "\n"
        msg = msg[:-1]
        return msg

    @property
    def board(self):
        return self._board

    @property
    def ships(self):
        return self._ships

    @property
    def size(self):
        return self._size

    def place_ship(self, ship: Ship):
        """
        Attempts to place a ship
        :param ship: ship to be placed
        :raises: IllegalMove if ship can't be placed
        """
        self.check(ship)
        for i in range(ship.size):
            x, y = ship.coords.x - i*ship.orientation, ship.coords.y + i*(not ship.orientation)
            self._board[x][y] = 1
            ship.add_piece(x, y)

        self._ships.append(ship)

    def check(self, ship: Ship):
        """
        Checks if a given ship can be placed
        :param ship: ship to be placed
        :raises: IllegalMove if ship is outside the board or it intersects other ships
        """
        for i in range(ship.size):
            if (not 0 <= ship.coords.x - i * ship.orientation < self._size) or \
                (not 0 <= ship.coords.y + i * (not ship.orientation) < self._size) or \
                    self._board[ship.coords.x - i * ship.orientation][ship.coords.y + i * (not ship.orientation)] != 0:
                raise IllegalMove

    def shoot(self, x: int, y: int):
        """
        Attempts to shoot at coordinates x, y
        :return: result of the shooting
            ShotResult.MISS: if the shot didn't hit a ship
            ShotResult.HIT: if the shot did hit a ship
            ShotResult.ALREADY_HIT: if the targeted spot was already shot at

            (ShotResult.SUNK, type: ShipType): if the shot sunk a ship; type - type of sunken boat
        :raises: IllegalMove if (x, y) is outside the board
        """
        if not ((0 <= x <= self._size) and
                (0 <= y <= self._size)):
            raise IllegalMove

        if self._board[x][y] not in [0, 1]:  # water or ship
            return ShotResult.ALREADY_HIT

        self.board[x][y] = 2

        for s in self.ships:
            hit = s.check_hit(x, y)
            try:
                if hit[0] == ShotResult.SUNK:
                    for piece in s.pieces:
                        self.board[piece[1]][piece[2]] = 3
            except Exception:
                pass
            if hit != ShotResult.MISS:
                return hit
        return ShotResult.MISS

    def all_sunk(self):
        """
        Checks if all the ships on the board were sunken
        :return: bool
        """
        return all(ship.sunk is True for ship in self._ships)
