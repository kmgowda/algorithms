"""Volume 15, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

import random
from typing import Hashable, Iterable


def majority_check(stream: list[Hashable]) -> Hashable | None:
    """Exercise 1 (LeetCode 169/229 idea): the vote gives a CANDIDATE; a second pass confirms it really is a majority."""
    candidate, count = None, 0
    for x in stream:
        if count == 0:
            candidate, count = x, 1
        else:
            count += 1 if x == candidate else -1
    return candidate if stream.count(candidate) * 2 > len(stream) else None


def sliding_window_average(stream: Iterable[float], window: int) -> list[float]:
    """Exercise 2: running average of the last `window` values with O(window) memory (a ring buffer, V3-C10)."""
    buf: list[float] = [0.0] * window
    total, out = 0.0, []
    for i, x in enumerate(stream):
        total += x - buf[i % window]
        buf[i % window] = x
        out.append(total / min(i + 1, window))
    return out


def sample_stream(stream: Iterable[Hashable], k: int, rng: random.Random) -> list[Hashable]:
    """Exercise 3: keep a fair random sample of an endless stream (reservoir sampling, V14-C7)."""
    sample: list[Hashable] = []
    for i, x in enumerate(stream, 1):
        if i <= k:
            sample.append(x)
        elif (j := rng.randint(1, i)) <= k:
            sample[j - 1] = x
    return sample


if __name__ == "__main__":
    print(majority_check([1, 2, 1, 1, 3]), majority_check([1, 2, 3]), sliding_window_average([1, 2, 3, 4, 5], 3),
          sample_stream(range(100), 3, random.Random(0)))
