from abc import abstractmethod
from typing import Tuple
from gates.gatesio.pipe import Pipe


class Gate:

    @abstractmethod
    def __init__(self, name=''):
        self.inputs = None
        self.outputs = None
        self.is_used = False
        self.last_outputs = None
        self.name = name

    @abstractmethod
    def _process(self):
        pass

    @abstractmethod
    def used(self):
        self.is_used = True

    @abstractmethod
    def update(self):
        self.is_used = False

    @abstractmethod
    def copy(self, new_name):
        pass

    def get(self) -> Tuple[bool, ...]:
        if self.is_used:
            return self.last_outputs
        else:
            self.used()
            self.last_outputs = self._process()
            return self.last_outputs

    def set_name(self, new_name: str):
        self.name = new_name


if __name__ == '__main__':
    pass

