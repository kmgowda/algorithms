"""Volume 6, Chapter 37 - Thinking Problems.

Problem 1: the diff keeps exactly LCS lines, so its n + m - 2 LCS changes are the fewest possible (checked).
Problem 2: undoing a patch: rebuild the old file from the new one and the same diff.
Problem 3: a diff by set membership ("lines not in the other file") breaks on repeated and moved lines.
"""

from __future__ import annotations

import importlib.util
import os

from ch37_examples import diff

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("ch16_v6", os.path.join(_here, "..", "chapter_16_lcs", "ch16_examples.py"))
_lcs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_lcs)


def lcs_length(a: list, b: list) -> int:
    return _lcs.lcs(a, b)[0]


def undo_diff(edits: list) -> list:
    """The old file is every kept or deleted line, in order."""
    return [line for tag, line in edits if tag in ("  ", "- ")]


def set_diff(old: list, new: list) -> list:
    gone = [("- ", x) for x in old if x not in new]
    added = [("+ ", x) for x in new if x not in old]
    return gone + added


def apply_set_diff(old: list, edits: list) -> list:
    gone = {x for t, x in edits if t == "- "}
    return [x for x in old if x not in gone] + [x for t, x in edits if t == "+ "]


if __name__ == "__main__":
    from ch37_examples import NEW, OLD
    print(lcs_length(OLD, NEW), undo_diff(diff(OLD, NEW)) == OLD)
    a, b = ["A", "B", "A"], ["B", "A", "A"]
    print(set_diff(a, b), apply_set_diff(a, set_diff(a, b)), diff(a, b))
