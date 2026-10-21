import random
import unittest

import ch05_examples as ex


class TestChapter5(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.crt([2, 3, 2], [3, 5, 7]), ex.crt([1, 2, 3, 4], [2, 3, 5, 7])), ((23, 105), (53, 210)))
        self.assertEqual((ex.crt([3, 4], [6, 8]), ex.crt([1, 2], [4, 6]), ex.crt([2, 4], [6, 8])), ((None, 24), (None, 12), (20, 24)))

    def test_every_case(self) -> None:
        self.assertEqual([ex.crt(r, m) for r, m in (([], []), ([5], [7]), ([12], [7]), ([0, 0, 0], [3, 5, 7]), ([1, 1], [2, 4]))],
                         [(0, 1), (5, 7), (5, 7), (0, 105), (1, 4)])
        with self.assertRaises(ValueError):
            ex.crt([1], [0])
        self.assertEqual((ex.crt([1, 2], [2, 3]), ex.crt([900000 % 97, 900000 % 98, 900000 % 99], [97, 98, 99])[0]), ((5, 6), 900000))
        r = random.Random(5)
        for _ in range(300):
            mods = [r.randint(1, 12) for _ in range(r.randint(1, 3))]
            rems = [r.randint(0, 20) for _ in mods]
            self.assertEqual(ex.crt(rems, mods)[0], ex.crt_by_search(rems, mods))


if __name__ == "__main__":
    unittest.main()
