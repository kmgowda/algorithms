import random
import unittest

import ch19_examples as ex
import ch19_solutions as sol


class TestChapter19Solutions(unittest.TestCase):
    def test_beam(self) -> None:
        self.assertEqual((sol.cut_beam(10, [2, 4, 7]), sol.cut_beam_brute(10, [2, 4, 7])), (20, 20))
        self.assertEqual([sol.cut_beam(5, m) for m in ([], [3], [1, 2])], [0, 5, 7])
        self.assertEqual(sol.cut_beam(0, []), 0)
        r = random.Random(19)
        for _ in range(300):
            length = r.randint(1, 40)
            marks = r.sample(range(1, length), min(length - 1, r.randint(0, 7))) if length > 1 else []
            self.assertEqual(sol.cut_beam(length, marks), sol.cut_beam_brute(length, marks))

    def test_knuth_fails_on_matrix_chain(self) -> None:
        d = [1, 3, 2, 4, 5]
        self.assertEqual((ex.matrix_chain(d)[0], ex.matrix_chain(d)[3], sol.matrix_chain_knuth(d)), (34, "(((A B) C) D)", 56))
        cost, table, split, _ = ex.matrix_chain(d)
        self.assertEqual((split[1][3], split[2][4], split[1][4]), (2, 2, 3))
        self.assertEqual([sol.matrix_chain_knuth(x) for x in ([], [4], [4, 5], [4, 5, 6])], [0, 0, 0, 120])


if __name__ == "__main__":
    unittest.main()
