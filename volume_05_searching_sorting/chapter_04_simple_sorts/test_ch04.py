import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


class TestSimpleSorts(unittest.TestCase):
    def test_correct(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            v = [rng.randint(-5, 5) for _ in range(rng.randint(0, 15))]
            for sort in (ex.bubble_sort, ex.selection_sort, ex.insertion_sort):
                self.assertEqual(sort(v)[0], sorted(v))
            self.assertEqual(ex.insertion_sort(v)[2], sol.count_inversions_slow(v))
            self.assertEqual(ex.bubble_sort(v)[2], sol.count_inversions_slow(v))

    def test_stability(self) -> None:
        cards = [(3, "a"), (1, "b"), (3, "c"), (1, "d")]

        class Card:
            def __init__(self, rank, tag):
                self.rank, self.tag = rank, tag

            def __lt__(self, other):
                return self.rank < other.rank

            def __gt__(self, other):
                return self.rank > other.rank

            def __le__(self, other):
                return self.rank <= other.rank

        objs = [Card(r, t) for r, t in cards]
        for sort in (ex.bubble_sort, ex.insertion_sort):
            self.assertEqual([c.tag for c in sort(objs)[0]], ["b", "d", "a", "c"])

    def test_work_table(self) -> None:
        t = ex.work_table(50)
        n = 50
        self.assertEqual(t["selection"]["sorted"][0], n * (n - 1) // 2)
        self.assertEqual(t["insertion"]["sorted"], (n - 1, 0))
        self.assertEqual(t["bubble"]["sorted"], (n - 1, 0))
        self.assertEqual(t["insertion"]["reversed"][1], n * (n - 1) // 2)
        self.assertLessEqual(t["selection"]["reversed"][1], n - 1)

    def test_late_entries(self) -> None:
        self.assertEqual(ex.add_late_entries([10, 20, 30, 40, 50, 60], [35, 5]), [5, 10, 20, 30, 35, 40, 50, 60])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.count_inversions_slow([3, 1, 2]), 2)
        self.assertEqual(sol.insertion_sort_desc([3, 1, 2]), [3, 2, 1])
        self.assertEqual(sol.sort_k_sorted([2, 1, 4, 3, 6, 5], 1), [1, 2, 3, 4, 5, 6])
        self.assertEqual(sol.bubble_passes([1, 2, 3, 4]), 1)
        self.assertEqual(sol.bubble_passes([4, 3, 2, 1]), 3)


if __name__ == "__main__":
    unittest.main()
