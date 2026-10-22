import random
import unittest

import ch13_solutions as sol


class TestBackwardShiftDelete(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertFalse(sol.backward_shift_delete([None], 5))
        one = [None]
        sol.lp_insert(one, 3)
        self.assertEqual(one, [3])
        self.assertTrue(sol.backward_shift_delete(one, 3))
        self.assertEqual(one, [None])
        self.assertFalse(sol.backward_shift_delete(one, 3))

    def test_worked_example_with_wrap(self) -> None:
        t = [None] * 8
        for key in (7, 15, 1, 9):
            sol.lp_insert(t, key)
        self.assertEqual(t, [15, 1, 9, None, None, None, None, 7])
        self.assertTrue(sol.backward_shift_delete(t, 7))
        self.assertEqual(t, [None, 1, 9, None, None, None, None, 15])
        self.assertEqual((sol.lp_find(t, 15), sol.lp_find(t, 7)), (7, -1))

    def test_key_at_home_stays(self) -> None:
        t = [None] * 8
        for key in (1, 9, 3, 17):          # 1 -> 1, 9 -> 2, 3 -> 3, 17 -> 4
            sol.lp_insert(t, key)
        sol.backward_shift_delete(t, 9)
        self.assertEqual(t, [None, 1, 17, 3, None, None, None, None])

    def test_full_table(self) -> None:
        t = [None] * 4
        for key in (0, 4, 8, 12):
            sol.lp_insert(t, key)
        self.assertTrue(sol.backward_shift_delete(t, 0))
        self.assertEqual(t, [4, 8, 12, None])

    def test_random_against_a_set(self) -> None:
        rng = random.Random(13)
        for m in (1, 2, 8, 16):
            t, live = [None] * m, set()
            for _ in range(2000):
                key = rng.randrange(3 * m)
                if rng.random() < 0.5 and len(live) < m - 1 or not live:
                    if len(live) < m - 1 or key in live:
                        sol.lp_insert(t, key)
                        live.add(key)
                else:
                    self.assertEqual(sol.backward_shift_delete(t, key), key in live)
                    live.discard(key)
                self.assertEqual({k for k in t if k is not None}, live)
                for k in range(3 * m):
                    self.assertEqual(sol.lp_find(t, k) >= 0, k in live)


if __name__ == "__main__":
    unittest.main()
