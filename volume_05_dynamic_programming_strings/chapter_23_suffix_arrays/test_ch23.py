import random
import unittest

import ch23_examples as ex

NL = "the reading club meets on monday; the club reads maps and poems at the library"


class TestChapter23(unittest.TestCase):
    def test_examples(self) -> None:
        sa = ex.suffix_array_simple("banana")
        self.assertEqual((sa, ex.suffix_array_doubling("banana")), ([5, 3, 1, 0, 4, 2], ([5, 3, 1, 0, 4, 2], 2)))
        self.assertEqual((ex.find_all("banana", sa, "ana"), ex.find_all("banana", sa, "nab")[0], ex.find_all("banana", sa, "a")[0]),
                         (([1, 3], 6), [], [1, 3, 5]))
        sa2, rounds = ex.suffix_array_doubling(NL)
        self.assertEqual((ex.find_all(NL, sa2, "club"), ex.find_all(NL, sa2, "the")[0], rounds), (([12, 38], 13), [0, 34, 67], 3))

    def test_every_case(self) -> None:
        self.assertEqual((ex.suffix_array_doubling(""), ex.suffix_array_doubling("a"), ex.suffix_array_doubling("aaaa")),
                         (([], 0), ([0], 1), ([3, 2, 1, 0], 2)))
        self.assertEqual((ex.find_all("abc", [0, 1, 2], "")[0], ex.find_all("abc", [0, 1, 2], "abcd")[0]), ([0, 1, 2, 3], []))
        self.assertEqual((ex.suffix_array_simple("abab"), ex.find_all("banana", ex.suffix_array_simple("banana"), "na")[0]), ([2, 0, 3, 1], [2, 4]))
        r = random.Random(23)
        for _ in range(200):
            t = "".join(r.choice("ab") for _ in range(r.randint(1, 25)))
            sa = ex.suffix_array_doubling(t)[0]
            self.assertEqual(sa, ex.suffix_array_simple(t))
            p = "".join(r.choice("ab") for _ in range(r.randint(1, 4)))
            self.assertEqual(ex.find_all(t, sa, p)[0], [i for i in range(len(t) - len(p) + 1) if t.startswith(p, i)])


    def test_doubling_and_radix(self) -> None:
        import random
        tr = ex.doubling_trace("banana")
        self.assertEqual([r[2] for r in tr], [[1, 0, 2, 0, 2, 0], [2, 1, 3, 1, 3, 0], [3, 2, 5, 1, 4, 0]])
        self.assertEqual(tr[1][1], [(1, 0), (0, 2), (2, 0), (0, 2), (2, 0), (0, -1)])
        self.assertEqual((ex.suffix_array_radix("banana"), ex.suffix_array_radix(""), ex.suffix_array_radix("a"),
                          ex.suffix_array_radix("abc"), ex.suffix_array_radix("aaaa")),
                         (([5, 3, 1, 0, 4, 2], 2), ([], 0), ([0], 0), ([0, 1, 2], 0), ([3, 2, 1, 0], 2)))
        self.assertEqual([r[2] for r in ex.doubling_trace("abab")], [[0, 1, 0, 1], [0, 2, 0, 1], [1, 3, 0, 2]])
        self.assertEqual(ex.counting_sort([3, 1, 2, 1], lambda x: x, 4), [1, 1, 2, 3])
        r = random.Random(23)
        for _ in range(200):
            t = "".join(r.choice("abc") for _ in range(r.randint(0, 30)))
            self.assertEqual(ex.suffix_array_radix(t)[0], ex.suffix_array_simple(t))


if __name__ == "__main__":
    unittest.main()
