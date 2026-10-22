import random
import unittest

import ch11_examples as ex


class TestChapter29(unittest.TestCase):
    def test_every_case(self) -> None:
        s = ex.MinStack()
        for v in (47, 63, 12, 25):
            s.push(v)
        mins = [s.min()]
        s.pop(); mins.append(s.min()); s.pop(); mins.append(s.min())
        self.assertEqual(mins, [12, 12, 47])
        d = ex.MinStack()
        for v in (5, 5, 5):
            d.push(v)
        d.pop()
        self.assertEqual(d.min(), 5)
        with self.assertRaises(IndexError):
            ex.MinStack().min()
        b = ex.BrowserHistory("home")
        self.assertEqual((b.back(), b.forward()), ("home", "home"))
        b.visit("a"); b.visit("b")
        self.assertEqual([b.back(), b.back(), b.back(), b.forward()], ["a", "home", "home", "a"])
        b.visit("c")
        self.assertEqual(b.forward(), "c")
        q = ex.MinQueue()
        for v in (5, 3, 8):
            q.enqueue(v)
        self.assertEqual([q.min(), q.dequeue(), q.min(), q.dequeue(), q.min()], [3, 5, 3, 3, 8])
        with self.assertRaises(ValueError):
            ex.MinQueue().min()

    def test_practice_traces(self) -> None:
        m, mins = ex.MinStack(), []
        for v in (30, 20, 20, 40):
            m.push(v)
            mins.append(m.min())
        for _ in range(3):
            m.pop()
            mins.append(m.min())
        self.assertEqual(mins, [30, 20, 20, 20, 20, 20, 30])

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
