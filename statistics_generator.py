from random import randint
from src.board import Board
from src.game import Game
from src.ship import ShipType, Ship

iterations = 100
for ai_offset in range(1, 51):
    f = open("statistics.txt", "a+")
    score = 0
    print("-----", ai_offset)
    for _ in range(iterations):
        player = Board(10)
        ai = Board(10)
        game = Game(player, ai, ai_offset)

        my_ships = []
        ships = [
            Ship(ShipType.CARRIER),
            Ship(ShipType.BATTLESHIP),
            Ship(ShipType.DESTROYER),
            Ship(ShipType.SUBMARINE),
            Ship(ShipType.PATROL_BOAT)
        ]
        while len(ships) != len(my_ships):
            o = randint(0, 1)
            x = randint(0, 9)
            y = randint(0, 9)
            try:
                game.place_ship(Ship(ships[len(my_ships) - len(ships)]).type, o, x, y)
                my_ships.append('a')
            except Exception:
                pass

        game.start()
        while game.playing:
            x, y = 0, 0
            try:
                game.shoot(int(x), int(y))
            except Exception as e:
                pass
        score += game.n
    f.write("offset " + str(ai_offset) + " - " + str(score) + " total shots over " + str(iterations) + " games; avg "
            + str(score/iterations) + "\n")
    f.close()
