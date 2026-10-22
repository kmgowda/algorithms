import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


def looped(n: int, back_to: int):
    return ex.with_loop(list(range(n)), back_to)


class TestThinkingProblems(unittest.TestCase):
    def test_floyd_meeting_matches_theorem(self) -> None:
        for n in range(1, 13):
            for mu in range(n):
                lam = n - mu
                d = lam * max(1, -(-mu // lam))
                self.assertEqual(sol.first_meeting(looped(n, mu)), d)
                self.assertLessEqual(d, n)
                node, length, meet, to_start = ex.loop_start(looped(n, mu))
                self.assertEqual((node.value, length, meet, to_start), (mu, lam, d, mu))

    def test_speed_three_always_meets(self) -> None:
        for n in range(1, 13):
            for mu in range(n):
                d = sol.first_meeting(looped(n, mu), speed=3)
                self.assertIsNotNone(d)
                self.assertLessEqual(d, n)
                self.assertEqual((2 * d) % (n - mu), 0)

    def test_no_loop(self) -> None:
        self.assertIsNone(sol.first_meeting(None))
        self.assertIsNone(sol.first_meeting(ex.build([1, 2, 3]), speed=3))

    def test_palindrome_smallest(self) -> None:
        self.assertTrue(sol.is_palindrome_train(None))
        self.assertTrue(sol.is_palindrome_train(ex.build([7])))
        self.assertTrue(sol.is_palindrome_train(ex.build([7, 7])))
        self.assertFalse(sol.is_palindrome_train(ex.build([7, 8])))

    def test_palindrome_examples_and_restore(self) -> None:
        t = ex.build([12, 25, 47, 25, 12])
        self.assertTrue(sol.is_palindrome_train(t))
        self.assertEqual(ex.values_of(t), [12, 25, 47, 25, 12])
        self.assertFalse(sol.is_palindrome_train(ex.build([12, 25, 25, 13])))

    def test_palindrome_random(self) -> None:
        rng = random.Random(5)
        for _ in range(400):
            vals = [rng.randint(0, 2) for _ in range(rng.randint(0, 9))]
            t = ex.build(vals)
            self.assertEqual(sol.is_palindrome_train(t), vals == vals[::-1])
            self.assertEqual(ex.values_of(t), vals)

    def test_speed_three_phase_two_is_wrong(self) -> None:
        train = ex.with_loop([12, 25, 31, 47, 58], 1)
        self.assertEqual(sol.first_meeting(train, speed=3), 2)
        self.assertIsNone(sol.loop_start_speed3(train))
        self.assertEqual(ex.loop_start(train)[0].value, 25)
        broken = ex.with_loop([12, 25, 47, 58, 63, 70, 84, 91], 3)   # odd loop: the bug hides
        self.assertEqual(sol.loop_start_speed3(broken).value, 58)


if __name__ == "__main__":
    unittest.main()
