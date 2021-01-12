# statistics_generator.py
# marc, marc@gruita.ro
from datetime import datetime
from random import randint

from src.game import Game


def game_simulations():
    """
    Calculates the avg shots needed for each ai offset to complete a game
    :return:
    """
    file_str = "new_ai/statistics_new_ai.txt"
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


def game_simulations_v2():
    """
    Calculates how many games end in x ai shots, x in [0, 100], out of @iteration games
    """
    file_str = "new_ai/new_statistics_new_ai.txt"
    iterations = 10000
    ai_offset = 33

    f = open(file_str, "a+")
    f.write(f"{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}: Starting simulating {iterations} games (ai offset 33)\n")

    frequency_list = [0 for _ in range(0, 101)]
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
        frequency_list[game.n] += 1

    total = 0
    for i in range(101):
        if frequency_list[i] > 0:
            f.write(
                str(i) + " moves: " + str(frequency_list[i]) + " games / " + str(iterations) + " (" +
                str(frequency_list[i] / iterations * 100) + "%)\n"
            )
            total += i * frequency_list[i]

    f.write(f"Average {str(total / iterations)}\n")

    f.close()
    f = open(file_str, "a+")
    f.write(f"{datetime.now().strftime('%m/%d/%Y %H:%M:%S')}: Simulations done\n\n")
    f.close()


# game_simulations()

game_simulations_v2()
