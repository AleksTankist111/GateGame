from gates import *
from board import Board
if __name__ == '__main__':

    cur_board = Board()
    cur_board.add_sources(2)
    cur_board.add_sinks(1)
    cur_board.add('NOT', 'NOT1')
    cur_board.add('NOT', 'NOT2')
    cur_board.sources[0].add_user(cur_board.gates['NOT1'].inputs[0])
    cur_board.sources[1].add_user(cur_board.gates['NOT2'].inputs[0])
    cur_board.add('AND', 'AND1')
    cur_board.gates['NOT1'].outputs[0].add_user(cur_board.gates['AND1'].inputs[0])
    cur_board.gates['NOT2'].outputs[0].add_user(cur_board.gates['AND1'].inputs[1])
    cur_board.add('NOT', 'NOT3')
    cur_board.gates['AND1'].outputs[0].add_user(cur_board.gates['NOT3'].inputs[0])
    cur_board.gates['NOT3'].outputs[0].add_user(cur_board.sinks[0])
    cur_board.save('OR')
    # Создали OR и очистили доску

    cur_board.add_sources(2)
    cur_board.add_sinks()
    cur_board.add('OR', 'OR1')
    cur_board.sources[0].add_user(cur_board.gates['OR1'].inputs[0])
    cur_board.sources[1].add_user(cur_board.gates['OR1'].inputs[1])
    cur_board.gates['OR1'].outputs[0].add_user(cur_board.sinks[0])

    cur_board.print_content()
    print('Result: ', cur_board.compute(), '. Should be False')  # <-- error in calculation
    cur_board.sources[0].change()
    print('Result: ', cur_board.compute(), '. Should be True')



