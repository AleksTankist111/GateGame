from gates import *
from board import Board
import os
import re


def draw_board(board):
    print(' ' + '-' * len(board[0]))
    for row in board:
        s = '|'
        for char in row:
            s += char
        s += '|'
        print(s)
    print(' ' + '-' * len(board[0]))


def parse(line):
    match = re.search('[-]{2}\w{0,}', line)
    if match:
        if not line.index(match[0]):
            return match[0]
    input('Wrong form of input. Press enter and try again')
    return None


def helper(item):
    os.system('cls')
    if not item:
        print('Space {:d}x{:d} is available for you to put there gates.'.format(N, M))
        print('Each gate not wider than 10 cells, but can be of any height(depends of number of I/O)')
        print('PLEASE USE NAMES <6 symbols length of!')
        print('Example of using the game:')
        print('--create SRC s1 5 5, s2 5 10')
        print('--create NOT my1 15 5, my2 15 10')
        print('--create AND my3 25 6')
        print('--create PIP s3 35 7')
        print('--connect s1 0 my1 0')
        print('--connect s2 0 my2 0')
        print('--connect my1 0 my3 0')
        print('--connect my2 0 my3 1')
        print('--connect my3 0 s3 0')
        print('--run 2')
        print('--set s1 True')
        print('--change s2')
        print('--run')
        print('This set of commands will create the NOT-OR gate on the board, and then on the Sink s2')
        print('you will see the value you received. After than you change the initial values on sources.')
        print('Then you will notice that value on the sink has changed.')
    else:
        pass

    print('Press "Enter" to go back to the game')
    input()


def clear_board():
    return [[' ' for i in range(M)] for j in range(N)]


def draw_gate(gate, x, y):
    inp_count = len(gate.inputs)
    out_count = len(gate.outputs)
    height = max(len(gate.inputs), len(gate.outputs))
    for i in range(x + 1, x + 9):
        text_board[y][i] = '_'
    for i in range(height):
        if inp_count > 0:
            text_board[y + 1 + i][x - 1] = '-'
            inp_count -= 1
        text_board[y + 1 + i][x] = '|'
        text_board[y + 1 + i][x + 9] = '|'
        if out_count > 0:
            text_board[y + 1 + i][x + 10] = '-'
            out_count -= 1
    for j in range(1, 9):
        text_board[y + 1 + i][x + j] = '_'
    bias = max((8 - len(gate.name)) // 2 + (8 - len(gate.name)) % 2, 0)
    for j in range(x + 1 + bias, x + 9 - bias):
        text_board[y + 1 + height // 2][j] = gate.name[j - x - 1 - bias]


N = 25
M = 100
status = True
text_board = clear_board()
commands = ['saved', 'save', 'create', 'connect', 'delcon', 'delete', 'run', 'change', 'set']
cur_board = Board()
coords = {}

while status:
    os.system('cls')
    print('Write "--help" for help to view a list of available commands')
    draw_board(text_board)

    line = input()
    command = parse(line)
    reminder = line[len(command):]
    if command == '--help':
        helper(reminder)

    if command == '--quit':
        status = False
        os.system('cls')

    if command == '--saved':
        cur_board.print_content()
        input('Press Enter to continue...')

    if command == '--save':
        match = re.search('\w{1,}', reminder)
        if match:
            cur_board.save(match[0])
            coords.clear()
            text_board = clear_board()
        else:
            input('Wrong name of gate. Press enter and try again...')

    if command == '--create':
        match = re.search('\w{1,}', reminder)
        if match:
            gate_type = match[0]
            new_gates = re.findall('\w{1,}[ ]\d{1,}[ ]\d{1,}', reminder[1 + len(gate_type):])
            if new_gates:
                for gate in new_gates:
                    name, x, y = gate.split(' ')
                    x = int(x)
                    y = int(y)
                    cur_board.add(gate_type, name)
                    coords[name] = (x, y)
                    if gate_type == 'SRC':
                        draw_gate(cur_board.sources[gate_type + name], x, y)
                    elif gate_type == 'PIP':
                        draw_gate(cur_board.sinks[gate_type + name], x, y)
                    else:
                        draw_gate(cur_board.gates[gate_type + name], x, y)
            else:
                input('Wrong creation call. Try again...')
        else:
            input('Wrong creation call. Try again...')

    if command == '--connect':
        pass

    if command == '--delete':
        pass

    if command == '--delcon':  # ToDo: implement this also
        pass

    if command == '--run':
        pass

    if command == '--change':
        pass

    if command == '--set':
        pass
