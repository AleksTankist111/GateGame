from gates.gate import Gate
from typing import Tuple
from gates.elementary import *
from gates.container import Container


class ComplexGate(Gate):

    def __init__(self, sources, gates, sinks, name):
        self.inputs = [Pipe(source.name[3:]) for source in sources]
        self.gates = list(gates)
        for gate in gates:
            for inp in gate.inputs:
                item = inp.get_pointer()
                if item in sources:
                    idx = sources.index(item)
                    inp.connect(self.inputs[idx])
        self.gates.extend(self.inputs)
        self.inputs = tuple(inp.inputs[0] for inp in self.inputs)
        self.gates.extend(sinks)
        self.outputs = tuple(sink.outputs[0] for sink in sinks)
        self.gates = tuple(self.gates)
        self.is_used = False
        self.update()
        self.last_outputs = self._process()
        self.update()
        self.name = 'COM_' + name

    def _process(self) -> Tuple[bool, ...]:
        return tuple(out.get() for out in self.outputs)

    def update(self):
        for gate in self.gates:
            gate.update()
        self.is_used = False

    def copy(self, new_name):

        dict_inputs = dict()
        dict_gates = dict()
        dict_outputs = dict()
        for item in self.outputs:
            item.deep_copy(dict_inputs, dict_gates, dict_outputs)

        new_sources = []
        for item in self.inputs:
            new_sources.append(dict_inputs[item.master.name])
        new_gates = []
        for item in self.gates:
            if item.name in dict_gates:
                new_gates.append(dict_gates[item.name])
        new_sinks = []
        for item in self.outputs:
            new_sinks.append(dict_outputs[item.master.name])

        return ComplexGate(new_sources, new_gates, new_sinks, self.name[4:] + new_name)
