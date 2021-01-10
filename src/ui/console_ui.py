# console_ui.py
# marc, marc@gruita.ro
from src.game import Game
from src.ship import ShipType
from src.ui.ui_abc import UI
from src.utils.utils import ShotResult, IllegalMove


class ConsoleUI(UI):
    def __init__(self):
        self.__game = Game(10)

        self.__messages = {
            ShotResult.MISS: "Miss",
            ShotResult.HIT: "Hit",
            ShotResult.SUNK: "Sunk {var}",
            ShotResult.WON: "{var} won!",
            ShotResult.ALREADY_HIT: "Area already hit"
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
                response = self.__game.shoot(int(y), int(x))
                self.print_board()
                if type(response) == tuple:
                    if type(response[1]) == ShipType:
                        print(self.__messages[response[0]].format(
                            var=self.ship_names[response[1]])
                        )
                    else:
                        print(self.__messages[response[0]].format(
                            var=self.players[response[1]])
                        )
                else:
                    print(self.__messages[response])
            except (IllegalMove, ValueError):
                self.print_board()
                print("Invalid move")

    def place_ships(self):
        for ship in self.__game.get_player_ships():
            self.print_board()
            print(f"Place the {ship.type.name} having length {str(ship.size)}")

            o, x, y = None, None, None
            while o not in [0, 1]:
                o = int(input("Orientation (1 - vertical, 0 - horizontal) = "))

            while type(x) != int:
                try:
                    x = int(input("x = "))
                except ValueError:
                    pass

            while type(y) != int:
                try:
                    y = int(input("y = "))
                except ValueError:
                    pass

            try:
                self.__game.place_ship(ship.type, o, y, x)
            except IllegalMove:
                print("Can't place this ship here. It's either too big or outside the playable area\n")

    def print_board(self):
        print("Your board:" + " " * 19 + "Your shots board:")
        for i in range(self.__game.player_board.size):
            print(str(self.__game.player_board).splitlines()[i] + " " * 10 + str(self.__game.shots_board).splitlines()[i])

        print("\n")
