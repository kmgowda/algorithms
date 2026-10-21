import random
import unittest

import ch08_examples as ex


class TestChapter8(unittest.TestCase):
    def test_keys(self) -> None:
        public, private = ex.make_keys(61, 53)
        self.assertEqual((public, private), ((3233, 17), (3233, 2753)))
        self.assertEqual((ex.encrypt(65, public), ex.decrypt(2790, private)), (2790, 65))
        code = [ex.encrypt(m, public) for m in ex.text_to_numbers("MEET AT 9")]
        self.assertEqual(code, [3123, 28, 28, 2159, 1992, 2790, 2159, 1992, 1175])
        self.assertEqual("".join(chr(ex.decrypt(c, private)) for c in code), "MEET AT 9")
        self.assertEqual(ex.factor_by_trial(3233), (53, 61))

    def test_every_case(self) -> None:
        public, private = ex.make_keys(61, 53)
        self.assertEqual((ex.encrypt(0, public), ex.encrypt(1, public), ex.encrypt(3232, public)), (0, 1, 3232))
        with self.assertRaises(ValueError):
            ex.make_keys(61, 53, 3)
        with self.assertRaises(ValueError):
            ex.encrypt(3233, public)
        for m in range(3233):
            self.assertEqual(ex.decrypt(ex.encrypt(m, public), private), m)


if __name__ == "__main__":
    unittest.main()
