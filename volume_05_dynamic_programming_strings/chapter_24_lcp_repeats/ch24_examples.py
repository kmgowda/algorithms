"""Volume 5, Chapter 24 - Repeats and the LCP Array: what neighbouring suffixes share.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations


def suffix_array(text: str) -> list:
    return sorted(range(len(text)), key=lambda i: text[i:])


def lcp_kasai(text: str, sa: list) -> list:
    """lcp[r] = letters shared by the suffixes in rows r-1 and r of the array (lcp[0] = 0) (Figure 24.1).
    Kasai's method: walk the text in order; each next suffix shares at least one letter fewer than the last."""
    n = len(text)
    rank = [0] * n
    for r, i in enumerate(sa):
        rank[i] = r
    lcp, h = [0] * n, 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and text[i + h] == text[j + h]:
                h += 1
            lcp[rank[i]] = h
            if h:
                h -= 1
        else:
            h = 0
    return lcp


def longest_repeat(text: str) -> str:
    """The longest substring occurring at least twice: the largest LCP value (Figure 24.2)."""
    if len(text) < 2:
        return ""
    sa = suffix_array(text)
    lcp = lcp_kasai(text, sa)
    r = max(range(len(lcp)), key=lambda k: lcp[k])
    return text[sa[r]:sa[r] + lcp[r]]


def distinct_substrings(text: str) -> int:
    """Each suffix adds its length minus what it shares with the previous suffix in the array."""
    sa = suffix_array(text)
    lcp = lcp_kasai(text, sa)
    return sum(len(text) - i for i in sa) - sum(lcp)


def longest_common(a: str, b: str, sep: str = "\x01") -> str:
    """Longest substring shared by a and b: the largest LCP between neighbouring suffixes from different strings."""
    t = a + sep + b
    sa = suffix_array(t)
    lcp = lcp_kasai(t, sa)
    best, at = 0, 0
    for r in range(1, len(sa)):
        if (sa[r] < len(a)) != (sa[r - 1] < len(a)) and lcp[r] > best:
            best, at = lcp[r], sa[r]
    return t[at:at + best]


if __name__ == "__main__":
    sa = suffix_array("banana")
    print(sa, lcp_kasai("banana", sa), longest_repeat("banana"), distinct_substrings("banana"))
    print(longest_repeat("the club reads; the club meets"), longest_common("reading club", "the club meets"))
    print(longest_repeat("abcdefg"), longest_repeat("aaaa"), distinct_substrings("aaaa"), longest_repeat(""), longest_common("abc", "xyz"))
