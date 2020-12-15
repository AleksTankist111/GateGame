class Pipe:

    def __init__(self, pipe=None):
        if pipe is not None:
            self._value = pipe
        else:
            self._value = False
        self.users = []

    def get(self) -> bool:
        if type(self._value) == bool:
            return self._value
        else:
            return self._value.get()

    def add_user(self, user):
        self.users.append(user)
        user.set(self)

    def del_user(self, user):
        if user in self.users:
            self.users.remove(user)
            user.set(False)

    def set(self, value):
        self._value = value

    def get_pointer(self):
        return self._value

    def to_pipe(self):
        return self


if __name__ == '__main__':
    pass
