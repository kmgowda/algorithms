import unittest

import ch04_examples as ex


class TestChapter4(unittest.TestCase):
    def test_trail(self) -> None:
        dist, parent, order = ex.dag_shortest(ex.STOPS, ex.PATHS, "Gate")
        self.assertEqual(order, ["Gate", "Maps", "Poetry", "Stories", "Science", "Cafe", "Stage"])
        self.assertEqual(dist, {"Gate": 0, "Poetry": 4, "Maps": 3, "Science": 4, "Stories": 6, "Cafe": 5, "Stage": 7})
        self.assertEqual(ex.route(parent, "Stage"), ["Gate", "Maps", "Poetry", "Stories", "Science", "Cafe", "Stage"])
        ld, lp, _ = ex.dag_shortest(ex.STOPS, ex.PATHS, "Gate", longest=True)
        self.assertEqual((ld["Stage"], ex.route(lp, "Stage")), (16, ["Gate", "Poetry", "Science", "Stage"]))

    def test_every_case(self) -> None:
        d = ex.dag_shortest(ex.STOPS, ex.PATHS, "Stories")[0]
        self.assertEqual((d["Gate"], d["Science"], d["Stage"]), (float("inf"), -2, 1))
        self.assertIsNone(ex.topological_order(["A", "B"], [("A", "B", 1), ("B", "A", 1)]))
        with self.assertRaises(ValueError):
            ex.dag_shortest(["A", "B"], [("A", "B", 1), ("B", "A", 1)], "A")
        self.assertEqual(ex.dag_shortest(["A"], [], "A")[0], {"A": 0})
        self.assertEqual(ex.dag_shortest(["A", "B"], [("A", "B", 0)], "A")[0], {"A": 0, "B": 0})

    def test_counts_and_build(self) -> None:
        count = {"Gate": 1}
        for v in ex.topological_order(ex.STOPS, ex.PATHS):
            for a, b, _ in ex.PATHS:
                if a == v:
                    count[b] = count.get(b, 0) + count[v]
        self.assertEqual(count["Stage"], 15)
        self.assertEqual(ex.dag_shortest(ex.STOPS, [p for p in ex.PATHS if p[2] != -2], "Gate")[0]["Stage"], 13)
        tasks = ["start", "frame", "tents", "lights", "sound", "signs", "rehearsal"]
        after = [("start", "frame", 0), ("start", "tents", 0), ("frame", "lights", 3), ("frame", "sound", 3),
                 ("tents", "signs", 5), ("lights", "rehearsal", 2), ("sound", "rehearsal", 4), ("signs", "rehearsal", 1)]
        self.assertEqual(ex.dag_shortest(tasks, after, "start", longest=True)[0]["rehearsal"] + 2, 9)

    def test_critical_path(self) -> None:
        finish, early, late, critical = ex.critical_path(ex.BUILD, ex.BEFORE)
        self.assertEqual(finish, 9)
        self.assertEqual(early, {"frame": 0, "tents": 0, "lights": 3, "sound": 3, "signs": 5, "rehearsal": 7})
        self.assertEqual(late, {"frame": 0, "tents": 1, "lights": 5, "sound": 3, "signs": 6, "rehearsal": 7})
        self.assertEqual(critical, ["frame", "sound", "rehearsal"])
        slow = dict(ex.BUILD, tents=7)
        self.assertEqual(ex.critical_path(slow, ex.BEFORE)[0], 10)
        self.assertEqual(ex.critical_path(slow, ex.BEFORE)[3], ["tents", "signs", "rehearsal"])
        self.assertEqual(ex.critical_path({}, []), (0, {}, {}, []))
        self.assertEqual(ex.critical_path({"a": 4}, []), (4, {"a": 0}, {"a": 0}, ["a"]))
        with self.assertRaises(ValueError):
            ex.critical_path({"a": 1, "b": 1}, [("a", "b"), ("b", "a")])
        late = [ex.critical_path(dict(ex.BUILD, van=4, sound=s), ex.BEFORE + [("van", "sound")]) for s in (4, 3, 2)]
        self.assertEqual([r[0] for r in late], [10, 9, 8])
        self.assertEqual(late[0][3], ["van", "sound", "rehearsal"])
        self.assertEqual(late[2][3], ["tents", "van", "signs", "sound", "rehearsal"])
        neg = ex.dag_shortest(["A", "B", "C"], [("A", "B", 3), ("A", "C", 5), ("C", "B", -4)], "A")[0]
        self.assertEqual(neg, {"A": 0, "B": 1, "C": 5})
        self.assertEqual(ex.dag_shortest(["A", "B"], [("B", "A", 2)], "A")[0], {"A": 0, "B": float("inf")})

if __name__ == "__main__":
    unittest.main()
