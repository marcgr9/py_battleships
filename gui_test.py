from time import sleep

import pygame

from src.board import Board
from src.game import Game
from src.ship import Ship
from src.utils import ShipType


class GUI:
    def __init__(self):
        pygame.init()


        pygame.display.set_caption("Battleships")


pygame.init()

board_size = 10
tile_size = 50

screen_width = board_size * tile_size + 1
screen_height = board_size * tile_size + 1
screen = pygame.display.set_mode(
            (screen_width, screen_height))
mousex, mousey = 0, 0
o = 1
game = Game(10)


def draw_board():
    screen.fill((200, 100, 30))
    for i in range(board_size):
        for j in range(board_size):
            col = (100, 100, 100, 25) if game.player_board.board[j][i] == 0 else (30, 43, 128)
            pygame.draw.rect(screen, rect=[tile_size * i + 1, tile_size * j + 1, tile_size - 1, tile_size - 1],
                             color=col)


colors = {
    3: (200, 0, 0),
    2: (200, 200, 0),
    1: (30, 43, 128),
    0: (100, 100, 100)
}

def draw_boards():
    screen.fill((200, 100, 30))
    for i in range(board_size):
        for j in range(board_size):
            col = colors[game.player_board.board[j][i]]
            pygame.draw.rect(screen, rect=[tile_size * i + 1, tile_size * j + 1, tile_size - 1, tile_size - 1],
                             color=col)

    for i in range(board_size):
        for j in range(board_size):
            col = colors[game.shots_board.board[j][i]]
            pygame.draw.rect(screen, rect=[(tile_size * i + 1) + tile_size * board_size + 20, tile_size * j + 1, tile_size - 1, tile_size - 1],
                             color=col)


while True:
    for ship in game.get_player_ships():
        draw_board()
        if o == 1:
            x, y = mousex // tile_size * tile_size, mousey // tile_size * tile_size
            pygame.draw.rect(screen, color=(50, 70, 90), rect=[x, y - tile_size * (ship.size - 1), tile_size+1, ship.size*tile_size+1])
        else:
            x, y = mousex//tile_size * tile_size, mousey//tile_size * tile_size
            pygame.draw.rect(screen, color=(50, 70, 90), rect=[x, y, ship.size*tile_size+1, tile_size+1])

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == pygame.KEYDOWN:
                o = not o
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.place_ship(ship.type, o, y // tile_size, x // tile_size)
            if event.type == pygame.QUIT:
                quit()
            pygame.display.update()

    game.start()
    screen = pygame.display.set_mode(
        (screen_width * 2 + 20, screen_height))
    while game.playing:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
                x, y = (mousex - 20) // tile_size * tile_size, mousey // tile_size * tile_size
                pygame.draw.rect(screen, color=(200, 150, 100),
                                 rect=[x + 20, y, tile_size + 1, tile_size + 1], width=4)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = mousey // tile_size * tile_size, (mousex - screen_width - 20) // tile_size * tile_size
                game.shoot(x // tile_size, y // tile_size)

            if event.type == pygame.QUIT:
                quit()
            pygame.display.update()
        draw_boards()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
