"""Volume 2, Chapter 20 - Sliding Window.

Run:  python3 ch20_examples.py
"""

from __future__ import annotations

VISITS = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]


def window_totals(counts: list[int], k: int) -> list[int]:
    """Total of every k-length stretch: add the newcomer, subtract the leaver (Figure 20.1)."""
    if k > len(counts):
        return []
    total = sum(counts[:k])
    out = [total]
    for i in range(k, len(counts)):
        total += counts[i] - counts[i - k]
        out.append(total)
    return out


def shortest_stretch(counts: list[int], target: int) -> int:
    """Length of the shortest run of neighbouring days summing to at least target (0 if none) (Figure 20.2).
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
    """(length, start) of the longest run with no repeated character (Figure 20.3)."""
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
    """Section 20.8: (length, start) of the longest stretch whose total stays at most limit (non-negative values)."""
    left, total, best = 0, 0, (0, 0)
    for right, x in enumerate(noise):
        total += x
        while total > limit:
            total -= noise[left]
            left += 1
        if right - left + 1 > best[0]:
            best = (right - left + 1, left)
    return best


def count_at_most(log: str, k: int) -> int:
    """How many stretches hold at most k different readers (Section 20.7).

    For each right edge, shrink until the window is legal; every start from left to right then gives a legal
    stretch ending here, so the window adds right - left + 1."""
    seen: dict[str, int] = {}
    left = total = 0
    for right, r in enumerate(log):
        seen[r] = seen.get(r, 0) + 1
        while len(seen) > k:
            seen[log[left]] -= 1
            if seen[log[left]] == 0:
                del seen[log[left]]
            left += 1
        total += right - left + 1
    return total


def count_exactly(log: str, k: int) -> int:
    """Stretches with exactly k different readers: at most k, minus at most k - 1 (Section 20.7)."""
    if k <= 0:
        return 0
    return count_at_most(log, k) - count_at_most(log, k - 1)


if __name__ == "__main__":
    print(window_totals(VISITS, 3), window_totals(VISITS, 4))
    print(shortest_stretch(VISITS, 15), shortest_stretch(VISITS, 20))
    n, s = longest_without_repeats("ABCBDAEFB")
    print(n, "ABCBDAEFB"[s:s + n], longest_without_repeats("LIBRARIAN"))
    noise = [2, 4, 1, 0, 3, 7, 1, 1, 2, 5]
    print(longest_quiet(noise, 12), longest_quiet(noise, 6))
