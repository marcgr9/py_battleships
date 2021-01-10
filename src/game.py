# game.py
# marc, marc@gruita.ro
from random import randint

from src.ai import AI
from src.board import Board
from src.ship import Ship
from src.utils.utils import ShotResult, Players, anything, ShipType


class Game:
    """
    Stores all the data needed to play a game
    """
    def __init__(self, size: int, ai_offset: int = 33):
        """
        :param size: size of board
        :param ai_offset: value used by ai to compute the most optimal shot
                        : default value is the best offset found by simulating 1000s of games
        """
        self._player_board = Board(size)
        self._ai_board = Board(size)
        self._shots_board = Board(size)

        self._playing = False
        self._winner = None

        self.__ships = [
            Ship(ShipType.CARRIER),
            Ship(ShipType.BATTLESHIP),
            Ship(ShipType.DESTROYER),
            Ship(ShipType.SUBMARINE),
            Ship(ShipType.PATROL_BOAT)
        ]

        self._ai_moves = []  # needed only if we use the dumb ai
        self.__ai = AI(self._player_board.size, ai_offset)
        self.n = 0  # for debugging: counting total ai shots

    @property
    def winner(self):
        return self._winner

    @property
    def playing(self):
        """
        True if game is ended, else False
        """
        return self._playing and self._winner is None

    @property
    def player_board(self):
        return self._player_board

    @property
    def shots_board(self):
        return self._shots_board

    def start(self):
        """
        To be called after user places his boats
        Places ai's ships and starts the game
        """
        self._place_ai_ships()
        self._playing = True

    def _place_ai_ships(self):
        """
        Computes a random valid position for each type of ship and places it on ai's board
        :return:
        """
        while len(self._ai_board.ships) != len(self.__ships):
            o = randint(0, 1)
            x = randint(0, 10)
            y = randint(0, 10)
            try:
                self._ai_board.place_ship(Ship(self.__ships[len(self._ai_board.ships) - len(self.__ships)].type, o, x, y))
            except Exception:
                pass

    def __ai_shoot(self, x=-1, y=-1):
        """
        Dumb ai shots; picking a random spot that wasn't fired at yet
        """
        if (x, y) == (-1, -1):
            x = randint(0, 9)
            y = randint(0, 9)
        while (anything, x, y) in self._ai_moves:
            x = randint(0, 9)
            y = randint(0, 9)

        result = self._player_board.shoot(x, y)
        self._ai_moves.append((result, x, y))

    def __cool_ai_shoot(self):
        """
        Uses the ai module to get the most optimal coordinates to fire a shot at
        Adds the chosen shot to ai's list of moves
        Increments the number of shots fired by the ai - for debugging
        """
        x, y = self.__ai.calculate_shot(self._player_board.ships)
        result = self._player_board.shoot(x, y)
        self.n += 1
        self.__ai.add_move((result, x, y))

    def get_player_ships(self):
        """
        Iterable - current value is the ship that needs to be placed by the user
        :yields: Ship
        """
        while len(self._player_board.ships) != len(self.__ships):
            yield self.__ships[len(self._player_board.ships) - len(self.__ships)]

    def place_ship(self, ship_type: ShipType, orientation: int, x: int, y: int):
        """
        Attempt to place given ship on the board
        :param ship_type: ship's type
        :param orientation: ship's orientation; 1 - vertical, 0 - horizontal
        :param x: x coordinate to place the ship
        :param y: y coordinate to place the ship
        :raises: IllegalMove; if the ship can't be placed at that position
        """
        self._player_board.place_ship(Ship(ship_type, orientation, x, y))

    def shoot(self, x: int, y: int):
        """
        Attempt to shoot at given coords
        :param x: x coordinate of spot
        :param y: y coordinate of spot
        :return: result of the shoot
            ShotResult.MISS: if the shot didn't hit a ship
            ShotResult.HIT: if the shot did hit a ship
            ShotResult.ALREADY_HIT: if the targeted spot was already shot at

            (ShotResult.WON, winner: Player): if the shot won the game; winner - winner of the game
            (ShotResult.SUNK, type: ShipType): if the shot sunk a ship; type - type of sunken boat
        """
        response = self._ai_board.shoot(x, y)
        self.__fill_shots_board(x, y, response)
        self.__cool_ai_shoot()
        winner = self.__get_winner()

        if winner:
            self._playing = False
            return ShotResult.WON, winner

        return response

    def __get_winner(self):
        """
        Checks each player's board in order to determine if someone won the game
        **The order of checks should be the same as the shooting order
        :return:
            None, if the game hasn't ended
            winner: Player, if the game has ended; winner - winner of the game
        """
        if self._player_board.all_sunk():
            self._winner = Players.AI
        if self._ai_board.all_sunk():
            self._winner = Players.HUMAN

        return self._winner

    def __fill_shots_board(self, x: int, y: int, response: tuple):
        """
        Populates player's shots board
        :param x: x coordinate of shooting
        :param y: y coordinate of shooting
        :param response: response of shooting at (x, y)
        :return:
        """
        if response == (ShotResult.SUNK, anything):
            self._shots_board.board[x][y] = 2
        elif response == ShotResult.HIT:
            self._shots_board.board[x][y] = 1
        elif response != ShotResult.ALREADY_HIT:
            self._shots_board.board[x][y] = 3
