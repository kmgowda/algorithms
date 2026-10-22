import itertools
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


def is_latin(g):
    n = len(g)
    want = set(range(1, n + 1))
    return all(set(row) == want for row in g) and all({g[r][c] for r in range(n)} == want for c in range(n))


class TestChapter04Solutions(unittest.TestCase):
    def test_latin_square(self) -> None:
        self.assertEqual(sol.latin_square([]), ([], 0))
        self.assertEqual(sol.latin_square([[0]])[0], [[1]])
        self.assertEqual(sol.latin_square([[1, 1], [0, 0]]), (None, 0))
        self.assertIsNone(sol.latin_square([[1, 0], [0, 2]])[0])
        self.assertEqual(sol.latin_square([[1, 0], [0, 1]])[0], [[1, 2], [2, 1]])
        g, _ = sol.latin_square([[0] * 5 for _ in range(5)])
        self.assertTrue(is_latin(g))
        r = random.Random(4)
        for _ in range(40):
            n = r.randint(1, 5)
            base = [[(i + j) % n + 1 for j in range(n)] for i in range(n)]
            puzzle = [[v if r.random() < 0.4 else 0 for v in row] for row in base]
            g, _ = sol.latin_square(puzzle)
            self.assertTrue(is_latin(g))
            self.assertTrue(all(puzzle[i][j] in (0, g[i][j]) for i in range(n) for j in range(n)))

    def test_queens_thinking(self) -> None:
        counts = [len(ex.queens(n)[0]) for n in range(2, 10)]
        self.assertTrue(all(c % 2 == 0 for c in counts))
        self.assertEqual(sol.queens_shared_set(4), 0)
        self.assertEqual(len(ex.queens(4)[0]), 2)


if __name__ == "__main__":
    unittest.main()
