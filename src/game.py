# game.py
# marc, marc@gruita.ro

from random import randint

from src.ai import AI
from src.board import Board
from src.ship import Ship, ShipType
from src.utils import ShotResult, Players, anything


class Game:
    def __init__(self, player_board: Board, ai_board: Board, ai_offset=42):
        self._player_board = player_board
        self._ai_board = ai_board
        self._shots_board = Board(10)
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
        self.__ai_boats = [
            Ship(ShipType.CARRIER),
            Ship(ShipType.BATTLESHIP),
            Ship(ShipType.DESTROYER),
            Ship(ShipType.SUBMARINE),
            Ship(ShipType.PATROL_BOAT)
        ]
        self.__ai = AI(self._player_board.size, self.__ships, ai_offset)

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
        x, y = self.__ai.calculate_shot(self._ai_moves, self.__ai_boats)
        while (anything, x, y) in self._ai_moves:
            x, y = self.__ai.calculate_shot(self._ai_moves, self.__ai_boats)
        result = self._player_board.shoot(x, y)
        self.n += 1
        self._ai_moves.append((result, x, y))
        if type(result) == tuple and result[0] == ShotResult.SUNK:
            self.__ai_boats.remove(Ship(result[1], 0, 0))

    def get_player_ships(self):
        while len(self._player_board.ships) != len(self.__ships):
            yield self.__ships[len(self._player_board.ships) - len(self.__ships)]

    def place_ship(self, ship_type: ShipType, orientation: int, x: int, y: int):
        self._player_board.place_ship(Ship(ship_type, orientation, x, y))

    def shoot(self, x, y):
        if self._shots_board.board[x][y] != 0:
            self.__cool_ai_shoot()
            return ShotResult.ALREADY_HIT

        response = self._ai_board.shoot(x, y)
        self.__fill_shots_board(x, y, response)
        self.__cool_ai_shoot()

        return response if self.__check_game_won() is None else (ShotResult.WON, self.__check_game_won())

    def __check_game_won(self):
        if all(s.sunk for s in self._player_board.ships):
            self._winner = Players.AI
        elif all(s.sunk for s in self._ai_board.ships):
            self._winner = Players.HUMAN
        return self._winner

    def __fill_shots_board(self, x, y, response):
        if response == (ShotResult.SUNK, anything):
            self._shots_board.board[x][y] = 2
        elif response == ShotResult.HIT:
            self._shots_board.board[x][y] = 1
        else:
            self._shots_board.board[x][y] = 3
