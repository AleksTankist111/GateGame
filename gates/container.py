class Container:

    def __init__(self, obj, obj_id: int):
        self.item = obj
        self.id = obj_id
        self.users = []

    def get(self):
        return self.item.get()[self.id]

    def add_user(self, user):
        self.users.append(user)
        user.set(self)

    def del_user(self, user):
        if user in self.users:
            self.users.remove(user)
            user.set(False)

