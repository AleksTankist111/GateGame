from gates.gate import Gate
from typing import Tuple
from gates.elementary import *
from gates.container import Container


class ComplexGate(Gate):

    def __init__(self, sources, gates, sinks, name):
        self.gates = tuple(gates)
        self.inputs = tuple(source.to_pipe() for source in sources)
        self.outputs = tuple(sinks)

        self.is_used = False
        self.update()
        self.last_outputs = self._process()
        self.update()
        self.name = name

    def _process(self) -> Tuple[bool, ...]:
        return tuple(out.get() for out in self.outputs)

    def update(self):
        for gate in self.gates:
            gate.update()
        self.is_used = False

    def copy(self, new_name):   # TODO: упростить! Положить всё в контейнеры? И использовать add_user.
        # new_gates = tuple(gate.copy(gate.name) for gate in self.gates)
        # new_sources = tuple(Pipe() for _ in self.inputs)
        # new_sinks = None
        # return ComplexGate(new_sources, new_gates, new_sinks, new_name)
        pass
