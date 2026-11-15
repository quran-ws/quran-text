"""The counts the prose states, held against the file that publishes them.

`data/differences.json` is regenerated on every build; the prose that quotes
it is not. The two drifted apart once without anything failing (#34), so the
figures a reader is most likely to copy are checked here: each status count,
the total, and how many ways the `rasm_variant` words divide the riwāyāt.

`docs/lessons.md` is left out: it is a log, and its figures are the ones each
lesson was learnt at.

Run with:  python3 -m unittest discover -s pipeline/tests
"""

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))

from qurantext.normalize import rasm  # noqa: E402

STATUSES = "rasm_variant|alif_variant|word_boundary|partial"
PROSE = [ROOT / "README.md", ROOT / "lib" / "README.md", ROOT / "service" / "README.md",
         *sorted(p for p in (ROOT / "docs").glob("*.md") if p.name != "lessons.md")]
NUMBER_WORDS = {w: n for n, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


def _int(text: str) -> int:
    return NUMBER_WORDS[text.lower()] if text.lower() in NUMBER_WORDS else int(text.replace(",", ""))


def _claims(pattern: str):
    """(file:line, status-or-None, stated value) for every match in the prose."""
    for path in PROSE:
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(pattern, text):
            where = f"{path.relative_to(ROOT)}:{text.count(chr(10), 0, m.start()) + 1}"
            yield where, m.groupdict().get("status"), _int(m.group("n"))


class TestDocCounts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads((ROOT / "data" / "differences.json").read_text(encoding="utf-8"))

    def test_each_status_count(self):
        by_status = self.doc["by_status"]
        patterns = [rf"\b(?P<n>\d[\d,]*) `(?P<status>{STATUSES})`",
                    rf"\| `(?P<status>{STATUSES})` \| (?P<n>\d[\d,]*) \|"]
        seen = 0
        for pattern in patterns:
            for where, status, n in _claims(pattern):
                seen += 1
                with self.subTest(where=where):
                    self.assertEqual(n, by_status[status], f"{where} says {n} `{status}`")
        self.assertGreater(seen, 0, "no status count found: has the wording changed?")

    def test_the_total(self):
        patterns = [r"\b(?P<n>\d[\d,]*) (?:published )?differences\b",
                    r"`partial` — (?P<n>\d[\d,]*) words —"]
        seen = 0
        for pattern in patterns:
            for where, _, n in _claims(pattern):
                seen += 1
                with self.subTest(where=where):
                    self.assertEqual(n, self.doc["count"], f"{where} says {n} differences")
        self.assertGreater(seen, 0, "no total found: has the wording changed?")

    def test_how_many_ways_the_letter_differences_divide_the_riwayat(self):
        partitions = set()
        for r in self.doc["words"]:
            if r["status"] != "rasm_variant":
                continue
            groups: dict[str, set] = {}
            for riwayah, form in r["forms"].items():
                groups.setdefault(rasm(form), set()).add(riwayah)
            partitions.add(frozenset(frozenset(g) for g in groups.values()))
        claims = list(_claims(r"divide them (?P<n>\w+) (?:different )?ways"))
        self.assertGreater(len(claims), 0, "no partition count found: has the wording changed?")
        for where, _, n in claims:
            with self.subTest(where=where):
                self.assertEqual(n, len(partitions), f"{where} says {n} ways")


if __name__ == "__main__":
    unittest.main()
