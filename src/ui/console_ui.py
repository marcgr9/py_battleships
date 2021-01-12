# console_ui.py
# marc, marc@gruita.ro
from src.game import Game
from src.ship import ShipType
from src.ui.ui_abc import UI
from src.utils.utils import ShotResult, IllegalMove


class ConsoleUI(UI):
    def __init__(self):
        self.__game = Game(10)

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

                if type(response) == ShotResult:
                    print(self.shot_responses[response])
                elif type(response) == tuple:
                    if response[0] == ShotResult.SUNK:
                        print("Sunk " + self.ship_names[response[1]])
                    elif response[0] == ShotResult.WON:
                        print(self.players[response[1]] + " won!")
            except (IllegalMove, ValueError, IndexError):
                self.print_board()
                print("Invalid move")

    def place_ships(self):
        for ship in self.__game.get_player_ships():
            self.print_board()
            print(f"Place the {self.ship_names[ship.type]} having length {str(ship.size)}")

            o, x, y = None, None, None
            while o not in [0, 1]:
                try:
                    o = int(input("Orientation (1 - vertical, up; 0 - horizontal, right) = "))
                except ValueError:
                    pass

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
        print("Your board:" + " " * 29 + "Your shots board:")
        for i in range(self.__game.player_board.size):
            print(str(self.__game.player_board).splitlines()[i] + " " * 10 + str(self.__game.shots_board).splitlines()[i])

        print("\n")
