"""Volume 3, Chapter 19 - Sorting Data Too Big for Memory: sorted runs and a k-way merge.

A 'disk' is a list we may only read and write in blocks; memory holds at most M items at once.

Run:  python3 ch19_examples.py
"""

from __future__ import annotations

import heapq
import math
import random

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


class Disk:
    """Counts block reads and writes, the cost that matters for data on disk."""

    def __init__(self, block: int):
        self.block = block
        self.reads = self.writes = 0

    def read(self, items: list) -> list:
        self.reads += math.ceil(len(items) / self.block) if items else 0
        return list(items)

    def write(self, items: list) -> list:
        self.writes += math.ceil(len(items) / self.block) if items else 0
        return list(items)


def make_runs(data: list, memory: int, disk: Disk) -> list[list]:
    """Phase 1 (Figure 19.2): read memory-sized chunks, sort each in memory, write it back as a run."""
    runs = []
    for i in range(0, len(data), memory):
        chunk = sorted(disk.read(data[i:i + memory]))
        runs.append(disk.write(chunk))
    return runs


def merge_runs(runs: list[list], disk: Disk, log: list | None = None) -> list:
    """Phase 2 (Figure 19.3): k-way merge with a heap of the front item of every run."""
    for r in runs:
        disk.read(r)
    heap = [(r[0], i, 0) for i, r in enumerate(runs) if r]
    heapq.heapify(heap)
    out = []
    while heap:
        v, i, j = heapq.heappop(heap)
        out.append(v)
        if log is not None:
            log.append((v, i))
        if j + 1 < len(runs[i]):
            heapq.heappush(heap, (runs[i][j + 1], i, j + 1))
    return disk.write(out)


def external_sort(data: list, memory: int, block: int, fan_in: int | None = None) -> tuple[list, Disk, int]:
    """Sort with at most `memory` items in memory; merge at most `fan_in` runs at a time. Returns (sorted, disk, passes)."""
    disk = Disk(block)
    runs = make_runs(data, memory, disk)
    k = fan_in or max(2, len(runs))
    passes = 0
    while len(runs) > 1:
        runs = [merge_runs(runs[i:i + k], disk) for i in range(0, len(runs), k)]
        passes += 1
    return (runs[0] if runs else []), disk, passes


if __name__ == "__main__":
    disk = Disk(block=1)
    runs = make_runs(PILE, 3, disk)
    log = []
    print(runs, merge_runs(runs, disk, log), log[:4], disk.reads, disk.writes)
    rng = random.Random(1)
    big = [rng.randrange(10 ** 6) for _ in range(100_000)]
    for fan in (2, 4, 10, None):
        out, d, p = external_sort(big, memory=1000, block=100, fan_in=fan)
        print(fan, p, d.reads, d.writes, out == sorted(big))
