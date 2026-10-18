"""Volume 7, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

from ch09_examples import SkipList


def average_search_steps(n: int, seed: int = 0) -> float:
    """Exercise 1: average horizontal steps per search - grows like log2 n, not n."""
    sl = SkipList(seed)
    for k in range(n):
        sl.insert(k)
    sl.steps = 0
    for k in range(n):
        sl.get(k)
    return sl.steps / n


def expected_pointers(n: int) -> float:
    """Exercise 2: each node has 1 + 1/2 + 1/4 + ... ~ 2 forward pointers on average."""
    return 2.0 * n


def floor_key(sl: SkipList, key):
    """Exercise 3: the largest key <= key, using the predecessor search."""
    pred = sl._find_predecessors(key)[0]
    nxt = pred.next[0]
    if nxt is not None and nxt.key == key:
        return key
    return pred.key


if __name__ == "__main__":
    print(round(average_search_steps(1000), 1), round(average_search_steps(16000), 1), expected_pointers(100))
    sl = SkipList(3)
    for k in (10, 20, 30):
        sl.insert(k)
    print(floor_key(sl, 25), floor_key(sl, 30), floor_key(sl, 5))
