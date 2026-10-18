"""Volume 3, Chapter 9 - Queues: First In, First Out.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Any


class _Node:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.next: _Node | None = None


class LinkedQueue:
    """Enqueue at the tail, dequeue at the head: every operation is worst-case O(1)."""

    def __init__(self) -> None:
        self._head: _Node | None = None
        self._tail: _Node | None = None
        self._size = 0

    def enqueue(self, item: Any) -> None:
        node = _Node(item)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self) -> Any:
        if self._head is None:
            raise IndexError("dequeue from empty queue")
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return node.value

    def peek(self) -> Any:
        if self._head is None:
            raise IndexError("peek at empty queue")
        return self._head.value

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size


class TwoStackQueue:
    """A queue built from two stacks: amortized O(1) per operation (LeetCode 232)."""

    def __init__(self) -> None:
        self._inbox: list[Any] = []
        self._outbox: list[Any] = []

    def enqueue(self, item: Any) -> None:
        self._inbox.append(item)

    def dequeue(self) -> Any:
        if not self._outbox:
            while self._inbox:                 # pour the inbox over: reverses the order once
                self._outbox.append(self._inbox.pop())
        if not self._outbox:
            raise IndexError("dequeue from empty queue")
        return self._outbox.pop()

    def __len__(self) -> int:
        return len(self._inbox) + len(self._outbox)


def slow_list_queue_cost(n: int) -> int:
    """Why not list.pop(0)? Count the shifts it causes for n dequeues: n(n-1)/2."""
    return n * (n - 1) // 2


# ------------------------------------------------------------------ applications
def serve_ticket_line(arrivals: list[str]) -> list[str]:
    """Beginner example: first come, first served."""
    line = LinkedQueue()
    for person in arrivals:
        line.enqueue(person)
    return [line.dequeue() for _ in range(len(line))]


def print_jobs(jobs: list[tuple[str, int]], pages_per_minute: int) -> list[tuple[str, float]]:
    """Practical example: a shared printer finishes jobs in arrival order. Returns (job, finish minute)."""
    queue: deque[tuple[str, int]] = deque(jobs)
    clock = 0.0
    finished = []
    while queue:
        name, pages = queue.popleft()
        clock += pages / pages_per_minute
        finished.append((name, round(clock, 2)))
    return finished


def call_center(calls: list[tuple[int, str, int]], agents: int) -> dict[str, int]:
    """Industry example: callers wait in one queue; the next free agent takes the next caller.

    calls are (arrival_minute, caller, duration). Returns each caller's waiting time.
    """
    waiting: deque[tuple[int, str, int]] = deque(sorted(calls))
    free_at = [0] * agents                       # when each agent becomes free
    waits: dict[str, int] = {}
    while waiting:
        arrival, caller, duration = waiting.popleft()
        agent = min(range(agents), key=lambda a: free_at[a])
        start = max(arrival, free_at[agent])
        waits[caller] = start - arrival
        free_at[agent] = start + duration
    return waits


def rate_limiter(request_times: list[float], limit: int, window: float) -> list[bool]:
    """Industry example: allow at most `limit` requests in any `window` seconds (a sliding-log queue)."""
    recent: deque[float] = deque()
    decisions = []
    for t in request_times:
        while recent and recent[0] <= t - window:
            recent.popleft()                     # forget requests that left the window
        if len(recent) < limit:
            recent.append(t)
            decisions.append(True)
        else:
            decisions.append(False)
    return decisions


def bfs_levels(friends: dict[str, list[str]], start: str) -> dict[str, int]:
    """Preview of Volume 8: a queue explores a social network level by level (friends, then friends of friends)."""
    distance = {start: 0}
    queue: deque[str] = deque([start])
    while queue:
        person = queue.popleft()
        for friend in friends.get(person, []):
            if friend not in distance:
                distance[friend] = distance[person] + 1
                queue.append(friend)
    return distance


if __name__ == "__main__":
    print(serve_ticket_line(["Ana", "Ben", "Cy", "Dev"]))
    q = TwoStackQueue()
    for x in "abc":
        q.enqueue(x)
    print(q.dequeue(), q.dequeue(), len(q))
    print("Shifts for 100,000 list.pop(0) calls:", f"{slow_list_queue_cost(100_000):,}")
    print(print_jobs([("report", 12), ("photo", 3), ("poster", 6)], pages_per_minute=6))
    print(call_center([(0, "A", 5), (1, "B", 3), (2, "C", 4), (3, "D", 2)], agents=2))
    print(rate_limiter([0, 0.2, 0.4, 0.6, 1.1, 1.3], limit=3, window=1.0))
    network = {"Maya": ["Leo", "Zoe"], "Leo": ["Sam"], "Zoe": ["Sam", "Ali"], "Sam": ["Kim"]}
    print(bfs_levels(network, "Maya"))
