"""Volume 13, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

from ch07_examples import AhoCorasick, Trie


def longest_common_prefix(words: list[str]) -> str:
    """Exercise 1 (LeetCode 14): walk down the trie while there is exactly one child and no word ends."""
    if not words:
        return ""
    t = Trie()
    for w in words:
        t.add(w)
    node, out = 0, []
    while len(t.children[node]) == 1 and not t.words[node]:
        ch, nxt = next(iter(t.children[node].items()))
        out.append(ch)
        node = nxt
    return "".join(out)


def count_each_pattern(text: str, patterns: list[str]) -> dict[str, int]:
    """Exercise 2: how often each keyword appears (e.g. gene markers in a genome)."""
    counts = {p: 0 for p in patterns}
    for _, p in AhoCorasick(patterns).search(text):
        counts[p] += 1
    return counts


def replace_with_roots(sentence: str, roots: list[str]) -> str:
    """Exercise 3 (LeetCode 648): replace each word by the SHORTEST dictionary root that starts it."""
    t = Trie()
    for r in roots:
        t.add(r)
    out = []
    for word in sentence.split():
        node, replacement = 0, word
        for i, ch in enumerate(word):
            if ch not in t.children[node]:
                break
            node = t.children[node][ch]
            if t.words[node]:
                replacement = word[:i + 1]
                break
        out.append(replacement)
    return " ".join(out)


if __name__ == "__main__":
    print(longest_common_prefix(["flower", "flow", "flight"]), count_each_pattern("ACGTACGTAC", ["ACG", "GTA", "TT"]),
          replace_with_roots("the cattle was rattled by the battery", ["cat", "bat", "rat"]))
