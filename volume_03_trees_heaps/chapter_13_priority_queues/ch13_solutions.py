"""Volume 3, Chapter 13 - Priority Queues: companion code for the Thinking Problems (Section 13.16).

Run:  python3 ch13_solutions.py
"""

from __future__ import annotations

from collections import deque


def aged_key(pages: int, arrival: int, rate: int = 10) -> int:
    """Thinking Problem 1: with ageing, a job's priority at minute t is pages - rate * (t - arrival).
    Every waiting job loses rate * t alike, so pages + rate * arrival orders them for ever."""
    return pages + rate * arrival


def aged_order(jobs, now: int, rate: int = 10) -> list:
    """The order the waiting jobs (name, pages, arrival) would be served at minute `now`, re-keying every job."""
    return [name for name, p, a in sorted(jobs, key=lambda j: (j[1] - rate * (now - j[2]), j[2]))]


class BucketPQ:
    """Thinking Problem 2: priorities 1..levels, one first-in-first-out line per level.
    insert is O(1); extract_min scans at most `levels` lines, O(levels); ties are served in arrival order."""

    def __init__(self, levels: int):
        self.lines = [deque() for _ in range(levels + 1)]   # line 0 is unused
        self.count = 0

    def insert(self, priority: int, item) -> None:
        self.lines[priority].append(item)
        self.count += 1

    def extract_min(self):
        for p in range(1, len(self.lines)):
            if self.lines[p]:
                self.count -= 1
                return p, self.lines[p].popleft()
        raise IndexError("extract from an empty priority queue")

    def __len__(self) -> int:
        return self.count


def key_only_heap_order(jobs: list[tuple[int, str]]) -> list[str]:
    """Thinking Problem 3: a binary heap (Chapter 14) that compares priorities only, never arrival tickets.
    Sifting uses a strict <, yet equal priorities still come out of arrival order."""
    a: list = []
    for job in jobs:                               # push: add at the end, sift up while strictly smaller
        a.append(job)
        i = len(a) - 1
        while i > 0 and a[i][0] < a[(i - 1) // 2][0]:
            a[i], a[(i - 1) // 2] = a[(i - 1) // 2], a[i]
            i = (i - 1) // 2
    out = []
    while a:                                       # pop: move the last item to the root, sift down
        out.append(a[0][1])
        last = a.pop()
        if a:
            a[0], i = last, 0
            while True:
                small = i
                for c in (2 * i + 1, 2 * i + 2):
                    if c < len(a) and a[c][0] < a[small][0]:
                        small = c
                if small == i:
                    break
                a[i], a[small] = a[small], a[i]
                i = small
    return out


if __name__ == "__main__":
    print(aged_key(300, 0), aged_key(50, 25), aged_order([("thesis", 300, 0), ("leaflet", 50, 20)], 30))
    q = BucketPQ(3)
    for name, p in (("Ana", 3), ("Ben", 1), ("Cai", 2), ("Dev", 3)):
        q.insert(p, name)
    print([q.extract_min() for _ in range(4)])
    print(key_only_heap_order([(3, "Ana"), (3, "Dev"), (3, "Eva")]))
