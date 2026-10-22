"""Volume 7, Chapter 30 - Sketches: Count-Min, a small table that never undercounts.

Run:  python3 ch30_examples.py
"""

from __future__ import annotations

import hashlib
import random
from collections import Counter


class CountMin:
    """depth rows of width counters; each item adds 1 to one counter per row; estimate = smallest of its counters (Figure 30.1)."""

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


def sized_for(eps: float, delta: float) -> tuple[int, int]:
    """Width e/eps and depth ln(1/delta), rounded up: then each estimate is at most true + eps x N with
    probability at least 1 - delta (Figure 30.3)."""
    import math
    return math.ceil(math.e / eps), math.ceil(math.log(1 / delta))


def guarantee_check(eps: float, delta: float, seed: int = 27) -> tuple[int, int, int, float]:
    """Build the sketch sized for (eps, delta) on the search stream and count the words whose overcount exceeds
    eps x N. Returns (width, depth, words over the limit, fraction over)."""
    r = random.Random(seed)
    words = [f"word{i}" for i in range(2000)]
    searches = [("dragons" if r.random() < 0.05 else r.choice(words)) for _ in range(20000)]
    true = Counter(searches)
    w, d = sized_for(eps, delta)
    cm = CountMin(w, d)
    for s_ in searches:
        cm.add(s_)
    bad = sum(1 for x, c in true.items() if cm.estimate(x) - c > eps * len(searches))
    return w, d, bad, bad / len(true)


class CountMinConservative(CountMin):
    """Conservative update: raise only the counters that are at the current minimum (never more than needed)."""

    def add(self, item, times: int = 1) -> None:
        if times < 0:
            raise ValueError("Count-Min only counts upwards")
        cols = self._cols(item)
        target = min(self.rows[r][c] for r, c in enumerate(cols)) + times
        for r, c in enumerate(cols):
            self.rows[r][c] = max(self.rows[r][c], target)


class CountSketch:
    """Charikar, Chen and Farach-Colton's Count sketch (Figure 30.4): each row also gives the item a random sign +1 or
    -1; add the sign to the item's counter, and estimate by the median over rows of sign x counter. Unbiased, and it
    allows removals (negative counts)."""

    def __init__(self, width: int, depth: int):
        if width < 1 or depth < 1:
            raise ValueError("width and depth must be at least 1")
        self.width, self.depth = width, depth
        self.rows = [[0] * width for _ in range(depth)]

    def _cell(self, r, item):
        h = int(hashlib.sha256(f"{r}:{item}".encode()).hexdigest(), 16)
        return h % self.width, 1 if (h >> 128) & 1 else -1

    def add(self, item, times: int = 1) -> None:
        for r in range(self.depth):
            c, sign = self._cell(r, item)
            self.rows[r][c] += sign * times

    def estimate(self, item) -> float:
        import statistics
        return statistics.median(sign * self.rows[r][c] for r in range(self.depth) for c, sign in [self._cell(r, item)])


def merge(a: CountMin, b: CountMin) -> CountMin:
    if (a.width, a.depth) != (b.width, b.depth):
        raise ValueError("only sketches of the same shape and hashes can be merged")
    out = CountMin(a.width, a.depth)
    out.rows = [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a.rows, b.rows)]
    return out


def compare_variants(width: int, depth: int, seed: int = 27) -> dict:
    """Average and worst overcount (absolute error for Count sketch) of the three variants on the search stream."""
    r = random.Random(seed)
    words = [f"word{i}" for i in range(2000)]
    searches = [("dragons" if r.random() < 0.05 else r.choice(words)) for _ in range(20000)]
    true = Counter(searches)
    out = {}
    for name, cls in (("count-min", CountMin), ("conservative", CountMinConservative), ("count sketch", CountSketch)):
        sk = cls(width, depth)
        for s_ in searches:
            sk.add(s_)
        errs = [abs(sk.estimate(x) - c) for x, c in true.items()]
        out[name] = (round(sum(errs) / len(errs), 2), max(errs), sk.estimate("dragons") - true["dragons"])
    return out


TINY = ["dragons", "maps", "dragons", "poems", "dragons", "maps", "atlas"]


def tiny_grid() -> tuple[list, dict]:
    """A 3 x 8 sketch of seven searches, for drawing (Figure 30.2): (rows, each word's columns)."""
    cm = CountMin(8, 3)
    for w in TINY:
        cm.add(w)
    return cm.rows, {w: cm._cols(w) for w in sorted(set(TINY))}


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
    print(sized_for(0.001, 0.01), sized_for(0.01, 0.05), guarantee_check(0.001, 0.01), guarantee_check(0.005, 0.05))
    print(compare_variants(100, 4))
    rows, cols = tiny_grid()
    print(rows, cols)
    a, b = CountMin(100, 4), CountMin(100, 4)
    for w in ("x", "y", "x"):
        a.add(w)
    for w in ("x", "z"):
        b.add(w)
    print(merge(a, b).estimate("x"))
