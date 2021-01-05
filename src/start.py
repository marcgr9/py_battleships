from src.board import Board
from src.game import Game
from src.ship import ShipType
from src.utils import ShotResult, Players

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

game.place_ship(ShipType.CARRIER, 1, 4, 9)
game.place_ship(ShipType.BATTLESHIP, 0, 5, 3)
game.place_ship(ShipType.DESTROYER, 0, 3, 6)
game.place_ship(ShipType.SUBMARINE, 0, 4, 1)
game.place_ship(ShipType.PATROL_BOAT, 0, 9, 5)

print("starting game")
game.start()
print(game._player_board)
msgs = {
    ShotResult.MISS: "Miss",
    ShotResult.HIT: "Hit",
    ShotResult.SUNK: "Sunk {var}",
    ShotResult.WON: "{var} won!"
}

players = {
    Players.AI: "AI",
    Players.HUMAN: "You"
}
# n = 0

while game.playing:
    # x, y = input().split(" ")
    x, y = 0, 0
    try:
        response = game.shoot(int(x), int(y))
        if type(response) == tuple:
            if type(response[1]) == ShipType:
                print(msgs[response[0]].format(var=response[1].name))
            else:
                print(msgs[response[0]].format(var=players[response[1]]))
        else:
            print(msgs[response])

    except Exception as e:
        print("Invalid move" + str(e))

print(game._ai_moves)