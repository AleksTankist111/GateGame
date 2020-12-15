from typing import Tuple
from gates.gate import Gate
from gates.container import Container


class ANDGate(Gate):

    def __init__(self, name):
        self.inputs = (Container(None, 0), Container(None, 0))
        self.outputs = (Container(self, 0),)
        self.last_outputs = self._process()
        self.is_used = False
        self.name = 'AND' + name

    def _process(self) -> Tuple[bool, ...]:
        product = all([inp.get() for inp in self.inputs])
        return product,

    def copy(self, new_name) -> Gate:
        return ANDGate(new_name)


class NOTGate(Gate):

    def __init__(self, name):
        self.inputs = (Container(None, 0),)
        self.outputs = (Container(self, 0),)
        self.last_outputs = self._process()
        self.is_used = False
        self.name = 'NOT' + name

    def _process(self) -> Tuple[bool, ...]:
        product = not self.inputs[0].get()
        return product,

    def copy(self, new_name) -> Gate:
        return NOTGate(new_name)


class Source(Gate):

    def __init__(self, name):
        self._value = False
        self.outputs = (Container(self, 0),)
        self.last_outputs = self._process()
        self.is_used = False
        self.name = 'SRC' + name

    def _process(self) -> Tuple[bool, ...]:
        return self._value,

    def copy(self, new_name) -> Gate:
        return Source(new_name)

    def set(self, value):
        self._value = value

    def change(self):
        self._value = not self._value

    def used(self):
        pass


class Pipe(Gate):

    def __init__(self, name):
        self.inputs = (Container(None, 0),)
        self.outputs = (Container(self, 0),)
        self.last_outputs = self._process()
        self.is_used = False
        self.name = 'PIP' + name

    def _process(self) -> Tuple[bool, ...]:
        return self.inputs[0].get(),

    def copy(self, new_name) -> Gate:
        return Pipe(new_name)


if __name__ == '__main__':
    pass
