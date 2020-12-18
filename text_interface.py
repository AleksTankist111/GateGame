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


def rnd_color_generator(gate_type):
    if gate_type != 'PIP' and gate_type != 'SRC':
        if gate_type == 'NOT':
            back = 34
        elif gate_type == 'AND':
            back = 35
        else:
            back = 36
    else:
        back = 31
        x_ar = [33, 36, 37, 38]
        fore = x_ar[randint(0, 3)]
        return ['\x1b[{:d}m'.format(fore), '\x1b[{:d}m'.format(back + 10)]
    fore = randint(31, 38)
    while fore == back:
        fore = randint(31, 38)
        if back in [31, 35] and fore in [31, 35]:
            fore = back
    return ['\x1b[{:d}m'.format(fore), '\x1b[{:d}m'.format(back+10)]


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
                        colors = rnd_color_generator(gate_type)
                        if gate_type == 'SRC':
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
                    if out_name not in text_board.coords or in_name not in text_board.coords:
                        input('Gate with this name is not exist. Try again...')
                        continue
                    text_board.draw_connection(out_name, out, in_name, inp)

                    if in_name[:3] != 'PIP':
                        cur_input = cur_board.gates[in_name].inputs[inp]
                    else:
                        cur_input = cur_board.sinks[in_name].inputs[inp]

                    if out_name[:3] == 'SRC':
                        cur_output = cur_board.sources[out_name]
                    elif out_name[:3] == 'PIP':
                        cur_output = cur_board.sinks[out_name]
                    else:
                        cur_output = cur_board.gates[out_name]

                    cur_input.connect(cur_output, out)
    if command == '--delete':  # ToDo: implement this also
        pass

    if command == '--delcon':  # ToDo: implement this also
        pass

    if command == '--clear':
        text_board.clear_board()

    if command == '--run':
        match = re.search('\d{1,}', reminder)
        if match:
            count = int(match[0])
        else:
            count = 1
        for j in range(count):
            print('##### Iteration {:d} #####'.format(j))
            res = cur_board.compute()
            for i, sink in enumerate(cur_board.sinks):
                print('{:s}: {:s}'.format(sink, str(res[i])))
                color = '\x1b[41m'
                if res[i]:
                    color = '\x1b[42m'
                text_board.coords[sink][3][1] = color
                text_board.draw_gate(sink)
        input('Press Enter to redraw all Pips...')
        continue

    if command == '--change':
        match = re.search('\w{1,}', reminder)
        if match:
            name = match[0]
            if name not in text_board.coords or 'SRC' not in name:
                input('Source with this name is not exist. Try again...')
                continue
            if text_board.coords[name][3][1] == '\x1b[42m':
                text_board.coords[name][3][1] = '\x1b[41m'
            else:
                text_board.coords[name][3][1] = '\x1b[42m'

            text_board.draw_gate(name)
            cur_board.sources[name].change()

    if command == '--set':
        match = re.search('\w{1,} \w{4,}', reminder)
        if match:
            name, value = match[0].split(' ')
            value = value.lower()
            if name not in text_board.coords or 'SRC' not in name:
                input('Source with this name is not exist. Try again...')
                continue
            if value == 'true':
                text_board.coords[name][3][1] = '\x1b[42m'
                v = True
            elif value == 'false':
                text_board.coords[name][3][1] = '\x1b[41m'
                v = False
            else:
                input('Command is not correct. Try again...')
                continue
            text_board.draw_gate(name)
            cur_board.sources[name].set(v)

