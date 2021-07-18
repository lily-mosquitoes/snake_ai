import pygame
import sys
import json
import time

class Playback():
    def __init__(self, board_size, steps, performance):
        print('steps: ', steps)
        print('performance: ', performance)
        board_size = (board_size[0]*10+10, board_size[1]*10+10)

        self.black = pygame.Color(0, 0, 0)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)

        pygame.init()
        pygame.display.set_caption('snake game visualizer')

        self.window = pygame.display.set_mode(board_size)
        self.fps = pygame.time.Clock()

    def draw_board(self, board_position):
        self.window.fill(self.black)

        food_x = board_position['food_pos'][0]*10
        food_y = board_position['food_pos'][1]*10
        pygame.draw.rect(self.window, self.red, pygame.Rect(food_x-1, food_y-1, 10-1, 10-1))

        snake = [[tile[0]*10, tile[1]*10] for tile in board_position['snake']]
        for x, y in snake:
            pygame.draw.rect(self.window, self.green, pygame.Rect(x-1, y-1, 10-1, 10-1))

        pygame.display.update()
        self.fps.tick(3)

if __name__ == '__main__':
    dump = open(sys.argv[1], 'r').read().split('\n')
    game = [json.loads(line) for line in dump]
    metadata = game.pop()

    playback = Playback(**metadata)

    board_position = iter(game)
    while True:
        try:
            playback.draw_board(next(board_position))
        except StopIteration:
            break

    time.sleep(1)
