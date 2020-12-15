from abc import abstractmethod
from typing import Tuple


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
    def copy(self, new_name):
        pass

    def update(self):
        self.is_used = False

    def used(self):
        self.is_used = True

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

