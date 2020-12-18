from gates import *
from board import Board
from support.priorqueue import PriorityQueue, Qitem
import re

class Textboard:

    def __init__(self, n, m):
        self.N = n
        self.M = m
        self.coords = {}
        self.board = None
        self.clear_board()


    def draw_board(self):
        print(' ' + '-' * self.M)
        for row in self.board:
            s = '|'
            for char in row:
                s += char
            s += '|'
            print(s)
        print(' ' + '-' * self.M)

    def clear_board(self):
        self.board = [[' ' for _ in range(self.M)] for j in range(self.N)]
        self.coords.clear()

    def draw_gate(self, name):
        RESET_COLORS = '\x1b[0m'
        underscore = '\x1b[4m'
        bright = '\x1b[1m'
        item = self.coords[name]
        gate = item[0]
        x, y = item[1:3]
        fore, back = item[3]
        if gate.name[:3] != 'SRC':
            inp_count = len(gate.inputs)
        else:
            inp_count = 0
        out_count = len(gate.outputs)
        height = max(inp_count, out_count)
        for i in range(x + 1, x + 9):
            self.board[y][i] = fore + '_' + RESET_COLORS
        for i in range(height):
            if inp_count > 0:
                self.board[y + 1 + i][x - 1] = fore + '-' + RESET_COLORS
                inp_count -= 1
            self.board[y + 1 + i][x] = fore + '|' + back
            self.board[y + 1 + i][x + 9] = RESET_COLORS + fore + '|' + RESET_COLORS
            if out_count > 0:
                self.board[y + 1 + i][x + 10] = fore + '-' + RESET_COLORS
                out_count -= 1
        for j in range(1, 9):
            self.board[y + 1 + i][x + j] = fore + back + '_' + RESET_COLORS
        bias = max((8 - len(gate.name)) // 2 + (8 - len(gate.name)) % 2, 0)
        for j in range(x + 1 + bias, x + 9 - bias):
            self.board[y + 1 + height // 2][j] = fore + back + bright + underscore \
                                                 + gate.name[j - x - 1 - bias] + RESET_COLORS

    def draw_connection(self, start_name, out, fin_name, inp):
        RESET_COLORS = '\x1b[0m'
        start_obj = self.coords[start_name]
        fin_obj = self.coords[fin_name]
        x0 = start_obj[1] + 10
        y0 = start_obj[2] + 1 + out
        x1 = fin_obj[1] - 1
        y1 = fin_obj[2] + 1 + inp
        c0 = start_obj[3][0]
        start = (x0, y0)
        goal = (x1, y1)

        frontier = PriorityQueue()
        frontier.put((x0, y0), 0)
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0
        current = None

        while not frontier.is_empty():
            prev = current
            current = frontier.get()

            if current == goal:
                came_from[goal] = prev
                break

            for vert in self.__neighbors(current):
                new_cost = cost_so_far[current] + 1
                if vert not in cost_so_far or new_cost < cost_so_far[vert]:
                    cost_so_far[vert] = new_cost
                    priority = new_cost + self.__heuristic(goal, vert)
                    frontier.put(vert, priority)
                    came_from[vert] = current

        prev = came_from[goal]
        self.board[goal[1]][goal[0]] = '-'
        last_char = '-'
        last_x = goal[0] + 1
        last_y = goal[1]

        while prev is not None:
            if last_char == '-' and prev[1] < current[1]:
                if last_x >= current[0]:
                    self.board[current[1]][current[0]] = c0 + '└' + RESET_COLORS
                else:
                    self.board[current[1]][current[0]] = c0 + '┘' + RESET_COLORS
                last_char = '|'
            elif last_char == '-' and prev[1] == current[1]:
                self.board[current[1]][current[0]] = c0 + '-' + RESET_COLORS
            elif last_char == '-' and prev[1] > current[1]:
                if last_x >= current[0]:
                    self.board[current[1]][current[0]] = c0 + '┌' + RESET_COLORS
                else:
                    self.board[current[1]][current[0]] = c0 + '┐' + RESET_COLORS
                last_char = '|'

            elif last_char == '|' and prev[0] < current[0]:
                if last_y >= current[1]:
                    self.board[current[1]][current[0]] = c0 + '┐' + RESET_COLORS
                else:
                    self.board[current[1]][current[0]] = c0 + '┘' + RESET_COLORS
                last_char = '-'
            elif last_char == '|' and prev[0] == current[0]:
                self.board[current[1]][current[0]] = c0 + '|' + RESET_COLORS
            elif last_char == '|' and prev[0] > current[0]:
                if last_y >= current[1]:
                    self.board[current[1]][current[0]] = c0 + '┌' + RESET_COLORS
                else:
                    self.board[current[1]][current[0]] = c0 + '└' + RESET_COLORS
                last_char = '-'

            last_x = current[0]
            last_y = current[1]
            current = prev
            prev = came_from[current]
        # Binary search tree for Heuristic distance function
        # ┐└ ┘┌

    def __neighbors(self, coord):
        left_flag = False
        up_flag = False
        right_flag = False
        down_flag = False
        if coord[0] > 0:
            if '_' not in self.board[coord[1]][coord[0]-1]:
                if coord[0]-1 > 0:
                    if not re.search('\[4\dm', self.board[coord[1]][coord[0]-2]):
                        left_flag = True
                else:
                    left_flag = True

        if coord[0] < self.M - 1:
            if '_' not in self.board[coord[1]][coord[0]+1] and \
                    (not re.search('\[4\dm', self.board[coord[1]][coord[0]+1])):
                right_flag = True

        if coord[1] > 0:
            if not re.search('\[4\dm', self.board[coord[1]-1][coord[0]]):
                up_flag = True

        if coord[1] < self.N - 1:
            if '_' not in self.board[coord[1]+1][coord[0]]:
                if coord[0] < self.M - 1:
                    if not re.search('_', self.board[coord[1]+1][coord[0]+1]):
                        down_flag = True
                if coord[0] > 0:
                    if re.search('_', self.board[coord[1] + 1][coord[0] - 1]):
                        down_flag = False

        res = []
        if up_flag:
            res.append((coord[0], coord[1] - 1))
        if down_flag:
            res.append((coord[0], coord[1] + 1))
        if left_flag:
            res.append((coord[0] - 1, coord[1]))
        if right_flag:
            res.append((coord[0] + 1, coord[1]))

        return tuple(res)

    def __heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
