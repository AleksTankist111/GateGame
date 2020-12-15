from gates.gate import Gate
from typing import Tuple
from gates.elementary import *
from gates.container import Container


class ComplexGate(Gate):

    def __init__(self, sources, gates, sinks, name):
        self.gates = tuple(gates)
        self.inputs = tuple(source.to_pipe() for source in sources)  # TODO: ошибка здесь
        if not (type(sinks[0]) is Container):
            self.outputs = []
            for sink in sinks:
                for i, gate in enumerate(gates):
                    for j, out in enumerate(gate.outputs):
                        if sink.get_pointer() is out:
                            self.outputs.append(Container(gate, j))
            self.outputs = tuple(self.outputs)
        else:
            self.outputs = tuple(sinks)

        self.is_used = False
        self.update()
        self.last_outputs = self._process()
        self.update()
        self.name = name

    def _process(self) -> Tuple[bool, ...]:
        return tuple(out.get() for out in self.outputs)

    def used(self):
        for gate in self.gates:  # TODO: оставить только последнюю строку
            gate.used()
        self.is_used = True

    def update(self):
        for gate in self.gates:
            gate.update()
        self.is_used = False

    def copy(self, new_name):   # TODO: упростить! Положить всё в контейнеры? И использовать add_user.
        new_gates = tuple(gate.copy(gate.name) for gate in self.gates)
        new_sources = tuple(Pipe() for _ in self.inputs)

        for i, source in enumerate(self.inputs):
            for j, gate in enumerate(self.gates):
                for k, inp in enumerate(gate.inputs):
                    if inp.get_pointer() is source:
                        new_sources[i].add_user(new_gates[j].inputs[k])

        new_sinks = []
        for i, sink in enumerate(self.outputs):
            for j, gate in enumerate(self.gates):
                if sink.item is gate:
                    new_sinks.append(Container(new_gates[j], sink.id))
        new_sinks = tuple(new_sinks)

        for i, gate_out in enumerate(self.gates):
            for io, out in enumerate(gate_out.outputs):
                for j, gate_in in enumerate(self.gates):
                    for ji, inp in enumerate(gate_in.inputs):
                        if inp.get_pointer() is out:
                            new_gates[i].outputs[io].add_user(new_gates[j].inputs[ji])

        return ComplexGate(new_sources, new_gates, new_sinks, new_name)
