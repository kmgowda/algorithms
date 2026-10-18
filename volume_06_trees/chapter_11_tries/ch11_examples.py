"""Volume 6, Chapter 11 - Tries: The Autocomplete Tree.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False
        self.count = 0                       # how many inserted words pass through this node (prefix count)
        self.popularity = 0                  # for ranking suggestions


class Trie:
    """Each edge is one letter; a path from the root spells a prefix. Operations cost O(length of the word)."""

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str, popularity: int = 0) -> None:
        node = self.root
        node.count += 1
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
            node.count += 1
        node.is_word = True
        node.popularity = max(node.popularity, popularity)

    def _walk(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def contains(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def count_prefix(self, prefix: str) -> int:
        """How many stored words begin with prefix - read straight from the node, no searching."""
        node = self._walk(prefix)
        return 0 if node is None else node.count

    def words_with_prefix(self, prefix: str) -> list[str]:
        """Every stored word beginning with prefix, in alphabetical order (depth-first walk below the prefix)."""
        node = self._walk(prefix)
        out: list[str] = []

        def collect(n: TrieNode, path: str) -> None:
            if n.is_word:
                out.append(path)
            for ch in sorted(n.children):
                collect(n.children[ch], path + ch)

        if node is not None:
            collect(node, prefix)
        return out

    def suggest(self, prefix: str, k: int = 3) -> list[str]:
        """Industry example: autocomplete - the k most popular words starting with what the user has typed."""
        node = self._walk(prefix)
        found: list[tuple[int, str]] = []

        def collect(n: TrieNode, path: str) -> None:
            if n.is_word:
                found.append((-n.popularity, path))
            for ch, child in n.children.items():
                collect(child, path + ch)

        if node is not None:
            collect(node, prefix)
        return [w for _, w in sorted(found)[:k]]

    def delete(self, word: str) -> bool:
        """Unmark the word and prune nodes no other word needs."""
        if not self.contains(word):
            return False
        node = self.root
        node.count -= 1
        for ch in word:
            child = node.children[ch]
            child.count -= 1
            if child.count == 0:
                del node.children[ch]           # nothing below is needed any more
                return True
            node = child
        node.is_word = False
        return True


def longest_common_prefix(words: list[str]) -> str:
    """Practical example: walk down while there is exactly one path and no word ends (V3-C4 did it with strings)."""
    if not words:
        return ""
    t = Trie()
    for w in words:
        t.insert(w)
    node, prefix = t.root, ""
    while len(node.children) == 1 and not node.is_word:
        ch, node = next(iter(node.children.items()))
        prefix += ch
    return prefix


if __name__ == "__main__":
    t = Trie()
    for word, pop in [("lion", 90), ("lioness", 40), ("lime", 70), ("limo", 10), ("zebra", 80), ("zebu", 5)]:
        t.insert(word, pop)
    print(t.contains("lion"), t.contains("lio"), t.starts_with("lio"), t.count_prefix("li"))
    print(t.words_with_prefix("li"), "| suggest('li'):", t.suggest("li"))
    t.delete("lioness")
    print("after delete:", t.words_with_prefix("lio"))
    print(longest_common_prefix(["flower", "flow", "flight"]))
