"""Volume 4, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Hashable


class TTLCache:
    """Exercise 1: entries expire `ttl` seconds after being stored (time is passed in, for testability)."""

    def __init__(self, ttl: float) -> None:
        self.ttl = ttl
        self._data: dict[Hashable, tuple[Any, float]] = {}

    def put(self, key: Hashable, value: Any, now: float) -> None:
        self._data[key] = (value, now + self.ttl)

    def get(self, key: Hashable, now: float, default: Any = None) -> Any:
        item = self._data.get(key)
        if item is None or item[1] <= now:
            self._data.pop(key, None)
            return default
        return item[0]


class ByteBudgetLRU:
    """Exercise 2: evict least recently used entries until the total size fits a byte budget."""

    def __init__(self, budget: int) -> None:
        self.budget = budget
        self.used = 0
        self._data: OrderedDict[Hashable, bytes] = OrderedDict()

    def put(self, key: Hashable, blob: bytes) -> None:
        if key in self._data:
            self.used -= len(self._data.pop(key))
        if len(blob) > self.budget:
            return                                      # too big to cache at all
        self._data[key] = blob
        self.used += len(blob)
        while self.used > self.budget:
            _, old = self._data.popitem(last=False)     # oldest first in this version
            self.used -= len(old)

    def get(self, key: Hashable) -> bytes | None:
        if key not in self._data:
            return None
        self._data.move_to_end(key)
        return self._data[key]


def fifo_vs_lru_misses(requests: list[str], capacity: int) -> tuple[int, int]:
    """Exercise 3: compare misses of first-in-first-out eviction with LRU eviction."""
    fifo: OrderedDict[str, None] = OrderedDict()
    lru: OrderedDict[str, None] = OrderedDict()
    fifo_miss = lru_miss = 0
    for key in requests:
        if key not in fifo:
            fifo_miss += 1
            fifo[key] = None
            if len(fifo) > capacity:
                fifo.popitem(last=False)
        if key in lru:
            lru.move_to_end(key)
        else:
            lru_miss += 1
            lru[key] = None
            if len(lru) > capacity:
                lru.popitem(last=False)
    return fifo_miss, lru_miss


if __name__ == "__main__":
    t = TTLCache(10)
    t.put("weather", "sunny", now=0)
    print(t.get("weather", now=5), t.get("weather", now=11))
    b = ByteBudgetLRU(10)
    b.put("a", b"12345")
    b.put("b", b"123456")
    print(b.get("a"), b.get("b"), b.used)
    print(fifo_vs_lru_misses(["a", "b", "a", "c", "a", "d", "a"], 2))
