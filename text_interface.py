from gates import *
from board import Board
import os
import re
from random import randint
from draw import *


def parse(line):
    match = re.search('[-]{2}\w{0,}', line)
    if match:
        if not line.index(match[0]):
            return match[0]
    input('Wrong form of input. Press enter and try again')
    return None


def helper(item):
    os.system('cls')
    if not item:    # TODO: перенести все записи в файл "help.txt"
        with open('help.txt', 'r') as h:
            line = h.readline()
            while line != '\n':
                print(line, end='')
                line = h.readline()

    else:
        pass

    print('Press "Enter" to go back to the game')
    input()


def rnd_color_generator():
    fore = randint(30, 39)
    back = randint(30, 39)
    while back == fore:
        back = randint(31, 39)
    return '\x1b[{:d}m'.format(fore), '\x1b[{:d}m'.format(back+10)


RESET_COLORS = '\x1b[0m'
N = 25
M = 100
status = True
text_board = Textboard(N, M)
commands = ['saved', 'save', 'create', 'connect', 'delcon', 'delete', 'clear', 'run', 'change', 'set']
cur_board = Board()

while status:
    os.system('cls')
    print('Write "--help" for help to view a list of available commands')
    text_board.draw_board()

    line = input()
    command = parse(line)
    if command is None:
        continue
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
            text_board.clear_board()
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
                    if gate_type + name in text_board.coords:
                        input('Gate with this name is already on board')
                    else:
                        cur_board.add(gate_type, name)
                        colors = rnd_color_generator()
                        if gate_type == 'SRC':
                            fnt = colors[0]
                            if fnt == '\x1b[31m':
                                fnt = '\x1b[32m'
                            colors = (fnt, '\x1b[41m')
                            text_board.coords[gate_type + name] = (cur_board.sources[gate_type + name], x, y, colors)
                        elif gate_type == 'PIP':
                            text_board.coords[gate_type + name] = (cur_board.sinks[gate_type + name], x, y, colors)
                        else:
                            text_board.coords[gate_type + name] = (cur_board.gates[gate_type + name], x, y, colors)
                        text_board.draw_gate(gate_type + name)
            else:
                input('Wrong creation call. Try again...')
        else:
            input('Wrong creation call. Try again...')

    if command == '--connect':
        gates = reminder.split(',')
        if len(gates) != 2:
            input('Wrong command. Try again...')
        else:
            out_gate = re.findall('\w{1,}\d{0,}' ,gates[0])
            if len(out_gate) == 0 or len(out_gate) > 2:
                input('Wrong command. Try again...')
            else:
                if len(out_gate) == 1:
                    out = 0
                    out_name = out_gate[0]
                else:
                    out_name = out_gate[0]
                    out = int(out_gate[1])
                in_gate = re.findall('\w{1,}\d{0,}', gates[1])
                if len(in_gate) == 0 or len(in_gate) > 2:
                    input('Wrong command. Try again...')
                else:
                    if len(in_gate) == 1:
                        inp = 0
                        in_name = in_gate[0]
                    else:
                        in_name = in_gate[0]
                        inp = int(in_gate[1])
                    text_board.draw_connection(out_name, out, in_name, inp)

    if command == '--delete':  # ToDo: implement this also
        pass

    if command == '--delcon':  # ToDo: implement this also
        pass

    if command == '--clear':
        text_board.clear_board()

    if command == '--run':
        pass

    if command == '--change':
        pass  # TODO: don't forget to change the color

    if command == '--set':
        pass
        '\x1b[{:d}m'  # <- color 41-red, 42-green

