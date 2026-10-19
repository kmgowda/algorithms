"""Volume 15, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

import math

from ch07_examples import map_reduce


def merge_passes(n_items: int, memory_items: int, fan_in: int) -> int:
    """Exercise 1: passes over the data for external merge sort - one pass to create ceil(n / M) runs,
    then each merge pass combines `fan_in` runs at a time."""
    runs = math.ceil(n_items / memory_items)
    passes = 1
    while runs > 1:
        runs = math.ceil(runs / fan_in)
        passes += 1
    return passes


def inverted_index(documents: dict[str, str]) -> dict[str, list[str]]:
    """Exercise 2: word -> sorted list of documents containing it, as MapReduce (the core of a search engine)."""
    names = sorted(documents)
    pairs = map_reduce(
        [f"{i}\t{documents[n]}" for i, n in enumerate(names)],
        lambda rec: {(w.lower(), 1 << int(rec.split("\t")[0])) for w in rec.split("\t")[1].split()},
        lambda _, masks: sum(set(masks)),
    )
    return {w: [names[i] for i in range(len(names)) if mask >> i & 1] for w, mask in sorted(pairs.items())}


def max_temperature(readings: list[str]) -> dict[str, int]:
    """Exercise 3: 'city,temp' lines -> hottest reading per city, as MapReduce."""
    return map_reduce(readings, lambda line: [(line.split(",")[0], int(line.split(",")[1]))], lambda _, ts: max(ts))


if __name__ == "__main__":
    print(merge_passes(10 ** 9, 10 ** 7, 10), inverted_index({"a": "red fish", "b": "blue fish"}),
          max_temperature(["Pune,31", "Delhi,40", "Pune,35"]))
