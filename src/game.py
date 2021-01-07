# game.py
# marc, marc@gruita.ro

from random import randint

from src.ai import AI
from src.board import Board
from src.ship import Ship, ShipType
from src.utils import ShotResult, Players, anything


class Game:
    def __init__(self, size, ai_offset=33):
        self._player_board = Board(size)
        self._ai_board = Board(size)
        self._shots_board = Board(size)
        self._playing = False
        self._winner = None
        self._ai_moves = []
        self.n = 0
        self.__ships = [
            Ship(ShipType.CARRIER),
            Ship(ShipType.BATTLESHIP),
            Ship(ShipType.DESTROYER),
            Ship(ShipType.SUBMARINE),
            Ship(ShipType.PATROL_BOAT)
        ]
        self.__ai = AI(self._player_board.size, ai_offset)

    @property
    def playing(self):
        return self._playing and self._winner is None

    @property
    def player_board(self):
        return self._player_board

    @property
    def shots_board(self):
        return self._shots_board

    def start(self):
        self._place_ai_ships()
        self._playing = True

    def _place_ai_ships(self):
        while len(self._ai_board.ships) != len(self.__ships):
            o = randint(0, 1)
            x = randint(0, 10)
            y = randint(0, 10)
            try:
                self._ai_board.place_ship(Ship(self.__ships[len(self._ai_board.ships) - len(self.__ships)].type, o, x, y))
            except Exception:
                pass

    def __ai_shoot(self):
        x = randint(0, 9)
        y = randint(0, 9)
        while (anything, x, y) in self._ai_moves:
            x = randint(0, 9)
            y = randint(0, 9)

        result = self._player_board.shoot(x, y)
        self._ai_moves.append((result, x, y))

    def __cool_ai_shoot(self):
        x, y = self.__ai.calculate_shot(self._ai_moves, self._player_board.ships)
        result = self._player_board.shoot(x, y)
        self.n += 1
        self._ai_moves.append((result, x, y))

    def get_player_ships(self):
        while len(self._player_board.ships) != len(self.__ships):
            yield self.__ships[len(self._player_board.ships) - len(self.__ships)]

    def place_ship(self, ship_type: ShipType, orientation: int, x: int, y: int):
        self._player_board.place_ship(Ship(ship_type, orientation, x, y))

    def shoot(self, x, y):
        response = self._ai_board.shoot(x, y)
        self.__fill_shots_board(x, y, response)
        self.__cool_ai_shoot()
        game_won = self.__check_game_won()

        if game_won is not None:
            self._playing = False
            return ShotResult.WON, game_won

        return response

    def __check_game_won(self):
        if self._player_board.all_sunk():
            self._winner = Players.AI
        if self._ai_board.all_sunk():
            self._winner = Players.HUMAN

        return self._winner

    def __fill_shots_board(self, x, y, response):
        if response == (ShotResult.SUNK, anything):
            self._shots_board.board[x][y] = 2
        elif response == ShotResult.HIT:
            self._shots_board.board[x][y] = 1
        else:
            self._shots_board.board[x][y] = 3
