import bisect
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


class TestChapter4Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        for shelf, batch, result, writes in [([], [], [], 0), ([12], [], [12], 0), ([], [40], [40], 1),
                                             ([12], [5], [5, 12], 2), ([12], [40], [12, 40], 1),
                                             ([58], [58], [58, 58], 1)]:
            s = list(shelf)
            self.assertEqual(sol.insert_batch(s, list(batch)), writes)
            self.assertEqual(s, result)

    def test_worked_examples(self) -> None:
        s = list(sol.SHELF)
        self.assertEqual(sol.insert_batch(s, [40, 60, 95]), 9)
        self.assertEqual(s, [12, 25, 31, 40, 47, 58, 60, 63, 70, 84, 91, 95])
        s = list(range(1000, 2000))
        self.assertEqual(sol.insert_batch(s, list(range(100))), 1100)
        self.assertEqual(s, list(range(100)) + list(range(1000, 2000)))

    def test_against_repeated_insert_sorted(self) -> None:
        rng = random.Random(4)
        for _ in range(500):
            shelf = sorted(rng.randint(0, 40) for _ in range(rng.randint(0, 10)))
            batch = sorted(rng.randint(0, 40) for _ in range(rng.randint(0, 6)))
            expected = list(shelf)
            for b in batch:
                bisect.insort_right(expected, b)
            slow = list(shelf)
            shifts = sum(ex.insert_sorted(slow, b) for b in batch)
            s = list(shelf)
            writes = sol.insert_batch(s, list(batch))
            self.assertEqual(s, expected)
            self.assertEqual(slow, expected)
            self.assertLessEqual(writes, len(shelf) + len(batch))
            self.assertLessEqual(writes, shifts + len(batch))

    def test_growing_by_a_fixed_step(self) -> None:
        self.assertEqual(sol.items_copied_growing_by(0, 10), 0)
        self.assertEqual(sol.items_copied_growing_by(10, 10), 0)
        self.assertEqual(sol.items_copied_growing_by(11, 10), 10)
        self.assertEqual(sol.items_copied_growing_by(1000, 10), 49_500)
        self.assertEqual(sol.items_copied_growing_by(10_000, 10), 4_995_000)


if __name__ == "__main__":
    unittest.main()
