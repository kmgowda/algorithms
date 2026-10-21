import itertools
import random
import unittest

import ch04_examples as ex


class TestChapter33(unittest.TestCase):
    def test_patterns(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            prices = [rng.randint(1, 40) for _ in range(rng.randint(0, 10))]
            card = rng.randint(2, 60)
            got = ex.pair_for_card(prices, card)
            exists = any(a + b == card for a, b in itertools.combinations(prices, 2))
            self.assertEqual(got is not None, exists)
            if got:
                self.assertEqual(sum(got), card)
            word = "".join(rng.choice("abc") for _ in range(rng.randint(0, 8)))
            brute = next((c for c in word if word.count(c) == 1), None)
            self.assertEqual(ex.first_unique(word), brute)
            self.assertEqual(ex.dedupe(list(word)), list(dict.fromkeys(word)))
        self.assertEqual(ex.first_unique("SWISSCHEESE"), "W")
        self.assertEqual(ex.first_unique("LIBRARY"), "L")
        self.assertEqual(ex.pair_for_card([12, 18, 5, 25], 30), (12, 18))
        self.assertEqual(ex.pair_for_card([15], 30), None)
        g = ex.group_anagrams(["stop", "pots", "tops", "post", "spot", "opts", "stip"])
        self.assertEqual(g, {"opst": ["stop", "pots", "tops", "post", "spot", "opts"], "ipst": ["stip"]})

    def test_leaderboard(self) -> None:
        rng = random.Random(2)
        log = [(f"r{rng.randint(1, 15)}", f"b{rng.randint(1, 10)}") for _ in range(200)]
        top, pop, doubles = ex.leaderboard(log, popular=8)
        distinct = {r: len({b for rr, b in log if rr == r}) for r, _ in log}
        self.assertEqual(top, sorted(distinct, key=lambda r: (-distinct[r], r))[:3])
        self.assertEqual(len(doubles), len(log) - len(set(log)))
        readers = {b: len({r for r, bb in set(log) if bb == b}) for _, b in log}
        self.assertEqual(pop, sorted(b for b, c in readers.items() if c > 8))


if __name__ == "__main__":
    unittest.main()
