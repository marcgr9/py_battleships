from board import Board
from game import Game
from ship import ShipType

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
game.start()

print(game._ai_board)
