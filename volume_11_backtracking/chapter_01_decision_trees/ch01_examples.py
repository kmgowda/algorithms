"""Volume 11, Chapter 1 - Exploring Every Possibility: The Decision Tree of Choices.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations


def all_outfits(choices: list[list[str]]) -> list[tuple[str, ...]]:
    """Every combination of one item per category - each level of the decision tree is one category."""
    if not choices:
        return [()]
    rest = all_outfits(choices[1:])
    return [(item,) + tail for item in choices[0] for tail in rest]


def count_tree_nodes(branching: list[int]) -> int:
    """Nodes in a full decision tree where level i offers branching[i] options (the root counts as one node)."""
    total, width = 1, 1
    for b in branching:
        width *= b
        total += width
    return total


def draw_tree(choices: list[list[str]], path: tuple[str, ...] = (), depth: int = 0) -> list[str]:
    """Text picture of the decision tree: one line per node, indented by depth."""
    lines = ["  " * depth + (" -> ".join(path) if path else "start")]
    if depth < len(choices):
        for item in choices[depth]:
            lines += draw_tree(choices, path + (item,), depth + 1)
    return lines


def all_bit_strings(n: int) -> list[str]:
    """The binary decision tree: at each of n levels, choose 0 or 1. 2^n leaves."""
    if n == 0:
        return [""]
    return [b + rest for b in "01" for rest in all_bit_strings(n - 1)]


def picnic_within_budget(prices: dict[str, int], budget: int) -> tuple[list[list[str]], int, int]:
    """Practical example: every set of snacks within budget. Returns (sets, nodes visited, nodes without the budget check).
    Checking the budget at each node skips whole subtrees - the first taste of pruning (Chapter 6)."""
    items = list(prices)
    found: list[list[str]] = []
    visited = 0

    def explore(i: int, chosen: list[str], spent: int) -> None:
        nonlocal visited
        visited += 1
        if spent > budget:
            return                                     # dead end: nothing below can fix overspending
        if i == len(items):
            found.append(list(chosen))
            return
        explore(i + 1, chosen + [items[i]], spent + prices[items[i]])   # take item i
        explore(i + 1, chosen, spent)                                   # skip item i

    explore(0, [], 0)
    return found, visited, count_tree_nodes([2] * len(items))


def password_space(length: int, alphabet: int) -> int:
    """Industry example: how many leaves a brute-force password search must consider."""
    return alphabet ** length


if __name__ == "__main__":
    wardrobe = [["red shirt", "blue shirt"], ["jeans", "shorts"], ["sneakers", "sandals"]]
    print(len(all_outfits(wardrobe)), "outfits; tree nodes:", count_tree_nodes([2, 2, 2]))
    print("\n".join(draw_tree(wardrobe[:2])))
    print(all_bit_strings(3))
    sets, visited, full = picnic_within_budget({"chips": 30, "juice": 40, "cake": 60, "fruit": 20}, 70)
    print(len(sets), "affordable sets; visited", visited, "of", full, "nodes")
    print("8-character lowercase passwords:", f"{password_space(8, 26):,}")
