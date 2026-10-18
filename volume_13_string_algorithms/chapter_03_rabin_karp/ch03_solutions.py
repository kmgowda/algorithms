"""Volume 13, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations

from ch03_examples import BASE, MOD, poly_hash, rabin_karp


def longest_duplicate_substring(s: str) -> str:
    """Exercise 1 (LeetCode 1044): the longest substring appearing twice. Binary search the length; for each
    length, rolling hashes find a repeated window in O(n)."""
    def repeat_of_length(k: int) -> str | None:
        if k == 0:
            return ""
        high = pow(BASE, k - 1, MOD)
        h = poly_hash(s[:k])
        seen: dict[int, list[int]] = {h: [0]}
        for i in range(1, len(s) - k + 1):
            h = ((h - ord(s[i - 1]) * high) * BASE + ord(s[i + k - 1])) % MOD
            for j in seen.get(h, []):
                if s[j:j + k] == s[i:i + k]:
                    return s[i:i + k]
            seen.setdefault(h, []).append(i)
        return None

    lo, hi, best = 1, len(s) - 1, ""
    while lo <= hi:
        mid = (lo + hi) // 2
        found = repeat_of_length(mid)
        if found is not None:
            best, lo = found, mid + 1
        else:
            hi = mid - 1
    return best


def count_distinct_windows(s: str, k: int) -> int:
    """Exercise 2: how many different k-letter substrings (DNA k-mers) appear - store window hashes in a set."""
    if k > len(s):
        return 0
    high = pow(BASE, k - 1, MOD)
    h = poly_hash(s[:k])
    windows = {(h, s[:k])}
    for i in range(1, len(s) - k + 1):
        h = ((h - ord(s[i - 1]) * high) * BASE + ord(s[i + k - 1])) % MOD
        windows.add((h, s[i:i + k]))
    return len(windows)


def is_rotation(a: str, b: str) -> bool:
    """Exercise 3 (LeetCode 796): b is a rotation of a exactly when b occurs inside a + a."""
    return len(a) == len(b) and bool(rabin_karp(a + a, b)[0])


if __name__ == "__main__":
    print(longest_duplicate_substring("banana"), count_distinct_windows("ACGTACGTAC", 3), is_rotation("waterbottle", "erbottlewat"))
