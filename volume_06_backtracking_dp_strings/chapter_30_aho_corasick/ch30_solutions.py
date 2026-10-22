"""Volume 6, Chapter 30 - model solutions to the Thinking Problems (Section 30.13)."""

from __future__ import annotations

from collections import deque

from ch30_examples import build


def count_each(text: str, words: list) -> dict:
    """How often each word occurs, in time about n + total word length, without listing the matches:
    count the visits to each node, then push the counts down the fallback links, longest nodes first."""
    goto, fail, _ = build(words)
    order, queue = [], deque(goto[0].values())
    while queue:                                       # breadth-first order of the nodes
        v = queue.popleft()
        order.append(v)
        queue.extend(goto[v].values())
    visits, node = [0] * len(goto), 0
    for ch in text:
        while node and ch not in goto[node]:
            node = fail[node]
        node = goto[node].get(ch, 0)
        visits[node] += 1
    for v in reversed(order):                          # deepest first: a node's link is always shallower
        visits[fail[v]] += visits[v]
    ends = {}
    for w in words:                                    # the node where each word ends
        v = 0
        for ch in w:
            v = goto[v][ch]
        ends[w] = v
    return {w: visits[ends[w]] for w in words}


def link_steps(words: list) -> int:
    """Thinking Problem 1: the number of links BuildLinks follows in its inner loop (at most the total length)."""
    goto, fail = [{}], [0]
    for w in words:
        node = 0
        for ch in w:
            if ch not in goto[node]:
                goto.append({}); fail.append(0)
                goto[node][ch] = len(goto) - 1
            node = goto[node][ch]
    queue, steps = deque(goto[0].values()), 0
    while queue:
        node = queue.popleft()
        for ch, child in goto[node].items():
            queue.append(child)
            f = fail[node]
            while f and ch not in goto[f]:
                f = fail[f]
                steps += 1
            fail[child] = goto[f].get(ch, 0) if goto[f].get(ch, 0) != child else 0
    return steps


def one_step_search(text: str, words: list) -> list:
    """Thinking Problem 3's bug: each link is set from the parent's link in one step, never following further."""
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
    while queue:
        node = queue.popleft()
        for ch, child in goto[node].items():
            queue.append(child)
            g = goto[fail[node]].get(ch, 0)
            fail[child] = g if g != child else 0
            out[child] = out[child] + out[fail[child]]
    node, found = 0, []
    for i, ch in enumerate(text):
        while node and ch not in goto[node]:
            node = fail[node]
        node = goto[node].get(ch, 0)
        found.extend((i - len(w) + 1, w) for w in out[node])
    return sorted(found)


if __name__ == "__main__":
    print(count_each("aaaa", ["a", "aa", "aaa"]))
    print(link_steps(["he", "she", "his", "hers"]), link_steps(["aab", "aaab", "ab"]))
    print(one_step_search("see", ["e", "see"]))
