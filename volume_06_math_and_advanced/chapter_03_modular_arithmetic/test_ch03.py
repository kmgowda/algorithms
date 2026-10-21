import random
import unittest

import ch03_examples as ex


class TestChapter3(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.clock(9, 5), ex.clock(11, 25), ex.clock(3, -5)), (2, 0, 10))
        self.assertEqual((ex.last_digit_table(7), ex.last_digit_table(3)), ([7, 9, 3, 1] * 2, [3, 9, 7, 1] * 2))
        self.assertEqual((ex.power_mod_naive(7, 100, 10), ex.power_mod(7, 100, 10), ex.power_mod(3, 1000, 1000007)), ((1, 100), (1, 9), (297623, 15)))
        self.assertEqual(ex.power_mod(2, 10 ** 18, 10 ** 9 + 7), (719476260, 83))

    def test_every_case(self) -> None:
        self.assertEqual([ex.power_mod(*a) for a in ((5, 0, 7), (5, 3, 1), (0, 0, 7), (-2, 3, 7))], [(1, 0), (0, 3), (1, 0), (6, 3)])
        for a in ((5, -1, 7), (5, 3, 0)):
            with self.assertRaises(ValueError):
                ex.power_mod(*a)
        self.assertEqual((ex.power_mod(10, 100, 7)[0], ex.power_mod(3, 13, 7)[0], ex.power_mod(3, 6, 7)[0], ex.last_digit_table(3, 4)[-1]), (4, 3, 1, 1))
        r = random.Random(3)
        for _ in range(300):
            b, e, m = r.randint(-50, 50), r.randint(0, 500), r.randint(1, 1000)
            self.assertEqual(ex.power_mod(b, e, m)[0], pow(b, e, m))


if __name__ == "__main__":
    unittest.main()
