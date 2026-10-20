"""Volume 1, Chapter 8 - Big O, Big Omega, and Big Theta.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations


def holds_from(f, g, c: float, n0: int, upto: int = 10_000) -> bool:
    """Check f(n) <= c * g(n) for every n from n0 to upto: evidence (not proof) that f is O(g)."""
    return all(f(n) <= c * g(n) for n in range(n0, upto + 1))


def first_n0(f, g, c: float, upto: int = 10_000) -> int | None:
    """The smallest n0 from which f(n) <= c * g(n) holds up to `upto` (the crossing in Figure 8.1)."""
    for n0 in range(1, upto + 1):
        if holds_from(f, g, c, n0, min(upto, n0 + 2000)):
            return n0
    return None


def dominant_share(n: int) -> float:
    """Share of 3n^2 + 5n + 20 that comes from the 3n^2 term (Figure 8.3)."""
    return 3 * n * n / (3 * n * n + 5 * n + 20)


if __name__ == "__main__":
    print(first_n0(lambda n: 3 * n + 10, lambda n: n, 4))
    print(holds_from(lambda n: n * (n - 1) / 2, lambda n: n * n, 0.5, 1),
          holds_from(lambda n: n * n / 4, lambda n: n * (n - 1) / 2, 1, 2))
    print([round(dominant_share(n), 4) for n in (1, 10, 1000)])
