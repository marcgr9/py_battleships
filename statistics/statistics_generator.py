from datetime import datetime
from random import randint

from src.ai import AI
from src.board import Board
from src.game import Game
from src.ship import ShipType, Ship
from src.utils import ShotResult, anything, deprecated


@deprecated
def one_way_play():
    iterations = 100
    for ai_offset in range(1, 51):
        f = open("statistics.txt", "a+")
        score = 0
        print("starting for offset", ai_offset)
        for _ in range(iterations):
            my_ships = []
            ships = [
                Ship(ShipType.CARRIER),
                Ship(ShipType.BATTLESHIP),
                Ship(ShipType.DESTROYER),
                Ship(ShipType.SUBMARINE),
                Ship(ShipType.PATROL_BOAT)
            ]
            b = Board(10)
            while len(ships) != len(my_ships):
                o = randint(0, 1)
                x = randint(0, 9)
                y = randint(0, 9)
                try:
                    s = Ship(ships[len(my_ships) - len(ships)], o, x, y)
                    b.place_ship(s)
                    my_ships.append(s)
                except Exception:
                    pass

            ai = AI(10, ai_offset)
            moves = []
            n = 0
            shots = 0
            while n != len(ships):
                x, y = ai.calculate_shot(moves, my_ships)
                r = b.shoot(x, y)
                shots += 1
                moves.append([r, x, y])
                if type(r) == tuple and r[0] == ShotResult.SUNK:
                    n += 1
                    my_ships.remove(Ship(r[1], 0, 0))
            score += shots
        f.write("offset " + str(ai_offset) + " - " + str(score) + " total shots over " + str(iterations) + " games; avg "
                + str(score/iterations) + "\n")
        f.close()


def game_simulations():
    file_str = "statistics/game/statistics.txt"
    iterations = 10  # 4:30 min
    f = open(file_str, "a+")
    f.write(f"{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}: Starting simulating {iterations} games for" +
            " each ai offset value.\n")
    for ai_offset in range(1, 51):
        f = open(file_str, "a+")
        score = 0
        print("starting for offset", ai_offset)
        for _ in range(iterations):
            game = Game(10)
            for ship in game.get_player_ships():
                o = randint(0, 1)
                x = randint(0, 9)
                y = randint(0, 9)
                try:
                    game.place_ship(ship.type, o, x, y)
                except Exception:
                    pass

            game.start()
            while game.playing:
                game.shoot(0, 0)
            score += game.n
        f.write(
            "Offset " + str(ai_offset) + " - " + str(score) + " total shots over; avg " + str(score / iterations) + "\n")
        f.close()
    f = open(file_str, "a+")
    f.write(f"{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}: Simulations done\n\n")
    f.close()


game_simulations()
