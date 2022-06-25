import numpy as np
import itertools
import random

from Cell import Cell
from Mujik import Mujik


class GameField:
    _N = 10
    _EXPLOSION_COUNT = 7
    _EXPLOSION_RADIUS = 1
    _BASE_DELAY = _EXPLOSION_RADIUS + 1
    _EXPLOSION_DELAY = 0
    _EXPLOSION_DURATION = 2
    _EXPLOSIONS_ADD_PER_TICK = _EXPLOSION_COUNT / _EXPLOSION_DURATION
    _DAMAGE = {0: 0, 1: 0, 2: 25, 3: 50, 4: 75}
    _TYPE_OF_CELL_STATES = {
        -1: 'out_of_bounds',
        0: 'white',  # no effect
        1: 'purple', # dangerous
        2: 'yellow', # low damage
        3: 'orange', # mid damage
        4: 'red'     # high damage
    }

    def __init__(self):
        self._player = Mujik(x=int(random.random()*self._N),
                             y=int(random.random()*self._N))
        self._active = {} # (x,y): [state, time_to_live]
        self._field = [[] for el in range(self._N)]
        self._action = 0
        self._ACTIONS_PROCESSOR = {0: self.process_hold, 1: self.process_move_up,
                                   2: self.process_move_down, 3: self.process_move_left,
                                   4:self.process_move_right}
        for i in range(self._N):
            for j in range(self._N):
                self._field[i].append(Cell(x=i, y=j))

    def mark_area(self, x, y, state=0):
        # Marks cells in square with centre in specified point
        if x > self._N-1 or x < 0:
            raise IndexError('x is out of bounds!')
        if y > self._N-1 or y < 0:
            raise IndexError('y is out of bounds!')

        buf_size = self._EXPLOSION_RADIUS*2 + 1
        buffer = np.zeros((buf_size,buf_size), int)
        centre = [int(buf_size/2), int(buf_size/2)]

        if state == 2:
            buffer[centre[0]][centre[1]] = 4
            shifts = list(filter(lambda xx: abs(xx[0]) != abs(xx[1]),
                                 set(itertools.combinations([0, 1, -1, 0], 2))))
            for shift in shifts:
                buffer[centre[0]+shift[0]][centre[1]+shift[1]] = 3

        for i in range(buf_size):
            for j in range(buf_size):
                if buffer[i][j] == 0:
                    buffer[i][j] = state

        if state == 1:
            self._active[(x, y)] = [state, self._BASE_DELAY + self._EXPLOSION_DELAY]
        elif state in(2, 3, 4):
            self._active[(x, y)] = [state, self._EXPLOSION_DURATION]

        x_start = x - centre[0]
        y_start = y - centre[1]
        for i in range(x_start, x_start+buf_size):
            for j in range(y_start, y_start+buf_size):
                if i > self._N-1 or i < 0 or j > self._N-1 or j < 0:
                    continue
                self._field[i][j].set_state(buffer[i-x_start][j-y_start])

    def tick(self):
        # Update actives
        if len(self._active) > 0:
            to_delete = []
            for (x, y), [state, time_to_live] in self._active.items():
                if time_to_live > 1:
                    self._active[(x,y)] = [state, time_to_live - 1]
                else:
                    if state == 1:
                        self.mark_area(x, y, 2)
                        self._active[(x,y)] = [2, self._EXPLOSION_DURATION]
                    elif state in (2, 3, 4):
                        self.mark_area(x, y, 0)
                        to_delete.append((x, y))
            for (x, y) in to_delete:
                del self._active[(x,y)]

        # Add new dangers (they shall become new explosions)
        # New explosions can spawn only in the way to not alias its cells with another explosion
        if len(self._active) == 0:
            generated_active = []
            counter = 0
            while len(generated_active) < self._EXPLOSION_COUNT:
                counter += 1
                new_x = int(random.random()*self._N)
                new_y = int(random.random()*self._N)
                if counter % 100000 == 0:
                    generated_active.append((new_x, new_y))
                    break
                if len(generated_active) != 0:
                    flag = False
                    for x, y in generated_active:
                        if abs(new_x - x) < 2*self._EXPLOSION_RADIUS + 1 and \
                                abs(new_y - y) < 2*self._EXPLOSION_RADIUS + 1:
                            flag = True
                            break
                    if not flag:
                        generated_active.append((new_x, new_y))
                else:
                    generated_active.append((new_x, new_y))

            for (x, y) in generated_active:
                self.mark_area(x, y, 1)

        #PROCESS PLAYER
        action_result = self._ACTIONS_PROCESSOR[self._action]()
        player_x, player_y = self._player.get_location()
        damage = -1*self._DAMAGE[self._field[player_x][player_y].get_state()]
        self._player.change_hp(damage)
        if self._player.get_hp() < 100:
            # Regeneration
            self._player.change_hp(1)
        return action_result, self._player.get_hp() > 0

    def set_action(self, action):
        self._action = action

    def process_move_up(self):
        # Returns 1 if action is invalid
        x, y = self._player.get_location()
        if y - 1 >= 0:
            self._player.move_up()
            return 0
        return 1

    def process_move_down(self):
        # Returns 1 if action is invalid
        x, y = self._player.get_location()
        if y + 1 <= self._N - 1:
            self._player.move_down()
            return 0
        return 1

    def process_move_left(self):
        # Returns 1 if action is invalid
        x, y = self._player.get_location()
        if x - 1 >= 0:
            self._player.move_left()
            return 0
        return 1

    def process_move_right(self):
        # Returns 1 if action is invalid
        x, y = self._player.get_location()
        if x + 1 <= self._N - 1:
            self._player.move_right()
            return 0
        return 1

    def process_hold(self):
        return 0

    def get_active(self):
        return self._active

    def get_field(self):
        return self._field

    def print_field(self):
        x, y = self._player.get_location()
        for j in range(self._N):
            for i in range(self._N):
                ender = '  '
                if i == x and j == y:
                    ender = 'p '
                print(self._field[i][j].get_state(), end=ender)
            print('')

    def get_player(self):
        return self._player

    def get_player_locality(self):
        x, y = self._player.get_location()
        # Each possible shift from player location in radius of 1
        shifts = list(set(itertools.combinations([-1, 0, 1, -1, 0, 1], 2)))
        shifts.sort()
        result = np.reshape([self._field[x+xn][y+yn].get_state()
                             if x+xn in range(10) and y+yn in range(10) else -1
                             for (xn, yn) in shifts], (3, 3)).transpose()
        return tuple(tuple(el for el in sub) for sub in result)
