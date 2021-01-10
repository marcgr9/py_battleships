# gui.py
# marc, marc@gruita.ro
import pygame

from src.game import Game


class GUI:

    tile_size = 50
    separation_width = 20

    colors = {
        'BACKGROUND': (71, 71, 71),
        'WATER': (96, 144, 219),
        'HIT': (200, 0, 0),
        'MISS': (110, 110, 110),
        'SUNK': (223, 227, 100),
        'SHIP': (227, 147, 18)
    }

    player_board_colors = {
        0: colors['WATER'],
        1: colors['SHIP'],
        2: colors['MISS'],
        3: colors['SUNK']
    }

    shots_board_colors = {
        0: colors['WATER'],
        1: colors['HIT'],
        2: colors['SUNK'],
        3: colors['MISS']
    }

    def __init__(self):
        self.__game = Game(10)
        self.__board_size = self.__game.player_board.size
        pygame.init()

        self.__screen_width = self.__board_size * self.tile_size + 1
        self.__screen_height = self.__board_size * self.tile_size + 1
        self.__screen = pygame.display.set_mode(
            (self.__screen_width, self.__screen_height))
        pygame.display.set_caption("Battleships")

    def play(self):
        while True:
            self.place_ships()
            self.__game.start()
            self.__screen = pygame.display.set_mode(
                (self.__screen_width * 2 + self.separation_width, self.__screen_height))

            while self.__game.playing:
                self.__draw_boards()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION:
                        mousex, mousey = event.pos
                        if mousex >= self.__screen_width + 20:
                            self.__draw_selected_area_border(mousex, mousey)

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if mousex >= self.__screen_width + 20:
                            self.__shoot(mousex, mousey)

                    if event.type == pygame.QUIT:
                        quit()

                    pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

    def place_ships(self):
        x, y, o = 0, 0, 1
        mousex, mousey = 0, 0
        for ship in self.__game.get_player_ships():
            self.draw_board()
            if o == 1:
                x, y = mousex // self.tile_size * self.tile_size, mousey // self.tile_size * self.tile_size
                pygame.draw.rect(self.__screen, color=(50, 70, 90),
                                 rect=[x, y - self.tile_size * (ship.size - 1), self.tile_size + 1, ship.size * self.tile_size + 1])
            else:
                x, y = mousex // self.tile_size * self.tile_size, mousey // self.tile_size * self.tile_size
                pygame.draw.rect(self.__screen, color=(50, 70, 90), rect=[x, y, ship.size * self.tile_size + 1, self.tile_size + 1])

            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == pygame.KEYDOWN:
                    o = event.key == pygame.K_UP

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.__game.place_ship(ship.type, o, y // self.tile_size, x // self.tile_size)

                if event.type == pygame.QUIT:
                    quit()

                pygame.display.update()

    def draw_board(self):
        self.__screen.fill((200, 100, 30))
        for i in range(self.__board_size):
            for j in range(self.__board_size):
                col = self.player_board_colors[self.__game.player_board.board[j][i]]
                pygame.draw.rect(self.__screen, rect=[self.tile_size * i + 1, self.tile_size * j + 1, self.tile_size - 1, self.tile_size - 1],
                                 color=col)

    def __draw_boards(self):
        self.draw_board()

        for i in range(self.__board_size):
            for j in range(self.__board_size):
                col = self.shots_board_colors[self.__game.shots_board.board[j][i]]
                pygame.draw.rect(self.__screen, rect=[(self.tile_size * i + 1) + self.tile_size * self.__board_size + 20, self.tile_size * j + 1,
                                               self.tile_size - 1, self.tile_size - 1],
                                 color=col)

    def __draw_selected_area_border(self, mousex, mousey):
        x, y = (mousex - 20) // self.tile_size * self.tile_size, mousey // self.tile_size * self.tile_size
        pygame.draw.rect(self.__screen, color=(200, 150, 100),
                         rect=[x + 20, y, self.tile_size + 1, self.tile_size + 1], width=4)

    def __shoot(self, mousex, mousey):
        x, y = mousey // self.tile_size * self.tile_size, (
                mousex - self.__screen_width - 20) // self.tile_size * self.tile_size
        self.__game.shoot(x // self.tile_size, y // self.tile_size)


ui = GUI()
ui.play()
