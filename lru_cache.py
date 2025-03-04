from collections import deque

class LRUCache:
    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self.cache = {}
        self.queue = deque()

    def get(self, key: str) -> str:
        if key in self.cache:
            self.queue.remove(key)
            self.queue.append(key)
            return self.cache[key]
        return ''

    def set(self, key: str, value: str) -> None:
        if key in self.cache:
            self.queue.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.queue.popleft()
            del self.cache[oldest]
            
        self.cache[key] = value
        self.queue.append(key)

    def rem(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]
            self.queue.remove(key)
