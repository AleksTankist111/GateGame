class Container:

    def __init__(self, obj, obj_id=0, master=None):
        self._item = obj
        self.id = obj_id
        self.master = master

    def get(self):
        if self._item is None:
            return False
        return self._item.get()[self.id]

    def connect(self, new_obj, new_id=0):
        self._item = new_obj
        self.id = new_id

    def get_pointer(self):
        return self._item

    def update(self):
        self._item.update()

    def used(self):
        self._item.used()

    def copy(self):
        return self._item.copy(self._item.name)

    def deep_copy(self, *args):
        return self._item.deep_copy(*args)

    @property
    def name(self):
        return self._item.name
