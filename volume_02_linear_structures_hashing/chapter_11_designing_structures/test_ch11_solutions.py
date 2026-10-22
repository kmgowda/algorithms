import collections
import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_distinct_count_counterexample(self) -> None:
        a_before, b_before, a_after, b_after = sol.distinct_count_is_not_a_tag()
        self.assertEqual(a_before, b_before)
        self.assertNotEqual(a_after, b_after)

    def test_bag_smallest(self) -> None:
        bag = sol.RandomBag(random.Random(1))
        self.assertEqual(len(bag), 0)
        self.assertFalse(bag.remove(5))
        with self.assertRaises(IndexError):
            bag.pick()
        self.assertTrue(bag.add(5))
        self.assertFalse(bag.add(5))
        self.assertEqual(bag.pick(), 5)
        self.assertTrue(bag.remove(5))
        self.assertEqual((bag.items, bag.pos), ([], {}))

    def test_bag_example(self) -> None:
        bag = sol.RandomBag(random.Random(11))
        for c in (47, 63, 12, 25):
            bag.add(c)
        bag.remove(63)
        self.assertEqual((bag.items, bag.pos), ([47, 25, 12], {47: 0, 25: 1, 12: 2}))

    def test_bag_against_set(self) -> None:
        rng = random.Random(111)
        bag, ref = sol.RandomBag(random.Random(3)), set()
        for _ in range(3000):
            x = rng.randint(0, 20)
            if rng.random() < 0.55:
                self.assertEqual(bag.add(x), x not in ref)
                ref.add(x)
            else:
                self.assertEqual(bag.remove(x), x in ref)
                ref.discard(x)
            self.assertEqual(sorted(bag.items), sorted(ref))
            self.assertTrue(all(bag.items[bag.pos[y]] == y for y in ref))
            if ref:
                self.assertIn(bag.pick(), ref)

    def test_bag_picks_are_fair(self) -> None:
        bag = sol.RandomBag(random.Random(5))
        for c in (12, 25, 47):
            bag.add(c)
        counts = collections.Counter(bag.pick() for _ in range(6000))
        self.assertTrue(all(1700 < counts[c] < 2300 for c in (12, 25, 47)))

    def test_sparse_min_stack_bug(self) -> None:
        s, good = sol.SparseMinStackBuggy(), ex.MinStack()
        for v in (30, 20, 20, 40):
            s.push(v)
            good.push(v)
        for _ in range(2):
            s.pop()
            good.pop()
        self.assertEqual((s.items, s.min(), good.min()), ([30, 20], 30, 20))


if __name__ == "__main__":
    unittest.main()
