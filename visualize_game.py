import pygame
import sys

window_size = (300, 300)

black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)


pygame.init()
pygame.display.set_caption('snake game visualizer')
window = pygame.display.set_mode(window_size)

fps = pygame.time.Clock()

def move(states_list):
    window.fill(black)

    snake = next(states_list)
    for x, y in snake:
        pygame.draw.rect(window, green, pygame.Rect(x-1, y-1, 10-1, 10-1))

    pygame.display.update()
    fps.tick(3)

def open_game(file):
    game_moves = open(file, 'rt').read().strip().split('\n')
    states_list = list()
    for move in game_moves:
        move = move.split(';')
        tiles = list()
        for snake in move:
            tiles.append([int(p) for p in snake.split(',')])
        states_list.append(tiles)

    return iter(states_list)

if __name__ == '__main__':
    states_list = open_game(sys.argv[1])

    while True:
        move(states_list)
