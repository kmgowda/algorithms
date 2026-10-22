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


def max_fan_in(memory: int, block: int, double_buffer: bool = False) -> int:
    """The most runs one merge can read at once (Section 19.6): one block of memory per input run plus one block for
    the output, so memory // block - 1. With double buffering every run and the output need two blocks."""
    blocks = memory // block
    return blocks // 2 - 1 if double_buffer else blocks - 1


def merge_passes(runs: int, fan_in: int) -> int:
    """How many merge passes reduce `runs` sorted runs to one when each merge combines at most `fan_in` runs."""
    if fan_in < 2:
        raise ValueError("a merge needs a fan-in of at least 2")
    passes = 0
    while runs > 1:
        runs = -(-runs // fan_in)
        passes += 1
    return passes


def external_sort(data: list, memory: int, block: int, fan_in: int | None = None) -> tuple[list, Disk, int]:
    """Sort with at most `memory` items in memory; merge at most `fan_in` runs at a time (by default as many as the
    memory allows, max_fan_in). Returns (sorted, disk, passes)."""
    limit = max_fan_in(memory, block)
    if limit < 2 and len(data) > memory:
        raise ValueError("memory must hold at least three blocks to merge")
    k = min(fan_in or limit, limit) if limit >= 2 else 2
    disk = Disk(block)
    runs = make_runs(data, memory, disk)
    passes = 0
    while len(runs) > 1:
        runs = [merge_runs(runs[i:i + k], disk) for i in range(0, len(runs), k)]
        passes += 1
    return (runs[0] if runs else []), disk, passes


def replacement_selection(data: list, memory: int) -> list[list]:
    """Run formation by replacement selection (Challenge 19.1): keep a heap of `memory` items; repeatedly write the
    smallest item that is not smaller than the last one written, and read the next item in its place. Items smaller
    than the last one written wait for the next run. On random data the runs average about 2 * memory."""
    it = iter(data)
    heap = [(0, x) for _, x in zip(range(memory), it)]
    heapq.heapify(heap)
    runs: list[list] = []
    while heap:
        run_no, x = heapq.heappop(heap)
        if run_no == len(runs):
            runs.append([])
        runs[run_no].append(x)
        nxt = next(it, None)
        if nxt is not None:
            heapq.heappush(heap, (run_no if nxt >= x else run_no + 1, nxt))
    return runs


def polyphase(runs_a: int, runs_b: int) -> list[tuple[int, int, int]]:
    """Polyphase merge on three files (Section 19.6). Files A and B start with runs_a and runs_b runs, C is empty.
    Each phase merges runs pairwise from the two non-empty files onto the empty one, until one file runs dry.
    Returns, for every phase, (runs left on the three files, total, initial runs written in that phase) as
    ((a, b, c), written). Run sizes are counted in initial runs."""
    files = [[1] * runs_a, [1] * runs_b, []]
    log = []
    while sum(len(f) for f in files) > 1:
        empty = next(i for i, f in enumerate(files) if not f)
        x, y = [i for i in range(3) if i != empty]
        written = 0
        while files[x] and files[y]:
            size = files[x].pop(0) + files[y].pop(0)
            files[empty].append(size)
            written += size
        log.append((tuple(len(f) for f in files), written))
    return log


if __name__ == "__main__":
    disk = Disk(block=1)
    runs = make_runs(PILE, 4, disk)
    log = []
    print(runs, merge_runs(runs, disk, log), log[:4], disk.reads, disk.writes)
    rng = random.Random(1)
    big = [rng.randrange(10 ** 6) for _ in range(100_000)]
    print(max_fan_in(1000, 100), merge_passes(100, 9), polyphase(8, 5))
    rs = replacement_selection(big, 1000)
    print(len(rs), merge_passes(len(rs), 9), all(r == sorted(r) for r in rs))
    for fan in (2, 4, 9, None):
        out, d, p = external_sort(big, memory=1000, block=100, fan_in=fan)
        print(fan, p, d.reads, d.writes, out == sorted(big))
