"""Volume 3, Chapter 15 - Heap Techniques: companion code for the Thinking Problems (Section 15.16).

Run:  python3 ch15_solutions.py
"""

from __future__ import annotations

import heapq


def smallest_window(lists: list[list]):
    """Thinking Problem 2: the shortest window [lo, hi] holding at least one value from every sorted list,
    in O(n log k). A heap holds one value per list; the window runs from the heap's top to the largest
    value held. Returns None when there are no lists or one of them is empty."""
    if not lists or any(not lst for lst in lists):
        return None
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists)]
    heapq.heapify(heap)
    hi = max(lst[0] for lst in lists)
    best = (heap[0][0], hi)
    while True:
        lo, i, j = heapq.heappop(heap)
        if hi - lo < best[1] - best[0]:
            best = (lo, hi)
        if j + 1 == len(lists[i]):                # list i is used up: no window can drop lo
            return best
        nxt = lists[i][j + 1]
        hi = max(hi, nxt)
        heapq.heappush(heap, (nxt, i, j + 1))


def cumulative_bind_cost(sizes) -> int:
    """Thinking Problem 3: the flawed plan. Sort once, bind the two smallest, then keep adding the next
    smallest ORIGINAL bundle to the growing volume."""
    s = sorted(sizes)
    if len(s) < 2:
        return 0
    total, volume = 0, s[0]
    for x in s[1:]:
        volume += x
        total += volume
    return total


if __name__ == "__main__":
    print(smallest_window([[540, 555, 610], [548, 600, 640], [570, 605, 700]]))
    from ch15_examples import join_cost
    print(cumulative_bind_cost([1, 1, 1, 1]), join_cost([1, 1, 1, 1])[0])
