from random import seed, randint, choice
from datetime import datetime
import json
import sys

RANDOM_SEED = 16
seed(RANDOM_SEED)

class Food():
    def __init__(self, board_max_x, board_max_y):
        self.max_x = board_max_x
        self.max_y = board_max_y
        self.respawn()

    def respawn(self):
        x = randint(0, self.max_x)
        y = randint(0, self.max_y)
        self.pos = [x, y]

class Snake():
    def __init__(self, board_max_x, board_max_y, exclude):
        self.max_x = board_max_x
        self.max_y = board_max_y
        self.spawn(exclude=exclude)

    def spawn(self, exclude):
        x = randint(0, self.max_x)
        y = randint(0, self.max_y)
        if [x, y] != exclude:
            self.body = [[x, y]]
        else:
            self.spawn(exclude)

    @property
    def head(self):
        return self.body[0]

    @property
    def tail(self):
        return self.body[-1]

class Board():
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y

        self.food = Food(self.max_x, self.max_y)
        self.snake = Snake(self.max_x, self.max_y, exclude=self.food.pos)

        self.move_snake([1, 0]) # default starting move / triggers validation

    def move_snake(self, direction):
        self.last_direction = direction
        x = self.snake.head[0] + direction[0]
        y = self.snake.head[1] + direction[1]
        self.validate([x, y])
        self.snake.body.insert(0, [x, y])
        if [x, y] == self.food.pos:
            self.food.respawn()
        else:
            self.snake.body.pop()

    def validate(self, position):
        try:
            assert position[0] >= 0 and position[1] >= 0
            assert position[0] <= self.max_x and position[1] <= self.max_y
            for point in self.snake.body:
                assert point != position
            self.valid_position = True
        except:
            self.valid_position = False

    def find_valid_move(self):
        x = randint(-1, 1)
        y = 0 if abs(x) == 1 else choice([-1, 1])
        if [-x, -y] != self.last_direction:
            return [x, y]
        else:
            return self.find_valid_move()

if __name__ == '__main__':
    board_size = (int(sys.argv[1]), int(sys.argv[2]))

    t_start = datetime.now()

    board = Board(board_size[0], board_size[1])

    game_record_dump = list()
    j = json.dumps({
        'food_pos': board.food.pos,
        'snake': board.snake.body,
    })
    game_record_dump.append(j)

    while board.valid_position == True:
        direction = board.find_valid_move()
        board.move_snake(direction)

        j = json.dumps({
            'food_pos': board.food.pos,
            'snake': board.snake.body,
        })
        game_record_dump.append(j)

    t_end = datetime.now()
    performance = t_end - t_start

    j = json.dumps({
        'board_size': board_size,
        'steps': len(game_record_dump),
        'performance': performance.total_seconds(),
    })
    game_record_dump.append(j)

    dump = '\n'.join(game_record_dump)

    # file_name = int(t_start.timestamp())
    file_name = f"game_number_{RANDOM_SEED}"
    open(f"{file_name}.json", 'w').write(dump)


# directions = {
#     'right': [1, 0],
#     'left': [-1, 0],
#     'up': [0, -1],
#     'down': [0, 1]
# }
