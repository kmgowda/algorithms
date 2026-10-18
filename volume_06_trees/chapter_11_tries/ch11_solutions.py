"""Volume 6, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations

from ch11_examples import Trie, TrieNode


def search_with_wildcard(trie: Trie, pattern: str) -> bool:
    """Exercise 1 (LeetCode 211): '.' matches any single letter."""
    def match(node: TrieNode, i: int) -> bool:
        if i == len(pattern):
            return node.is_word
        if pattern[i] == ".":
            return any(match(child, i + 1) for child in node.children.values())
        child = node.children.get(pattern[i])
        return child is not None and match(child, i + 1)
    return match(trie.root, 0)


def replace_with_roots(roots: list[str], sentence: str) -> str:
    """Exercise 2 (LeetCode 648): replace each word by its shortest root found in the trie."""
    t = Trie()
    for r in roots:
        t.insert(r)
    out = []
    for word in sentence.split():
        node, prefix = t.root, ""
        for ch in word:
            if ch not in node.children or node.is_word:
                break
            node = node.children[ch]
            prefix += ch
        out.append(prefix if node.is_word else word)
    return " ".join(out)


def count_distinct_substrings(text: str) -> int:
    """Exercise 3: insert every suffix; each trie node (except the root) is one distinct substring. O(n^2)."""
    t = Trie()
    for i in range(len(text)):
        t.insert(text[i:])
    stack, nodes = [t.root], 0
    while stack:
        n = stack.pop()
        nodes += 1
        stack.extend(n.children.values())
    return nodes - 1


def phone_contacts_matching(contacts: list[str], typed: str) -> list[str]:
    """Exercise 4 (LeetCode 1268 idea): up to 3 alphabetical suggestions after each typed letter."""
    t = Trie()
    for c in contacts:
        t.insert(c)
    return [", ".join(t.words_with_prefix(typed[:i])[:3]) for i in range(1, len(typed) + 1)]


if __name__ == "__main__":
    t = Trie()
    for w in ("bad", "dad", "mad"):
        t.insert(w)
    print(search_with_wildcard(t, ".ad"), search_with_wildcard(t, "b.."), search_with_wildcard(t, "b."))
    print(replace_with_roots(["cat", "bat", "rat"], "the cattle was rattled by the battery"))
    print(count_distinct_substrings("abab"), phone_contacts_matching(["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mou"))
