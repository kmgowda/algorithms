import random
import unittest

import ch15_examples as ex
import ch15_solutions as sol


class TestPerfectTable(unittest.TestCase):
    def test_shelf_build(self) -> None:
        t = ex.PerfectTable(ex.SHELF)
        self.assertEqual((t.a, t.b, t.primary_tries), (18, 72, 1))
        sizes = [0 if b is None else len(b[2]) for b in t.buckets]
        self.assertEqual(sizes, [1, 1, 0, 0, 1, 9, 4, 0, 1])
        self.assertEqual(t.buckets[5][2], [None, 58, None, None, 12, None, 63, None, None])
        self.assertEqual(t.secondary_tries[6], 2)          # 31 and 84 collided once
        self.assertEqual(t.space(), 26)
        self.assertTrue(all(t.find(k) for k in ex.SHELF))

    def test_every_case(self) -> None:
        t = ex.PerfectTable(ex.SHELF)
        self.assertTrue(t.find(47))                         # bucket of one
        self.assertTrue(t.find(63))                         # bucket of three
        self.assertFalse(t.find(13))                        # absent, empty bucket 3
        self.assertFalse(t.find(60))                        # absent, bucket 5 holds three keys
        self.assertFalse(t.find(8))                         # absent, lands on 58's slot: the comparison matters
        self.assertFalse(t.find(500))                       # outside the key range
        e = ex.PerfectTable([])
        self.assertEqual((e.find(5), e.space()), (False, 0))
        one = ex.PerfectTable([42])
        self.assertTrue(one.find(42) and not one.find(41))
        self.assertEqual(one.space(), 2)
        d = ex.PerfectTable([12, 12, 25])                   # duplicates ignored
        self.assertEqual((d.m, d.find(12), d.find(25)), (2, True, True))
        self.assertEqual(ex.bucket_sizes([4, 8, 12, 16], 1, 0, 101, 4), [4, 0, 0, 0])   # 16 = 4n: rejected
        with self.assertRaises(ValueError):
            ex.PerfectTable([200])

    def test_random_sets(self) -> None:
        rng = random.Random(4)
        for trial in range(60):
            n = rng.randint(0, 60)
            keys = rng.sample(range(1, 2_000_000), n)
            t = ex.PerfectTable(keys, p=2_147_483_647, seed=trial)
            self.assertLess(t.space() - t.m, 4 * max(1, n))
            self.assertTrue(all(t.find(k) for k in keys))
            self.assertFalse(any(t.find(k) for k in rng.sample(range(2_000_000, 3_000_000), 20)))

    def test_rates_and_space(self) -> None:
        self.assertAlmostEqual(ex.collision_free_rate(9, 9), 0.00094, delta=0.001)
        self.assertGreater(ex.collision_free_rate(9, 81), 0.5)
        avg, ok = ex.space_experiment(1000, trials=50)
        self.assertLess(avg, 2 * 1000 + 100)
        self.assertEqual(ok, 1.0)

    def test_compare(self) -> None:
        c = ex.compare()
        self.assertEqual(c["chaining"], (4, 20))
        self.assertEqual(c["linear probing"], (8, 11))
        self.assertEqual(c["perfect (FKS)"], (2, 26))


class TestWordTable(unittest.TestCase):
    def test_smallest(self) -> None:
        empty = sol.build_word_table([])
        self.assertFalse(empty("if"))
        one = sol.build_word_table(["if"])
        self.assertTrue(one("if"))
        self.assertFalse(one("fi"))
        self.assertFalse(one(""))

    def test_keywords(self) -> None:
        words = ["if", "else", "while", "for", "return", "def", "class", "and", "or", "if"]
        has = sol.build_word_table(words)
        self.assertTrue(all(has(w) for w in words))
        for w in ("whale", "IF", "els", "", "classes", "nor"):
            self.assertFalse(has(w))

    def test_random_words(self) -> None:
        rng = random.Random(2)
        words = {"".join(rng.choice("abc") for _ in range(rng.randint(1, 6))) for _ in range(200)}
        has = sol.build_word_table(sorted(words), seed=3)
        self.assertTrue(all(has(w) for w in words))
        others = {"".join(rng.choice("abcd") for _ in range(rng.randint(0, 7))) for _ in range(300)} - words
        self.assertFalse(any(has(w) for w in others))


if __name__ == "__main__":
    unittest.main()
