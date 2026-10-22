import random
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_sorted_insert_shifts(self) -> None:
        self.assertEqual(sol.sorted_insert_shifts([]), 0)
        self.assertEqual(sol.sorted_insert_shifts([5]), 0)
        self.assertEqual(sol.sorted_insert_shifts(sorted(ex.SHELF)), 0)
        self.assertEqual(sol.sorted_insert_shifts(sorted(ex.SHELF, reverse=True)), 36)
        for n in range(12):
            self.assertEqual(sol.sorted_insert_shifts(list(range(n, 0, -1))), n * (n - 1) // 2)

    def test_seat_desk_smallest(self) -> None:
        self.assertIsNone(sol.SeatDesk(0).any_free())
        d = sol.SeatDesk(1)
        self.assertEqual(d.any_free(), 0)
        self.assertTrue(d.occupy(0))
        self.assertFalse(d.occupy(0))
        self.assertIsNone(d.any_free())
        self.assertTrue(d.leave(0))
        self.assertFalse(d.leave(0))
        self.assertEqual(d.any_free(), 0)

    def test_seat_desk_trace(self) -> None:
        d = sol.SeatDesk(4)
        d.occupy(1)
        self.assertEqual((d.free[:d.count], d.where), ([0, 3, 2], [0, -1, 2, 1]))
        d.occupy(3)
        d.leave(1)
        d.occupy(0)
        self.assertEqual((d.free[:d.count], d.any_free()), ([1, 2], 2))

    def test_seat_desk_against_a_set(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            n = rng.randint(1, 8)
            d, free = sol.SeatDesk(n), set(range(n))
            for _ in range(30):
                s = rng.randrange(n)
                if rng.random() < 0.5:
                    self.assertEqual(d.occupy(s), s in free)
                    free.discard(s)
                else:
                    self.assertEqual(d.leave(s), s not in free)
                    free.add(s)
                self.assertEqual(set(d.free[:d.count]), free)
                a = d.any_free()
                self.assertTrue(a in free if free else a is None)

    def test_list_queue_shifts(self) -> None:
        self.assertEqual(sol.list_queue_shifts(0), 0)
        self.assertEqual(sol.list_queue_shifts(1), 0)
        self.assertEqual(sol.list_queue_shifts(4), 6)
        self.assertEqual(sol.list_queue_shifts(1000), 499_500)


if __name__ == "__main__":
    unittest.main()
