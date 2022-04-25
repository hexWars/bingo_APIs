from random import shuffle
from diskcache import Deque, Index


class PersistentList:
    def __init__(self, cls):
        self.memo = Deque(directory=f"data/{cls.__name__}")
        self.list = list(self.memo)

    def append(self, new_item):
        self.memo.append(new_item)
        self.list.append(new_item)

    def appendleft(self, new_item):
        self.memo.appendleft(new_item)
        self.list.append(new_item)

    def extend(self, new_items):
        self.memo.extend(new_items)
        self.list.extend(new_items)

    def extendleft(self, new_items):
        self.memo.extendleft(new_items)
        self.list.extend(new_items)

    def clear(self):
        self.memo.clear()
        self.list.clear()

    def shuffle(self):
        shuffle(self.list)

    def __getitem__(self, item):
        return self.list.__getitem__(item)

    def peek(self):
        return self.memo.peek()

    def peekleft(self):
        return self.memo.peekleft()

    def transact(self):
        return self.memo.transact()

    def __len__(self):
        return len(self.list)


class PersistentDict:
    def __init__(self, cls):
        self.memo = Index(directory=f"data/{cls.__name__}")
        self.dict = dict(self.memo)

    def clear(self):
        self.memo.clear()
        self.dict.clear()

    def __setitem__(self, key, value):
        self.memo[key] = value
        self.dict[key] = value

    def __getitem__(self, item):
        return self.dict.__getitem__(item)

    def transact(self):
        return self.memo.transact()

    def __len__(self):
        return len(self.dict)


from .experiments import app as experiment_router
from .scales import app as scale_router
from .wechatAPIs import app as user_router

__all__ = {"experiment_router", "scale_router", "user_router"}
