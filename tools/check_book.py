"""Static quality checks for the Algorithms Simplified Markdown chapters.

Checks performed on every chapter file:
  * Mermaid blocks start with a known diagram type and have balanced brackets.
  * Flowchart node labels that contain risky characters are wrapped in quotes.
  * Required chapter sections exist (comparison, exercises, solutions, FAQ, summary).
  * Every volume folder has a preface.md.
  * Reports which diagram types each chapter uses.

Usage:
    python3 tools/check_book.py /path/to/kmg-book
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DIAGRAM_KINDS = {
    "flowchart": "flowchart",
    "graph": "graph",
    "sequenceDiagram": "sequence",
    "stateDiagram-v2": "state",
    "stateDiagram": "state",
    "timeline": "timeline",
    "mindmap": "mindmap",
    "classDiagram": "class",
    "erDiagram": "er",
    "pie": "pie",
    "quadrantChart": "quadrant",
    "xychart-beta": "xychart",
    "block-beta": "block",
    "architecture-beta": "architecture",
}

REQUIRED_SECTIONS = ["compar", "exercise", "solution", "faq", "summary"]
PAIRS = {"(": ")", "[": "]", "{": "}"}
MERMAID_BLOCK = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
QUOTED = re.compile(r'"[^"]*"')
UNQUOTED_LABEL = re.compile(r"\w\[([^\]\"]*[()<>{}:;#][^\]\"]*)\]")


def bracket_problem(line: str) -> str | None:
    """Return a message if brackets outside quotes are unbalanced on this line."""
    stripped = QUOTED.sub('""', line)
    stack: list[str] = []
    for char in stripped:
        if char in PAIRS:
            stack.append(PAIRS[char])
        elif char in PAIRS.values():
            if not stack or stack.pop() != char:
                return "unbalanced brackets"
    return "unbalanced brackets" if stack else None


def check_block(block: str) -> tuple[str, list[str]]:
    lines = [line for line in block.splitlines() if line.strip() and not line.strip().startswith("%%")]
    if not lines:
        return "empty", ["empty mermaid block"]
    head = lines[0].strip().split()[0]
    kind = DIAGRAM_KINDS.get(head)
    problems: list[str] = []
    if kind is None:
        problems.append(f"unknown diagram type '{head}'")
        return "unknown", problems
    if kind in ("flowchart", "graph"):
        for line in lines[1:]:
            message = bracket_problem(line)
            if message:
                problems.append(f"{message}: {line.strip()}")
            if UNQUOTED_LABEL.search(line):
                problems.append(f"unquoted label with special characters: {line.strip()}")
    if kind == "timeline":
        for line in lines[1:]:
            if ":" in line and line.count(":") >= 1 and line.strip().startswith(":") is False:
                section = line.split(":")[0]
                if "(" in section or ")" in section:
                    problems.append(f"parentheses in timeline period: {line.strip()}")
    return kind, problems


def check_file(path: Path, root: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []
    kinds: set[str] = set()
    for number, match in enumerate(MERMAID_BLOCK.finditer(text), start=1):
        kind, block_problems = check_block(match.group(1))
        kinds.add(kind)
        problems.extend(f"diagram {number}: {p}" for p in block_problems)
    if path.name.startswith("chapter-"):
        lower = text.lower()
        headings = " ".join(line for line in lower.splitlines() if line.startswith("#"))
        for section in REQUIRED_SECTIONS:
            if section not in headings:
                problems.append(f"missing section heading containing '{section}'")
    count = len(MERMAID_BLOCK.findall(text))
    print(f"{path.relative_to(root)}: {count} diagrams, types = {sorted(kinds)}")
    return problems


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    failures = 0
    for volume in sorted(root.glob("volume-*")):
        if volume.is_dir() and not (volume / "preface.md").exists():
            failures += 1
            print(f"  PROBLEM {volume.name}: missing preface.md")
    for path in sorted(root.rglob("*.md")):
        for problem in check_file(path, root):
            failures += 1
            print(f"  PROBLEM {path.relative_to(root)}: {problem}")
    print(f"\n{failures} problem(s) found")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
