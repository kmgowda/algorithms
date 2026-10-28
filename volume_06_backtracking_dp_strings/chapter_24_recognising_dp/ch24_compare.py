"""Chapter 24, Sections 24.9-24.10: four strategies (greedy, backtracking, plain divide-and-conquer recursion,
dynamic programming) run on the same problems, counting the work each one does and checking each answer."""
import os
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(folder: str, module: str):
    """Load a sibling chapter's module from its file under a unique name: module names repeat across volumes
    (every volume has a ch06_examples), so a plain import could pick up the wrong one."""
    import importlib.util
    path = os.path.join(HERE, "..", folder, module + ".py")
    spec = importlib.util.spec_from_file_location(f"{os.path.basename(os.path.dirname(HERE))}.{folder}.{module}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

c12 = _load("chapter_12_one_dimensional_dp", "ch12_examples")
c14 = _load("chapter_14_knapsack", "ch14_examples")
c06 = _load("chapter_06_branch_and_bound", "ch06_examples")
c24 = _load("chapter_24_recognising_dp", "ch24_examples")

COINS, AMOUNT = c12.ODD, 6          # coins 4p, 3p, 1p; make 6p


def coins_greedy(amount: int, coins: list) -> list:
    """Take the largest coin that fits, again and again (Volume 5, Chapter 14)."""
    used = []
    for c in sorted(coins, reverse=True):
        while c <= amount:
            used.append(c)
            amount -= c
    return used if amount == 0 else []


def coins_backtrack(amount: int, coins: list, log: list | None = None) -> tuple[int, int]:
    """Try coins largest first, abandoning any branch that already uses as many coins as the best answer so far.
    log, if given, receives (node, parent, amount left, coin taken, outcome) for every node visited.
    Returns (fewest coins, nodes visited)."""
    coins = sorted(coins, reverse=True)
    best, nodes = [float("inf")], [0]

    def go(left, used, start, parent, coin):
        nodes[0] += 1
        me = nodes[0]
        if left == 0:
            outcome = "new best" if used < best[0] else "no better"
            best[0] = min(best[0], used)
        elif used + 1 >= best[0]:
            outcome = "cut"
        else:
            outcome = "branch"
        if log is not None:
            log.append((me, parent, left, coin, outcome))
        if outcome != "branch":
            return
        for i in range(start, len(coins)):
            if coins[i] <= left:
                go(left - coins[i], used + 1, i, me, coins[i])

    go(amount, 0, 0, 0, None)
    return best[0], nodes[0]


def coins_plain(amount: int, coins: list, calls: list) -> int:
    """fewest(a) = 1 + min over coins c <= a of fewest(a - c), recomputed every time it is needed."""
    calls[0] += 1
    if amount == 0:
        return 0
    return 1 + min(coins_plain(amount - c, coins, calls) for c in coins if c <= amount)


def coins_compare(amount: int = AMOUNT, coins: list = COINS) -> dict:
    calls = [0]
    plain = coins_plain(amount, coins, calls)
    bt, nodes = coins_backtrack(amount, coins)
    dp, used, _ = c12.fewest_coins(amount, coins)
    g = coins_greedy(amount, coins)
    return {"greedy": (len(g), g, len(g)), "backtracking": (bt, nodes), "plain": (plain, calls[0]),
            "dp": (dp, sorted(used, reverse=True), amount), "best": dp}


BUDGET = 20


def knapsack_greedy(books: list, budget: int) -> tuple[int, list]:
    """Whole books in order of votes per pound, each one that still fits."""
    votes, names = 0, []
    for name, price, v in sorted(books, key=lambda b: b[2] / b[1], reverse=True):
        if price <= budget:
            budget -= price
            votes += v
            names.append(name)
    return votes, names


def knapsack_compare(books: list = c14.BOOKS, budget: int = BUDGET) -> dict:
    g, gnames = knapsack_greedy(books, budget)
    full, _, full_nodes = c06.branch_and_bound(books, budget, use_bound=False)
    bb, bbnames, bb_nodes = c06.branch_and_bound(books, budget)
    dp, dpnames, _ = c14.knapsack(books, budget)
    return {"greedy": (g, gnames), "backtracking": (full, full_nodes), "branch_and_bound": (bb, bb_nodes),
            "dp": (dp, dpnames, len(books) * budget), "best": c14.brute(books, budget)}


def bookings_brute(bookings: list) -> tuple[int, int]:
    """Every subset of bookings that do not overlap: (most members, subsets checked)."""
    best, checked = 0, 0
    for r in range(len(bookings) + 1):
        for sub in combinations(bookings, r):
            checked += 1
            if all(a[2] <= b[1] or b[2] <= a[1] for a, b in combinations(sub, 2)):
                best = max(best, sum(b[3] for b in sub))
    return best, checked


def bookings_plain(bookings: list) -> tuple[int, int]:
    """opt(j) = max(opt(j - 1), value_j + opt(p[j])) without remembering: (most members, calls)."""
    _, _, p, _ = c12.weighted_intervals(bookings)
    jobs = sorted(bookings, key=lambda b: b[2])
    calls = [0]

    def opt(j):
        calls[0] += 1
        if j == 0:
            return 0
        return max(opt(j - 1), jobs[j - 1][3] + opt(p[j - 1]))
    return opt(len(jobs)), calls[0]


def plain_counts(amount: int, coins: list) -> list:
    """How many times plain recursion solves each amount 0..amount while making the full amount."""
    seen = [0] * (amount + 1)

    def go(a):
        seen[a] += 1
        for c in coins:
            if c <= a:
                go(a - c)
    go(amount)
    return seen


def bookings_compare(bookings: list = c12.BOOKINGS) -> dict:
    earliest = c12.greedy_intervals(bookings, key=lambda b: b[2])
    biggest = c12.greedy_intervals(bookings, key=lambda b: -b[3])
    dp, chosen, _, _ = c12.weighted_intervals(bookings)
    brute, checked = bookings_brute(bookings)
    # unweighted: the most bookings; earliest finish is optimal there
    count_best = max(len(s) for r in range(len(bookings) + 1) for s in combinations(bookings, r)
                     if all(a[2] <= b[1] or b[2] <= a[1] for a, b in combinations(s, 2)))
    plain = bookings_plain(bookings)
    return {"plain": plain, "earliest_finish": earliest, "biggest_first": biggest, "dp": (dp, chosen), "brute": (brute, checked),
            "most_bookings": count_best, "earliest_count": len(earliest[1])}


def banner_compare(n: int = 8, price: dict | None = None) -> dict:
    price = price or c24.PRICE
    calls = [0]
    plain = c24.best_plain(n, price, calls)
    best, _, _ = c24.best_table(n, price)
    return {"greedy": c24.greedy_best_rate(n, price), "plain": (plain, calls[0]), "dp": best}


if __name__ == "__main__":
    print(coins_compare())
    print(knapsack_compare())
    print(bookings_compare())
    print(banner_compare())
    for n in (4, 8):
        print(n, banner_compare(n))
