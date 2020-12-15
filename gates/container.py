class Container:

    def __init__(self, obj, obj_id: int):
        self._item = obj
        self.id = obj_id
        self.users = []

    def get(self):
        if self._item is None:
            return False
        return self._item.get()[self.id]

    def add_user(self, user):
        self.users.append(user)
        user.set(self)

    def del_user(self, user):
        if user in self.users:
            self.users.remove(user)
            user.set(False)

    def set(self, obj):
        self._item = obj

    def get_pointer(self):
        return self._item
