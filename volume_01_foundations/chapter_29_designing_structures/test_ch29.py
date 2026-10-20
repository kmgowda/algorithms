import random
import unittest

import ch29_examples as ex


class TestChapter29(unittest.TestCase):
    def test_min_stack_against_reference(self) -> None:
        rng = random.Random(1)
        s, ref = ex.MinStack(), []
        for _ in range(3000):
            if ref and rng.random() < 0.45:
                self.assertEqual(s.pop(), ref.pop())
            else:
                v = rng.randint(0, 99)
                s.push(v)
                ref.append(v)
            if ref:
                self.assertEqual((s.top(), s.min()), (ref[-1], min(ref)))

    def test_min_queue_against_reference(self) -> None:
        rng = random.Random(2)
        q, ref = ex.MinQueue(), []
        for _ in range(3000):
            if ref and rng.random() < 0.45:
                self.assertEqual(q.dequeue(), ref.pop(0))
            else:
                v = rng.randint(0, 99)
                q.enqueue(v)
                ref.append(v)
            if ref:
                self.assertEqual(q.min(), min(ref))

    def test_browser(self) -> None:
        h = ex.BrowserHistory("A")
        h.visit("B"); h.visit("C")
        self.assertEqual(h.back(), "B")
        self.assertEqual(h.back(), "A")
        h.visit("D")
        self.assertEqual(h.forward(), "D")
        self.assertEqual(h.back(), "A")
        h2 = ex.BrowserHistory("A")
        h2.visit("B"); h2.back(); h2.visit("C"); h2.back()
        self.assertEqual(h2.forward(), "C")


if __name__ == "__main__":
    unittest.main()
