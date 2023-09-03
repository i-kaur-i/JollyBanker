class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def insert(self, item):
        self.items.insert(0, item)

    def pop(self):
        return self.items.pop()

    def get_size(self):
        return len(self.items)
