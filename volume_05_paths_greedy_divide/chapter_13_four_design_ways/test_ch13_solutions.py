import random
import unittest

import ch13_examples as ex
import ch13_solutions as sol


class TestChapter13Solutions(unittest.TestCase):
    def test_club(self) -> None:
        self.assertEqual(sol.meet_in_the_middle(ex.BOOKS, 20), 16)
        self.assertEqual(sol.meet_in_the_middle(ex.BOOKS, 25), 19)

    def test_smallest(self) -> None:
        self.assertEqual(sol.meet_in_the_middle([], 20), 0)
        self.assertEqual(sol.meet_in_the_middle([("A", 5, 3)], 4), 0)
        self.assertEqual(sol.meet_in_the_middle([("A", 5, 3)], 5), 3)
        self.assertEqual(sol.meet_in_the_middle(ex.BOOKS, 0), 0)

    def test_random_against_brute_force(self) -> None:
        rng = random.Random(13)
        for _ in range(300):
            books = [(str(i), rng.randint(1, 12), rng.randint(0, 9)) for i in range(rng.randint(0, 9))]
            budget = rng.randint(0, 40)
            self.assertEqual(sol.meet_in_the_middle(books, budget), ex.brute_force(books, budget)[0])

    def test_equal_prices_most_votes_is_optimal(self) -> None:
        rng = random.Random(14)
        for _ in range(200):
            p = rng.randint(1, 6)
            books = [(str(i), p, rng.randint(0, 9)) for i in range(rng.randint(0, 8))]
            budget = rng.randint(0, 30)
            self.assertEqual(ex.greedy(books, budget, key=lambda b: -b[2])[0], ex.brute_force(books, budget)[0])

    def test_ratio_trap_and_repair(self) -> None:
        trap = [("Bookmark", 1, 2), ("Encyclopedia", 20, 20)]
        self.assertEqual(ex.greedy(trap, 20, key=lambda b: -b[2] / b[1])[0], 2)
        self.assertEqual(sol.ratio_greedy_with_best_single(trap, 20), 20)
        rng = random.Random(15)
        for _ in range(300):
            books = [(str(i), rng.randint(1, 12), rng.randint(0, 9)) for i in range(rng.randint(0, 8))]
            budget = rng.randint(0, 30)
            self.assertGreaterEqual(2 * sol.ratio_greedy_with_best_single(books, budget), ex.brute_force(books, budget)[0])


if __name__ == "__main__":
    unittest.main()
