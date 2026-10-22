"""Volume 4, Chapter 18 - Thinking Problems: model solutions.

Thinking Problem 1: a sorting network needs depth at least ceil(log2 n); influence_sets checks the counting step.
Thinking Problem 2: sorting a list in which every item is at most k places from its sorted place, in O(n log k).
Thinking Problem 3: odd-even transposition with too few layers, and the 0-1 input that exposes it.

Run:  python3 ch18_solutions.py
"""

from __future__ import annotations

import heapq
import itertools

import ch18_examples as ex


def influence_sets(network: list[tuple[int, int]], n: int) -> list[set[int]]:
    """For every wire, the input wires whose values can reach it after the whole network (Thinking Problem 15.1)."""
    reach = [{w} for w in range(n)]
    for layer in ex.stages(network):
        for i, j in layer:
            reach[i] = reach[j] = reach[i] | reach[j]
    return reach


def sort_k_sorted(a: list, k: int) -> list:
    """Sort a list in which every item is at most k places from its place in sorted order: keep a min-heap of the
    next k + 1 items; the smallest of them belongs next (Thinking Problem 15.2). O(n log k) time, O(k) memory."""
    heap, out = [], []
    for x in a:
        heapq.heappush(heap, x)
        if len(heap) > k:
            out.append(heapq.heappop(heap))
    while heap:
        out.append(heapq.heappop(heap))
    return out


def odd_even_transposition(n: int, layers: int) -> list[tuple[int, int]]:
    """Layers alternate between comparing (0,1), (2,3), ... and (1,2), (3,4), ... (bubble sort in parallel)."""
    return [(i, i + 1) for t in range(layers) for i in range(t % 2, n - 1, 2)]


def first_01_failure(network: list[tuple[int, int]], n: int):
    """The first 0-1 input (in counting order) that the network fails to sort, or None if it sorts them all."""
    for bits in itertools.product((0, 1), repeat=n):
        if ex.apply_network(network, bits) != sorted(bits):
            return list(bits)
    return None


if __name__ == "__main__":
    print(sort_k_sorted([25, 12, 58, 31, 47, 70, 63, 91, 84], 2))
    for layers in (4, 7, 8):
        net = odd_even_transposition(8, layers)
        print(layers, len(net), first_01_failure(net, 8))
    print(max(len(s) for s in influence_sets(ex.sorting_network(8), 8)))
