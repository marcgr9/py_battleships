from board import Board
from game import Game
from ship import ShipType
from utils import anything

player = Board(10)
ai = Board(10)
game = Game(player, ai)

#game.read_player_board()

#game.start()


# for ship in game.get_player_ships():
#     print("plaseaza", str(ship.type.name), str(ship.size))
#     o = int(input())
#     x = int(input())
#     y = int(input())
#     try:
#         game.place_ship(ship.type, o, x, y)
#         print(game._player_board)
#     except Exception:
#         print("loc ocupat")
# game.start()
#
# print(game._ai_board)
#
# while game._winner is None:
#     x = int(input())
#     y = int(input())
#
#     response = game.shoot(x, y)

game._place_ai_ships()
print(game._ai_board)

while True:
    x = int(input())
    y = int(input())

    print(game.shoot(x, y))
    print(game._ai_board)
