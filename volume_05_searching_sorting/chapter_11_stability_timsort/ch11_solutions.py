"""Volume 5, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations


def stabilize(items: list, key) -> list:
    """Exercise 1: make ANY sort stable by sorting (key, original position) pairs."""
    decorated = [(key(x), i, x) for i, x in enumerate(items)]
    decorated.sort(key=lambda t: (t[0], t[1]))
    return [x for _, _, x in decorated]


def count_runs(items: list) -> int:
    """Exercise 2: how many ascending runs does a list have? Fewer runs = less work for Timsort."""
    if not items:
        return 0
    return 1 + sum(1 for a, b in zip(items, items[1:]) if b < a)


def sort_emails(emails: list[tuple[str, str, int]]) -> list[tuple[str, str, int]]:
    """Exercise 3: (sender, subject, day) - newest day first; within a day, sender A-Z. Two stable passes."""
    by_sender = sorted(emails, key=lambda e: e[0])
    return sorted(by_sender, key=lambda e: e[2], reverse=True)   # reverse=True is still stable in Python


if __name__ == "__main__":
    print(stabilize([("x", 2), ("y", 1), ("z", 2)], key=lambda p: p[1]), count_runs([1, 2, 5, 3, 4, 0]))
    print(sort_emails([("Zoe", "hi", 1), ("Ali", "re", 2), ("Ben", "ok", 2)]))
