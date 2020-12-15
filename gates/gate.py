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

    def deep_copy(self, dict_inputs, dict_gates, dict_outputs):
        if not ((self.name in dict_inputs) or (self.name in dict_gates) or (self.name in dict_outputs)):
            new_item = self.copy(self.name)
            if self.name[:3] == 'PIP':
                if self.name[3:5] == 'IN':
                    dict_inputs[self.name] = new_item
                else:
                    dict_outputs[self.name] = new_item
            else:
                dict_gates[self.name] = new_item

            for i, inp in enumerate(self.inputs):
                if inp.get_pointer() is None:
                    new_inp = None
                else:
                    new_inp = inp.get_pointer().deep_copy(dict_inputs, dict_gates, dict_outputs)
                new_item.inputs[i].connect(new_inp, inp.id)

            return new_item

        else:
            if self.name in dict_inputs:
                return dict_inputs[self.name]
            elif self.name in dict_gates:
                return dict_gates[self.name]
            else:
                return dict_outputs[self.name]


if __name__ == '__main__':
    pass

