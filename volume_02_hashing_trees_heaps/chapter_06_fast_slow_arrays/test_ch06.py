import collections
import random
import unittest

import ch06_examples as ex


class TestChapter35(unittest.TestCase):
    def test_find_duplicate(self) -> None:
        self.assertEqual(ex.find_duplicate([3, 1, 3, 4, 2]), 3)
        self.assertEqual(ex.find_duplicate([1, 3, 4, 2, 2]), 2)
        rng = random.Random(1)
        for _ in range(500):
            n = rng.randint(1, 60)
            a = [rng.randint(1, n) for _ in range(n + 1)]
            dups = {v for v, c in collections.Counter(a).items() if c > 1}
            self.assertIn(ex.find_duplicate(a), dups)
        for seed in range(20):
            log = ex.ticket_log(500, seed)
            self.assertEqual(ex.find_duplicate(log), collections.Counter(log).most_common(1)[0][0])

    def test_happy(self) -> None:
        def brute(n):
            seen = set()
            while n != 1 and n not in seen:
                seen.add(n)
                n = ex.digit_square_sum(n)
            return n == 1
        for n in range(1, 2000):
            self.assertEqual(ex.is_happy(n), brute(n))
        self.assertTrue(ex.is_happy(19) and ex.is_happy(7))
        self.assertFalse(ex.is_happy(4))


if __name__ == "__main__":
    unittest.main()
