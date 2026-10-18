import random
import unittest

import ch10_examples as ex
import ch10_solutions as sol


class TestGrowth(unittest.TestCase):
    def test_constant(self) -> None:
        self.assertEqual(ex.first_in_line(["a", "b"]), ("a", 1))
        self.assertEqual(ex.gauss_sum(100), (5050, 3))
        self.assertEqual(ex.gauss_sum(10_000)[1], 3)

    def test_linear_steps_double(self) -> None:
        self.assertEqual(ex.loop_sum(100), (5050, 100))
        self.assertEqual(ex.loop_sum(200)[1], 2 * ex.loop_sum(100)[1])

    def test_quadratic(self) -> None:
        for n in range(0, 30):
            count, steps = ex.handshakes([str(i) for i in range(n)])
            self.assertEqual(count, n * (n - 1) // 2)
            self.assertEqual(steps, count)

    def test_duplicates_agree(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            items = [str(rng.randint(0, 40)) for _ in range(rng.randint(0, 20))]
            self.assertEqual(ex.has_duplicate_slow(items)[0], ex.has_duplicate_fast(items)[0])
        unique = [str(i) for i in range(100)]
        self.assertEqual(ex.has_duplicate_slow(unique)[1], 100 * 99 // 2)
        self.assertEqual(ex.has_duplicate_fast(unique)[1], 100)

    def test_logarithmic(self) -> None:
        self.assertEqual(ex.halvings(1), 0)
        self.assertEqual(ex.halvings(8), 3)
        self.assertEqual(ex.halvings(1_000_000), 19)
        worst = max(ex.guess_the_number(secret) for secret in range(1, 101))
        self.assertEqual(worst, 7)
        with self.assertRaises(ValueError):
            ex.guess_the_number(500)

    def test_exponential_and_space(self) -> None:
        self.assertEqual(ex.all_outfits(["hat", "scarf", "gloves"]), 8)
        items = [1, 2, 3, 4]
        self.assertEqual(ex.reverse_copy(items), [4, 3, 2, 1])
        self.assertEqual(items, [1, 2, 3, 4])
        ex.reverse_in_place(items)
        self.assertEqual(items, [4, 3, 2, 1])

    def test_growth_table(self) -> None:
        row = ex.growth_table([1024])[0]
        self.assertEqual(row["O(log n)"], 10)
        self.assertEqual(row["O(n log n)"], 10240)
        self.assertEqual(row["O(n^2)"], 1024 * 1024)

    def test_time_it_returns_seconds(self) -> None:
        self.assertGreaterEqual(ex.time_it(ex.loop_sum, 1000, repeats=1), 0.0)


class TestSolutions(unittest.TestCase):
    def test_small(self) -> None:
        self.assertEqual(sol.last_item([1, 2, 3]), 3)
        self.assertEqual(sol.count_evens([1, 2, 4, 7]), 2)
        self.assertEqual(sol.multiplication_grid(2), [[1, 2], [2, 4]])
        self.assertEqual([sol.digits_in(x) for x in (0, 9, 10, 12345, -700)], [1, 1, 2, 5, 3])

    def test_common_students(self) -> None:
        self.assertEqual(sol.common_students(["Ana", "Ben"], ["Ben", "Cy"]), {"Ben"})
        self.assertEqual(sol.common_students([], ["Ben"]), set())

    def test_pair_with_sum(self) -> None:
        self.assertEqual(sol.pair_with_sum([300, 150, 700, 450], 750), (0, 3))
        self.assertIsNone(sol.pair_with_sum([100, 200], 1000))
        self.assertIsNone(sol.pair_with_sum([375], 750))
        self.assertEqual(sol.pair_with_sum([375, 375], 750), (0, 1))

    def test_simplify(self) -> None:
        self.assertEqual(sol.simplify({"n^2": 3, "n": 5, "1": 100}), "O(n^2)")
        self.assertEqual(sol.simplify({"n": 2, "log n": 9}), "O(n)")
        self.assertEqual(sol.simplify({"1": 500}), "O(1)")


if __name__ == "__main__":
    unittest.main()
