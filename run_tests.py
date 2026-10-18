"""Run every chapter's tests in the repository.

Usage (from the repository root):
    python3 run_tests.py            # run all tests
    python3 run_tests.py volume_01  # run only folders whose path contains "volume_01"

Only the Python standard library is used, so nothing needs to be installed.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def chapter_dirs(filter_text: str = "") -> list[Path]:
    """Return every folder that contains at least one test_*.py file."""
    folders = {path.parent for path in ROOT.glob("volume_*/chapter_*/test_*.py")}
    return sorted(folder for folder in folders if filter_text in str(folder))


def main() -> int:
    filter_text = sys.argv[1] if len(sys.argv) > 1 else ""
    suite = unittest.TestSuite()
    for folder in chapter_dirs(filter_text):
        # Each chapter folder is its own "top level" so its modules import each other simply.
        suite.addTests(unittest.defaultTestLoader.discover(str(folder), top_level_dir=str(folder)))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
