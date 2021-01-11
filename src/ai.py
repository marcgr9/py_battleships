# ai.py
# marc, marc@gruita.ro
from random import randint
from time import sleep

from src.board import Board
from src.ship import Ship
from src.utils.utils import ShotResult, anything, IllegalMove


class AI:
    """
    AI module that covers everything related to the BattleShip AI
    """
    def __init__(self, board_size: int, offset: int):
        """
        :param board_size: size of the board
        :param offset: value used to compute shots
        """
        self.__size = board_size
        self.offset = offset
        self.__moves = []

    def calculate_shot(self, player_ships):
        """
        Computes the most likely spot that contains a ship
        :param player_ships: list of remaining ships
        :return: (int, int)

        pseudocode:
        for every shot until now:
            spot = (x, y) of shot
            result = hit/miss/sunk

            mark spot as inaccessible
            if result was a hit:
                if spot is not part of a sunken ship:
                    for every neighbour of spot:
                        if neighbour was a hit:
                            increase the probability for the opposite neighbour
                        increase the probability for the neighbour

        for every ship placement possible using unsunken ships:
            increase by 1 the probability for every spot of the ship

        return (x, y) of the spot with the highest probability
        """
        board = Board(self.__size)
        prob_board = Board(self.__size)

        for move in self.__moves:
            x, y = move[1], move[2]
            board.shoot(x, y)
            prob_board.board[x][y] = -1000

            if move[0] == ShotResult.HIT:
                if any(ship.sunk and [anything, x, y] in ship.pieces for ship in player_ships):
                    continue

                for (i, j) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    try:  # easier to ask for forgiveness that permission :d
                        if (ShotResult.HIT, x - i, y - j) in self.__moves:
                            prob_board.board[x + i][y + j] += self.offset
                        prob_board.board[x + i][y + j] += self.offset
                    except IndexError:
                        pass

        final_x, final_y = 0, 0
        max_prob = -1
        for s in player_ships:
            if not s.sunk:
                for i in range(self.__size):
                    for j in range(self.__size):
                        for o in range(0, 2):
                            try:
                                board.check(Ship(s.type, o, i, j))
                                for offset in range(s.size):
                                    x, y = i - offset * o, j + offset * (not o)
                                    prob_board.board[x][y] += 1
                            except IllegalMove:
                                pass

        for i in range(self.__size):
            for j in range(self.__size):
                if prob_board.board[i][j] > max_prob:
                    final_x, final_y = i, j
                    max_prob = prob_board.board[i][j]
                elif prob_board.board[i][j] == max_prob:
                    if randint(0, 10) < 5:
                        final_x, final_y = i, j
        return final_x, final_y

    def add_move(self, move: tuple):
        """
        Adds given move to the list of past moves
        :param move:
        """
        self.__moves.append(move)

"""
adauga offset pt vecini numa daca piesa curenta nu ii dintr-o barca scufundata
    - marcheaza barcile scufundate cu altceva, nu doar ult bucata (o sa ajuta la gui) - DONE

cand calculezi probabilitatiile, foloseste si locurile cu HIT (nu SUNK) ca si locuri unde poate aparea o barca
    - FARA sa transmiti player_board catre AI
"""