"""Run every chapter's tests in the repository.

Usage (from the repository root):
    python3 run_tests.py            # run all tests
    python3 run_tests.py volume_01  # run only folders whose path contains "volume_01"

Only the Python standard library is used, so nothing needs to be installed.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTER_MODULE = re.compile(r"^(test_)?ch\d+(_\w+)?$")


def chapter_dirs(filter_text: str = "") -> list[Path]:
    """Return every folder that contains at least one test_*.py file."""
    folders = {path.parent for path in ROOT.glob("volume_*/chapter_*/test_*.py")}
    return sorted(folder for folder in folders if filter_text in str(folder))


def forget_chapter_modules() -> None:
    """Chapters in different volumes reuse module names (ch01_examples, test_ch01, ...).
    Drop them from Python's import cache so the next chapter loads its own files."""
    for name in list(sys.modules):
        if CHAPTER_MODULE.match(name):
            module_file = getattr(sys.modules[name], "__file__", "") or ""
            if str(ROOT) in module_file:
                del sys.modules[name]


def main() -> int:
    filter_text = sys.argv[1] if len(sys.argv) > 1 else ""
    suite = unittest.TestSuite()
    for folder in chapter_dirs(filter_text):
        forget_chapter_modules()
        # Each chapter folder is its own "top level" so its modules import each other simply.
        suite.addTests(unittest.defaultTestLoader.discover(str(folder), top_level_dir=str(folder)))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
