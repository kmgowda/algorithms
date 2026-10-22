"""Volume 2, Chapter 10 - Caches: Keeping the Most Useful Things Close.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import random
from collections import deque


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key, self.value, self.prev, self.next = key, value, None, None


class LRUCache:
    """A map from key to node plus a doubly linked list from least to most recently used (Figure 10.4)."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map: dict = {}
        self.head, self.tail = _Node(), _Node()          # dummy ends: no special cases
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node: _Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _append(self, node: _Node) -> None:
        node.prev, node.next = self.tail.prev, self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return None
        self._unlink(node)
        self._append(node)                               # now the most recent
        return node.value

    def put(self, key, value) -> None:
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._unlink(node)
            self._append(node)
            return
        if len(self.map) == self.capacity:
            oldest = self.head.next                      # least recently used
            self._unlink(oldest)
            del self.map[oldest.key]
        node = _Node(key, value)
        self._append(node)
        self.map[key] = node

    def keys_oldest_first(self) -> list:
        out, n = [], self.head.next
        while n is not self.tail:
            out.append(n.key)
            n = n.next
        return out


def count_hits(requests, capacity: int, policy: str = "lru") -> int:
    """Hits for a request sequence under LRU or FIFO (Figure 10.2)."""
    hits = 0
    if policy == "lru":
        c = LRUCache(capacity)
        for r in requests:
            if c.get(r) is not None:
                hits += 1
            else:
                c.put(r, True)
        return hits
    shelf: deque = deque()
    for r in requests:
        if r in shelf:
            hits += 1
        else:
            if len(shelf) == capacity:
                shelf.popleft()
            shelf.append(r)
    return hits


def optimal_hits(requests, capacity: int) -> int:
    """Belady's ideal policy, which knows the future: on a miss with a full shelf, evict the item whose next
    request is furthest away (or never comes). No real policy can beat it (Practice Problem 10.3)."""
    if capacity <= 0:
        return 0
    hits, shelf = 0, set()
    for i, r in enumerate(requests):
        if r in shelf:
            hits += 1
            continue
        if len(shelf) == capacity:
            def next_use(item):
                for j in range(i + 1, len(requests)):
                    if requests[j] == item:
                        return j
                return len(requests)
            shelf.remove(max(sorted(shelf), key=next_use))
        shelf.add(r)
    return hits


def popular_requests(n: int, items: int = 200, seed: int = 7) -> list[int]:
    """Requests where an item's popularity falls off as 1/rank (Figure 10.3)."""
    rng = random.Random(seed)
    return rng.choices(range(items), weights=[1 / (k + 1) for k in range(items)], k=n)


if __name__ == "__main__":
    req = ["Maps", "Ocean", "Maps", "Clocks", "Stars", "Maps", "Ocean", "Stars"]
    print(count_hits(req, 3, "lru"), count_hits(req, 3, "fifo"))
    reqs = popular_requests(20_000)
    for size in (1, 5, 20, 80):
        print(size, count_hits(reqs, size, "lru") / len(reqs), count_hits(reqs, size, "fifo") / len(reqs))
    views = popular_requests(10_000, items=5000, seed=3)
    print("cached page views:", count_hits(views, 500, "lru") / len(views))
