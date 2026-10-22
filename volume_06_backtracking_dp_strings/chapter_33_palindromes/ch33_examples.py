"""Volume 6, Chapter 33 - Palindromes and Manacher: the longest stretch that reads the same both ways.

Run:  python3 ch33_examples.py
"""

from __future__ import annotations


def expand_around_centres(s: str) -> tuple[str, int]:
    """Try every centre (a letter or a gap) and grow outwards while the ends match (Figure 33.2).
    Returns (longest palindrome, letter comparisons)."""
    best, comparisons = "", 0
    for c in range(2 * len(s) - 1):
        lo, hi = c // 2, (c + 1) // 2
        while lo >= 0 and hi < len(s):
            comparisons += 1
            if s[lo] != s[hi]:
                break
            lo, hi = lo - 1, hi + 1
        if hi - lo - 1 > len(best):
            best = s[lo + 1:hi]
    return best, comparisons


def manacher(s: str) -> tuple[str, list, int]:
    """Radii of palindromes around every centre of s with '#' between letters, reusing the mirror inside the
    rightmost palindrome found (Figure 33.3). Returns (longest palindrome, radii, comparisons)."""
    t = "#" + "#".join(s) + "#" if s else "#"
    n = len(t)
    radius = [0] * n
    centre = right = 0
    comparisons = 0
    for i in range(n):
        if i < right:
            radius[i] = min(right - i, radius[2 * centre - i])     # copy from the mirror position
        while i - radius[i] - 1 >= 0 and i + radius[i] + 1 < n:
            comparisons += 1
            if t[i - radius[i] - 1] != t[i + radius[i] + 1]:
                break
            radius[i] += 1
        if i + radius[i] > right:
            centre, right = i, i + radius[i]
    k = max(range(n), key=lambda j: radius[j])
    start = (k - radius[k]) // 2
    return s[start:start + radius[k]], radius, comparisons


def manacher_trace(s: str) -> list:
    """Manacher's method step by step (Section 33.5): for each position i of the #-string, (i, symbol, how the
    radius started: "outside", "copied" (final, strictly inside) or "copied to the edge", comparisons, radius)."""
    t = "#" + "#".join(s) + "#" if s else "#"
    n = len(t)
    radius, centre, right, out = [0] * n, 0, 0, []
    for i in range(n):
        how = "outside"
        if i < right:
            radius[i] = min(right - i, radius[2 * centre - i])
            how = "copied to the edge" if radius[i] == right - i else "copied"
        compared = 0
        if how != "copied":                            # a mirror strictly inside the big palindrome is final
            while i - radius[i] - 1 >= 0 and i + radius[i] + 1 < n:
                compared += 1
                if t[i - radius[i] - 1] != t[i + radius[i] + 1]:
                    break
                radius[i] += 1
        if i + radius[i] > right:
            centre, right = i, i + radius[i]
        out.append((i, t[i], how, compared, radius[i]))
    return out


def count_palindromes(s: str) -> int:
    """Palindromic substrings counted with repeats (Challenge 1): each centre of the #-string with radius r holds
    (r + 1) // 2 of them."""
    if not s:
        return 0
    return sum((r + 1) // 2 for r in manacher(s)[1])


if __name__ == "__main__":
    for w in ("level", "abacabad", "noon", "racecar drive"):
        print(w, expand_around_centres(w), manacher(w)[::2])
    print(expand_around_centres("a" * 1000)[1], manacher("a" * 1000)[2])
