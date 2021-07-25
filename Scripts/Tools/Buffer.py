from time import time
class Buffer:
    def __init__(self) -> None:
        self.items: dict[str, float] = {}
        self.lasttime = 0

    def update(self):
        deltatime = time()-self.lasttime
        self.lasttime = time()

        to_del = []
        for name in self.items.keys():
            if self.items[name] <= 0:
                to_del.append(name)
                continue
            self.items[name] -= deltatime
        for name in to_del:
            del self.items[name]

    def set(self, name: str, timeleft: float):
        if timeleft>0:
            self.items[name] = timeleft

    def get(self, name: str):
        return name in self.items

    def pop(self, name: str):
        if name in self.items:
            del self.items[name]
            return True
        return False