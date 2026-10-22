"""Volume 3, Chapter 10 - Tries.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import random
import timeit


class Trie:
    """Words stored letter by letter; shared prefixes share a path (Figures 10.1 to 10.3)."""

    def __init__(self):
        self.children: dict[str, "Trie"] = {}
        self.is_word = False

    def insert(self, word: str) -> None:
        node = self
        for ch in word:
            node = node.children.setdefault(ch, Trie())   # reuse the path or add a letter
        node.is_word = True

    def delete(self, word: str) -> bool:
        """Unmark the word, then climb back up removing letters no other word needs (Figure 10.4).
        Returns whether the word was stored."""
        path, node = [self], self
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
            path.append(node)
        if not node.is_word:
            return False
        node.is_word = False
        for i in range(len(word), 0, -1):                 # prune from the last letter upwards
            if path[i].is_word or path[i].children:       # still needed by another word: stop
                break
            del path[i - 1].children[word[i - 1]]
        return True

    def starting_with(self, prefix: str) -> list[str]:
        node = self
        for ch in prefix:                                 # walk the typed letters
            if ch not in node.children:
                return []
            node = node.children[ch]
        found, stack = [], [(node, prefix)]
        while stack:                                      # collect every word below
            n, spelled = stack.pop()
            if n.is_word:
                found.append(spelled)
            for ch in sorted(n.children, reverse=True):
                stack.append((n.children[ch], spelled + ch))
        return found


def count_nodes(t: Trie) -> int:
    return 1 + sum(count_nodes(c) for c in t.children.values())


def vocabulary(n: int = 14_000, seed: int = 1) -> list[str]:
    """Section 10.8: made-up words built from common syllables, so many share beginnings."""
    rng = random.Random(seed)
    syllables = ["ca", "ro", "ma", "li", "ter", "an", "de", "so", "mi", "bo", "ra", "en", "tu", "pe", "lo", "ing"]
    words = set()
    while len(words) < n:
        words.add("".join(rng.choice(syllables) for _ in range(rng.randint(1, 4))))
    return sorted(words)


def scan_prefix(words, prefix: str, limit: int = 10) -> list[str]:
    """The hash-set way: test every word's beginning."""
    return sorted(w for w in words if w.startswith(prefix))[:limit]


def compare(seed: int = 1) -> dict:
    words = vocabulary(seed=seed)
    trie, store = Trie(), set(words)
    for w in words:
        trie.insert(w)
    rng = random.Random(seed + 1)
    prefixes = [rng.choice(words)[:rng.randint(2, 4)] for _ in range(1000)]
    t_trie = min(timeit.repeat(lambda: [trie.starting_with(p)[:10] for p in prefixes], number=1, repeat=3))
    t_scan = min(timeit.repeat(lambda: [scan_prefix(store, p) for p in prefixes], number=1, repeat=3))
    return {"words": len(words), "letters": sum(map(len, words)), "trie nodes": count_nodes(trie),
            "trie ms": round(t_trie * 1000, 1), "scan ms": round(t_scan * 1000, 1)}


if __name__ == "__main__":
    t = Trie()
    for w in ["CAT", "CAR", "CART", "CARD", "DOG", "DOT"]:
        t.insert(w)
    print(t.starting_with("CAR"), t.starting_with("DO"), t.starting_with("CO"), count_nodes(t))
    t.insert("DOVE")
    print(t.starting_with("D"))
    for w in ["CAR", "CART", "CARD"]:                    # Figure 10.4: unmark, prune one, prune two
        t.delete(w)
        print("delete", w, count_nodes(t), t.starting_with("C"))
    print(compare())
