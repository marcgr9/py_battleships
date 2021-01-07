# ai.py
# marc, marc@gruita.ro
from time import sleep

from src.board import Board
from src.ship import Ship
from src.utils import ShotResult, anything, IllegalMove


class AI:
    def __init__(self, board_size, offset):
        self.__size = board_size
        self.offset = offset

    def calculate_shot(self, moves, player_ships):
        board = Board(self.__size)
        prob_board = Board(self.__size)

        for move in moves:
            x, y = move[1], move[2]
            board.shoot(x, y)
            prob_board.board[x][y] = -1000

            if move[0] == ShotResult.HIT:
                if any(ship.sunk and [anything, x, y] in ship.pieces for ship in player_ships):
                    continue

                for (i, j) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    try:
                        if (ShotResult.HIT, x - i, y - j) in moves:
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
        return final_x, final_y


"""
adauga offset pt vecini numa daca piesa curenta nu ii dintr-o barca scufundata
    - marcheaza barcile scufundate cu altceva, nu doar ult bucata (o sa ajuta la gui) - DONE

cand calculezi probabilitatiile, foloseste si locurile cu HIT (nu SUNK) ca si locuri unde poate aparea o barca
    - FARA sa transmiti player_board catre AI
"""