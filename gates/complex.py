from gates.gate import Gate
from typing import Tuple
from gates.elementary import *
from gates.container import Container


class ComplexGate(Gate):

    def __init__(self, sources, gates, sinks, name):
        self.inputs = tuple(Pipe(source.name) for source in sources)
        self.gates = tuple(gates)
        for gate in gates:
            for inp in gate:
                item = inp.get_pointer()
                if item in sinks:
                    idx = sinks.index(item)
                    inp.connect(self.inputs[idx])

        self.outputs = tuple(sinks)

        self.is_used = False
        self.update()
        self.last_outputs = self._process()
        self.update()
        self.name = 'COM' + name

    def _process(self) -> Tuple[bool, ...]:
        return tuple(out.get() for out in self.outputs)

    def update(self):
        for gate in self.gates:
            gate.update()
        for out in self.outputs:
            out.update()
        for inp in self.inputs:
            inp.update()
        self.is_used = False

    def copy(self, new_name):

        dict_inputs = dict()
        dict_gates = dict()
        dict_outputs = dict()
        for item in self.outputs:
            item.deep_copy(dict_inputs, dict_gates, dict_outputs)

        new_sources = []
        for item in self.inputs:
            new_sources.append(dict_inputs[item.name])
        new_gates = []
        for item in self.gates:
            new_gates.append(dict_gates[item.name])
        new_sinks = []
        for item in self.outputs:
            new_sinks.append(dict_outputs[item.name])

        # Идея - рекурсивная статическая функция класса Gate. Идет от конца к началу, добавляя в словарь
        # созданные копии (ключ - имя оригинала). КАК ПОЛУЧИТЬ ДОСТУП К СЛОВАРЮ внутри функции?
        # Как себя такая функция будет вести при копировании сложного гейта внутри сложного гейта?
        # Если передавать словари как аргументы, то вроде норм. Хоть и реданданси.
        return ComplexGate(new_sources, new_gates, new_sinks, new_name)
