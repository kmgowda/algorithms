"""Volume 13, Chapter 9 - Palindromes: Manacher's Algorithm.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

import timeit


def expand_around_centers(s: str) -> str:
    """O(n^2): try each of the 2n - 1 centres and grow outward while the ends match."""
    best = ""
    for c in range(2 * len(s) - 1):
        lo, hi = c // 2, (c + 1) // 2
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
            lo, hi = lo - 1, hi + 1
        if hi - lo - 1 > len(best):
            best = s[lo + 1:hi]
    return best


def manacher_radii(s: str) -> list[int]:
    """Insert '#' between letters so every palindrome has odd length. radius[i] = how far the palindrome
    centred at i reaches in the padded string (which equals its length in the original). O(n): inside the
    rightmost palindrome found so far, a mirror position gives a free starting radius."""
    t = "#" + "#".join(s) + "#"
    n = len(t)
    radius = [0] * n
    center = right = 0
    for i in range(n):
        if i < right:
            radius[i] = min(right - i, radius[2 * center - i])     # mirror inside the known palindrome
        while i - radius[i] - 1 >= 0 and i + radius[i] + 1 < n and t[i - radius[i] - 1] == t[i + radius[i] + 1]:
            radius[i] += 1
        if i + radius[i] > right:
            center, right = i, i + radius[i]
    return radius


def longest_palindrome(s: str) -> str:
    """LeetCode 5 in linear time."""
    if not s:
        return ""
    radius = manacher_radii(s)
    i = max(range(len(radius)), key=lambda k: radius[k])
    start = (i - radius[i]) // 2
    return s[start:start + radius[i]]


def count_palindromes(s: str) -> int:
    """LeetCode 647 in linear time: a centre with radius r contributes ceil(r / 2) palindromic substrings."""
    return sum((r + 1) // 2 for r in manacher_radii(s))


def race(s: str) -> dict[str, float]:
    return {"expand around centres": min(timeit.repeat(lambda: expand_around_centers(s), number=1, repeat=3)),
            "Manacher": min(timeit.repeat(lambda: longest_palindrome(s), number=1, repeat=3))}


def palindromic_sites(dna: str, min_len: int) -> list[str]:
    """Industry example: DNA 'palindromes' read the same as their reverse complement (restriction enzyme sites
    like GAATTC). Checked directly here; Manacher's idea works too if 'equal' means 'complementary'."""
    comp = str.maketrans("ACGT", "TGCA")
    out = set()
    for i in range(len(dna)):
        for j in range(i + min_len, len(dna) + 1, 2):
            piece = dna[i:j]
            if (j - i) % 2 == 0 and piece == piece.translate(comp)[::-1]:
                out.add(piece)
    return sorted(out)


if __name__ == "__main__":
    print(manacher_radii("abaaba"), longest_palindrome("forgeeksskeegfor"), count_palindromes("aaa"))
    s = "a" * 3000
    print({k: f"{v * 1000:.1f} ms" for k, v in race(s).items()})
    print(palindromic_sites("TTGAATTCAAGGATCC", 6))
