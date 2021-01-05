from src.board import Board
from src.game import Game
from src.ship import ShipType

player = Board(10)
ai = Board(10)
game = Game(player, ai)

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

game.place_ship(ShipType.BARCA, 1, 2, 2)
game.place_ship(ShipType.SUBMARIN, 1, 5, 5)
game.place_ship(ShipType.DESTROYER, 0, 9, 0)

print("starting game")
game.start()
print(game._ai_board)
# n = 0

while game.playing:
    x, y = input().split(" ")
    try:
        response = game.shoot(int(x), int(y))
        if type(response) == ShipType:
            print("Sunk " + response.name)
            print(game._player_board)
        elif type(response) in (int, bool):
            if response == 0:
                print("Hit")
                pass
            else:
                # n += 1
                print("Miss")  # , n)

        else:
            print(response, "won")

    except Exception:
        print("Invalid move")