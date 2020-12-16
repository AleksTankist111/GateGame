from gates.gate import *
from typing import Tuple
from gates.complex import ComplexGate
from gates.elementary import *


class Board:

    def __init__(self):
        self.sources = {}
        self.sinks = {}
        self.gates = {}
        self.__saved_modules = {'NOT': NOTGate(''), 'AND': ANDGate(''), 'SRC': Source(''), 'PIP': Pipe('')}
        self._cur_name = ''

    @property
    def count(self):
        return len(self.gates) + len(self.sinks) + len(self.sources)

    def clear(self):
        self.sources.clear()
        self.sinks.clear()
        self.gates.clear()
        self._cur_name = ''

    def delete(self, name: str):
        if name in self.gates.keys():
            del self.gates[name]

    def save(self, name):
        if name not in self.__saved_modules.keys() and len(name) > 0 \
                and len(self.sources) > 0 and len(self.sinks) > 0:

            new_gate = ComplexGate(list(self.sources.values()),
                                   list(self.gates.values()), list(self.sinks.values()), name)
            self.__saved_modules[new_gate.name] = new_gate
            self.clear()
        else:
            print('This module name already exist')

    def delete_save(self, name):
        if name in self.__saved_modules.keys() and (name != 'NOT') and (name != 'AND') \
                and (name != 'SRC') and (name != 'PIP'):
            del self.__saved_modules[name]

    def add(self, name, new_name=None):
        if name not in self.__saved_modules.keys() or name == self._cur_name:
            print('Module with this name is not exist or not available now')
        else:
            if new_name is None:
                new_name = str(len(self.__saved_modules))
            new_gate = self.__saved_modules[name].copy(new_name)
            if name == 'SRC':
                self.sources[new_gate.name] = new_gate
            elif name == 'PIP':
                self.sinks[new_gate.name] = new_gate
            else:
                self.gates[new_gate.name] = new_gate

    def load(self, name):  # TODO: implement load module to board for changes (NOTE: CUR MOD CANNOT add cur elem)
        pass

    def update(self):
        for gate in self.gates.values():
            gate.update()
        for sink in self.sinks.values():
            sink.update()

    def compute(self) -> Tuple[bool, ...]:
        res = tuple(out.get() for out in self.sinks.values())
        self.update()
        return res

    # for debug and version 0.0001              TODO: delete after debug
    def print_content(self):
        print('##### Sources #####')
        if not len(self.sources):
            print('0 items;')
        else:
            for name in self.sources.keys():
                print(name)

        print('##### Gates #####')
        if not len(self.gates):
            print('0 items;')
        else:
            for name in self.gates.keys():
                print(name)

        print('##### Sinks #####')
        if not len(self.sinks):
            print('0 items;')
        else:
            for name in self.sinks.keys():
                print(name)

        print('##### Saved Gates #####')
        for name in self.__saved_modules.keys():
            print(name)
