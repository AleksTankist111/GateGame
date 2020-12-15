from typing import Tuple
from gates.gate import Gate
from gates.gatesio.pipe import Pipe
from gates.container import Container


class ANDGate(Gate):

    def __init__(self, name):
        self.inputs = (Pipe(), Pipe())
        self.outputs = (Container(self, 0),)
        self.last_outputs = self._process()
        self.is_used = False
        self.name = name

    def _process(self) -> Tuple[bool, ...]:
        product = all([pipe.get() for pipe in self.inputs])
        return product,

    def used(self):
        self.is_used = True

    def update(self):
        self.is_used = False

    def copy(self, new_name) -> Gate:
        return ANDGate(new_name)


class NOTGate(Gate):

    def __init__(self, name):
        self.inputs = (Pipe(),)
        self.outputs = (Container(self, 0),)
        self.last_outputs = self._process()
        self.is_used = False
        self.name = name

    def _process(self) -> Tuple[bool, ...]:
        product = not self.inputs[0].get()
        return product,

    def used(self):
        self.is_used = True

    def update(self):
        self.is_used = False

    def copy(self, new_name) -> Gate:
        return NOTGate(new_name)


if __name__ == '__main__':
    pass

