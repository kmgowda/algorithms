import unittest

import ch28_examples as ex


class TestChapter28(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual([ex.front_insert_moves(n) for n in (0, 1, 2, 10, 50000)], [0, 0, 1, 45, 1249975000])
        self.assertEqual((ex.returns_desk([47, 12, 63], True), ex.returns_desk([47, 12, 63], False)),
                         ([63, 12, 47], [47, 12, 63]))
        self.assertEqual((ex.returns_desk([7], True), ex.returns_desk([7], False), ex.returns_desk([], True)), ([7], [7], []))

    def test_simple(self) -> None:
        self.assertEqual(ex.front_insert_moves(50_000), 1_249_975_000)
        self.assertEqual(ex.returns_desk([47, 12, 63], True), [63, 12, 47])
        self.assertEqual(ex.returns_desk([47, 12, 63], False), [47, 12, 63])

    def test_timings_show_the_shape(self) -> None:
        t = ex.time_operations(20_000)
        self.assertGreater(t["insert at front: Python list"], 5 * t["insert at front: deque"])


if __name__ == "__main__":
    unittest.main()
