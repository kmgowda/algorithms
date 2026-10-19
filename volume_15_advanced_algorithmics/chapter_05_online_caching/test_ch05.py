import itertools
import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


def brute_opt(requests, size):
    """Smallest misses over every possible eviction choice (tiny inputs only)."""
    best = None

    def go(i, cache, misses):
        nonlocal best
        if best is not None and misses >= best:
            return
        if i == len(requests):
            best = misses
            return
        p = requests[i]
        if p in cache:
            go(i + 1, cache, misses)
        elif len(cache) < size:
            go(i + 1, cache | {p}, misses + 1)
        else:
            for victim in cache:
                go(i + 1, (cache - {victim}) | {p}, misses + 1)

    go(0, frozenset(), 0)
    return best


class TestOnline(unittest.TestCase):
    def test_belady_optimal(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            reqs = [rng.choice("ABCDE") for _ in range(rng.randint(0, 12))]
            size = rng.randint(1, 3)
            opt = ex.belady_misses(reqs, size)
            self.assertEqual(opt, brute_opt(reqs, size))
            self.assertLessEqual(opt, ex.lru_misses(reqs, size))
            self.assertLessEqual(opt, ex.fifo_misses(reqs, size))
            self.assertLessEqual(opt, sol.lfu_misses(reqs, size))
            self.assertLessEqual(ex.lru_misses(reqs, size), size * opt + size)     # LRU is size-competitive

    def test_ski_and_examples(self) -> None:
        for rent, buy in [(100, 1000), (30, 100), (7, 7)]:
            for days in range(1, 60):
                online, opt = ex.ski_rental(rent, buy, days)
                self.assertLess(online, 2 * opt)
            self.assertLess(sol.worst_case_ratio(rent, buy, 200), 2)
        self.assertEqual(ex.ski_rental(100, 1000, 10), (1900, 1000))
        self.assertEqual(ex.cache_report(list("ABCABDADBCDA"), 3), {"LRU": 6, "FIFO": 9, "optimal": 5})
        adv = sol.adversary_for_lru(3, 40)
        self.assertEqual(ex.lru_misses(adv, 3), 40)
        reqs = ex.zipf_requests(500, 50, random.Random(2))
        self.assertLess(ex.belady_misses(reqs, 5), ex.lru_misses(reqs, 5))


if __name__ == "__main__":
    unittest.main()
