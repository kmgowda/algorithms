"""Volume 5, Chapter 22 - Many Patterns at Once: Aho-Corasick, a trie with fallback links.

Run:  python3 ch22_examples.py
"""

from __future__ import annotations

from collections import deque

WORDS = ["he", "she", "his", "hers"]                   # the classic example
BANNED = ["spoiler", "ending", "dies"]                  # words the book club's forum hides


def build(words: list) -> tuple[list, list, list]:
    """Trie of the words (goto), fallback links (fail), and words ending at each node (out) (Figure 22.2)."""
    goto, fail, out = [{}], [0], [[]]
    for w in words:
        node = 0
        for ch in w:
            if ch not in goto[node]:
                goto.append({}); fail.append(0); out.append([])
                goto[node][ch] = len(goto) - 1
            node = goto[node][ch]
        out[node].append(w)
    queue = deque(goto[0].values())
    while queue:                                       # breadth-first: shorter nodes get their links first
        node = queue.popleft()
        for ch, child in goto[node].items():
            queue.append(child)
            f = fail[node]
            while f and ch not in goto[f]:
                f = fail[f]
            fail[child] = goto[f].get(ch, 0) if goto[f].get(ch, 0) != child else 0
            out[child] = out[child] + out[fail[child]]   # words that end here through the fallback
    return goto, fail, out


def search(text: str, words: list) -> tuple[list, int]:
    """Every (position, word) found in one pass over the text. Returns (matches, steps taken)."""
    goto, fail, out = build(words)
    node, found, steps = 0, [], 0
    for i, ch in enumerate(text):
        while node and ch not in goto[node]:
            node = fail[node]
            steps += 1
        node = goto[node].get(ch, 0)
        steps += 1
        for w in out[node]:
            found.append((i - len(w) + 1, w))
    return sorted(found), steps


def search_each(text: str, words: list) -> list:
    return sorted((i, w) for w in words for i in range(len(text) - len(w) + 1) if text.startswith(w, i))


if __name__ == "__main__":
    goto, fail, out = build(WORDS)
    print(len(goto), fail, out)
    print(search("ushers", WORDS))
    post = "warning: spoiler ahead. in the ending the hero dies, the spoiler said"
    print(search(post, BANNED))
