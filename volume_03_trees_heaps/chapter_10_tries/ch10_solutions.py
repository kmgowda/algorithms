"""Volume 3, Chapter 10 - Tries: companion code for the Thinking Problems (Section 10.16).

Run:  python3 ch10_solutions.py
"""

from __future__ import annotations

from ch10_examples import Trie


def lcp(u: str, v: str) -> int:
    k = 0
    while k < min(len(u), len(v)) and u[k] == v[k]:
        k += 1
    return k


def nodes_by_formula(words) -> int:
    """Thinking Problem 1: 1 + the sum, over the sorted distinct words, of len(w) - lcp(w, previous word)."""
    ws = sorted(set(words))
    return 1 + sum(len(w) - (lcp(w, ws[i - 1]) if i else 0) for i, w in enumerate(ws))


def shortest_unique_prefixes(words) -> dict:
    """Thinking Problem 2: for each word, its shortest prefix that no other stored word starts with,
    or the whole word if every prefix is shared (the word begins another word). O(total letters)."""
    root, count = {}, {}                          # child maps, and how many words pass through each node
    ws = list(dict.fromkeys(words))               # distinct words, first-seen order
    for w in ws:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
            count[id(node)] = count.get(id(node), 0) + 1
    out = {}
    for w in ws:
        node, k = root, 0
        while k < len(w):
            node = node[w[k]]
            k += 1
            if count[id(node)] == 1:               # only this word passes here
                break
        out[w] = w[:k]
    return out


def delete_branch_only(trie: Trie, word: str) -> bool:
    """Thinking Problem 3: a wrong delete that prunes upwards while a node has at most one child,
    forgetting to check the word marks. It removes other words."""
    path, node = [trie], trie
    for ch in word:
        if ch not in node.children:
            return False
        node = node.children[ch]
        path.append(node)
    if not node.is_word:
        return False
    node.is_word = False
    for i in range(len(word), 0, -1):
        if len(path[i].children) >= 2:           # the bug: a marked node with no children is pruned too
            break
        del path[i - 1].children[word[i - 1]]
    return True


if __name__ == "__main__":
    from ch10_examples import count_nodes
    six = ["CAT", "CAR", "CART", "CARD", "DOG", "DOT"]
    t = Trie()
    for w in six:
        t.insert(w)
    print(nodes_by_formula(six), count_nodes(t))
    print(shortest_unique_prefixes(six + ["DOVE"]))
    t = Trie()
    for w in ["CAR", "CART", "CAT"]:
        t.insert(w)
    delete_branch_only(t, "CART")
    print(t.starting_with(""))
