import unittest

import ch10_examples as ex


class TestChapter2(unittest.TestCase):
    def test_tables(self) -> None:
        self.assertEqual(ex.ways_table(10), [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89])
        self.assertEqual(ex.ways_two_numbers(10), 89)
        self.assertEqual(len(str(ex.ways_table(5000)[-1])), 1045)
        self.assertEqual(ex.least_effort(ex.EFFORT), (10, [0, 3, 9, 5, 12, 9, 17, 10, 16, 10], [1, 3, 5, 7]))

    def test_every_case(self) -> None:
        self.assertEqual((ex.ways_two_numbers(1), ex.ways_two_numbers(0), ex.ways_table(0), ex.ways_table(9, (2,))[-1]), (1, 1, [1], 0))
        self.assertEqual((ex.least_effort([])[0], ex.least_effort([5])[::2], ex.least_effort([5, 1])[::2]), (0, (0, []), (1, [2])))
        e = list(ex.EFFORT)
        e[5] = 2
        self.assertEqual((ex.least_effort(e)[0], ex.ways_table(12)[-2:]), (10, [144, 233]))
        for n in range(2, 30):
            self.assertEqual(ex.ways_two_numbers(n), ex.ways_table(n)[-1])


    def test_top_down_equals_bottom_up(self) -> None:
        import random
        r = random.Random(2)
        self.assertEqual((ex.least_effort_memo(ex.EFFORT), ex.least_effort_memo([]), ex.least_effort_memo([5])), (10, 0, 0))
        for _ in range(300):
            a = [r.randint(0, 9) for _ in range(r.randint(0, 12))]
            self.assertEqual(ex.least_effort(a)[0], ex.least_effort_memo(a))


if __name__ == "__main__":
    unittest.main()
