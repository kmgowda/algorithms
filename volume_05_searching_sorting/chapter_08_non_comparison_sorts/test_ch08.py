import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestNonComparison(unittest.TestCase):
    def test_counting_and_radix(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            v = [rng.randint(0, 50) for _ in range(rng.randint(0, 30))]
            self.assertEqual(ex.counting_sort(v, 50), sorted(v))
            big = [rng.randint(0, 10**6) for _ in range(rng.randint(0, 30))]
            self.assertEqual(ex.radix_sort(big), sorted(big))
            self.assertEqual(ex.radix_sort(big, base=256), sorted(big))

    def test_stable_by_key(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            items = [(rng.randint(0, 5), i) for i in range(rng.randint(0, 20))]
            self.assertEqual(ex.counting_sort_by_key(items, lambda p: p[0], 5), sorted(items, key=lambda p: p[0]))

    def test_bucket(self) -> None:
        rng = random.Random(3)
        for _ in range(200):
            v = [rng.random() for _ in range(rng.randint(0, 40))]
            self.assertEqual(ex.bucket_sort(v), sorted(v))

    def test_industry(self) -> None:
        self.assertEqual(ex.sort_by_age([("Ana", 34), ("Ben", 7), ("Cy", 34), ("Dev", 61), ("Eve", 7)]),
                         [("Ben", 7), ("Eve", 7), ("Ana", 34), ("Cy", 34), ("Dev", 61)])
        codes = ["560034", "110001", "560001", "400050"]
        self.assertEqual(ex.sort_postcodes(codes), sorted(codes))
        self.assertEqual(ex.sort_postcodes([]), [])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        rng = random.Random(4)
        for _ in range(200):
            v = [rng.randint(-20, 20) for _ in range(rng.randint(0, 15))]
            self.assertEqual(sol.sort_with_negatives(v), sorted(v))
            c = [rng.randint(0, 12) for _ in range(rng.randint(0, 10))]
            s = sorted(c, reverse=True)
            h = 0
            while h < len(s) and s[h] >= h + 1:
                h += 1
            self.assertEqual(sol.h_index_counting(c), h)
        self.assertEqual(sol.sort_grades(list("CABFAB")), list("AABBCF"))
        self.assertEqual(sol.maximum_gap([3, 6, 9, 1]), 3)
        self.assertEqual(sol.maximum_gap([10]), 0)


if __name__ == "__main__":
    unittest.main()
