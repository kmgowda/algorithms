"""Volume 4, Chapter 10 - Designing Caches: The LRU Cache.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Callable, Hashable


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: Hashable = None, value: Any = None) -> None:
        self.key, self.value = key, value
        self.prev: _Node | None = None
        self.next: _Node | None = None


class LRUCache:
    """LeetCode 146: get and put in O(1). Evicts the Least Recently Used entry when full.

    Composition (V3-C12): a dictionary finds nodes by key in O(1); a doubly linked list with sentinels
    (V3-C6) keeps entries ordered from most recently used (front) to least recently used (back).
    Invariant: the dictionary and the list hold exactly the same keys, and len <= capacity.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self._map: dict[Hashable, _Node] = {}
        self._front, self._back = _Node(), _Node()
        self._front.next, self._back.prev = self._back, self._front
        self.hits = self.misses = 0

    def _unlink(self, node: _Node) -> None:
        assert node.prev is not None and node.next is not None
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node: _Node) -> None:
        first = self._front.next
        assert first is not None
        node.prev, node.next = self._front, first
        self._front.next = first.prev = node

    def get(self, key: Hashable, default: Any = None) -> Any:
        node = self._map.get(key)
        if node is None:
            self.misses += 1
            return default
        self.hits += 1
        self._unlink(node)                      # mark as most recently used
        self._push_front(node)
        return node.value

    def put(self, key: Hashable, value: Any) -> None:
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self._map) == self.capacity:
            oldest = self._back.prev            # least recently used sits just before the back sentinel
            assert oldest is not None
            self._unlink(oldest)
            del self._map[oldest.key]
        node = _Node(key, value)
        self._map[key] = node
        self._push_front(node)

    def keys_most_recent_first(self) -> list[Hashable]:
        out, node = [], self._front.next
        while node is not self._back:
            assert node is not None
            out.append(node.key)
            node = node.next
        return out

    def __len__(self) -> int:
        return len(self._map)


class OrderedDictLRU:
    """The same behaviour in a few lines using collections.OrderedDict (move_to_end and popitem)."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._data: OrderedDict[Hashable, Any] = OrderedDict()

    def get(self, key: Hashable, default: Any = None) -> Any:
        if key not in self._data:
            return default
        self._data.move_to_end(key, last=False)
        return self._data[key]

    def put(self, key: Hashable, value: Any) -> None:
        self._data[key] = value
        self._data.move_to_end(key, last=False)
        if len(self._data) > self.capacity:
            self._data.popitem(last=True)


def cached_lookup(fetch: Callable[[str], str], capacity: int) -> Callable[[str], str]:
    """Industry example: wrap a slow fetch (database, website) with an LRU cache."""
    cache = LRUCache(capacity)

    def lookup(key: str) -> str:
        value = cache.get(key)
        if value is None:
            value = fetch(key)
            cache.put(key, value)
        return value

    lookup.cache = cache  # type: ignore[attr-defined]
    return lookup


def hit_rate(requests: list[str], capacity: int) -> float:
    """What fraction of requests would an LRU cache of this size answer without the slow fetch?"""
    cache = LRUCache(capacity)
    for key in requests:
        if cache.get(key) is None:
            cache.put(key, True)
    return round(cache.hits / len(requests), 3) if requests else 0.0


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put("lion", "Africa")
    cache.put("panda", "China")
    cache.get("lion")
    cache.put("koala", "Australia")          # evicts panda, the least recently used
    print(cache.keys_most_recent_first(), cache.get("panda"), cache.get("koala"))
    calls = []
    profile = cached_lookup(lambda user: calls.append(user) or f"profile of {user}", capacity=2)
    for user in ["maya", "leo", "maya", "zoe", "maya", "leo"]:
        profile(user)
    print("Slow fetches:", calls)
    trace = ["home", "news", "home", "maps", "home", "news", "mail", "home", "news", "maps"]
    print({cap: hit_rate(trace, cap) for cap in (1, 2, 3, 4)})
