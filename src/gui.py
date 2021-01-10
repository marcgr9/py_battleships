# gui.py
# marc, marc@gruita.ro
import pygame

from src.game import Game
from src.utils import ShotResult, Players, IllegalMove


class GUI:
    """
    spaghetti code
    It's a mess right now but I'll fix it
    """

    tile_size = 50
    separation_width = 20
    bottom_margin = 50

    colors = {
        'BACKGROUND': (200, 100, 30),
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
            (self.__screen_width,
             self.__screen_height + self.bottom_margin))

        self._text_area = None
        pygame.display.set_caption("Battleships")

    def play(self):
        ended = False
        while True:
            if not ended:
                self.place_ships()
                self.__game.start()
                # print(self.__game._ai_board)
                self.__screen = pygame.display.set_mode(
                    (self.__screen_width * 2 + self.separation_width,
                     self.__screen_height + self.bottom_margin))

                self.__display_text(None)

                while self.__game.playing:
                    self.__draw_boards()
                    if self._text_area:
                        self.__screen.blit(self._text_area[0], self._text_area[1])

                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEMOTION:
                            mousex, mousey = event.pos

                            if self.__check_mouse(mousex, mousey, shooting=True):
                                self.__draw_selected_area_border(mousex, mousey)

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if self.__check_mouse(mousex, mousey, shooting=True):
                                self.__shoot(mousex, mousey)

                        if event.type == pygame.QUIT:
                            quit()

                        pygame.display.update()

                self.__draw_boards()
                self.__display_text(self.__game._winner)
                self.__screen.blit(self._text_area[0], self._text_area[1])
                pygame.display.update()
                ended = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if ended:
                        self.__init__()
                        self.play()

    def place_ships(self):
        x, y, o = 0, 0, 1
        mousex, mousey = 0, 0
        for ship in self.__game.get_player_ships():
            self.draw_board()
            self.__display_text("Place " + ship.type.name, full=False)

            if self._text_area:
                self.__screen.blit(self._text_area[0], self._text_area[1])
            if self.__check_mouse(mousex, mousey):
                x, y = mousex // self.tile_size * self.tile_size, mousey // self.tile_size * self.tile_size

                if o == 1:  # vertical ship
                    pygame.draw.rect(self.__screen,
                                     color=(50, 70, 90),
                                     rect=[x, y - self.tile_size * (ship.size - 1),
                                           self.tile_size + 1, ship.size * self.tile_size + 1],
                                     width=3)
                else:  # horizontal ship
                    pygame.draw.rect(self.__screen,
                                     color=(50, 70, 90),
                                     rect=[x, y, ship.size * self.tile_size + 1, self.tile_size + 1],
                                     width=3)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == pygame.KEYDOWN:
                    o = event.key == pygame.K_UP

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    try:
                        self.__game.place_ship(ship.type, o, y // self.tile_size, x // self.tile_size)
                    except IllegalMove:
                        self.__display_text("Can't place a ship here", full=False)

                if event.type == pygame.QUIT:
                    quit()

                pygame.display.update()

    def draw_board(self):
        self.__screen.fill(self.colors['BACKGROUND'])
        for i in range(self.__board_size):
            for j in range(self.__board_size):
                col = self.player_board_colors[self.__game.player_board.board[j][i]]
                pygame.draw.rect(self.__screen,
                                 rect=[self.tile_size * i + 1, self.tile_size * j + 1,
                                       self.tile_size - 1, self.tile_size - 1],
                                 color=col)

    def __draw_boards(self):
        self.draw_board()

        for i in range(self.__board_size):
            for j in range(self.__board_size):
                col = self.shots_board_colors[self.__game.shots_board.board[j][i]]
                pygame.draw.rect(self.__screen,
                                 rect=[(self.tile_size * i + 1) + self.tile_size * self.__board_size + 20,
                                       self.tile_size * j + 1,
                                       self.tile_size - 1, self.tile_size - 1],
                                 color=col)

    def __draw_selected_area_border(self, mousex, mousey):
        x, y = (mousex - 20) // self.tile_size * self.tile_size, \
               mousey // self.tile_size * self.tile_size

        pygame.draw.rect(self.__screen,
                         color=(200, 150, 100),
                         rect=[x + 20, y, self.tile_size + 1, self.tile_size + 1],
                         width=4)

    def __shoot(self, mousex, mousey):
        x, y = mousey // self.tile_size * self.tile_size, \
               (mousex - self.__screen_width - 20) // self.tile_size * self.tile_size

        response = self.__game.shoot(x // self.tile_size, y // self.tile_size)

        if response != ShotResult.ALREADY_HIT:
            for part_filled in range(0, self.tile_size, 6):
                if part_filled > 0:
                    pygame.draw.rect(self.__screen,
                                     color=self.shots_board_colors[self.__game.shots_board.board[x//self.tile_size][y//self.tile_size]],
                                     rect=(y + self.__screen_width + 20, x, part_filled, part_filled))
                    pygame.display.update()
                    pygame.time.Clock().tick(30)

        self.__display_text(response)

    def __display_text(self, response, full=True):
        text = ""
        if type(response) == tuple and response[0] == ShotResult.SUNK:
            text = "Sunk " + response[1].name
        elif type(response) == ShotResult:
            text = response.name
        elif type(response) == Players:
            text = response.name + " won! Press any key to start a new game"
        elif type(response) == str:
            text = response
        elif response is None:
            self._text_area = None
            return

        text_object = pygame.font.Font('freesansbold.ttf', 20).render(text, True, (255, 200, 130))
        text_rect = text_object.get_rect()
        width = self.__screen_width // 2 if not full else self.__screen_width + self.separation_width // 2
        text_rect.center = (width, self.__screen_height + self.bottom_margin // 2)

        self._text_area = text_object, text_rect

    def __check_mouse(self, mousex, mousey, shooting=False):
        return (True if not shooting else mousex >= self.__screen_width + 20) and mousey <= self.__screen_height
