import unittest

import ch02_examples as ex


class TestChapter2(unittest.TestCase):
    def test_binary(self) -> None:
        for n in range(0, 2000):
            self.assertEqual(ex.to_binary(n), bin(n)[2:])
            self.assertEqual(ex.from_binary(ex.to_binary(n)), n)
        self.assertEqual(ex.from_binary("01001101"), 77)
        self.assertEqual(ex.from_binary("00101010"), 42)
        self.assertEqual(ex.to_binary(13), "1101")

    def test_trace(self) -> None:
        self.assertEqual(ex.trace_sum(ex.SHELF, 3), [0, 12, 37, 68])
        self.assertEqual(ex.trace_sum(ex.SHELF, 3, start=7)[-1], 75)


if __name__ == "__main__":
    unittest.main()
