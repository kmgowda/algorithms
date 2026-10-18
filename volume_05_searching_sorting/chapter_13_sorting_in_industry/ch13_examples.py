"""Volume 5, Chapter 13 - Sorting in Industry: External Sorting and Database ORDER BY.

Run:  python3 ch13_examples.py
"""

from __future__ import annotations

import heapq
import math
import os
import tempfile
from typing import Iterable, Iterator


def write_sorted_runs(numbers: Iterable[int], memory_limit: int, folder: str) -> list[str]:
    """Phase 1: read as many numbers as fit in 'memory', sort them, write them to a run file. Repeat."""
    paths, chunk = [], []
    for x in numbers:
        chunk.append(x)
        if len(chunk) == memory_limit:
            paths.append(_flush(sorted(chunk), folder, len(paths)))
            chunk = []
    if chunk:
        paths.append(_flush(sorted(chunk), folder, len(paths)))
    return paths


def _flush(sorted_chunk: list[int], folder: str, index: int) -> str:
    path = os.path.join(folder, f"run_{index}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(f"{x}\n" for x in sorted_chunk)
    return path


def _read_run(path: str) -> Iterator[int]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield int(line)


def merge_runs(paths: list[str]) -> Iterator[int]:
    """Phase 2: k-way merge. heapq.merge keeps only ONE number per run in memory at a time."""
    return heapq.merge(*(_read_run(p) for p in paths))


def external_sort(numbers: Iterable[int], memory_limit: int) -> list[int]:
    """Sort data bigger than memory: sorted runs on disk + one k-way merge pass."""
    with tempfile.TemporaryDirectory() as folder:
        runs = write_sorted_runs(numbers, memory_limit, folder)
        return list(merge_runs(runs))


def merge_passes(total_items: int, memory_limit: int, fan_in: int) -> int:
    """How many merge passes are needed: runs = ceil(N / M), each pass merges `fan_in` runs into one."""
    runs = math.ceil(total_items / memory_limit)
    passes = 0
    while runs > 1:
        runs = math.ceil(runs / fan_in)
        passes += 1
    return passes


def order_by(rows: list[dict], clauses: list[tuple[str, str]], limit: int | None = None) -> list[dict]:
    """Industry example: SQL 'ORDER BY col1 ASC, col2 DESC LIMIT k'.

    With LIMIT, a database keeps only the best k rows (a heap) instead of sorting everything.
    Without LIMIT, it applies stable sorts from the last clause to the first.
    """
    if limit is not None:
        def sort_key(row: dict) -> tuple:
            return tuple(row[c] if d == "ASC" else _Desc(row[c]) for c, d in clauses)
        return heapq.nsmallest(limit, rows, key=sort_key)
    out = list(rows)
    for column, direction in reversed(clauses):
        out.sort(key=lambda r: r[column], reverse=(direction == "DESC"))
    return out


class _Desc:
    """Wraps a value so that comparisons are reversed - lets DESC work for text as well as numbers."""

    def __init__(self, value) -> None:
        self.value = value

    def __lt__(self, other: "_Desc") -> bool:
        return other.value < self.value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _Desc) and self.value == other.value


if __name__ == "__main__":
    import random
    rng = random.Random(1)
    data = [rng.randint(0, 10**6) for _ in range(10_000)]
    result = external_sort(data, memory_limit=1_000)
    print("external sort correct:", result == sorted(data), "| runs used:", 10)
    print("passes for 1 TB of 100-byte rows, 1 GB memory, 100-way merge:",
          merge_passes(10**10, 10**7, 100))
    orders = [{"city": "Pune", "total": 250, "id": 1}, {"city": "Agra", "total": 900, "id": 2},
              {"city": "Pune", "total": 700, "id": 3}, {"city": "Agra", "total": 120, "id": 4}]
    print([r["id"] for r in order_by(orders, [("city", "ASC"), ("total", "DESC")])])
    print([r["id"] for r in order_by(orders, [("total", "DESC")], limit=2)])
