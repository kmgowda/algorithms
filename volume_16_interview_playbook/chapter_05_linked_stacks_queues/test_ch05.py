import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


class TestLinkedStacksQueues(unittest.TestCase):
    def test_lists(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            vals = [rng.randint(0, 9) for _ in range(rng.randint(0, 10))]
            self.assertEqual(ex.to_list(ex.reverse_list(ex.build(vals))), vals[::-1])
            other = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 6)))
            self.assertEqual(ex.to_list(ex.merge_two(ex.build(sorted(vals)), ex.build(other))), sorted(vals + other))
            self.assertFalse(ex.has_cycle(ex.build(vals)))
            if vals:
                head = ex.build(vals)
                nodes = []
                cur = head
                while cur:
                    nodes.append(cur)
                    cur = cur.next
                nodes[-1].next = nodes[rng.randrange(len(nodes))]
                self.assertTrue(ex.has_cycle(head))
                n = rng.randint(1, len(vals))
                self.assertEqual(ex.to_list(ex.remove_nth_from_end(ex.build(vals), n)), vals[:len(vals) - n] + vals[len(vals) - n + 1:])
                self.assertEqual(sol.middle_node(ex.build(vals)).val, vals[len(vals) // 2])

    def test_stacks_queues(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            s = "".join(rng.choice("()[]{}") for _ in range(rng.randint(0, 8)))
            t = s
            for _ in range(10):
                t = t.replace("()", "").replace("[]", "").replace("{}", "")
            self.assertEqual(ex.valid_brackets(s), t == "")
            temps = [rng.randint(60, 80) for _ in range(rng.randint(0, 10))]
            self.assertEqual(ex.daily_temperatures(temps),
                             [next((j - i for j in range(i + 1, len(temps)) if temps[j] > temps[i]), 0) for i in range(len(temps))])
            nums = [rng.randint(-5, 5) for _ in range(rng.randint(1, 10))]
            k = rng.randint(1, len(nums))
            self.assertEqual(sol.sliding_max(nums, k), [max(nums[i:i + k]) for i in range(len(nums) - k + 1)])
        ms, plain = sol.MinStack(), []
        q, model = sol.QueueFromStacks(), []
        for _ in range(500):
            if plain and rng.random() < 0.4:
                self.assertEqual(ms.pop(), plain.pop())
            else:
                v = rng.randint(-50, 50)
                ms.push(v)
                plain.append(v)
            if plain:
                self.assertEqual(ms.get_min(), min(plain))
                self.assertEqual(ms.top(), plain[-1])
            if model and rng.random() < 0.4:
                self.assertEqual(q.pop(), model.pop(0))
            else:
                v = rng.randint(0, 9)
                q.push(v)
                model.append(v)
        self.assertEqual(ex.undo_editor(["Hel", "lo", " wrld", "UNDO", " world"]), "Hello world")


if __name__ == "__main__":
    unittest.main()
