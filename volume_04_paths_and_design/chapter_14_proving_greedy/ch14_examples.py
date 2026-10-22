"""Volume 4, Chapter 14 - Proving a Greedy Choice: the exchange argument, on the fractional budget.

Run:  python3 ch14_examples.py
"""

from __future__ import annotations

import itertools
from fractions import Fraction

# The club's books from Chapter 12; this time a subscription can be bought in part (half a year, a third...).
BOOKS = [("Atlas", 9, 6), ("Novel", 6, 4), ("Poems", 5, 6), ("Comic", 5, 2), ("Cookbook", 10, 7)]


def fractional(books: list, budget) -> tuple[Fraction, list]:
    """Fill the budget in order of votes per pound, taking part of the last item (Figure 14.2)."""
    left, votes, taken = Fraction(budget), Fraction(0), []
    for name, price, v in sorted(books, key=lambda b: Fraction(b[2], b[1]), reverse=True):
        if left <= 0:
            break
        part = min(Fraction(1), left / price)
        left -= part * price
        votes += part * v
        taken.append((name, part))
    return votes, taken


def exchange_gain(books: list, plan: dict, budget) -> list:
    """Every swap of spending from a lower-ratio item to a higher-ratio item, with the votes it gains (Figure 14.3)."""
    ratio = {n: Fraction(v, p) for n, p, v in books}
    price = {n: p for n, p, _ in books}
    out = []
    for lo, hi in itertools.permutations(plan, 2):
        if ratio[hi] > ratio[lo] and plan[lo] > 0 and plan[hi] < 1:
            pounds = min(plan[lo] * price[lo], (1 - plan[hi]) * price[hi])
            out.append((lo, hi, pounds, pounds * (ratio[hi] - ratio[lo])))
    return out


def best_fraction_check(books: list, budget, steps: int = 4) -> Fraction:
    """Brute-force check over a grid of fractions (0, 1/4, ..., 1) for every item."""
    grid = [Fraction(k, steps) for k in range(steps + 1)]
    best = Fraction(0)
    for parts in itertools.product(grid, repeat=len(books)):
        cost = sum(f * p for f, (_, p, _) in zip(parts, books))
        if cost <= budget:
            best = max(best, sum(f * v for f, (_, _, v) in zip(parts, books)))
    return best


# Section 14.6: book repairs at the bindery desk, one at a time: (book, hours of work, hours until it is due).
REPAIRS = [("Atlas", 3, 6), ("Novel", 2, 8), ("Poems", 1, 9), ("Comic", 4, 9), ("Cookbook", 2, 14)]


def lateness(order: list) -> tuple[int, list]:
    """Run the jobs back to back in this order from hour 0. Returns (largest lateness, [(job, start, end, late)])."""
    t, rows = 0, []
    for name, hours, due in order:
        rows.append((name, t, t + hours, max(0, t + hours - due)))
        t += hours
    return max((r[3] for r in rows), default=0), rows


def total_lateness(order: list) -> int:
    """Challenge 2: the sum of every job's lateness, a different goal from the largest lateness."""
    return sum(late for *_, late in lateness(order)[1])


def earliest_deadline_first(jobs: list) -> list:
    """Greedy: do the job that is due soonest first (Figure 14.4). Ties keep the input order."""
    return sorted(jobs, key=lambda j: j[2])


def inversions(order: list) -> int:
    """Pairs done in the wrong order: an earlier job that is due strictly later than a later one."""
    return sum(1 for i in range(len(order)) for j in range(i + 1, len(order)) if order[i][2] > order[j][2])


def remove_inversions(order: list) -> list:
    """The exchange argument as a procedure (Figure 14.5): swap neighbouring jobs that are due in the wrong order,
    one swap at a time, recording (order, largest lateness) after each swap. The lateness never goes up."""
    order, steps = list(order), [(list(order), lateness(order)[0])]
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(order) - 1):
            if order[i][2] > order[i + 1][2]:
                order[i], order[i + 1] = order[i + 1], order[i]
                steps.append((list(order), lateness(order)[0]))
                swapped = True
    return steps


def best_lateness(jobs: list) -> int:
    """Brute force over every order (n! of them)."""
    return min((lateness(list(p))[0] for p in itertools.permutations(jobs)), default=0)


if __name__ == "__main__":
    print(lateness(earliest_deadline_first(REPAIRS)), best_lateness(REPAIRS))
    print(lateness(sorted(REPAIRS, key=lambda j: j[1]))[0], lateness(sorted(REPAIRS, key=lambda j: j[2] - j[1]))[0])
    votes, taken = fractional(BOOKS, 20)
    print(votes, float(votes), taken)
    plan = {"Atlas": Fraction(1), "Novel": Fraction(1), "Poems": Fraction(1), "Comic": Fraction(0), "Cookbook": Fraction(0)}
    print(exchange_gain(BOOKS, plan, 20))
    print(best_fraction_check(BOOKS, 20))
