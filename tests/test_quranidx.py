"""Unit tests for the pieces where a silent mistake would corrupt the index.

Run with:  python3 -m unittest discover -s tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from quranidx.align import Column, _distribute, merge          # noqa: E402
from quranidx.normalize import (forms, pointed, rasm, simple,  # noqa: E402
                                split_by_rasm, split_trailing_waqf)
from quranidx.tokenize import Token, tokenize_ayah             # noqa: E402


def tok(rasm_: str) -> Token:
    return Token(sura=1, aya=1, pos=1, uthmani=rasm_, folded=rasm_,
                 pointed=rasm_, rasm=rasm_, simple=rasm_)


class TestNormalize(unittest.TestCase):
    def test_rasm_folds_alef_forms(self):
        # Every alif spelling must collapse, or the riwāyāt will not align.
        for word in ["ٱللَّهِ", "اِ۬للَّهِ", "ࡴ۬للَّهِ", "ࡵ۬للَّهِ"]:
            self.assertEqual(rasm(word), "الله", word)

    def test_rasm_drops_the_dots(self):
        # The codices were undotted, so one rasm carries both readings and the
        # word keeps one ID.  The reading itself survives in `pointed`.
        self.assertEqual(rasm("تَعۡمَلُونَ"), rasm("يَعۡمَلُونَ"))
        self.assertEqual(rasm("تَعۡمَلُونَ"), "ٮعملوں")
        self.assertNotEqual(pointed("تَعۡمَلُونَ"), pointed("يَعۡمَلُونَ"))

    def test_dots_part_company_at_the_end_of_a_word(self):
        # ب ت ث ن ي share a tooth medially only; final ن and ي keep their tails.
        self.assertEqual(rasm("نَبَتَ")[:-1], "ٮٮ")
        self.assertNotEqual(rasm("مِن"), rasm("مِي"))

    def test_rasm_drops_hamza(self):
        # Hamza is 8th-century notation, not part of the codices.  Warsh's
        # yeh-barree-with-hamza and Ḥafṣ's hamza-on-yeh are one word.
        self.assertEqual(rasm("يَسۡتَهۡزِئُ"), rasm("يَسْتَهْزِۓُ"))
        self.assertEqual(rasm("هَٰٓؤُلَآءِ"), rasm("هَٰؤُلَآࢇ"))

    def test_dagger_alif_is_a_written_alef(self):
        # The packages disagree only about where the publisher put the ā ...
        self.assertEqual(rasm("هَٰرُوتَ"), rasm("هَارُوتَ"))
        self.assertEqual(rasm("ءَامَنُواْ"), rasm("اٰمَنُواْ"))
        # ... but a real difference in whether the ā is there at all stands.
        self.assertNotEqual(rasm("مَٰلِكِ"), rasm("مَلِكِ"))

    def test_adjacent_alefs_are_not_welded(self):
        # Bazzī's لَأُاْقۡسِمُ is لَآ + أُقۡسِمُ printed as one word: the two alefs are
        # separate letters, and collapsing them would break 75:1.
        self.assertEqual(rasm("لَأُاْقۡسِمُ"), rasm("لَآ") + rasm("أُقۡسِمُ"))

    def test_rasm_keeps_real_letter_differences(self):
        # Bazzī reads قَالَ where the others read قُلۡ: different letters.
        self.assertNotEqual(rasm("قُلۡ"), rasm("قَالَ"))

    def test_silah_is_a_vowel_not_a_letter(self):
        # Bazzī's ṣilat al-mīm is written superscript, so it is not part of the
        # rasm: عَلَيۡهِمُۥ and عَلَيۡهِمۡ are one word read two ways, and must align.
        self.assertEqual(rasm("عَلَيۡهِمُۥ"), rasm("عَلَيۡهِمۡ"))
        self.assertEqual(pointed("عَلَيۡهِمُۥ"), "عليهم")

    def test_superscript_yeh_is_a_letter_others_write_on_the_line(self):
        # ٱلنَّبِيِّۧنَ writes its second yāʾ superscript; Warsh prints it as ۑ.
        self.assertEqual(rasm("ٱلنَّبِيِّۧنَ"), rasm("ࡰ۬لنَّبِيِٕٓۑنَ"))

    def test_simple_spelling_expands_superscript_alef(self):
        self.assertEqual(simple("مَٰلِكِ"), "مالك")

    def test_waqf_is_peeled_not_dropped(self):
        word, waqf = split_trailing_waqf("رَيۡبَۛ")
        self.assertEqual(waqf, "ۛ")
        self.assertEqual(pointed(word), "ريب")

    def test_notation_folding_unifies_releases(self):
        # The 2022 files write the KFGQPC sukūn head, the 2026 files a sukūn.
        self.assertEqual(forms("بِسۡمِ")["folded"], forms("بِسْمِ")["folded"])

    def test_notation_folding_decomposes_the_attached_alef(self):
        # ࡰ is one codepoint for what other releases write as alef + fatha.
        self.assertEqual(forms("ࡰلۡحَمۡدُ")["folded"], forms("اَلۡحَمۡدُ")["folded"])

    def test_notation_folding_ignores_the_editorial_sah(self):
        # U+08CC is a proofreader's mark, and the largest single source of
        # spurious differences in the corpus.
        self.assertEqual(forms("وَمَارُوتَ࣌")["uthmani"], forms("وَمَارُوتَ")["uthmani"])

    def test_notation_folding_ignores_tanween_order(self):
        self.assertEqual(forms("حَطَبࣰا")["folded"], forms("حَطَباࣰ")["folded"])


class TestSplitByRasm(unittest.TestCase):
    def test_splits_a_word_printed_without_its_space(self):
        pieces = split_by_rasm("كَانُواْيَعۡمَلُونَ", [5, 7])
        self.assertEqual([pointed(p) for p in pieces], ["كانوا", "يعملون"])

    def test_marks_stay_with_the_letter_they_sit_on(self):
        pieces = split_by_rasm("قَتَرٞوَلَا", [3, 3])
        self.assertEqual(pieces[0], "قَتَرٞ")      # the tanwīn belongs to قتر
        self.assertEqual(pieces[1], "وَلَا")

    def test_round_trips(self):
        word = "وَمَالِيَ"
        self.assertEqual("".join(split_by_rasm(word, [3, 2])), word)


class TestTokenize(unittest.TestCase):
    def test_hizb_symbol_is_not_a_word(self):
        toks = tokenize_ayah(2, 1, "۞ وَٱللَّهُ")
        self.assertEqual(len(toks), 1)
        self.assertTrue(toks[0].hizb)

    def test_sajdah_is_recorded_not_dropped(self):
        toks = tokenize_ayah(7, 206, "يَسۡجُدُونَۤ۩")
        self.assertEqual(len(toks), 1)
        self.assertTrue(toks[0].sajdah)
        self.assertEqual(toks[0].pointed, "يسجدون")


class TestAlign(unittest.TestCase):
    def test_identical_streams_share_every_column(self):
        spine = [Column(tokens={"a": tok(r)}) for r in ["ا", "ب", "ج"]]
        out = merge(spine, "b", [tok("ا"), tok("ب"), tok("ج")])
        self.assertEqual(len(out), 3)
        self.assertTrue(all(set(c.tokens) == {"a", "b"} for c in out))

    def test_a_joined_word_is_resegmented_into_its_columns(self):
        spine = [Column(tokens={"a": tok("كانوا")}), Column(tokens={"a": tok("يعملون")})]
        out = merge(spine, "b", [tok("كانوايعملون")])
        self.assertEqual(len(out), 2)
        # Both columns keep riwāyah b, so no word is reported missing.
        self.assertTrue(all("b" in c.tokens for c in out))
        self.assertEqual([c.boundary["b"] for c in out],
                         ["joined_in_source"] * 2)

    def test_an_inserted_word_gets_its_own_column(self):
        spine = [Column(tokens={"a": tok("تجري")}), Column(tokens={"a": tok("تحتها")})]
        out = merge(spine, "b", [tok("تجري"), tok("من"), tok("تحتها")])
        self.assertEqual([c.rasm for c in out], ["تجري", "من", "تحتها"])
        self.assertNotIn("a", out[1].tokens)      # only Bazzī has مِن at 9:101

    def test_distribute_groups_by_letters_not_by_position(self):
        cols = [Column(tokens={"a": tok("ما")}), Column(tokens={"a": tok("لي")})]
        groups = _distribute(cols, [tok("مالي")])
        self.assertEqual(len(groups), 1)
        self.assertEqual((len(groups[0][0]), len(groups[0][1])), (2, 1))


if __name__ == "__main__":
    unittest.main()
