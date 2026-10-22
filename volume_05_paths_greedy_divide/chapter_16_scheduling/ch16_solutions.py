"""Volume 5, Chapter 16 - Thinking Problems.

Problem 1: the room-reuse rule uses exactly as many rooms as the largest number of overlapping requests (checked).
Problem 2: the fewest check-in times so that every booking is in progress at one of them: greedy by end time.
Problem 3: 'shortest request first' can keep fewer requests than earliest finish.
"""

from __future__ import annotations

import itertools

from ch16_examples import by_rule, earliest_finish, max_overlap, most_by_brute_force, rooms_needed


def stab_points(requests: list) -> list:
    """Times t such that every request (name, start, end) has start <= t < end at some t; fewest possible."""
    points = []
    for _, s, e in sorted(requests, key=lambda r: r[2]):
        if not points or points[-1] < s:
            points.append(e - 1)                    # the latest moment still inside this request (whole hours)
    return points


def fewest_points_brute(requests: list) -> int:
    times = sorted({t for _, s, e in requests for t in range(s, e)})
    for k in range(len(times) + 1):
        for pts in itertools.combinations(times, k):
            if all(any(s <= t < e for t in pts) for _, s, e in requests):
                return k
    return 0


SHORT_TRAP = [("A", 1, 5), ("B", 4, 7), ("C", 6, 10)]


if __name__ == "__main__":
    from ch16_examples import REQUESTS
    print(rooms_needed(REQUESTS)[0], max_overlap(REQUESTS), stab_points(REQUESTS))
    print(len(by_rule(SHORT_TRAP, lambda r: r[2] - r[1])), len(earliest_finish(SHORT_TRAP)))
