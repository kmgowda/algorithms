"""Volume 5, Chapter 19 - Online Algorithms: deciding without seeing the future, measured against one who can.

Run:  python3 ch19_examples.py
"""

from __future__ import annotations

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("ch18_v5", os.path.join(HERE, "..", "chapter_18_when_greedy_fails", "ch18_examples.py"))
ch18 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ch18)
REQUESTS, SHELF = ch18.REQUESTS, ch18.SHELF


def ski_rental(days: int, rent: int, buy: int) -> int:
    """Rent until the rent paid would reach the price, then buy. Cost for a season of `days` days."""
    if rent <= 0 or buy <= 0:
        raise ValueError("prices must be positive")
    threshold = -(-buy // rent) - 1          # rent this many days, buy on the next
    return days * rent if days <= threshold else threshold * rent + buy


def ski_best(days: int, rent: int, buy: int) -> int:
    """What someone who knew the season's length would pay."""
    return min(days * rent, buy)


def worst_ratio(rent: int, buy: int, max_days: int = 200) -> float:
    return max(ski_rental(d, rent, buy) / ski_best(d, rent, buy) for d in range(1, max_days + 1))


def lru(requests: list, k: int) -> int:
    return ch18.least_recently_used(requests, k)


def fifo(requests: list, k: int) -> int:
    return ch18.first_in_first_out(requests, k)


def belady(requests: list, k: int) -> int:
    return ch18.farthest_in_future(requests, k)


def adversary_sequence(rule, k: int, length: int) -> list:
    """Always ask for the one book of k + 1 that `rule`'s shelf does not hold: every request misses."""
    books = [f"b{i}" for i in range(k + 1)]
    seq = []
    for _ in range(length):
        for b in books:                      # find a book the rule would not have on its shelf now
            if rule(seq + [b], k) == rule(seq, k) + 1:
                seq.append(b)
                break
    return seq


if __name__ == "__main__":
    print([ski_rental(d, 10, 100) for d in (3, 9, 10, 30)], [ski_best(d, 10, 100) for d in (3, 9, 10, 30)], worst_ratio(10, 100))
    print(lru(REQUESTS, SHELF), fifo(REQUESTS, SHELF), belady(REQUESTS, SHELF))
    adv = adversary_sequence(lru, 3, 12)
    print(adv, lru(adv, 3), belady(adv, 3))
