# statistics_generator.py
# marc, marc@gruita.ro
from datetime import datetime
from random import randint

from src.ai import AI
from src.board import Board
from src.game import Game
from src.ship import ShipType, Ship
from src.utils import ShotResult, anything


def game_simulations():
    file_str = "game/statistics_new_ai.txt"
    iterations = 1000  # 4:30 min / offset
    f = open(file_str, "a+")
    f.write(f"{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}: Starting simulating {iterations} games for" +
            " each ai offset value.\n")
    for ai_offset in range(1, 51):
        f = open(file_str, "a+")
        score = 0
        print("starting for offset", ai_offset)
        for _ in range(iterations):
            if _ == iterations/4:
                print("1/4")
            elif _ == iterations/2:
                print("1/2")
            elif _ == (3*iterations) / 4:
                print("3/4")
            game = Game(10, ai_offset)
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
