"""Volume 6, Chapter 32 - Repeats and the LCP Array: what neighbouring suffixes share.

Run:  python3 ch32_examples.py
"""

from __future__ import annotations


def suffix_array(text: str) -> list:
    return sorted(range(len(text)), key=lambda i: text[i:])


def lcp_kasai(text: str, sa: list) -> list:
    """lcp[r] = letters shared by the suffixes in rows r-1 and r of the array (lcp[0] = 0) (Figure 32.1).
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


def kasai_trace(text: str, sa: list) -> list:
    """Kasai's method step by step (Section 32.4): for each i in text order, (i, the suffix just above it, h it
    started from, h found)."""
    n = len(text)
    rank = [0] * n
    for r, i in enumerate(sa):
        rank[i] = r
    h, out = 0, []
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            start = h
            while i + h < n and j + h < n and text[i + h] == text[j + h]:
                h += 1
            out.append((i, j, start, h))
            if h:
                h -= 1
        else:
            h = 0
    return out


class LCPQuery:
    """The longest common prefix of ANY two suffixes (Section 32.5): it is the smallest LCP value between their rows
    of the suffix array, answered in one step with a sparse table of minimums (Volume 3)."""

    def __init__(self, text: str):
        self.sa = suffix_array(text)
        self.lcp = lcp_kasai(text, self.sa)
        self.rank = {i: r for r, i in enumerate(self.sa)}
        self.n = len(text)
        self.table = [list(self.lcp)]                  # table[k][r] = min of lcp[r .. r + 2^k - 1]
        k = 1
        while (1 << k) <= len(self.lcp):
            prev = self.table[-1]
            half = 1 << (k - 1)
            self.table.append([min(prev[r], prev[r + half]) for r in range(len(self.lcp) - (1 << k) + 1)])
            k += 1

    def query(self, i: int, j: int) -> int:
        if i == j:
            return self.n - i
        a, b = sorted((self.rank[i], self.rank[j]))
        lo, hi = a + 1, b                              # the minimum of lcp[a + 1 .. b]
        k = (hi - lo + 1).bit_length() - 1
        return min(self.table[k][lo], self.table[k][hi - (1 << k) + 1])


def longest_repeat(text: str) -> str:
    """The longest substring occurring at least twice: the largest LCP value (Figure 32.2)."""
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


def suffix_automaton(text: str) -> tuple:
    """Section 32.6: the smallest machine accepting every substring of text (Blumer et al., 1985).

    Returns (next, link, length): per state, its letter moves, its suffix link, and its longest string's length.
    """
    nxt, link, length = [{}], [-1], [0]
    last = 0
    for ch in text:
        cur = len(nxt)
        nxt.append({}); link.append(0); length.append(length[last] + 1)
        p = last
        while p != -1 and ch not in nxt[p]:
            nxt[p][ch] = cur
            p = link[p]
        if p != -1:
            q = nxt[p][ch]
            if length[p] + 1 == length[q]:
                link[cur] = q
            else:
                clone = len(nxt)
                nxt.append(dict(nxt[q])); link.append(link[q]); length.append(length[p] + 1)
                while p != -1 and nxt[p].get(ch) == q:
                    nxt[p][ch] = clone
                    p = link[p]
                link[q] = link[cur] = clone
        last = cur
    return nxt, link, length


def automaton_distinct(text: str) -> int:
    """Different non-empty substrings: each state adds length - length of its suffix link."""
    _, link, length = suffix_automaton(text)
    return sum(length[s] - length[link[s]] for s in range(1, len(length)))


def automaton_longest_common(a: str, b: str) -> str:
    """Longest passage of b that occurs in a: walk b through a's automaton, falling back by suffix links."""
    nxt, link, length = suffix_automaton(a)
    state = run = best = end = 0
    for i, ch in enumerate(b):
        while state and ch not in nxt[state]:
            state = link[state]
            run = length[state]
        if ch in nxt[state]:
            state, run = nxt[state][ch], run + 1
        if run > best:
            best, end = run, i + 1
    return b[end - best:end]


def suffix_tree(text: str) -> dict:
    """A compressed trie of every suffix of text + "$" (built naively, O(n^2)). A node is a dict from the first
    letter of each edge to (edge label, child node); a leaf is an empty dict."""
    root = {}
    t = text + "$"
    for i in range(len(t)):
        node, rest = root, t[i:]
        while True:
            if rest[0] not in node:
                node[rest[0]] = (rest, {})
                break
            label, child = node[rest[0]]
            k = 0
            while k < len(label) and k < len(rest) and label[k] == rest[k]:
                k += 1
            if k == len(label):
                node, rest = child, rest[k:]
                continue
            middle = {label[k]: (label[k:], child)}       # split the edge where the suffix leaves it
            node[rest[0]] = (label[:k], middle)
            middle[rest[k]] = (rest[k:], {})
            break
    return root


def tree_stats(node: dict) -> tuple[int, int, int]:
    """(leaves, inner nodes below the root, total letters on edges not counting the final $)."""
    leaves = inner = letters = 0
    for label, child in node.values():
        letters += len(label.rstrip("$"))
        if child:
            inner += 1
            a, b, c = tree_stats(child)
            leaves, inner, letters = leaves + a, inner + b, letters + c
        else:
            leaves += 1
    return leaves, inner, letters


def tree_contains(node: dict, pattern: str) -> bool:
    """Is pattern a substring? Walk down from the root along matching edges: O(len(pattern))."""
    while pattern:
        if pattern[0] not in node:
            return False
        label, child = node[pattern[0]]
        k = min(len(label), len(pattern))
        if label[:k] != pattern[:k]:
            return False
        node, pattern = child, pattern[k:]
    return True


if __name__ == "__main__":
    sa = suffix_array("banana")
    print(sa, lcp_kasai("banana", sa), longest_repeat("banana"), distinct_substrings("banana"))
    print(longest_repeat("the club reads; the club meets"), longest_common("reading club", "the club meets"))
    print(longest_repeat("abcdefg"), longest_repeat("aaaa"), distinct_substrings("aaaa"), longest_repeat(""), longest_common("abc", "xyz"))
    print(tree_stats(suffix_tree("banana")), tree_contains(suffix_tree("banana"), "nan"))
