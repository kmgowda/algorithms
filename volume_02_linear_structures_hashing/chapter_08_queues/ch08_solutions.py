"""Volume 2, Chapter 8 - Thinking Problems.

Problem 1: the finishing slot of every student in round robin, by a formula instead of a simulation.
Problem 2: the last reader in the parcel game in O(n) time and O(1) memory, without a queue.
Problem 3: the wrong two-stack queue that pours on every dequeue, kept here so the tests can show it.
"""

from __future__ import annotations

from collections import deque


def finish_slots(needs: dict[str, int]) -> dict[str, int]:
    """Student s finishes after everyone's first need[s] slots before it (and itself), and need[s] - 1 after."""
    order = list(needs)
    out = {}
    for i, s in enumerate(order):
        k = needs[s]
        out[s] = sum(min(needs[t], k) for t in order[:i + 1]) + sum(min(needs[t], k - 1) for t in order[i + 1:])
    return out


def last_reader(n: int, moves: int) -> int:
    survivor = 0                                # with one reader, position 0 is left
    for size in range(2, n + 1):
        survivor = (survivor + moves + 1) % size
    return survivor


def last_reader_by_queue(n: int, moves: int) -> int:
    q = deque(range(n))
    while len(q) > 1:
        q.rotate(-moves)                        # the parcel moves on: front readers go to the back
        q.popleft()                             # the reader now holding it leaves
    return q[0]


class PourAlwaysQueue:
    """WRONG: pours the in-stack onto the out-stack on every dequeue, even when out is not empty."""

    def __init__(self):
        self.inbox: list = []
        self.outbox: list = []

    def enqueue(self, x) -> None:
        self.inbox.append(x)

    def dequeue(self):
        while self.inbox:
            self.outbox.append(self.inbox.pop())
        return self.outbox.pop()


if __name__ == "__main__":
    print(finish_slots({"Ana": 3, "Ben": 1, "Cai": 2}), last_reader(5, 2), "ABCDE"[last_reader(5, 2)])
    q = PourAlwaysQueue()
    q.enqueue(1); q.enqueue(2); print(q.dequeue()); q.enqueue(3); print(q.dequeue())
