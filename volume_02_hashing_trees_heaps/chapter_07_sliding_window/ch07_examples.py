"""Volume 2, Chapter 7 - Sliding Window.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

VISITS = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]


def window_totals(counts: list[int], k: int) -> list[int]:
    """Total of every k-length stretch: add the newcomer, subtract the leaver (Figure 7.1)."""
    if k > len(counts):
        return []
    total = sum(counts[:k])
    out = [total]
    for i in range(k, len(counts)):
        total += counts[i] - counts[i - k]
        out.append(total)
    return out


def shortest_stretch(counts: list[int], target: int) -> int:
    """Length of the shortest run of neighbouring days summing to at least target (0 if none) (Figure 7.2).
    Counts must not be negative."""
    left, total, best = 0, 0, 0
    for right, c in enumerate(counts):
        total += c                                  # grow on the right
        while left < right and total - counts[left] >= target:   # shrink while still big enough
            total -= counts[left]
            left += 1
        if total >= target and (best == 0 or right - left + 1 < best):
            best = right - left + 1
    return best


def longest_without_repeats(log: str) -> tuple[int, int]:
    """(length, start) of the longest run with no repeated character (Figure 7.3)."""
    last: dict[str, int] = {}
    left, best = 0, (0, 0)
    for right, ch in enumerate(log):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        if right - left + 1 > best[0]:
            best = (right - left + 1, left)
    return best


def longest_quiet(noise: list[int], limit: int) -> tuple[int, int]:
    """Section 7.8: (length, start) of the longest stretch whose total stays at most limit (non-negative values)."""
    left, total, best = 0, 0, (0, 0)
    for right, x in enumerate(noise):
        total += x
        while total > limit:
            total -= noise[left]
            left += 1
        if right - left + 1 > best[0]:
            best = (right - left + 1, left)
    return best


if __name__ == "__main__":
    print(window_totals(VISITS, 3), window_totals(VISITS, 4))
    print(shortest_stretch(VISITS, 15), shortest_stretch(VISITS, 20))
    n, s = longest_without_repeats("ABCBDAEFB")
    print(n, "ABCBDAEFB"[s:s + n], longest_without_repeats("LIBRARIAN"))
    noise = [2, 4, 1, 0, 3, 7, 1, 1, 2, 5]
    print(longest_quiet(noise, 12), longest_quiet(noise, 6))
