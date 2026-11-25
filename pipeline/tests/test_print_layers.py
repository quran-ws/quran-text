"""The layers read from a printed edition: they point at the Ḥafṣ words, hold
none of their own, and publish nothing unproved.

Run with:  python3 -m unittest discover -s pipeline/tests
"""

import csv
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))

from qurantext import print_layers as pl  # noqa: E402

KEY = "hafs-1405"


class TestPrintLayers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads((ROOT / "data" / "mushaf" / "hafs.json").read_text(encoding="utf-8"))
        cls.doc = json.loads((ROOT / "data" / "print" / f"{KEY}.json").read_text(encoding="utf-8"))
        cls.refs = pl.word_keys(cls.base)

    def _rows(self, name):
        with (pl.PRINTS / KEY / name).open(encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))

    def test_committed_file_is_what_the_evidence_builds(self):
        self.assertEqual(pl.document(KEY, self.base), self.doc)

    def test_it_holds_no_words(self):
        self.assertNotIn("words", self.doc)
        self.assertEqual(self.doc["base"]["words_sha256"], pl.words_sha256(self.base["words"]))

    def test_13_37_is_two_words(self):
        self.assertIn("13:37:8", self.refs)
        self.assertIn("13:37:9", self.refs)

    def test_refs_are_unique_and_in_order(self):
        keys = [tuple(map(int, r.split(":"))) for r in self.refs]
        self.assertEqual(keys, sorted(set(keys)))

    def test_every_line_start_is_proved_and_no_row_is_lost(self):
        rows = self._rows("lines.csv")
        self.assertEqual(len(rows), len(self.doc["line_starts"]))
        self.assertTrue({r["proof"] for r in rows} <= set(self.doc["layers"]["proof_vocabulary"]) - {pl.UNPROVED})

    def test_marks_are_the_proved_rows(self):
        rows = self._rows("waqf.csv")
        self.assertTrue({r["proof"] for r in rows} <= set(self.doc["layers"]["proof_vocabulary"]))
        want = [(r["word"], r["sign"]) for r in rows if r["proof"] != pl.UNPROVED]
        got = [(self.refs[p], self.doc["mark_types"][t]["sign"]) for p, t in self.doc["marks"]]
        self.assertEqual(got, want)
        held = {x["word"] for x in self.doc["unproved"]["waqf"]}
        self.assertFalse(held & {w for w, _ in got})

    def test_no_more_than_fifteen_lines_on_a_page(self):
        self.assertTrue(all(1 <= int(r["line"]) <= 15 for r in self._rows("lines.csv")))

    def test_a_changed_word_list_is_refused(self):
        base = copy.deepcopy(self.base)
        base["words"][5] += "x"
        with self.assertRaises(pl.PrintError):
            pl.document(KEY, base)

    def test_waqf_al_muanaqah_signs_come_in_pairs(self):
        n = sum(self.doc["mark_types"][t]["sign"] == "ۛ" for _, t in self.doc["marks"])
        self.assertEqual(n % 2, 0)

    def test_the_schema_names_every_field(self):
        self.assertEqual(pl.check_prints({KEY: self.doc}, {"hafs": self.base}), [])


if __name__ == "__main__":
    unittest.main()
