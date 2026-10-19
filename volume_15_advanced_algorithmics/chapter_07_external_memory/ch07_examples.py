"""Volume 15, Chapter 7 - External Memory and Big Data: Disk-Based Algorithms, MapReduce.

The cost that matters is how many BLOCKS move between slow storage and fast memory, not CPU steps.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

import heapq
import os
import random
import tempfile
from collections import defaultdict
from typing import Callable, Iterable


def external_sort(values: Iterable[int], memory_items: int, workdir: str) -> tuple[list[int], int, int]:
    """Sort data larger than memory: (1) read `memory_items` at a time, sort each chunk, write it as a 'run' file;
    (2) k-way merge all runs with a heap, reading them sequentially (V7-C3, V5-C13).
    Returns (sorted values, number of runs, items read + written = I/O volume)."""
    runs, chunk, io = [], [], 0

    def flush() -> None:
        nonlocal io
        path = os.path.join(workdir, f"run{len(runs)}.txt")
        with open(path, "w") as f:
            f.write("\n".join(map(str, sorted(chunk))))
        io += len(chunk)
        runs.append(path)
        chunk.clear()

    for v in values:
        io += 1
        chunk.append(v)
        if len(chunk) == memory_items:
            flush()
    if chunk:
        flush()

    files = [open(p) for p in runs]
    try:
        heads = []
        for i, f in enumerate(files):
            line = f.readline()
            if line:
                heapq.heappush(heads, (int(line), i))
        out = []
        while heads:
            v, i = heapq.heappop(heads)
            out.append(v)
            io += 2                                   # read from a run, write to the output
            line = files[i].readline()
            if line:
                heapq.heappush(heads, (int(line), i))
    finally:
        for f in files:
            f.close()
    return out, len(runs), io


def block_reads(n_items: int, block: int, pattern: str, rng: random.Random) -> int:
    """How many disk blocks a scan touches: sequential reads reuse each block; random reads mostly don't
    (only the most recent block is 'cached' here)."""
    order = range(n_items) if pattern == "sequential" else [rng.randrange(n_items) for _ in range(n_items)]
    reads, current = 0, None
    for i in order:
        if i // block != current:
            current = i // block
            reads += 1
    return reads


def map_reduce(records: Iterable[str], mapper: Callable[[str], Iterable[tuple[str, int]]],
               reducer: Callable[[str, list[int]], int], workers: int = 4) -> dict[str, int]:
    """A miniature MapReduce: MAP each record to (key, value) pairs on its worker, SHUFFLE pairs to the worker
    owning hash(key) % workers, then REDUCE all values of each key. Every step can run on separate machines."""
    records = list(records)
    shards = [records[w::workers] for w in range(workers)]             # split input among workers
    shuffled: list[dict[str, list[int]]] = [defaultdict(list) for _ in range(workers)]
    for shard in shards:                                                # map phase (one per worker)
        for record in shard:
            for key, value in mapper(record):
                owner = sum(map(ord, key)) % workers                    # stable partitioning by key
                shuffled[owner][key].append(value)
    result: dict[str, int] = {}
    for part in shuffled:                                               # reduce phase (one per worker)
        for key, values in part.items():
            result[key] = reducer(key, values)
    return result


def word_count(documents: list[str]) -> dict[str, int]:
    """Industry example: the classic MapReduce job."""
    return map_reduce(documents, lambda doc: ((w.lower().strip(".,!?"), 1) for w in doc.split()),
                      lambda _, counts: sum(counts))


if __name__ == "__main__":
    rng = random.Random(1)
    data = [rng.randint(0, 10 ** 6) for _ in range(20000)]
    with tempfile.TemporaryDirectory() as d:
        out, runs, io = external_sort(data, 2000, d)
    print("external sort ok:", out == sorted(data), "| runs:", runs, "| items moved:", io)
    print("blocks read, sequential:", block_reads(100000, 100, "sequential", rng),
          "| random:", block_reads(100000, 100, "random", rng))
    docs = ["the cat sat", "the dog sat", "The cat ran!"]
    print(word_count(docs))
