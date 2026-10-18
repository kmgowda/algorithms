import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


def brute_cycle(start, step):
    seen = {}
    x, i = start, 0
    while x not in seen:
        seen[x] = i
        x, i = step(x), i + 1
    return seen[x], i - seen[x]


class TestFastSlow(unittest.TestCase):
    def test_happy(self) -> None:
        for n in range(1, 500):
            self.assertEqual(ex.is_happy(n), sol.is_happy_with_set(n))
        self.assertTrue(ex.is_happy(19))
        self.assertFalse(ex.is_happy(2))

    def test_find_cycle_matches_brute(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            n = rng.randint(1, 30)
            table = [rng.randrange(n) for _ in range(n)]
            start = rng.randrange(n)
            self.assertEqual(ex.find_cycle(start, lambda x: table[x]), brute_cycle(start, lambda x: table[x]))
        self.assertEqual(ex.find_cycle(7, ex.lcg), brute_cycle(7, ex.lcg))

    def test_find_duplicate(self) -> None:
        rng = random.Random(2)
        for _ in range(300):
            n = rng.randint(1, 20)
            dup = rng.randint(1, n)
            ids = list(range(1, n + 1)) + [dup]
            for _ in range(rng.randint(0, n - 1)):          # overwrite some other ids with more copies of dup
                ids[rng.randrange(len(ids))] = dup
            if ids.count(dup) < 2:
                ids.append(dup)
                ids.pop(next(i for i, x in enumerate(ids) if x != dup))
            rng.shuffle(ids)
            copy = list(ids)
            self.assertEqual(ex.find_duplicate(ids), dup)
            self.assertEqual(ids, copy)

    def test_shuffle(self) -> None:
        self.assertEqual(ex.shuffle_repeat_period([1, 2, 0, 4, 3]), 6)
        self.assertEqual(ex.shuffle_repeat_period([0, 1, 2]), 1)
        order = [1, 2, 0, 4, 3]
        state = list(range(5))
        for k in range(1, 7):
            state = [state[order[i]] for i in range(5)]
            self.assertEqual(state == list(range(5)), k == 6)


class TestSolutions(unittest.TestCase):
    def test_circular_loop(self) -> None:
        self.assertTrue(sol.circular_loop([2, -1, 1, 2, 2]))
        self.assertFalse(sol.circular_loop([-1, 2]))
        self.assertFalse(sol.circular_loop([-2, 1, -1, -2, -2]))
        self.assertTrue(sol.circular_loop([1, 1]))

    def test_gift_chain(self) -> None:
        self.assertEqual(sol.gift_chain_length([1, 2, 0, 4, 3], 0), 3)
        self.assertEqual(sol.gift_chain_length([1, 2, 0, 4, 3], 3), 2)


if __name__ == "__main__":
    unittest.main()
