import heapq


class PriorityQueue:
    def __init__(self):
        self._q = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._q, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._q)[-1]


class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item({})'.format(self.name)


q = PriorityQueue()
q.push(Item('foo'), 1)
q.push(Item('bar'), 3)
q.push(Item('foo2'), 5)
q.push(Item('bar2'), 3)
assert str(q.pop()) == 'Item(foo2)'
assert str(q.pop()) == 'Item(bar)'
assert str(q.pop()) == 'Item(bar2)'
assert str(q.pop()) == 'Item(foo)'
