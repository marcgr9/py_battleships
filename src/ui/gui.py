# gui.py
# marc, marc@gruita.ro
from random import uniform
import pygame

from src.game import Game
from src.ui.ui_abc import UI
from src.utils.utils import ShotResult, Player, IllegalMove


class GUI(UI):
    """
    A lot of messy indexes & values but hey, it's a ui based on coordinates
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
        pygame.display.set_caption("Battleships")
        logo = pygame.image.load("res/imgs/logo.png")
        pygame.display.set_icon(logo)

        self.__screen_width = self.__board_size * self.tile_size + 1
        self.__screen_height = self.__board_size * self.tile_size + 1
        self.__screen = pygame.display.set_mode(
            (self.__screen_width,
             self.__screen_height + self.bottom_margin))

        self._text_area = None

        self.__explosion = [
            pygame.image.load("res/imgs/output-onlinepngtools-3.png"),
            pygame.image.load("res/imgs/output-onlinepngtools-4.png"),
            pygame.image.load("res/imgs/output-onlinepngtools-5.png"),
            pygame.image.load("res/imgs/output-onlinepngtools-6.png"),
            pygame.image.load("res/imgs/output-onlinepngtools-7.png"),
            pygame.image.load("res/imgs/output-onlinepngtools-8.png"),
            pygame.image.load("res/imgs/output-onlinepngtools-9.png"),
            pygame.image.load("res/imgs/output-onlinepngtools-10.png")]

    def play(self):
        started = False
        while True:
            while not started:
                self.__show_help_screen(start=True)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        started = True

            if not self.__game.winner:
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
                self.__display_text(self.__game.winner)
                self.__screen.blit(self._text_area[0], self._text_area[1])
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if self.__game.winner:
                        self.__init__()
                        self.play()

    def place_ships(self):
        x, y, o = 0, 0, 1
        mousex, mousey = 0, 0
        for ship in self.__game.get_player_ships():
            self.draw_board()
            self.__display_text("Place " + self.ship_names[ship.type], full=False)

            if self._text_area:
                self.__screen.blit(self._text_area[0], self._text_area[1])
            if self.__check_mouse(mousex, mousey):
                x, y = mousex // self.tile_size * self.tile_size, mousey // self.tile_size * self.tile_size

                if o == 1:  # vertical ship, must compute the area (ship.size) squares above
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
                    o = event.key == pygame.K_UP if event.key in [pygame.K_UP, pygame.K_RIGHT] else o

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    try:
                        if self.__check_mouse(mousex, mousey):
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
                                 rect=[(self.tile_size * i + 1) + self.__screen_width + self.separation_width,
                                       self.tile_size * j + 1,
                                       self.tile_size - 1, self.tile_size - 1],
                                 color=col)

    def __draw_selected_area_border(self, mousex, mousey):
        x, y = (mousex - self.separation_width) // self.tile_size * self.tile_size, \
               mousey // self.tile_size * self.tile_size

        pygame.draw.rect(self.__screen,
                         color=(200, 150, 100),
                         rect=[x + self.separation_width, y, self.tile_size + 1, self.tile_size + 1],
                         width=4)

    def __shoot(self, mousex, mousey):
        x, y = mousey // self.tile_size * self.tile_size, \
               (mousex - self.__screen_width - self.separation_width) // self.tile_size * self.tile_size

        response = self.__game.shoot(x // self.tile_size, y // self.tile_size)

        if response != ShotResult.ALREADY_HIT:
            for part_filled in range(0, self.tile_size, 6):
                pygame.draw.rect(self.__screen,
                                 color=self.shots_board_colors[
                                     self.__game.shots_board.board[x // self.tile_size][y // self.tile_size]
                                 ],
                                 rect=(y + self.__screen_width + self.separation_width, x, part_filled, part_filled))

                try:  # easier to ask for forgiveness than permission
                    if response[0] == ShotResult.SUNK or response == (ShotResult.WON, Player.HUMAN):
                        image = self.__explosion[part_filled // 6]
                        offset = uniform(0.8, 1.7)
                        image = pygame.transform.scale(image,
                                                       (int(self.tile_size * offset), int(self.tile_size * offset)))
                        self.__screen.blit(image, (y + self.__screen_width + self.separation_width, x))
                except (IndexError, TypeError):
                    pass

                pygame.display.flip()
                pygame.time.Clock().tick(30)

        self.__display_text(response)

    def __display_text(self, response, full=True):
        text = ""
        if type(response) == tuple and response[0] == ShotResult.SUNK:
            text = "Sunk " + self.ship_names[response[1]]
        elif type(response) == ShotResult:
            text = self.shot_responses[response]
        elif type(response) == Player:
            text = self.players[response] + " won! Press any key to start a new game"
        elif type(response) == str:
            text = response
        elif response is None:
            self._text_area = None
            return

        text_object = pygame.font.Font('freesansbold.ttf', self.bottom_margin//2).render(text, True, (255, 200, 130))
        text_rect = text_object.get_rect()
        width = self.__screen_width // 2 if not full else self.__screen_width + self.separation_width // 2
        text_rect.center = (width, self.__screen_height + self.bottom_margin // 2)

        self._text_area = text_object, text_rect

    def __check_mouse(self, mousex, mousey, shooting=False):
        if shooting:
            return self.__screen_width + self.separation_width <= mousex < \
                   2 * self.__screen_width + self.separation_width - 1 and \
                   0 <= mousey < self.__screen_height - 1
        else:
            return 0 <= mousex < self.__screen_width - 1 and \
                   0 <= mousey < self.__screen_height - 1

    def __show_help_screen(self, start=False):
        self.__screen.fill(self.colors['BACKGROUND'])

        text_object = pygame.font.Font('freesansbold.ttf', 50).render("Battleships", True, (255, 200, 130))
        text_rect = text_object.get_rect()
        text_rect.center = (self.__screen_width // 2, self.bottom_margin)
        self.__screen.blit(text_object, text_rect)

        text_object = pygame.font.Font('freesansbold.ttf', 15).render("by marc", True, self.colors['HIT'])
        text_rect = text_object.get_rect()
        text_rect.center = (self.__screen_width // 2 + self.__screen_width // 4, self.bottom_margin * 1.7)
        self.__screen.blit(text_object, text_rect)

        text_object = pygame.font.Font('freesansbold.ttf', 30).render("Placing ships", True,
                                                                      self.colors['WATER'])
        text_rect = text_object.get_rect()
        text_rect.bottomleft = (self.separation_width, int(self.bottom_margin * 3))
        self.__screen.blit(text_object, text_rect)

        self.draw_text(font=pygame.font.Font('freesansbold.ttf', 20),
                       color=self.colors['SHIP'],
                       text="Hover the mouse over the desired ship location. " +
                            "Place it by clicking the mouse and rotate it with the UP and RIGHT arrows",
                       rect=(
                           self.separation_width, self.bottom_margin * 3.5, self.__screen_width - self.separation_width,
                           80))

        text_object = pygame.font.Font('freesansbold.ttf', 30).render("Playing the game", True,
                                                                      self.colors['WATER'])
        text_rect = text_object.get_rect()
        text_rect.bottomleft = (self.separation_width, int(self.bottom_margin * 6))
        self.__screen.blit(text_object, text_rect)

        self.draw_text(font=pygame.font.Font('freesansbold.ttf', 20),
                       color=self.colors['SHIP'],
                       text="The left board represents your board, where the AI will take shots. " +
                            "The right board is the board where you take the shots. " +
                            "You take shots by clicking on a square",
                       rect=(
                           self.separation_width, self.bottom_margin * 6.5, self.__screen_width - self.separation_width,
                           100))

        text = "start" if start else "resume"
        text_object = pygame.font.Font('freesansbold.ttf', 30).render(f"Press any key to {text}", True,
                                                                      self.colors['WATER'])
        text_rect = text_object.get_rect()
        text_rect.center = (self.__screen_width // 2, self.__screen_height - self.bottom_margin // 2)
        self.__screen.blit(text_object, text_rect)
        pygame.display.flip()

    def draw_text(self, text, color, rect, font, aa=False, bkg=None):
        """
        from https://www.pygame.org/wiki/TextWrap
        """
        rect = pygame.Rect(rect)
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            self.__screen.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text
