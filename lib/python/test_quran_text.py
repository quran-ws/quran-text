"""Run with:  python3 -m unittest lib/python/test_quran_text.py  (from the repo root)"""

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
DATA = HERE.parents[1] / "data"

from quran_text import AyahMap, Mushaf, WordIndex, ayah_mark, fold  # noqa: E402

hafs = Mushaf.load(DATA / "mushaf" / "hafs.json")
warsh = Mushaf.load(DATA / "mushaf" / "warsh.json")
bazzi = Mushaf.load(DATA / "mushaf" / "bazzi.json")


class TestAyah(unittest.TestCase):
    def test_text_layers_and_rendering(self):
        a = hafs.ayah(2, 255)
        self.assertEqual(a.key, "2:255")
        self.assertEqual(len(a), 50)
        self.assertEqual((a.page.number, a.juz.number, a.line.number), (42, 3, 8))
        self.assertTrue(a.text.startswith("ٱللَّهُ لَآ إِلَٰهَ"))
        self.assertTrue(a.render(ayah_marks=True).endswith(" ۝٢٥٥"))
        self.assertIn("ۚ", a.render(marks=True))
        self.assertIn("ۚ", a.render(marks={"waqf"}))
        self.assertNotIn("ۚ", a.render(marks={"division"}))
        self.assertNotIn("ۚ", a.render())
        self.assertEqual(a.next().key, "2:256")
        self.assertEqual(hafs.ayah(2, 286).next().key, "3:1")
        self.assertIsNone(hafs.ayah(1, 1).previous())
        with self.assertRaises(IndexError):
            hafs.ayah(2, 287)

    def test_surah_page_line_juz(self):
        s = hafs.surah(112)
        self.assertEqual(len(s.ayahs), 4)
        self.assertEqual(s.render(ayah_marks=True).count("۝"), 4)
        self.assertIsNone(s.basmalah)
        p = hafs.page(3)
        self.assertEqual(len(p.lines), 15)
        self.assertEqual((p.ayahs[0].key, p.ayahs[-1].key), ("2:6", "2:16"))
        self.assertEqual(len(p.render(lines=True).split("\n")), 15)
        self.assertEqual(p.line(1).text, p.lines[0].text)
        self.assertEqual(hafs.juz(30).first_ayah.key, "78:1")
        self.assertEqual(hafs.juz(30).pages[-1].number, 604)
        self.assertEqual(hafs.surah(2).last_page.number, 49)
        self.assertEqual([a.key for a in hafs.line(1, 3).ayahs], ["1:3", "1:4"])

    def test_words_marks_numbering(self):
        w = hafs.word(1, 4, 1)
        self.assertEqual((w.text, w.number, w.rasm_imlai, w.index), ("مَٰلِكِ", 11, "مالك", 1))
        self.assertEqual([a.key for a in hafs.sajdat()][:2], ["7:206", "13:15"])
        self.assertEqual(len(hafs.sajdat()), 15)
        self.assertTrue(hafs.ayah(7, 206).has_sajdah)
        self.assertEqual(len(hafs.division_marks()), 199)
        self.assertEqual(hafs.division_marks()[0].render(), "۞ إِنَّ")
        self.assertEqual(hafs.number_at(73948), 73950)
        self.assertEqual(hafs.word_at(73948).number_last, 73951)
        self.assertIsNone(hafs.word_by_number(25685))
        self.assertEqual(hafs.word_by_number(73951).text, "وَأَلَّوِ")
        self.assertEqual(hafs.word_by_number(11).text, "مَٰلِكِ")

    def test_unnumbered_basmalah_and_absent_layers(self):
        self.assertFalse(warsh.basmalah_counted)
        self.assertEqual(len(warsh.surah(1).basmalah), 4)
        self.assertIsNone(warsh.word_at(0).ayah)
        self.assertIsNone(warsh.ayah_at(3))
        self.assertEqual(len(warsh.ayah(1, 1)), 4)
        self.assertEqual(len(warsh.surah(1).ayahs), 7)
        self.assertTrue(warsh.ayah(2, 253).render(ayah_marks=True).endswith("۝٢٥٣"))
        with self.assertRaisesRegex(KeyError, "no juz layer"):
            bazzi.juz(1)
        self.assertIsNone(bazzi.word_at(5).juz)
        self.assertFalse(bazzi.has("juz"))
        self.assertIsNone(bazzi.word_at(5).rasm_imlai)

    def test_search(self):
        hits = hafs.search("مالك يوم الدين")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].first_ayah.key, "1:4")
        self.assertEqual(fold("ٱلۡحَمۡدُ"), "الحمد")
        self.assertEqual(ayah_mark(255), "۝٢٥٥")


class TestBundled(unittest.TestCase):
    def test_hafs_is_bundled(self):
        self.assertEqual(Mushaf.hafs().ayah(2, 255).key, "2:255")
        self.assertEqual(Mushaf.hafs().word_count, hafs.word_count)
        font = Mushaf.hafs().font
        self.assertEqual(font.family, "KFGQPC HAFS Uthmanic Script")
        self.assertTrue(font.path.exists())
        self.assertEqual(warsh.font.family, "KFGQPC Warsh Uthmanic Script")
        self.assertTrue(warsh.font.path.exists())


class TestToAnotherRiwayah(unittest.TestCase):
    def test_ayah_and_word(self):
        m = hafs.ayah(2, 255).to(warsh)
        self.assertEqual((m.key, m.relation, len(m.ayahs)), ("2:253-254", "split", 2))
        self.assertEqual(warsh.ayah(2, 253).to(hafs).key, "2:255")
        self.assertEqual(hafs.ayah(1, 1).to(warsh).relation, "unnumbered")
        self.assertEqual(hafs.ayah(57, 24).to(warsh).relation, "shifted")
        self.assertEqual(hafs.ayah(112, 1).to(bazzi).relation, "same")
        self.assertIsNone(hafs.word(57, 24, 10).to(warsh))
        self.assertEqual(warsh.word(2, 253, 3).to(hafs).text, "إِلَٰهَ")

    def test_agrees_with_ayah_map_for_surah_2(self):
        rows = [r for r in AyahMap.load(DATA / "ayah-map.json")._rows.values() if r["surah"] == 2]
        for r in rows:
            cell = r["warsh"]
            got = hafs.ayah(2, r["ayah"]).to(warsh)
            self.assertEqual(got.relation, cell["relation"], r["ayah"])
            if got.ayahs:
                self.assertEqual(got.first.number, cell["ayah"], r["ayah"])


class TestAyahMap(unittest.TestCase):
    def test_convert(self):
        m = AyahMap.load(DATA / "ayah-map.json")
        r = m.convert(2, 255, "warsh")
        self.assertEqual((r.surah, r.ayah, r.ayah_last, r.relation), (2, 253, 254, "split"))
        self.assertEqual(r.key, "2:253-254")
        self.assertEqual(m.all(1, 1)["warsh"].relation, "unnumbered")
        with self.assertRaises(KeyError):
            m.convert(2, 255, "nope")


class TestWordIndex(unittest.TestCase):
    def test_lookups(self):
        idx = WordIndex.load(DATA / "word-index.json")
        self.assertEqual(idx.word(11).form("warsh"), "مَلِكِ")
        self.assertEqual(idx.find(2, 255, 3).rasm_uthmani, "إِلَٰهَ")
        self.assertIn(11, [w.number for w in idx.search("مالك")])
        self.assertEqual(len(idx.differing()), 53134)


if __name__ == "__main__":
    unittest.main()
