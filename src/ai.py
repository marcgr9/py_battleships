# ai.py
# marc, marc@gruita.ro
from copy import deepcopy
from time import sleep

from src.board import Board
from src.ship import Ship
from src.utils import ShotResult, anything


class AI:
    def __init__(self, board_size, ships):
        self.__size = board_size
        self.__ships = ships

    def calculate_shot(self, moves):
        board = Board(self.__size)
        prob_board = Board(self.__size)
        for move in moves:
            x, y = move[1], move[2]
            board.shoot(x, y)
            prob_board.board[x][y] = -1000
            try:
                if move[0] == ShotResult.HIT:
                    prob_board.board[x+1][y] += 50
                    prob_board.board[x][y+1] += 50
                    prob_board.board[x][y-1] += 50
                    prob_board.board[x-1][y] += 50
            except IndexError:
                pass

        final_x, final_y = 0, 0
        max_prob = -1
        for i in range(self.__size):
            for j in range(self.__size):
                for o in range(0, 2):
                    for s in self.__ships:
                        if [anything, i, j] not in moves:
                            try:
                                board._check(Ship(s.type, o, i, j))

                                for offset in range(s.size):
                                    x, y = i - offset * o, j + offset * (not o)
                                    prob_board.board[x][y] += 1
                                    if prob_board.board[x][y] > max_prob:
                                        final_x, final_y = x, y
                                        max_prob = prob_board.board[x][y]
                            except Exception:
                                pass
        print(prob_board)
        print(final_x, final_y, max_prob)
        return final_x, final_y
