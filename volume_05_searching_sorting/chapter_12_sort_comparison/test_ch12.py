import random
import unittest

import ch12_examples as ex
import ch12_solutions as sol


class TestSorts(unittest.TestCase):
    def test_all_correct(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            v = [rng.randint(0, 100) for _ in range(rng.randint(0, 40))]
            for name, sort in ex.SORTS.items():
                self.assertEqual(sort(v), sorted(v), name)

    def test_inputs(self) -> None:
        for kind in ("random", "sorted", "reversed", "nearly sorted", "few distinct"):
            self.assertEqual(len(ex.make_input(kind, 100)), 100)
        with self.assertRaises(ValueError):
            ex.make_input("weird", 5)

    def test_race_shape(self) -> None:
        r = ex.race(1500, ["random", "sorted"], ["insertion", "merge", "built-in sorted (Timsort)"])
        self.assertLess(r["merge"]["random"], r["insertion"]["random"])
        self.assertLess(r["built-in sorted (Timsort)"]["sorted"], r["merge"]["sorted"])
        self.assertLess(r["insertion"]["sorted"], r["insertion"]["random"])

    def test_recommend(self) -> None:
        self.assertEqual(ex.recommend(n=10), "insertion sort")
        self.assertEqual(ex.recommend(n=10**6, small_int_keys=True), "counting or radix sort")
        self.assertEqual(ex.recommend(n=10**6, memory_tight=True, worst_case_guarantee=True), "heapsort")
        self.assertTrue(ex.recommend(n=10**6).startswith("Timsort"))


class TestSolutions(unittest.TestCase):
    def test_doubling(self) -> None:
        self.assertGreater(sol.doubling_ratio("insertion", 800), 2.8)
        self.assertLess(sol.doubling_ratio("merge", 4000), 3.0)

    def test_crossover(self) -> None:
        n = sol.crossover("insertion", "merge", [8, 16, 32, 64, 128, 256, 512, 1024])
        self.assertIsNotNone(n)


if __name__ == "__main__":
    unittest.main()
