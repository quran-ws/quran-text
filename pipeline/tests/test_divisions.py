"""The recorded divisions, held against the muṣḥaf file each one describes.

`sources/divisions/` records where a muṣḥaf's rubu_al_hizbs or thumns fall,
with the evidence for each. Every entry copies three things out of `data/`:
the shared word `number`, and this edition's `ayah` and `page`. Nothing
rebuilds those copies, so they drift when the data moves. The Ḥafṣ file did:
its numbers were written before 25685 entered Ḥafṣ's `missing`, and 159 of the
240 then pointed one or two words early without anything failing (#63).

So each file is resolved here against `data/mushaf/<mushaf>.json`: every number
must lead back to the āyah and page beside it, every `division_mark` must sit
on a ۞, every `juz_start` on a juz start, and the grid must close.

Run with:  python3 -m unittest discover -s pipeline/tests
"""

import json
import unittest
from bisect import bisect_right
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIVISIONS = sorted((ROOT / "sources" / "divisions").glob("*.json"))
JUZ_COUNT = 30


def _positions_by_number(mushaf: dict) -> dict:
    """Shared word number → position in this muṣḥaf's `words` (docs/format.md, Numbering)."""
    missing = set(mushaf["numbering"]["missing"])
    joined = {run["position"]: run["numbers"] for run in mushaf["numbering"]["written_joined"]}
    positions, number = {}, 1
    for position in range(len(mushaf["words"])):
        while number in missing:
            number += 1
        last = joined[position][1] if position in joined else number
        for covered in range(number, last + 1):
            positions[covered] = position
        number = last + 1
    return positions


class TestRecordedDivisions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = []
        for path in DIVISIONS:
            recorded = json.loads(path.read_text(encoding="utf-8"))
            mushaf = json.loads(
                (ROOT / "data" / "mushaf" / f"{recorded['mushaf']}.json").read_text(encoding="utf-8"))
            cls.files.append((path.name, recorded, mushaf, _positions_by_number(mushaf)))

    def test_there_is_something_to_check(self):
        self.assertTrue(self.files, "sources/divisions/ holds no file")

    def test_the_grid_closes(self):
        for name, recorded, _, _ in self.files:
            with self.subTest(file=name):
                entries = recorded["positions"]
                numbers = [entry["number"] for entry in entries]
                self.assertEqual(len(entries), recorded["total"])
                self.assertEqual(numbers, sorted(set(numbers)), "numbers must rise, none twice")
                self.assertEqual(recorded["total"] % JUZ_COUNT, 0)
                per_juz = recorded["total"] // JUZ_COUNT
                for index, entry in enumerate(entries):
                    if "juz" in entry:
                        self.assertEqual(
                            (index % per_juz, index // per_juz + 1), (0, entry["juz"]),
                            f"juz {entry['juz']} is tagged at entry {index}, {entry['ayah']}")

    def test_every_number_leads_back_to_its_ayah_and_page(self):
        for name, recorded, mushaf, positions in self.files:
            surah_starts, ayah_starts = mushaf["surah_starts"], mushaf["ayah_starts"]
            for entry in recorded["positions"]:
                with self.subTest(file=name, ayah=entry["ayah"]):
                    self.assertIn(entry["number"], positions,
                                  f"{entry['number']} is not a word this muṣḥaf reads")
                    position = positions[entry["number"]]
                    surah = bisect_right(surah_starts, position)
                    first_ayah = mushaf["surahs"][surah - 1]["first_ayah"]
                    # A basmalah that is not counted stands before āyah 1 of its sūrah.
                    ayah = max(1, bisect_right(ayah_starts, position) - first_ayah)
                    self.assertEqual(f"{surah}:{ayah}", entry["ayah"])
                    self.assertEqual(bisect_right(mushaf["page_starts"], position), entry["page"])

    def test_each_source_is_where_the_data_puts_it(self):
        for name, recorded, mushaf, positions in self.files:
            division = {kind for kind, mark in enumerate(mushaf["mark_types"])
                        if mark["kind"] == "division"}
            marked = {position for position, kind in mushaf["marks"] if kind in division}
            juz_starts = set(mushaf["juz_starts"] or [])
            openings = set(mushaf["surah_starts"]) | set(mushaf["ayah_starts"])
            for entry in recorded["positions"]:
                position = positions.get(entry["number"])
                with self.subTest(file=name, ayah=entry["ayah"], source=entry["source"]):
                    if entry["source"] == "division_mark":
                        self.assertIn(position, marked, "no ۞ stands before this word")
                    else:
                        # Only a printed ۞ can fall inside an āyah; the rest open one.
                        self.assertIn(position, openings, "this word opens no āyah")
                        self.assertNotIn(position, marked, "a ۞ stands here: the source is division_mark")
                    if entry["source"] == "juz_start":
                        self.assertIn(position, juz_starts, "the layout CSV starts no juz here")


if __name__ == "__main__":
    unittest.main()
