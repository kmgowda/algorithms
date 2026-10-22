"""Volume 7, Chapter 30 - Thinking Problems.

Problem 1: in one row, the expected overcount of an item is at most N / width (checked by averaging over seeds).
Problem 2: the k most searched words from a sketch plus a small heap of candidates, one pass.
Problem 3: the same hash in every row makes all rows identical, so extra rows add nothing.
"""

from __future__ import annotations

import hashlib
import heapq
import random

from ch30_examples import CountMin


def one_row_overcount(words: list, target: str, width: int, salt: str) -> int:
    """Overcount of target in a single row whose hash is salted by `salt`."""
    col = lambda w: int(hashlib.sha256(f"{salt}:{w}".encode()).hexdigest(), 16) % width
    c = col(target)
    return sum(1 for w in words if w != target and col(w) == c)


def top_k_sketch(stream: list, k: int, width: int = 1000, depth: int = 4) -> list:
    """Keep the k items with the largest estimates seen so far (a dictionary of candidates, trimmed by a heap)."""
    cm, cand = CountMin(width, depth), {}
    for x in stream:
        cm.add(x)
        cand[x] = cm.estimate(x)
        if len(cand) > k:
            drop = min(cand, key=cand.get)
            del cand[drop]
    return [w for w, _ in heapq.nlargest(k, cand.items(), key=lambda t: t[1])]


class SameHashCountMin(CountMin):
    """The bug: every row uses the same hash."""

    def _cols(self, item):
        c = int(hashlib.sha256(f"0:{item}".encode()).hexdigest(), 16) % self.width
        return [c] * self.depth


if __name__ == "__main__":
    r = random.Random(30)
    words = [f"w{r.randrange(500)}" for _ in range(5000)]
    avg = sum(one_row_overcount(words, "w7", 100, str(s)) for s in range(200)) / 200
    print(round(avg, 1), len(words) / 100)
    stream = ["dragons"] * 300 + ["maps"] * 200 + ["poems"] * 150 + words
    print(top_k_sketch(stream, 3))
