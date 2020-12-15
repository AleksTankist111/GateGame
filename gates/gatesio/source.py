from gates.gatesio.pipe import Pipe


class Source(Pipe):

    def __init__(self):
        self._value = False
        self.users = []

    def change(self):
        self._value = not self._value

    def set(self, value: bool):
        assert type(value) == bool
        self._value = value

    def to_pipe(self) -> Pipe:
        pipe = Pipe()
        for item in self.users:
            pipe.add_user(item)
        return pipe


if __name__ == '__main__':
    pass
