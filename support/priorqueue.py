class Qitem:

    def __init__(self, obj, prior):
        self.obj = obj
        self.priority = prior
        self.next = None


class PriorityQueue:

    def __init__(self):
        self.queue = None

    def put(self, obj, prior):
        prev = None
        cur = self.queue
        while not (cur is None):
            if cur.priority >= prior:
                break
            prev = cur
            cur = cur.next
        if prev is None:
            self.queue = Qitem(obj, prior)
            if cur is not None:
                self.queue.next = cur
        else:
            item = Qitem(obj, prior)
            next_item = prev.next
            prev.next = item
            item.next = next_item

    def get(self):
        item = self.queue
        self.queue = self.queue.next
        return item.obj

    def is_empty(self):
        return self.queue is None
