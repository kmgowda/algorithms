"""Volume 13, Chapter 7 - Tries Revisited and Aho-Corasick.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

from collections import deque


class Trie:
    """A trie (V6-C11) stored as parallel lists: children[node] maps a letter to a node index."""

    def __init__(self) -> None:
        self.children: list[dict[str, int]] = [{}]
        self.words: list[list[str]] = [[]]           # patterns ending exactly at each node

    def add(self, word: str) -> None:
        node = 0
        for ch in word:
            if ch not in self.children[node]:
                self.children[node][ch] = len(self.children)
                self.children.append({})
                self.words.append([])
            node = self.children[node][ch]
        self.words[node].append(word)

    def starts_with(self, prefix: str) -> list[str]:
        """All stored words beginning with prefix (autocomplete)."""
        node = 0
        for ch in prefix:
            if ch not in self.children[node]:
                return []
            node = self.children[node][ch]
        out, stack = [], [node]
        while stack:
            v = stack.pop()
            out += self.words[v]
            stack += self.children[v].values()
        return sorted(out)


class AhoCorasick:
    """Many patterns, one pass. A trie plus FAILURE links: fail[v] = the node for the longest proper suffix of v's
    string that is also in the trie (KMP's prefix function, generalised to a set of patterns)."""

    def __init__(self, patterns: list[str]) -> None:
        self.trie = Trie()
        for p in patterns:
            self.trie.add(p)
        n = len(self.trie.children)
        self.fail = [0] * n
        self.out = [list(w) for w in self.trie.words]
        queue = deque(self.trie.children[0].values())
        while queue:                                   # BFS: shorter strings get their links first
            v = queue.popleft()
            for ch, w in self.trie.children[v].items():
                f = self.fail[v]
                while f and ch not in self.trie.children[f]:
                    f = self.fail[f]
                self.fail[w] = self.trie.children[f].get(ch, 0) if self.trie.children[f].get(ch, 0) != w else 0
                self.out[w] += self.out[self.fail[w]]   # inherit matches ending here via suffixes
                queue.append(w)

    def search(self, text: str) -> list[tuple[int, str]]:
        """Every (start position, pattern) occurrence in O(n + total pattern length + number of matches)."""
        node, hits = 0, []
        for i, ch in enumerate(text):
            while node and ch not in self.trie.children[node]:
                node = self.fail[node]
            node = self.trie.children[node].get(ch, 0)
            for p in self.out[node]:
                hits.append((i - len(p) + 1, p))
        return sorted(hits)


def mask_banned_words(message: str, banned: list[str]) -> str:
    """Industry example: a chat filter replacing every banned word (even inside longer words) with stars."""
    hits = AhoCorasick([b.lower() for b in banned]).search(message.lower())
    chars = list(message)
    for start, word in hits:
        for k in range(start, start + len(word)):
            chars[k] = "*"
    return "".join(chars)


if __name__ == "__main__":
    t = Trie()
    for w in ["car", "card", "care", "cat", "dog"]:
        t.add(w)
    print("autocomplete 'car':", t.starts_with("car"))
    ac = AhoCorasick(["he", "she", "his", "hers"])
    print(ac.search("ushers"))
    print(mask_banned_words("That darn spam is SPAMMY", ["darn", "spam"]))
