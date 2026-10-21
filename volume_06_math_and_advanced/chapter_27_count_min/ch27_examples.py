"""Volume 6, Chapter 27 - Sketches: Count-Min, a small table that never undercounts.

Run:  python3 ch27_examples.py
"""

from __future__ import annotations

import hashlib
import random
from collections import Counter


class CountMin:
    """depth rows of width counters; each item adds 1 to one counter per row; estimate = smallest of its counters (Figure 27.1)."""

    def __init__(self, width: int, depth: int):
        if width < 1 or depth < 1:
            raise ValueError("width and depth must be at least 1")
        self.width, self.depth = width, depth
        self.rows = [[0] * width for _ in range(depth)]

    def _cols(self, item):
        return [int(hashlib.sha256(f"{r}:{item}".encode()).hexdigest(), 16) % self.width for r in range(self.depth)]

    def add(self, item, times: int = 1) -> None:
        if times < 0:
            raise ValueError("Count-Min only counts upwards")
        for r, c in enumerate(self._cols(item)):
            self.rows[r][c] += times

    def estimate(self, item) -> int:
        return min(self.rows[r][c] for r, c in enumerate(self._cols(item)))


def experiment(width: int, depth: int, seed: int = 27) -> tuple[int, int, float]:
    """20,000 searches over 2,000 catalogue words (a few very popular). Returns (overcount on 'dragons', worst overcount, average overcount)."""
    r = random.Random(seed)
    words = [f"word{i}" for i in range(2000)]
    searches = [("dragons" if r.random() < 0.05 else r.choice(words)) for _ in range(20000)]
    true = Counter(searches)
    cm = CountMin(width, depth)
    for s in searches:
        cm.add(s)
    over = [cm.estimate(w) - c for w, c in true.items()]
    return cm.estimate("dragons") - true["dragons"], max(over), round(sum(over) / len(over), 2)


if __name__ == "__main__":
    for w, d in ((100, 1), (100, 4), (1000, 4)):
        print(w, d, experiment(w, d))
    cm = CountMin(50, 3)
    print(cm.estimate("never added"))
