import math
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


class TestDepth(unittest.TestCase):
    def test_crt_decryption(self) -> None:
        m, v = ex.decrypt_crt(2790, 61, 53, 2753)
        self.assertEqual((m, v), (65, {"dp": 53, "dq": 49, "m1": 4, "m2": 12, "q_inv": 38, "h": 1}))
        public, _ = ex.make_keys(61, 53)
        for msg in range(3233):
            self.assertEqual(ex.decrypt_crt(ex.encrypt(msg, public), 61, 53, 2753)[0], msg)

    def test_chapter_numbers(self) -> None:
        public, private = ex.make_keys(61, 53)
        s_ = ex.decrypt(65, private)                      # signing uses the private power
        self.assertEqual((s_, ex.encrypt(s_, public)), (588, 65))
        pub, priv = ex.make_keys(5, 11, 3)
        self.assertEqual((priv, ex.encrypt(7, pub), ex.decrypt(13, priv)), ((55, 27), 13, 7))
        self.assertEqual((ex.factor_from_phi(77, 60), sum(1 for e in range(1, 3121) if math.gcd(e, 3120) == 1)), ((7, 11), 768))

    def test_attacks_and_phi(self) -> None:
        public, private = ex.make_keys(61, 53)
        self.assertEqual(ex.factor_from_phi(3233, 3120), (53, 61))
        self.assertIsNone(ex.factor_from_phi(3233, 3000))
        self.assertEqual((ex.encrypt(61, public), ex.decrypt(610, private)), (610, 61))       # p divides the message
        pub3, _ = ex.make_keys(1019, 1031, 3)
        self.assertEqual((pub3, ex.encrypt(97, pub3), ex.integer_cube_root(912673)), ((1050589, 3), 912673, 97))
        self.assertEqual(ex.encrypt(2, public) * ex.encrypt(65, public) % 3233, ex.encrypt(130, public))
        self.assertEqual((ex.fermat_factor(3233), ex.fermat_factor(1019 * 1031)), ((53, 61, 1), (1019, 1031, 1)))
        self.assertEqual([ex.integer_cube_root(x) for x in (0, 1, 7, 8, 26, 27, 10 ** 30)], [0, 1, 1, 2, 2, 3, 10 ** 10])


    def test_diffie_hellman(self) -> None:
        import random
        self.assertEqual(ex.diffie_hellman(23, 5, 6, 15), (8, 19, 2, 2))
        self.assertEqual(ex.discrete_log_brute(5, 8, 23)[0], 6)
        self.assertEqual(ex.baby_step_giant_step(5, 8, 23)[0], 6)
        r = random.Random(8)
        p, g = 1_000_003, 2
        for _ in range(20):
            x = r.randrange(p - 1)
            h = pow(g, x, p)
            got, work = ex.baby_step_giant_step(g, h, p)
            self.assertEqual(pow(g, got, p), h)
            self.assertLessEqual(work, 2 * 1001 + 2)


if __name__ == "__main__":
    unittest.main()
