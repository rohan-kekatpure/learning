class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.ranks = []
        self.kv = {}

    def get(self, key: int) -> int:
        val = self.kv.get(key, -1)
        
        # Reorder keys
        if val != -1:            
            r = self.ranks.index(key)
            k = self.ranks.pop(r)
            self.ranks.append(k)
            
        return val

    def put(self, key: int, value: int) -> None:
        if key in self.kv:
            self.kv[key] = value
            r = self.ranks.index(key)
            k = self.ranks.pop(r)
            self.ranks.append(k)
            return
            
        if len(self.kv) == self.capacity:
            lru_key = self.ranks.pop(0)
            self.kv.pop(lru_key)
            self.ranks.append(key)
            self.kv[key] = value
        else:
            self.kv[key] = value
            self.ranks.append(key)


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)