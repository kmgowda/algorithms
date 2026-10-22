"""Volume 1, Chapter 20, Thinking Problem 2 - how soon can the volunteers shelve the returns pile?

Volunteer i shelves one book every minutes[i] minutes, all working at once. The fewest whole minutes after which
at least m books are back on the shelves is a first "yes": in T minutes they shelve sum(T // t) books, which never
decreases as T grows. The search costs O(w log(m * min(minutes))) for w volunteers.

Run:  python3 ch20_solutions.py
"""

from __future__ import annotations

from ch20_examples import first_true


def shelving_time(minutes: list[int], m: int) -> int:
    """Fewest whole minutes for volunteers with these minutes-per-book to shelve at least m books (m >= 0)."""
    return first_true(0, m * min(minutes), lambda t: sum(t // each for each in minutes) >= m)


if __name__ == "__main__":
    print(shelving_time([3, 5, 8], 20))
