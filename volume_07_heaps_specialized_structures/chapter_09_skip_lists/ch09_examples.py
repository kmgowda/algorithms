"""Volume 7, Chapter 9 - Skip Lists: Express Lanes for Linked Lists.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

import random
from typing import Any, Iterator


class SkipNode:
    def __init__(self, key: Any, value: Any, levels: int) -> None:
        self.key, self.value = key, value
        self.next: list[SkipNode | None] = [None] * levels      # next[i] = next node on lane i


class SkipList:
    """A sorted linked list with extra 'express lanes'. Each node joins lane i+1 with probability 1/2,
    so lane i has about n / 2^i nodes. Search, insert, delete: O(log n) expected."""

    MAX_LEVEL = 32

    def __init__(self, seed: int | None = None) -> None:
        self.head = SkipNode(None, None, self.MAX_LEVEL)
        self.level = 1
        self.size = 0
        self.rng = random.Random(seed)
        self.steps = 0                                          # for measuring search work

    def _random_level(self) -> int:
        level = 1
        while level < self.MAX_LEVEL and self.rng.random() < 0.5:
            level += 1
        return level

    def _find_predecessors(self, key: Any) -> list[SkipNode]:
        """On each lane from the top, move right while the next key is smaller; remember where we dropped down."""
        preds = [self.head] * self.MAX_LEVEL
        node = self.head
        for lane in range(self.level - 1, -1, -1):
            nxt = node.next[lane]
            while nxt is not None and nxt.key < key:
                node, nxt = nxt, nxt.next[lane]
                self.steps += 1
            preds[lane] = node
        return preds

    def get(self, key: Any) -> Any:
        node = self._find_predecessors(key)[0].next[0]
        if node is not None and node.key == key:
            return node.value
        raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        node = self._find_predecessors(key)[0].next[0]
        return node is not None and node.key == key

    def insert(self, key: Any, value: Any = None) -> None:
        preds = self._find_predecessors(key)
        node = preds[0].next[0]
        if node is not None and node.key == key:
            node.value = value
            return
        levels = self._random_level()
        self.level = max(self.level, levels)
        new = SkipNode(key, value, levels)
        for lane in range(levels):                              # splice into each of its lanes
            new.next[lane] = preds[lane].next[lane]
            preds[lane].next[lane] = new
        self.size += 1

    def delete(self, key: Any) -> bool:
        preds = self._find_predecessors(key)
        node = preds[0].next[0]
        if node is None or node.key != key:
            return False
        for lane in range(len(node.next)):
            if preds[lane].next[lane] is node:
                preds[lane].next[lane] = node.next[lane]
        while self.level > 1 and self.head.next[self.level - 1] is None:
            self.level -= 1
        self.size -= 1
        return True

    def keys(self) -> Iterator[Any]:
        node = self.head.next[0]
        while node is not None:
            yield node.key
            node = node.next[0]

    def range(self, low: Any, high: Any) -> list[Any]:
        """Find low with the express lanes, then walk the bottom lane: O(log n + answer size)."""
        node, out = self._find_predecessors(low)[0].next[0], []
        while node is not None and node.key <= high:
            out.append(node.key)
            node = node.next[0]
        return out

    def lane_sizes(self) -> list[int]:
        sizes = []
        for lane in range(self.level):
            count, node = 0, self.head.next[lane]
            while node is not None:
                count, node = count + 1, node.next[lane]
            sizes.append(count)
        return sizes


def leaderboard(scores: dict[str, int]) -> list[str]:
    """Industry example: Redis keeps sorted sets (leaderboards) in skip lists. Key = (-score, name)."""
    sl = SkipList(seed=1)
    for name, s in scores.items():
        sl.insert((-s, name))
    return [name for _, name in sl.keys()]


if __name__ == "__main__":
    sl = SkipList(seed=7)
    for k in range(1, 1025):
        sl.insert(k, f"stop {k}")
    print("lane sizes:", sl.lane_sizes()[:8], "...")
    sl.steps = 0
    sl.get(777)
    print("steps to find stop 777:", sl.steps, "| range 100..105:", sl.range(100, 105))
    sl.delete(101)
    print("after deleting 101:", sl.range(100, 105))
    print(leaderboard({"Ana": 120, "Ben": 300, "Cy": 210}))
