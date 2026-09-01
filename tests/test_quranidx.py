"""Unit tests for the pieces where a silent mistake would corrupt the index.

Run with:  python3 -m unittest discover -s tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from quranidx.align import Column, _distribute, merge          # noqa: E402
from quranidx.build import (STATUS_IDENTICAL, STATUS_MADD,     # noqa: E402
                            STATUS_RASM, classify)
from quranidx.normalize import (forms, pointed, rasm, rasm_plene,  # noqa: E402
                                simple, split_by_rasm, split_trailing_waqf)
from quranidx.tokenize import Token, tokenize_ayah             # noqa: E402


def tok(rasm_: str) -> Token:
    return Token(sura=1, aya=1, pos=1, uthmani=rasm_, folded=rasm_,
                 pointed=rasm_, rasm=rasm_, rasm_plene=rasm_, simple=rasm_)


def real(word: str) -> Token:
    """A token with every form derived from ``word``, as the build makes it."""
    f = forms(word)
    return Token(sura=1, aya=1, pos=1, uthmani=f["uthmani"], folded=f["folded"],
                 pointed=f["pointed"], rasm=f["rasm"],
                 rasm_plene=f["rasm_plene"], simple=f["simple"])


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

    def test_the_dagger_alif_is_not_on_the_line(self):
        # A superscript alef is by definition an alef the scribe did not write.
        # ملك is the skeleton that carries both مَٰلِكِ and مَلِكِ — the ḥadhf
        # al-alif that lets one muṣḥaf serve seven riwāyāt — so folding it to a
        # letter invents a disagreement between codices that agree.
        self.assertEqual(rasm("مَٰلِكِ"), rasm("مَلِكِ"))
        self.assertEqual(rasm("دِفَٰعُ"), rasm("دَفۡعُ"))
        self.assertEqual(rasm("ٱلرِّيَٰحَ"), rasm("ٱلرِّيحَ"))
        self.assertEqual(rasm("طَٰٓئِراَۢ"), rasm("طَيۡرَۢا"))

    def test_the_reading_keeps_the_a_that_the_line_does_not(self):
        # The ā is real, it is just not written: `pointed` spells the word as
        # it is read, so مَٰلِكِ and مَلِكِ stay two readings of one rasm.
        self.assertNotEqual(pointed("مَٰلِكِ"), pointed("مَلِكِ"))
        self.assertEqual(pointed("مَٰلِكِ"), "مالك")

    def test_a_dagger_on_an_alef_already_there_adds_nothing(self):
        self.assertEqual(pointed("ءَامَنُواْ"), pointed("اٰمَنُواْ"))
        self.assertEqual(rasm("ءَامَنُواْ"), rasm("اٰمَنُواْ"))

    def test_plene_and_defective_are_told_apart_from_a_real_difference(self):
        # The two typesettings disagree in both directions about which ā to put
        # on the line, so the bare rasm alone cannot tell that difference of
        # hand from a difference of codex.  `rasm_plene` is what does.
        self.assertNotEqual(rasm("هَٰرُوتَ"), rasm("هَارُوتَ"))
        self.assertEqual(rasm_plene("هَٰرُوتَ"), rasm_plene("هَارُوتَ"))
        self.assertEqual(rasm_plene("مُبَٰرَك"), rasm_plene("مُبَارَك"))
        # A letter one codex has and another does not survives both.
        self.assertNotEqual(rasm("قُلۡ"), rasm("قَالَ"))
        self.assertNotEqual(rasm_plene("قُلۡ"), rasm_plene("قَالَ"))

    def test_adjacent_alefs_are_not_welded(self):
        # Bazzī's لَأُاْقۡسِمُ is لَآ + أُقۡسِمُ printed as one word: the two alefs are
        # separate letters, and collapsing them would break 75:1.
        self.assertEqual(rasm("لَأُاْقۡسِمُ"), rasm("لَآ") + rasm("أُقۡسِمُ"))

    def test_dagger_standing_in_for_a_suppressed_hamza_is_not_an_alef(self):
        # Warsh's tashīl drops the hamza of أَرَءَيۡتَ and leaves its madd on a
        # dagger alif.  A madd with no hamza after it is notating a hamza, not
        # an ā — so it is not a letter even in the form that spells the reading.
        self.assertEqual(rasm("أَرَءَيۡتَ"), rasm("ࡰرَٰٓيْتَ"))
        self.assertEqual(pointed("أَرَءَيۡتَ"), pointed("ࡰرَٰٓيْتَ"))
        self.assertEqual(rasm("أَرَءَيۡتَكُمۡ"), rasm("أَرَٰ۬يْتَكُمْ"))

    def test_a_madd_that_does_have_its_hamza_is_still_an_alef(self):
        # Where the hamza is present the dagger is a genuine ā, so it belongs
        # to the reading — and to `rasm_plene`, which is what makes Ḥafṣ's
        # إِسۡرَٰٓءِيلَ and Warsh's إِسْرَآءِيلَ one spelling of one word.
        self.assertEqual(pointed("إِسۡرَٰٓءِيلَ"), pointed("إِسْرَآءِيلَ"))
        self.assertEqual(rasm_plene("إِسۡرَٰٓءِيلَ"), rasm_plene("إِسْرَآءِيلَ"))
        self.assertEqual(rasm("هَٰٓؤُلَآءِ"), rasm("هَٰؤُلَآࢇ"))

    def test_madd_lazim_over_a_shadda_is_still_an_alef(self):
        # تَتَّبِعَٰٓنِّ and فَذَٰٓنِّكَ put the madd over a doubled letter, not a
        # hamza: a real long ā, which other packages write on the line.
        self.assertEqual(pointed("تَتَّبِعَآنِّ"), pointed("تَتَّبِعَٰٓنِّ"))
        self.assertEqual(rasm_plene("فَذَٰنِكَ"), rasm_plene("فَذَٰٓنِّكَ"))

    def test_a_word_final_madd_is_not_a_letter_of_its_own(self):
        # عَلَىٰٓ is ʿalā and عَلَيَّ is ʿalayya — a real variant at 7:105, and a
        # variant of *reading*: both are written على, which is the point of the
        # skeleton.  Emitting the dagger as an extra alef made the word علىا.
        self.assertEqual(rasm("عَلَىٰٓ"), "على")
        self.assertEqual(rasm("عَلَىٰٓ"), rasm("عَلَيَّ"))
        self.assertNotEqual(pointed("عَلَىٰٓ"), pointed("عَلَيَّ"))
        # 34:17 نُجَٰزِي / يُجَٰزَىٰ: four letters, whichever way it is read.
        self.assertEqual(rasm("يُجَٰزَىٰ"), rasm("نُجَٰزِيٓ"))
        self.assertEqual(rasm("يُجَٰزَىٰ"), "ٮحرى")

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


class TestClassify(unittest.TestCase):
    """A difference of hand and a difference of codex are not one label."""

    KEYS = ["hafs", "warsh"]

    def column(self, hafs: str, warsh: str) -> Column:
        return Column(tokens={"hafs": real(hafs), "warsh": real(warsh)})

    def test_plene_against_defective_is_a_difference_of_hand(self):
        # Both hands read Hārūt; they disagree only over where to put the ā.
        self.assertEqual(classify(self.column("هَٰرُوتَ", "هَارُوتَ"), self.KEYS),
                         STATUS_MADD)
        # And in the other direction, which is why neither hand can be trusted
        # to mean the codex when it prints one rather than the other.
        self.assertEqual(classify(self.column("مُبَارَكࣰا", "مُبَٰرَكاࣰ"), self.KEYS),
                         STATUS_MADD)

    def test_a_letter_one_codex_lacks_is_a_rasm_variant(self):
        self.assertEqual(classify(self.column("قُلۡ", "قَالَ"), self.KEYS),
                         STATUS_RASM)

    def test_a_dagger_against_nothing_is_not_a_rasm_variant(self):
        # 1:4 — ملك in every codex, read مالك by Ḥafṣ.  The reading survives in
        # `pointed`, so this is a dotting/vowelling difference, not a rasm one.
        self.assertNotIn(classify(self.column("مَٰلِكِ", "مَلِكِ"), self.KEYS),
                         (STATUS_RASM, STATUS_MADD))
        self.assertNotEqual(classify(self.column("مَٰلِكِ", "مَلِكِ"), self.KEYS),
                            STATUS_IDENTICAL)


if __name__ == "__main__":
    unittest.main()
