import random
import unittest

import ch29_solutions as sol


class TestMergedSketches(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.merge_kmv([], [], 4), [])
        self.assertEqual(sol.union_and_shared([], [], 4), (0.0, 0.0))
        one = sol.kmv_sketch(["x"], 4)
        self.assertEqual(sol.union_and_shared(one, [], 4), (1.0, 0.0))
        self.assertEqual(sol.union_and_shared(one, one, 4), (1.0, 1.0))
        self.assertEqual(sol.merge_kmv(one, one, 0), [])

    def test_merge_is_the_sketch_of_the_union(self) -> None:
        r = random.Random(3)
        for _ in range(100):
            k = r.randint(1, 12)
            a = [r.randrange(40) for _ in range(r.randint(0, 30))]
            b = [r.randrange(20, 60) for _ in range(r.randint(0, 30))]
            self.assertEqual(sol.merge_kmv(sol.kmv_sketch(a, k), sol.kmv_sketch(b, k), k), sol.kmv_sketch(a + b, k))
            if len(set(a) | set(b)) < k:                       # few distinct readers: both counts are exact
                self.assertEqual(sol.union_and_shared(sol.kmv_sketch(a, k), sol.kmv_sketch(b, k), k),
                                 (float(len(set(a) | set(b))), float(len(set(a) & set(b)))))

    def test_branches(self) -> None:
        r = random.Random(29)
        north = [f"card{r.randrange(20000)}" for _ in range(40000)]
        south = [f"card{r.randrange(10000, 30000)}" for _ in range(40000)]
        union, shared = sol.union_and_shared(sol.kmv_sketch(north, 1024), sol.kmv_sketch(south, 1024), 1024)
        self.assertEqual((len(set(north) | set(south)), len(set(north) & set(south))), (27031, 7465))
        self.assertEqual((round(union), round(shared)), (27989, 8282))


if __name__ == "__main__":
    unittest.main()
