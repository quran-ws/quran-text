"""The division layers, held against the evidence they were built from.

`sources/divisions/` records, per muṣḥaf, the divisions the printed muṣḥaf
marks only in its margin. `pipeline/qurantext/divisions.py` adds them to the
inline ۞ of the release and publishes `hizb_starts` with `rubu_al_hizb_starts`
or `thumn_starts`. These tests read the published files and the evidence side
by side, and check that the build refuses a grid that does not close.

The evidence is keyed by āyah, not by word number. An earlier shape copied the
shared word numbers in, and 159 of Ḥafṣ's 240 went stale without anything
failing (#63, #64).

Run with:  python3 -m unittest discover -s pipeline/tests
"""

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))

from qurantext import divisions  # noqa: E402

MUSHAFS = sorted(p.stem for p in (ROOT / "data" / "mushaf").glob("*.json"))


def _numbers(mushaf: dict) -> list:
    """The shared number of the word at each position (docs/format.md, Numbering)."""
    missing = set(mushaf["numbering"]["missing"])
    joined = {run["position"]: run["numbers"] for run in mushaf["numbering"]["written_joined"]}
    out, number = [], 1
    for position in range(len(mushaf["words"])):
        while number in missing:
            number += 1
        out.append(number)
        number = joined[position][1] + 1 if position in joined else number + 1
    return out


class TestDivisionLayers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs = {key: json.loads((ROOT / "data" / "mushaf" / f"{key}.json")
                                    .read_text(encoding="utf-8")) for key in MUSHAFS}
        cls.evidence = {}
        for key in MUSHAFS:
            path = divisions.evidence_path(key)
            if path:
                cls.evidence[key] = json.loads(path.read_text(encoding="utf-8"))

    def test_six_are_assembled_and_bazzi_says_why_it_is_not(self):
        self.assertEqual(sorted(self.evidence), ["duri", "hafs", "qalun", "shubah", "susi", "warsh"])
        bazzi = self.docs["bazzi"]
        for layer in ("hizb", "rubu_al_hizb", "thumn"):
            self.assertNotIn(f"{layer}_starts", bazzi)
            self.assertNotIn(layer, bazzi["layers"]["present"])
            self.assertIn("no printed muṣḥaf", bazzi["layers"]["absent"][layer])

    def test_each_file_carries_the_unit_its_print_uses(self):
        units = {"hafs": "rubu_al_hizb", "shubah": "rubu_al_hizb",
                 "warsh": "thumn", "qalun": "thumn", "duri": "thumn", "susi": "thumn"}
        for key, unit in units.items():
            with self.subTest(mushaf=key):
                doc = self.docs[key]
                other = "thumn" if unit == "rubu_al_hizb" else "rubu_al_hizb"
                self.assertEqual(self.evidence[key]["unit"], unit)
                self.assertIn("hizb", doc["layers"]["present"])
                self.assertIn(unit, doc["layers"]["present"])
                self.assertIn(other, doc["layers"]["absent"])
                self.assertNotIn(f"{other}_starts", doc)
                self.assertEqual(doc["provenance"]["divisions"]["print"]["sha256"],
                                 self.evidence[key]["print"]["sha256"])

    def test_the_grid_closes(self):
        for key, evidence in self.evidence.items():
            with self.subTest(mushaf=key):
                doc = self.docs[key]
                starts = doc[f"{evidence['unit']}_starts"]
                per = divisions.PER_HIZB[evidence["unit"]]
                self.assertEqual(len(starts), evidence["total"])
                self.assertEqual(starts, sorted(set(starts)))
                self.assertEqual(starts[0], 0)
                self.assertEqual(len(doc["hizb_starts"]), 60)
                self.assertEqual(doc["hizb_starts"], starts[::per])

    def test_every_division_is_a_printed_mark_or_a_margin_reading(self):
        for key, evidence in self.evidence.items():
            with self.subTest(mushaf=key):
                doc = self.docs[key]
                starts = set(doc[f"{evidence['unit']}_starts"])
                kinds = {i for i, mark in enumerate(doc["mark_types"]) if mark["kind"] == "division"}
                inline = {position for position, kind in doc["marks"] if kind in kinds}
                excluded = {divisions._ayah_start(doc, entry["ayah"])
                            for entry in evidence.get("not_a_division", [])}
                margin = {divisions._ayah_start(doc, entry["ayah"])
                          for entry in evidence["margin_division_marks"]}
                self.assertFalse(margin & inline, "a margin entry sits on a printed ۞")
                self.assertLessEqual(excluded, inline)
                self.assertEqual(starts, {0} | (inline - excluded) | margin)
                for entry in evidence["margin_division_marks"]:
                    self.assertTrue(entry["label"].strip(), entry["ayah"])

    def test_juz_differs_from_the_layout_only_where_the_evidence_says(self):
        stated = {"hafs": [4, 11], "qalun": [20, 22], "duri": [11, 26], "susi": [11, 26],
                  "shubah": [], "warsh": []}
        for key, juzs in stated.items():
            with self.subTest(mushaf=key):
                doc = self.docs[key]
                differs = [j + 1 for j, start in enumerate(doc["juz_starts"])
                           if doc["hizb_starts"][2 * j] != start]
                self.assertEqual(differs, juzs)
                self.assertEqual(
                    [d["juz"] for d in doc["layers"]["derived"]["divisions"]["juz_differs_from_layout"]],
                    juzs)

    def test_shubah_divides_at_the_same_words_as_hafs(self):
        hafs, shubah = self.docs["hafs"], self.docs["shubah"]
        self.assertEqual([_numbers(hafs)[p] for p in hafs["rubu_al_hizb_starts"]],
                         [_numbers(shubah)[p] for p in shubah["rubu_al_hizb_starts"]])

    def test_duri_and_susi_divide_at_the_same_words(self):
        duri, susi = self.docs["duri"], self.docs["susi"]
        self.assertEqual([_numbers(duri)[p] for p in duri["thumn_starts"]],
                         [_numbers(susi)[p] for p in susi["thumn_starts"]])


class TestTheBuildRefusesAnOpenGrid(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads((ROOT / "data" / "mushaf" / "qalun.json").read_text(encoding="utf-8"))
        cls.evidence = json.loads(divisions.evidence_path("qalun").read_text(encoding="utf-8"))

    def _broken(self):
        return copy.deepcopy(self.evidence)

    def test_the_evidence_as_recorded_closes(self):
        starts, counts = divisions.grid(self.doc, self.evidence)
        self.assertEqual(len(starts), 480)
        self.assertEqual(counts, {"opening": 1, "inline_division_marks": 436,
                                  "margin_division_marks": 43})

    def test_a_missing_margin_reading(self):
        evidence = self._broken()
        evidence["margin_division_marks"].pop()
        with self.assertRaisesRegex(divisions.DivisionError, "not 480"):
            divisions.grid(self.doc, evidence)

    def test_a_mark_that_should_have_been_excluded(self):
        evidence = self._broken()
        evidence["not_a_division"] = []
        with self.assertRaisesRegex(divisions.DivisionError, "not 480"):
            divisions.grid(self.doc, evidence)

    def test_a_margin_reading_on_a_printed_mark(self):
        evidence = self._broken()
        evidence["margin_division_marks"][0] = {"ayah": "2:13", "page": 3, "label": "ثمن"}
        with self.assertRaisesRegex(divisions.DivisionError, "prints a ۞ there"):
            divisions.grid(self.doc, evidence)

    def test_a_margin_reading_on_the_wrong_page(self):
        evidence = self._broken()
        evidence["margin_division_marks"][0]["page"] += 1
        with self.assertRaisesRegex(divisions.DivisionError, "the evidence says"):
            divisions.grid(self.doc, evidence)


if __name__ == "__main__":
    unittest.main()
