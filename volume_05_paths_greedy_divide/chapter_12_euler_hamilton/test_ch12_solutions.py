import itertools
import unittest

import ch12_examples as ex
import ch12_solutions as sol


class TestChapter12Solutions(unittest.TestCase):
    def check(self, k, n):
        s = sol.de_bruijn(k, n)
        self.assertEqual(len(s), k ** n + n - 1)
        codes = [s[i:i + n] for i in range(len(s) - n + 1)]
        digits = "0123456789abcdefghijklmnopqrstuvwxyz"[:k]
        self.assertEqual(sorted(codes), sorted("".join(p) for p in itertools.product(digits, repeat=n)))

    def test_de_bruijn(self) -> None:
        self.assertEqual(sol.de_bruijn(2, 3), "0001011100")
        for k, n in [(2, 1), (2, 2), (2, 4), (3, 2), (3, 3), (10, 3), (4, 4)]:
            self.check(k, n)

    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.de_bruijn(1, 1), "0")
        self.assertEqual(sol.de_bruijn(1, 4), "0000")
        self.assertEqual(sol.de_bruijn(3, 1), "012")
        self.assertEqual((sol.de_bruijn(0, 3), sol.de_bruijn(2, 0)), ("", ""))

    def test_windmill(self) -> None:
        for blades, paths in [(1, 3), (2, 4), (3, 0)]:
            places, roads = sol.windmill(blades)
            self.assertTrue(ex.one_piece(roads))
            self.assertTrue(min(ex.degrees(places, roads).values()) >= 2)
            self.assertEqual(len(ex.hamiltonian_paths(places, roads)), paths)


if __name__ == "__main__":
    unittest.main()
