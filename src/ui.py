# ui.py
# marc, marc@gruita.ro
from src.board import Board
from src.game import Game
from src.ship import ShipType
from src.utils import ShotResult, Players, anything


class UI:
    def __init__(self):
        self.__game = Game(10)

        self.__messages = {
            ShotResult.MISS: "Miss",
            ShotResult.HIT: "Hit",
            ShotResult.SUNK: "Sunk {var}",
            ShotResult.WON: "{var} won!",
            ShotResult.ALREADY_HIT: "Area already hit"
        }

        self.__players = {
            Players.AI: "AI",
            Players.HUMAN: "You"
        }

    def play(self):
        self.place_ships()
        print("\n" * 50)
        print("Battlefields ready!")
        self.__game.start()

        while self.__game.playing:
            print("Pick your shot! ('x y'):")
            try:
                x, y = input().split(" ")
                response = self.__game.shoot(int(x), int(y))
                self.print_board()
                if type(response) == tuple:
                    if type(response[1]) == ShipType:
                        print(self.__messages[response[0]].format(var=response[1].name))
                    else:
                        print(self.__messages[response[0]].format(var=self.__players[response[1]]))
                else:
                    print(self.__messages[response])
            except Exception:
                print("Invalid move")
                self.print_board()

    def place_ships(self):
        for ship in self.__game.get_player_ships():
            self.print_board()
            print(f"Place the {ship.type.name} having length {str(ship.size)}")
            o = int(input("Orientation = "))
            x = int(input("x = "))
            y = int(input("y = "))
            try:
                self.__game.place_ship(ship.type, o, x, y)
            except Exception:
                print("Can't place a ship here")

    def print_board(self):
        print("Your board:" + " " * 19 + "Your shots board:")
        for i in range(self.__game.player_board.size):
            print(str(self.__game.player_board).splitlines()[i] + " " * 10 + str(self.__game.shots_board).splitlines()[i])

        print("\n")


ui = UI()
ui.play()
