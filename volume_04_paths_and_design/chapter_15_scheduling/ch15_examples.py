"""Volume 4, Chapter 15 - Scheduling and Intervals: earliest finish first, and counting rooms.

Run:  python3 ch15_examples.py
"""

from __future__ import annotations

import heapq
import itertools

# Requests for the library's one meeting room: (group, start hour, end hour).
REQUESTS = [("Chess", 9, 11), ("Poetry", 10, 12), ("Knitting", 11, 13), ("Coding", 9, 15), ("Maps", 12, 14),
            ("Choir", 13, 16), ("Writers", 14, 15), ("Film", 15, 17)]


def by_rule(requests: list, key) -> list:
    """Greedy: take requests in the order given by key, keeping each that does not clash with those kept."""
    kept = []
    for r in sorted(requests, key=key):
        if all(r[2] <= k[1] or r[1] >= k[2] for k in kept):
            kept.append(r)
    return sorted(kept, key=lambda r: r[1])


def earliest_finish(requests: list) -> list:
    """The greedy rule that is always best (Figure 15.2): next, the request that ends soonest."""
    kept, free_at = [], float("-inf")
    for r in sorted(requests, key=lambda r: r[2]):
        if r[1] >= free_at:
            kept.append(r)
            free_at = r[2]
    return kept


def most_by_brute_force(requests: list) -> int:
    best = 0
    for k in range(len(requests) + 1):
        for combo in itertools.combinations(requests, k):
            s = sorted(combo, key=lambda r: r[1])
            if all(a[2] <= b[1] for a, b in zip(s, s[1:])):
                best = max(best, k)
    return best


def rooms_needed(requests: list) -> tuple[int, dict]:
    """Give every request a room, reusing a room as soon as it is free (Figure 15.4). Returns (rooms, room of each)."""
    free, room_of, busy = [], {}, []                     # busy: (end, room)
    count = 0
    for name, s, e in sorted(requests, key=lambda r: r[1]):
        while busy and busy[0][0] <= s:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            count += 1
            room = count
        room_of[name] = room
        heapq.heappush(busy, (e, room))
    return count, room_of


def max_overlap(requests: list) -> int:
    events = sorted([(s, 1) for _, s, _ in requests] + [(e, -1) for _, _, e in requests])
    now = best = 0
    for _, d in events:
        now += d
        best = max(best, now)
    return best


if __name__ == "__main__":
    print(earliest_finish(REQUESTS), most_by_brute_force(REQUESTS))
    print(len(by_rule(REQUESTS, lambda r: r[1])), len(by_rule(REQUESTS, lambda r: r[2] - r[1])))
    print(rooms_needed(REQUESTS), max_overlap(REQUESTS))
