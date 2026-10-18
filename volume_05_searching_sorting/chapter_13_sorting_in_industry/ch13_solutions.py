"""Volume 5, Chapter 13 - Solutions to the exercises."""

from __future__ import annotations

import heapq
import math
from typing import Iterable, Iterator


def runs_needed(total_bytes: int, memory_bytes: int) -> int:
    """Exercise 1: how many sorted run files phase 1 creates."""
    return math.ceil(total_bytes / memory_bytes)


def merge_sorted_streams(*streams: Iterable[int]) -> Iterator[int]:
    """Exercise 2: k-way merge with an explicit heap of (value, stream number) - what heapq.merge does inside."""
    iterators = [iter(s) for s in streams]
    heap = []
    for i, it in enumerate(iterators):
        first = next(it, None)
        if first is not None:
            heap.append((first, i))
    heapq.heapify(heap)
    while heap:
        value, i = heapq.heappop(heap)
        yield value
        nxt = next(iterators[i], None)
        if nxt is not None:
            heapq.heappush(heap, (nxt, i))


def dedupe_sorted_stream(stream: Iterable[int]) -> Iterator[int]:
    """Exercise 3: after an external sort, duplicates are neighbours - remove them with O(1) memory (like SELECT DISTINCT)."""
    previous = object()
    for x in stream:
        if x != previous:
            yield x
            previous = x


def top_k_streaming(stream: Iterable[int], k: int) -> list[int]:
    """Exercise 4: ORDER BY value DESC LIMIT k over a huge stream - a size-k min-heap, O(k) memory."""
    heap: list[int] = []
    for x in stream:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    return sorted(heap, reverse=True)


if __name__ == "__main__":
    print(runs_needed(10**12, 10**9), list(merge_sorted_streams([1, 4, 9], [2, 3, 10], [0])))
    print(list(dedupe_sorted_stream([1, 1, 2, 3, 3, 3, 5])), top_k_streaming(range(1000), 3))
