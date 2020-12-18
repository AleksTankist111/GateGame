from gates import *
from board import Board

if __name__ == '__main__':

    cur_board = Board()
    cur_board.add('SRC', 'IN1')
    cur_board.add('SRC', 'IN2')
    cur_board.add('PIP', 'OUT1')
    cur_board.add('NOT', '1')
    cur_board.add('NOT', '2')
    cur_board.gates['NOT1'].inputs[0].connect(cur_board.sources['SRCIN1'])
    cur_board.gates['NOT2'].inputs[0].connect(cur_board.sources['SRCIN2'])
    cur_board.add('AND', '1')
    cur_board.gates['AND1'].inputs[0].connect(cur_board.gates['NOT1'])
    cur_board.gates['AND1'].inputs[1].connect(cur_board.gates['NOT2'])
    cur_board.add('NOT', '3')
    cur_board.gates['NOT3'].inputs[0].connect(cur_board.gates['AND1'])
    cur_board.sinks['PIPOUT1'].inputs[0].connect(cur_board.gates['NOT3'])
    cur_board.save('OR')
    # Создали OR и очистили доску
    cur_board.add('SRC', 'IN1')
    cur_board.add('SRC', 'IN2')
    cur_board.add('PIP', 'OUT1')
    cur_board.add('COM_OR', '1')
    cur_board.gates['COM_OR1'].inputs[0].connect(cur_board.sources['SRCIN1'])
    cur_board.gates['COM_OR1'].inputs[1].connect(cur_board.sources['SRCIN2'])
    cur_board.sinks['PIPOUT1'].inputs[0].connect(cur_board.gates['COM_OR1'])

    cur_board.print_content()
    print('Result: ', cur_board.compute(), '. Should be False')
    cur_board.sources['SRCIN1'].change()
    print('Result: ', cur_board.compute(), '. Should be True')





