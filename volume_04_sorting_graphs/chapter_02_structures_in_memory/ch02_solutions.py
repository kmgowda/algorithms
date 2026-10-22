"""Volume 4, Chapter 2 - Structures in Memory: companion code for the Thinking Problems (Section 2.17).

A tiny cache simulator counts misses, so the answers do not depend on the machine.
Run:  python3 ch02_solutions.py
"""

from __future__ import annotations

import random
from collections import OrderedDict


def cache_misses(addresses, line_bytes: int = 64, capacity_lines: int = 8) -> int:
    """Count the misses of a cache that holds capacity_lines lines and evicts the least recently used."""
    cache, misses = OrderedDict(), 0
    for a in addresses:
        line = a // line_bytes
        if line in cache:
            cache.move_to_end(line)
        else:
            misses += 1
            cache[line] = True
            if len(cache) > capacity_lines:
                cache.popitem(last=False)
    return misses


def scan(start: int, n: int, step: int = 8) -> list[int]:
    """Thinking Problem 1: the byte addresses of n consecutive 8-byte numbers."""
    return [start + i * step for i in range(n)]


def transpose_naive(a: list, n: int) -> list:
    """b[c][r] = a[r][c] for an n x n grid stored row by row in one flat list."""
    b = [None] * (n * n)
    for r in range(n):
        for c in range(n):
            b[c * n + r] = a[r * n + c]
    return b


def transpose_blocked(a: list, n: int, t: int) -> list:
    """Thinking Problem 2: the same transpose, one t x t tile at a time, so each tile's lines stay cached."""
    b = [None] * (n * n)
    for r0 in range(0, n, t):
        for c0 in range(0, n, t):
            for r in range(r0, min(r0 + t, n)):
                for c in range(c0, min(c0 + t, n)):
                    b[c * n + r] = a[r * n + c]
    return b


def transpose_addresses(n: int, t: int | None = None) -> list[int]:
    """The byte addresses a transpose touches: read a[r][c] at 8(rn + c), write b[c][r] after the n*n source."""
    out, base, t = [], 8 * n * n, t or max(n, 1)
    for r0 in range(0, n, t):
        for c0 in range(0, n, t):
            for r in range(r0, min(r0 + t, n)):
                for c in range(c0, min(c0 + t, n)):
                    out += [8 * (r * n + c), base + 8 * (c * n + r)]
    return out


def three_orders(n: int = 4096, capacity_lines: int = 8, seed: int = 1) -> tuple[int, int, int]:
    """Thinking Problem 3: misses for reading n numbers forwards, backwards and in random order."""
    forward = scan(0, n)
    shuffled = forward[:]
    random.Random(seed).shuffle(shuffled)
    return (cache_misses(forward, capacity_lines=capacity_lines),
            cache_misses(forward[::-1], capacity_lines=capacity_lines),
            cache_misses(shuffled, capacity_lines=capacity_lines))


if __name__ == "__main__":
    print(cache_misses(scan(0, 1000)), cache_misses(scan(56, 2)))
    n = 64
    print(cache_misses(transpose_addresses(n), capacity_lines=32),
          cache_misses(transpose_addresses(n, 8), capacity_lines=32))
    print(three_orders())
