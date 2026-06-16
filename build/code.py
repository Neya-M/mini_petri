import keypad
import board
import digitalio
import time
import copy
from adafruit_max7219 import matrices

global past_empty
past_empty = True
global paused
paused = False
curr = [0, 0]  # y, x
global start_pos
start_pos = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]

global curr_grid
curr_grid = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]

new_grid = [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]

global past_grids
past_grids = [[[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]],

              [[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]],

              [[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]]

alive = []
global alive_neighbors
alive_neighbors = []
global back_step
back_step = 0

keys = keypad.KeyMatrix(
    row_pins=(board.A0, board.A1, board.A2),
    column_pins=(board.A3, board.SDA, board.SCL),
)

cs = digitalio.DigitalInOut(board.MISO)
spi = board.SPI()
matrix = matrices.Matrix8x8(spi, cs)


def step_forward():
    global alive_neighbors
    global back_step
    if back_step > 0:
        back_step += 1
        curr_grid = copy.deepcopy(past_grids[back_step])
    else:
        for row_num, row in enumerate(curr_grid):
            for col_num, value in enumerate(row):
                if value == 1:
                    alive.append((row_num, col_num))
            neighbors = []
            neighbor_count = 0
            for cell in alive:
                neighbors.append((cell[0] - 1, cell[1] - 1),
                                 (cell[0] - 1, cell[1]),
                                 (cell[0] - 1, cell[1] + 1),
                                 (cell[0], cell[1] - 1),
                                 (cell[0], cell[1] + 1),
                                 (cell[0] + 1, cell[1] - 1),
                                 (cell[0] + 1, cell[1]),
                                 (cell[0] + 1, cell[1] + 1))
                for neighbor in neighbors:
                    if neighbor[0] < 0 or neighbor[1] < 0:
                        neighbors.remove(neighbor)
                        continue
                    neighbor_count += curr_grid[neighbor]
                if neighbor_count < 4 and neighbor_count > 2:
                    new_grid[cell[0]][cell[1]] = 1
                alive_neighbors.append(neighbors)
            alive_set = set(alive)
            temp = list(set(alive_neighbors))
            alive_neighbors = [item for item in temp if item not in alive_set]
            neighbor_neighbors = []
            neighbor_count2 = 0
            for cell in alive_neighbors:
                neighbor_neighbors.append(
                    (cell[0] - 1, cell[1] - 1),
                    (cell[0] - 1, cell[1]),
                    (cell[0] - 1, cell[1] + 1),
                    (cell[0], cell[1] - 1),
                    (cell[0], cell[1] + 1),
                    (cell[0] + 1, cell[1] - 1),
                    (cell[0] + 1, cell[1]),
                    (cell[0] + 1, cell[1] + 1))
                for neighbor in neighbor_neighbors:
                    if neighbor[0] < 0 or neighbor[1] < 0:
                        continue
                    neighbor_count2 += curr_grid[neighbor]
                if neighbor_count2 == 3:
                    new_grid[cell[0]][cell[1]] = 1


def step_back():
    global back_step
    global curr_grid
    curr_grid = copy.deepcopy(past_grids[back_step])
    if not back_step == 2:
        back_step += 1


def playpause():
    global paused
    paused.toggle()
    while not paused:
        if curr_grid == [[0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0]]:
            paused = True
        step_forward()
        time.sleep(1.0)


def reset():
    global curr_grid
    global start_pos
    if curr_grid == start_pos:
        curr_grid = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

        start_pos = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]
    else:
        curr_grid = copy.deepcopy(start_pos)


def toggle():
    global past_empty
    global past_grids
    curr_grid[curr[0]][curr[1]] = 1 - curr_grid[curr[0]][curr[1]]
    start_pos[curr[0]][curr[1]] = 1 - start_pos[curr[0]][curr[1]]
    if not past_empty:
        past_grids = [[[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]],

                      [[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]],

                      [[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]]]
        past_empty = True


def update():
    while True:
        matrix.fill(False)
        for row in range(8):
            for col in range(8):
                if curr_grid[row][col] == 1:
                    matrix.pixel(col, row, True)
        matrix.show()
        time.sleep(0.1)


while True:
    event = keys.events.get()
    if event:
        key = event.key_number
        if event.pressed:
            if key == 0:
                curr[0] -= 1
            elif key == 1:
                curr[0] += 1
            elif key == 2:
                curr[1] -= 1
            elif key == 3:
                curr[1] += 1
            elif key == 4:
                toggle()
            elif key == 5:
                playpause()
            elif key == 6:
                reset()
            elif key == 7:
                step_forward()
            elif key == 8:
                step_back()
