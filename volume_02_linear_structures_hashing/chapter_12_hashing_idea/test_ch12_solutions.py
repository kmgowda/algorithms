import itertools
import math
import unittest

import ch12_examples as ex
import ch12_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_pigeonhole_forces_a_crowd(self) -> None:
        words = ["".join(p) for p in itertools.product("ABC", repeat=4)]         # 81 keys
        for m in (1, 2, 5, 8, 16):
            for n in (1, 2, 3, 4):
                keys = words[:(n - 1) * m + 1]
                if len(keys) == (n - 1) * m + 1:
                    for fn in (ex.letter_sum_hash, ex.multiply_add_hash):
                        self.assertGreaterEqual(sol.crowded_slot(keys, m, fn)[1], n)

    def test_find_collision_smallest(self) -> None:
        a, b, tries = sol.find_collision(1)
        self.assertNotEqual(a, b)
        self.assertEqual(tries, 2)

    def test_find_collision_is_real_and_quick(self) -> None:
        m = 65_536
        tries = []
        for seed in range(60):
            a, b, t = sol.find_collision(m, seed)
            self.assertNotEqual(a, b)
            self.assertEqual(ex.multiply_add_hash(a, m), ex.multiply_add_hash(b, m))
            self.assertLessEqual(t, m + 1)                     # the pigeonhole guarantee
            tries.append(t)
        self.assertLess(sum(tries) / len(tries), 2 * math.sqrt(m))   # birthday: about 321 expected

    def test_bound_and_numbers(self) -> None:
        for m in (1, 8, 100, 365):
            for n in range(0, m + 3):
                self.assertLessEqual(sol.no_collision_chance(n, m), sol.no_collision_bound(n, m) + 1e-12)
        self.assertEqual(sol.no_collision_chance(366, 365), 0)
        self.assertAlmostEqual(sol.no_collision_chance(23, 365), 0.4927, places=4)
        self.assertAlmostEqual(sol.no_collision_chance(2000, 10**6), 0.1353, places=4)


if __name__ == "__main__":
    unittest.main()
