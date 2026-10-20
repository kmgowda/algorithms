"""Volume 1, Chapter 16 - Analysing Recursive Algorithms.

Run:  python3 ch16_examples.py
"""

from __future__ import annotations


def unroll(recurrence: str, n: int) -> int:
    """Evaluate one of Section 16.8's recurrences exactly (with T(1) = 1 and whole-number halving)."""
    if n <= 1:
        return 1
    rules = {"T(n-1)+1": lambda: unroll(recurrence, n - 1) + 1,
             "T(n/2)+1": lambda: unroll(recurrence, n // 2) + 1,
             "T(n/2)+n": lambda: unroll(recurrence, n // 2) + n,
             "2T(n/2)+n": lambda: 2 * unroll(recurrence, n // 2) + n,
             "2T(n-1)+1": lambda: 2 * unroll(recurrence, n - 1) + 1}
    return rules[recurrence]()


def master(a: int, b: int, d: int) -> str:
    """The master theorem's verdict for T(n) = a T(n/b) + n^d (Figure 16.4)."""
    if a < b ** d:
        return f"O(n^{d})"
    if a == b ** d:
        return f"O(n^{d} log n)"
    return f"O(n^log_{b}({a}))"


if __name__ == "__main__":
    print("T(n-1)+1", unroll("T(n-1)+1", 300))
    for r in ("T(n/2)+1", "T(n/2)+n", "2T(n/2)+n"):
        print(r, unroll(r, 512))
    print("2T(n-1)+1", unroll("2T(n-1)+1", 10))
    print(master(1, 2, 1), master(2, 2, 1), master(4, 2, 1), master(3, 3, 1))
