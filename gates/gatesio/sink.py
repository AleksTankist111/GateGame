from gates.gatesio.pipe import Pipe


class Sink(Pipe):

    @property
    def state(self) -> bool:
        return self.get()

    def to_pipe(self) -> Pipe:
        pipe = Pipe()
        pipe.set(self._value)
        self._value.add_user(pipe)
        self._value.del_user(self)
        return pipe

