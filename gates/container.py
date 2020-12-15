class Container:

    def __init__(self, obj, obj_id: int):
        self._item = obj
        self.id = obj_id

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
        return Container(None, self.id)
