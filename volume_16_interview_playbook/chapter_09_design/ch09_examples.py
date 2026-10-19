"""Volume 16, Chapter 9 - Designing Data Structures: LRU, Iterators, Time-Based Stores.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

import bisect
import random
from collections import OrderedDict, deque
from typing import Iterator


class LRUCache:
    """LeetCode 146: get and put in O(1). An ordered dictionary keeps keys from least to most recently used."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.data: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key: int, value: int) -> None:
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)


class PeekingIterator:
    """LeetCode 284: look at the next item without consuming it - cache one item ahead."""

    def __init__(self, it: Iterator[int]) -> None:
        self.it = it
        self.ahead = next(it, None)

    def peek(self) -> int | None:
        return self.ahead

    def next(self) -> int | None:
        value, self.ahead = self.ahead, next(self.it, None)
        return value

    def has_next(self) -> bool:
        return self.ahead is not None


class TimeMap:
    """LeetCode 981: set(key, value, time) and get(key, time) = the value with the latest time <= time.
    Times arrive increasing, so each key's list stays sorted and get is a binary search."""

    def __init__(self) -> None:
        self.times: dict[str, list[int]] = {}
        self.values: dict[str, list[str]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times.setdefault(key, []).append(timestamp)
        self.values.setdefault(key, []).append(value)

    def get(self, key: str, timestamp: int) -> str:
        i = bisect.bisect_right(self.times.get(key, []), timestamp)
        return self.values[key][i - 1] if i else ""


class RandomizedSet:
    """LeetCode 380: insert, remove and get_random all in O(1) - a list for random access plus a dict of positions.
    Remove swaps the item with the last one, then pops."""

    def __init__(self, rng: random.Random) -> None:
        self.items: list[int] = []
        self.pos: dict[int, int] = {}
        self.rng = rng

    def insert(self, x: int) -> bool:
        if x in self.pos:
            return False
        self.pos[x] = len(self.items)
        self.items.append(x)
        return True

    def remove(self, x: int) -> bool:
        if x not in self.pos:
            return False
        i, last = self.pos.pop(x), self.items.pop()
        if i < len(self.items):
            self.items[i] = last
            self.pos[last] = i
        return True

    def get_random(self) -> int:
        return self.rng.choice(self.items)


class RateLimiter:
    """Industry example: allow at most `limit` requests per user in any `window` seconds (sliding log)."""

    def __init__(self, limit: int, window: int) -> None:
        self.limit, self.window = limit, window
        self.log: dict[str, deque[int]] = {}

    def allow(self, user: str, now: int) -> bool:
        q = self.log.setdefault(user, deque())
        while q and q[0] <= now - self.window:
            q.popleft()
        if len(q) < self.limit:
            q.append(now)
            return True
        return False


if __name__ == "__main__":
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    print(c.get(1), end=" ")
    c.put(3, 3)
    print(c.get(2), c.get(3))
    p = PeekingIterator(iter([1, 2, 3]))
    print(p.next(), p.peek(), p.next(), p.next(), p.has_next())
    tm = TimeMap()
    tm.set("price", "100", 1)
    tm.set("price", "120", 4)
    print(tm.get("price", 3), tm.get("price", 5), repr(tm.get("price", 0)))
    rl = RateLimiter(3, 10)
    print([rl.allow("u1", t) for t in (0, 1, 2, 3, 11, 12)])
