"""Unit tests for the pieces where a silent mistake would corrupt the index.

Run with:  python3 -m unittest discover -s tests
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qurantext.align import (WRITTEN_JOINED, Column, _distribute,  # noqa: E402
                            _pair_by_letters, merge)
from qurantext.build import (STATUS_ALIF, STATUS_IDENTICAL,     # noqa: E402
                            STATUS_RASM, Word,
                            classify)
from qurantext.normalize import (forms, pointed, rasm, rasm_plene,  # noqa: E402
                                plain, split_by_rasm, split_trailing_waqf,
                                unpositioned)
from qurantext.report import _difference_is_length                 # noqa: E402
from qurantext.validate import check_alif_splits                    # noqa: E402
from qurantext.tokenize import Token, tokenize_ayah             # noqa: E402
from qurantext.rasm_imlai import _pair                              # noqa: E402
from qurantext.layout import Place                              # noqa: E402
from qurantext.mushaf import _marks, _starts, numbering, printed_words  # noqa: E402
from qurantext.validate import check_numbering, check_positions  # noqa: E402


def tok(rasm_: str, surah: int = 1) -> Token:
    return Token(surah=surah, ayah=1, position=1, rasm_uthmani=rasm_, folded=rasm_,
                 pointed=rasm_, rasm=rasm_, rasm_plene=rasm_, plain=rasm_)


def real(word: str) -> Token:
    """A token with every form derived from ``word``, as the build makes it."""
    f = forms(word)
    return Token(surah=1, ayah=1, position=1, rasm_uthmani=f["rasm_uthmani"], folded=f["folded"],
                 pointed=f["pointed"], rasm=f["rasm"],
                 rasm_plene=f["rasm_plene"], plain=f["plain"])


class TestNormalize(unittest.TestCase):
    def test_rasm_folds_alef_forms(self):
        # Every alif spelling must collapse, or the riwāyāt will not align.
        for word in ["ٱللَّهِ", "اِ۬للَّهِ", "ࡴ۬للَّهِ", "ࡵ۬للَّهِ"]:
            self.assertEqual(rasm(word), "الله", word)

    def test_rasm_drops_the_dots(self):
        # The codices were undotted, so one rasm carries both qiraahs and the
        # word keeps one ID.  The qiraah itself survives in `pointed`.
        self.assertEqual(rasm("تَعۡمَلُونَ"), rasm("يَعۡمَلُونَ"))
        self.assertEqual(rasm("تَعۡمَلُونَ"), "ٮعملوں")
        self.assertNotEqual(pointed("تَعۡمَلُونَ"), pointed("يَعۡمَلُونَ"))

    def test_dots_part_company_at_the_end_of_a_word(self):
        # ب ت ث ن ي share a tooth medially only; final ن and ي keep their tails.
        self.assertEqual(rasm("نَبَتَ")[:-1], "ٮٮ")
        self.assertNotEqual(rasm("مِن"), rasm("مِي"))

    def test_rasm_drops_hamzah(self):
        # Hamzah is 8th-century notation, not part of the codices.  Warsh's
        # yeh-barree-with-hamzah and Ḥafṣ's hamzah-on-yeh are one word.
        self.assertEqual(rasm("يَسۡتَهۡزِئُ"), rasm("يَسْتَهْزِۓُ"))
        self.assertEqual(rasm("هَٰٓؤُلَآءِ"), rasm("هَٰؤُلَآࢇ"))

    def test_the_omitted_alif_is_not_on_the_line(self):
        # A superscript alef is by definition an alef the scribe did not write.
        # ملك is the skeleton that carries both مَٰلِكِ and مَلِكِ — the ḥadhf
        # al-alif that lets one muṣḥaf serve seven riwāyāt — so folding it to a
        # letter invents a disagreement between codices that agree.
        self.assertEqual(rasm("مَٰلِكِ"), rasm("مَلِكِ"))
        self.assertEqual(rasm("دِفَٰعُ"), rasm("دَفۡعُ"))
        self.assertEqual(rasm("ٱلرِّيَٰحَ"), rasm("ٱلرِّيحَ"))
        self.assertEqual(rasm("طَٰٓئِراَۢ"), rasm("طَيۡرَۢا"))

    def test_the_qiraah_keeps_the_a_that_the_line_does_not(self):
        # The ā is real, it is just not written: `pointed` spells the word as
        # it is recited, so مَٰلِكِ and مَلِكِ stay two qiraahs of one rasm.
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

    def test_dagger_standing_in_for_a_suppressed_hamzah_is_not_an_alef(self):
        # Warsh's tashīl drops the hamzah of أَرَءَيۡتَ and leaves its madd on a
        # dagger alif.  A madd with no hamzah after it is notating a hamzah, not
        # an ā — so it is not a letter even in the form that spells the qiraah.
        self.assertEqual(rasm("أَرَءَيۡتَ"), rasm("ࡰرَٰٓيْتَ"))
        self.assertEqual(pointed("أَرَءَيۡتَ"), pointed("ࡰرَٰٓيْتَ"))
        self.assertEqual(rasm("أَرَءَيۡتَكُمۡ"), rasm("أَرَٰ۬يْتَكُمْ"))

    def test_a_madd_that_does_have_its_hamzah_is_still_an_alef(self):
        # Where the hamzah is present the dagger is a genuine ā, so it belongs
        # to the qiraah — and to `rasm_plene`, which is what makes Ḥafṣ's
        # إِسۡرَٰٓءِيلَ and Warsh's إِسْرَآءِيلَ one spelling of one word.
        self.assertEqual(pointed("إِسۡرَٰٓءِيلَ"), pointed("إِسْرَآءِيلَ"))
        self.assertEqual(rasm_plene("إِسۡرَٰٓءِيلَ"), rasm_plene("إِسْرَآءِيلَ"))
        self.assertEqual(rasm("هَٰٓؤُلَآءِ"), rasm("هَٰؤُلَآࢇ"))

    def test_madd_lazim_over_a_shaddah_is_still_an_alef(self):
        # تَتَّبِعَٰٓنِّ and فَذَٰٓنِّكَ put the madd over a doubled letter, not a
        # hamzah: a real long ā, which other packages write on the line.
        self.assertEqual(pointed("تَتَّبِعَآنِّ"), pointed("تَتَّبِعَٰٓنِّ"))
        self.assertEqual(rasm_plene("فَذَٰنِكَ"), rasm_plene("فَذَٰٓنِّكَ"))

    def test_a_word_final_madd_is_not_a_letter_of_its_own(self):
        # عَلَىٰٓ is ʿalā and عَلَيَّ is ʿalayya — a real variant at 7:105, and a
        # variant of *qiraah*: both are written على, which is the point of the
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

    def test_madd_al_silah_is_a_vowel_not_a_letter(self):
        # Bazzī's ṣilat al-mīm is written superscript, so it is not part of the
        # rasm: عَلَيۡهِمُۥ and عَلَيۡهِمۡ are one word read two ways, and must align.
        self.assertEqual(rasm("عَلَيۡهِمُۥ"), rasm("عَلَيۡهِمۡ"))
        self.assertEqual(pointed("عَلَيۡهِمُۥ"), "عليهم")

    def test_superscript_yeh_is_a_letter_others_write_on_the_line(self):
        # ٱلنَّبِيِّۧنَ writes its second yāʾ superscript; Warsh prints it as ۑ.
        self.assertEqual(rasm("ٱلنَّبِيِّۧنَ"), rasm("ࡰ۬لنَّبِيِٕٓۑنَ"))

    def test_plain_spelling_expands_superscript_alef(self):
        self.assertEqual(plain("مَٰلِكِ"), "مالك")

    def test_waqf_is_peeled_not_dropped(self):
        word, waqf = split_trailing_waqf("رَيۡبَۛ")
        self.assertEqual(waqf, "ۛ")
        self.assertEqual(pointed(word), "ريب")

    def test_notation_folding_unifies_releases(self):
        # The 2022 files write the KFGQPC sukūn head, the 2026 files a sukūn.
        self.assertEqual(forms("بِسۡمِ")["folded"], forms("بِسْمِ")["folded"])

    def test_notation_folding_decomposes_the_attached_alef(self):
        # ࡰ is one codepoint for what other releases write as alef + fathah.
        self.assertEqual(forms("ࡰلۡحَمۡدُ")["folded"], forms("اَلۡحَمۡدُ")["folded"])

    def test_notation_folding_ignores_the_editorial_sah(self):
        # U+08CC is a proofreader's mark, and the largest single source of
        # spurious differences in the corpus.
        self.assertEqual(forms("وَمَارُوتَ࣌")["rasm_uthmani"], forms("وَمَارُوتَ")["rasm_uthmani"])

    def test_notation_folding_ignores_tanwin_order(self):
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
    def test_division_symbol_is_not_a_word(self):
        toks = tokenize_ayah(2, 1, "۞ وَٱللَّهُ")
        self.assertEqual(len(toks), 1)
        self.assertTrue(toks[0].division)

    def test_sajdah_is_recorded_not_dropped(self):
        toks = tokenize_ayah(7, 206, "يَسۡجُدُونَۤ۩")
        self.assertEqual(len(toks), 1)
        self.assertTrue(toks[0].sajdah)
        self.assertEqual(toks[0].pointed, "يسجدون")


class TestAlign(unittest.TestCase):
    def test_identical_streams_share_every_column(self):
        columns = [Column(tokens={"a": tok(r)}) for r in ["ا", "ب", "ج"]]
        out = merge(columns, "b", [tok("ا"), tok("ب"), tok("ج")])
        self.assertEqual(len(out), 3)
        self.assertTrue(all(set(c.tokens) == {"a", "b"} for c in out))

    def test_a_joined_word_is_resegmented_into_its_columns(self):
        columns = [Column(tokens={"a": tok("كانوا")}), Column(tokens={"a": tok("يعملون")})]
        out = merge(columns, "b", [tok("كانوايعملون")])
        self.assertEqual(len(out), 2)
        # Both columns keep riwāyah b, so no word is reported missing.
        self.assertTrue(all("b" in c.tokens for c in out))
        self.assertEqual([c.boundary["b"] for c in out],
                         ["joined_in_source"] * 2)

    def test_an_inserted_word_gets_its_own_column(self):
        columns = [Column(tokens={"a": tok("تجري")}), Column(tokens={"a": tok("تحتها")})]
        out = merge(columns, "b", [tok("تجري"), tok("من"), tok("تحتها")])
        self.assertEqual([c.rasm for c in out], ["تجري", "من", "تحتها"])
        self.assertNotIn("a", out[1].tokens)      # only Bazzī has مِن at 9:101

    def test_distribute_groups_by_letters_not_by_position(self):
        cols = [Column(tokens={"a": tok("ما")}), Column(tokens={"a": tok("لي")})]
        groups = _distribute(cols, [tok("مالي")])
        self.assertEqual(len(groups), 1)
        self.assertEqual((len(groups[0][0]), len(groups[0][1])), (2, 1))

    def test_a_different_word_pairs_by_letters_not_by_position(self):
        # 40:26 — Ḥafṣ أَوۡ أَن against Warsh وَأَنْ.  Left-to-right pairing put
        # وَأَنْ against أَوۡ; the letters say it is أَن, and أَوۡ is the word
        # Warsh does not read.
        cols = [Column(tokens={"hafs": tok("او")}), Column(tokens={"hafs": tok("اں")})]
        out: list[Column] = []
        _pair_by_letters(cols, [tok("واں")], "warsh", out)
        self.assertEqual([sorted(c.tokens) for c in out], [["hafs"], ["hafs", "warsh"]])

    def test_a_declared_join_covers_both_columns(self):
        # 73:20 — the columns hold أَن لَّن; Dūrī prints أَلَّن.  Nothing is
        # missing: the one token covers two numbers.
        an, lan = real("أَن"), real("لَّن")
        an.surah = lan.surah = 73
        columns = [Column(tokens={"hafs": an}), Column(tokens={"hafs": lan})]
        joined = real("أَلَّن")
        joined.surah = 73
        out = merge(columns, "duri", [joined])
        self.assertEqual(len(out), 2)
        self.assertTrue(all(c.present("duri") for c in out))
        self.assertEqual([c.boundary["duri"] for c in out], [WRITTEN_JOINED] * 2)
        self.assertIs(out[1].covers["duri"], joined)
        self.assertNotIn("duri", out[1].tokens)

    def test_a_declared_join_already_aligned_is_split_for_the_others(self):
        # 72:16 — Ḥafṣ came first with وَأَلَّوِ; Warsh brings وَأَن لَّوِ.
        joined = real("وَأَلَّوِ")
        joined.surah = 72
        wa_an, law = real("وَأَن"), real("لَّوِ")
        wa_an.surah = law.surah = 72
        out = merge([Column(tokens={"hafs": joined})], "warsh", [wa_an, law])
        self.assertEqual(len(out), 2)
        self.assertEqual([c.rasm for c in out], [wa_an.rasm, law.rasm])
        self.assertEqual(out[0].boundary, {"hafs": WRITTEN_JOINED})
        self.assertIs(out[1].covers["hafs"], joined)
        self.assertNotIn("warsh", out[0].boundary)     # Warsh writes them apart


class TestClassify(unittest.TestCase):
    """A difference of hand and a difference of codex are not one label."""

    KEYS = ["hafs", "warsh"]

    def column(self, hafs: str, warsh: str) -> Column:
        return Column(tokens={"hafs": real(hafs), "warsh": real(warsh)})

    def test_plene_against_defective_is_its_own_status(self):
        # هَٰرُوتَ against هَارُوتَ is a difference of hand, not of codex: the two
        # typesettings disagree in both directions and every such word in the
        # corpus splits the seven the same single way.  It is reported, but
        # apart from the letters the codices actually disagree about.
        self.assertEqual(classify(self.column("هَٰرُوتَ", "هَارُوتَ"), self.KEYS),
                         STATUS_ALIF)
        self.assertEqual(classify(self.column("مُبَارَكࣰا", "مُبَٰرَكاࣰ"), self.KEYS),
                         STATUS_ALIF)
        self.assertEqual(rasm_plene("هَٰرُوتَ"), rasm_plene("هَارُوتَ"))
        # The bare rasm still keeps it: within one muṣḥaf it is that muṣḥaf's
        # own ḥadhf.
        self.assertNotEqual(rasm("هَٰرُوتَ"), rasm("هَارُوتَ"))

    def test_a_letter_one_codex_lacks_is_a_rasm_variant(self):
        self.assertEqual(classify(self.column("قُلۡ", "قَالَ"), self.KEYS),
                         STATUS_RASM)

    def test_a_letter_added_is_a_rasm_variant_not_an_alif_one(self):
        # 5:54 يَرۡتَدَّ / يَرۡتَدِدۡ and 43:71 تَشۡتَهِيهِ / تَشۡتَهِي: a letter on the line
        # that the other codex does not have at all.
        self.assertEqual(classify(self.column("يَرۡتَدَّ", "يَرۡتَدِدۡ"), self.KEYS),
                         STATUS_RASM)
        self.assertEqual(classify(self.column("تَشۡتَهِيهِ", "تَشۡتَهِي"), self.KEYS),
                         STATUS_RASM)

    def test_a_word_written_joined_is_not_a_rasm_variant(self):
        col = Column(tokens={"hafs": real("أَن"), "duri": real("أَلَّن")},
                     boundary={"duri": WRITTEN_JOINED})
        self.assertEqual(classify(col, ["hafs", "duri"]), "word_boundary")

    def test_a_dagger_against_nothing_is_not_a_rasm_variant(self):
        # 1:4 — ملك in every codex, read مالك by Ḥafṣ.  The qiraah survives in
        # `pointed`, so this is a dotting/vowelling difference, not a rasm one.
        self.assertNotEqual(classify(self.column("مَٰلِكِ", "مَلِكِ"), self.KEYS),
                            STATUS_RASM)
        self.assertNotEqual(classify(self.column("مَٰلِكِ", "مَلِكِ"), self.KEYS),
                            STATUS_IDENTICAL)


class TestAlifSplitsOneWay(unittest.TestCase):
    """The one fact `alif_variant` rests on, asserted rather than assumed."""

    def word(self, id_: int, **forms_: str) -> Word:
        return Word(id=id_, surah=1, index=id_, key=f"k{id_}", rasm="", pointed="",
                    rasm_uthmani="", plain="", status="alif_variant",
                    present=list(forms_), missing=[], forms=forms_, ayah={},
                    waqf={}, boundary={}, division=[], sajdah=[])

    def test_one_partition_passes(self):
        # Both directions are fine — what matters is who is on each side.
        words = [self.word(1, hafs="هَٰرُوتَ", bazzi="هَٰرُوتَ", warsh="هَارُوتَ"),
                 self.word(2, hafs="مُبَارَك", bazzi="مُبَارَك", warsh="مُبَٰرَك")]
        self.assertEqual(check_alif_splits(words), [])

    def test_makkah_leaving_the_kufi_side_is_reported(self):
        # Bazzī is Makkī.  A plene/defective word that puts it with Madinah is a
        # khilāf of the amṣār, not a house style, and the status would no longer
        # be warranted.
        words = [self.word(1, hafs="هَٰرُوتَ", bazzi="هَٰرُوتَ", warsh="هَارُوتَ"),
                 self.word(2, hafs="هَٰرُوتَ", bazzi="هَارُوتَ", warsh="هَارُوتَ")]
        problems = check_alif_splits(words)
        self.assertEqual([p["check"] for p in problems], ["alif_splits_one_way"])

    def test_other_statuses_are_not_its_business(self):
        words = [self.word(1, hafs="قُلۡ", warsh="قَالَ")]
        words[0].status = "rasm_variant"
        self.assertEqual(check_alif_splits(words), [])


class TestShapeOfDifference(unittest.TestCase):
    """What kind of letter difference a rasm variant is."""

    def word(self, **forms_: str) -> Word:
        return Word(id=1, surah=1, index=1, key="k",
                    rasm=rasm(next(iter(forms_.values()))), pointed="", rasm_uthmani="",
                    plain="", status=STATUS_RASM, present=list(forms_),
                    missing=[], forms=forms_, ayah={}, waqf={}, boundary={},
                    division=[], sajdah=[])

    def test_final_shapes_fold_to_their_class(self):
        # ں and ى are a nūn and a yāʾ at the end of a word; medially both are ٮ.
        self.assertEqual(unpositioned("ٮسٮهى"), "ٮسٮهٮ")
        self.assertEqual(unpositioned("ٮعملوں"), "ٮعملوٮ")
        self.assertEqual(unpositioned("ٮعملوٮ"), "ٮعملوٮ")

    def test_one_letter_more(self):
        # 5:54 يَرۡتَدَّ/يَرۡتَدِدۡ — a dāl added, nothing exchanged.
        self.assertTrue(_difference_is_length(
            self.word(hafs="يَرۡتَدَّ", warsh="يَرۡتَدِدۡ")))
        # 43:71 تَشۡتَهِيهِ/تَشۡتَهِي — a hāʾ added.  Only the final-shape fold makes
        # that visible: ٮسٮهى against ٮسٮهٮه would otherwise read as a swap too.
        self.assertTrue(_difference_is_length(
            self.word(hafs="تَشۡتَهِيهِ", warsh="تَشۡتَهِي")))

    def test_one_letter_for_another(self):
        # 91:15 وَلَا/فَلَا and 7:137 كَلِمَتُ/كَلِمَةُ — exchanged, not added.
        self.assertFalse(_difference_is_length(
            self.word(hafs="وَلَا", warsh="فَلَا")))
        self.assertFalse(_difference_is_length(
            self.word(hafs="كَلِمَتُ", warsh="كَلِمَةُ")))


class TestStarts(unittest.TestCase):
    """Every layer is a sorted list of positions, one per unit."""

    def test_a_start_is_where_the_value_changes(self):
        self.assertEqual(_starts([1, 1, 1, 2, 2]), [0, 3])

    def test_a_single_word_unit_is_one_start(self):
        self.assertEqual(_starts([7]), [0])

    def test_a_repeated_value_that_is_not_adjacent_starts_again(self):
        # Āyah numbers restart every sūrah, so 1 follows 1 across a boundary
        # without the two being the same āyah.
        self.assertEqual(_starts([(1, 1), (1, 2), (2, 1)]), [0, 1, 2])


class TestMarks(unittest.TestCase):
    """A mark says which side of the word it is printed on."""

    def word(self, **kw):
        return Word(id=1, surah=1, index=1, key="k", rasm="r", pointed="p",
                    rasm_uthmani="u", plain="s", status=STATUS_IDENTICAL,
                    present=["hafs"], missing=[], forms={"hafs": "u"},
                    ayah={"hafs": 1}, waqf=kw.get("waqf", {}), boundary={},
                    division=kw.get("division", []), sajdah=kw.get("sajdah", []),
                    place={})

    def test_rubu_al_hizb_sits_before_the_word(self):
        self.assertEqual(_marks(self.word(division=["hafs"]), "hafs"),
                         [{"kind": "division", "side": "before", "sign": "۞"}])

    def test_a_waqf_mark_sits_after_it(self):
        self.assertEqual(_marks(self.word(waqf={"hafs": "ۖ"}), "hafs"),
                         [{"kind": "waqf", "side": "after", "sign": "ۖ"}])

    def test_sajdah_is_its_own_kind_not_a_waqf_mark(self):
        # ۩ arrives through the same channel as the waqf marks and must not
        # also be reported as one.
        marks = _marks(self.word(waqf={"hafs": "۩"}, sajdah=["hafs"]), "hafs")
        self.assertEqual(marks, [{"kind": "sajdah", "side": "after", "sign": "۩"}])

    def test_a_word_of_another_riwayah_carries_none_of_them(self):
        self.assertEqual(_marks(self.word(division=["hafs"]), "warsh"), [])


class TestNumbering(unittest.TestCase):
    """The numbering block is the whole map from positions to numbers."""

    def word(self, n, **kw):
        return Word(id=n, surah=1, index=n, key="k", rasm="r", pointed="p",
                    rasm_uthmani="u", plain="s", status=STATUS_IDENTICAL,
                    present=list(kw.get("forms", {"a": "u"})), missing=[],
                    forms=kw.get("forms", {"a": "u"}), ayah={"a": 1}, waqf={},
                    boundary={}, division=[], sajdah=[], place={},
                    continuation=kw.get("continuation", []))

    def test_a_missing_number_is_a_gap_not_a_position(self):
        words = [self.word(1), self.word(2, forms={"b": "u"}), self.word(3)]
        printed, missing = printed_words(words, "a")
        self.assertEqual([p.position for p in printed], [0, 1])
        self.assertEqual(numbering(printed, missing, total=3),
                         {"total": 3, "missing": [2], "written_joined": []})

    def test_a_joined_word_covers_a_run(self):
        words = [self.word(1), self.word(2), self.word(3, continuation=["a"]),
                 self.word(4)]
        printed, missing = printed_words(words, "a")
        self.assertEqual(len(printed), 3)
        self.assertEqual(numbering(printed, missing, total=4)["written_joined"],
                         [{"position": 1, "numbers": [2, 3]}])

    def test_the_invariants_catch_a_run_that_does_not_tile(self):
        doc = {"mushaf": {"key": "x", "word_count": 2}, "words": ["a", "b"],
               "numbering": {"total": 3, "missing": [], "written_joined": []}}
        self.assertTrue(any(p["check"] == "numbering_tiles"
                            for p in check_numbering({"x": doc})))


class TestPublishedFiles(unittest.TestCase):
    """The committed out/ must satisfy what the spec promises.

    Skipped when out/ has not been built; run after ``python3 build.py``.
    """

    KEYS = ["hafs", "shubah", "warsh", "qalun", "duri", "susi", "bazzi"]

    @classmethod
    def setUpClass(cls):
        paths = [ROOT / "out" / "mushaf" / f"{k}.json" for k in cls.KEYS]
        if not all(p.exists() for p in paths):
            raise unittest.SkipTest("out/ not built")
        cls.docs = {k: json.loads(p.read_text(encoding="utf-8"))
                    for k, p in zip(cls.KEYS, paths)}

    def test_numbering_tiles_the_master(self):
        self.assertEqual(check_numbering(self.docs), [])
        self.assertEqual({d["numbering"]["total"] for d in self.docs.values()},
                         {77434})

    def test_positions_are_well_formed(self):
        self.assertEqual(check_positions(self.docs), [])

    def test_written_joined_is_exactly_the_two_ayahs(self):
        # Ḥafṣ, Shuʿbah, Bazzī at 72:16; Dūrī, Sūsī at 73:20.  The issue's
        # claim that these five āyāt are the entire scope, asserted.
        seen = {(k, tuple(j["numbers"]))
                for k, d in self.docs.items()
                for j in d["numbering"]["written_joined"]}
        self.assertEqual(seen, {
            ("hafs", (73950, 73951)), ("shubah", (73950, 73951)),
            ("bazzi", (73950, 73951)),
            ("duri", (74226, 74227)), ("susi", (74226, 74227))})

    def test_missing_is_exactly_the_three_words(self):
        missing = {k: d["numbering"]["missing"] for k, d in self.docs.items()}
        self.assertEqual(missing["hafs"], [25685])           # Bazzī's مِن
        self.assertEqual(missing["warsh"], [25685, 60522, 69720])  # + أَوۡ, هُوَ
        self.assertEqual(missing["bazzi"], [60522])

    def test_ayah_slices_are_correct_in_all_seven(self):
        for k, d in self.docs.items():
            a = d["ayah_starts"]
            first = d["words"][a[0]:a[1]]
            if d["counting"]["basmalah_counted"]:
                self.assertEqual(len(first), 4, k)            # the basmalah
                self.assertEqual(a[0], 0, k)
            else:
                self.assertEqual(a[0], 4, k)                  # after the basmalah
                self.assertEqual(len(first), 4, k)            # ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ
            self.assertEqual(len(a), d["counting"]["ayah_count"], k)
            # Slicing never crosses a sūrah: the last āyah of sūrah 1 ends
            # where sūrah 2 starts.
            self.assertEqual(a[d["surahs"][1]["first_ayah"]], d["surah_starts"][1], k)

    def test_counting_systems_are_as_expected(self):
        systems = {k: d["counting"]["system"] for k, d in self.docs.items()}
        self.assertEqual(systems, {
            "hafs": "kufi", "shubah": "kufi",
            "warsh": "madani-last", "qalun": "madani-last",
            "duri": "madani-first", "susi": "madani-first",
            "bazzi": "makki"})
        counts = {k: d["counting"]["ayah_count"] for k, d in self.docs.items()}
        self.assertEqual(counts, {"hafs": 6236, "shubah": 6236, "warsh": 6214,
                                  "qalun": 6214, "duri": 6217, "susi": 6218,
                                  "bazzi": 6220})

    def test_duri_and_susi_part_company_at_67_9_only(self):
        d, s = self.docs["duri"]["counting"], self.docs["susi"]["counting"]
        differ = [(a["kufi"], a["counted"], b["counted"])
                  for a, b in zip(d["khilaf"], s["khilaf"])
                  if a["counted"] != b["counted"]]
        self.assertEqual(differ, [("67:9", False, True)])
        self.assertEqual(next(a for a in d["khilaf"] if a["kufi"] == "67:9")["follows"],
                         ["abu-jafar"])
        self.assertEqual(next(a for a in s["khilaf"] if a["kufi"] == "67:9")["follows"],
                         ["shayba"])

    def test_unexplained_is_allowlisted(self):
        from qurantext.counting import check_unexplained, open_findings
        self.assertEqual(check_unexplained(self.docs), [])
        unexplained = {(k, u["surah"], u["ayah"]) for k, d in self.docs.items()
                       for u in d["counting"]["unexplained"]}
        self.assertEqual(unexplained,
                         {(f["mushaf"], f["surah"], f["ayah"]) for f in open_findings()})

    def test_the_word_index_gives_every_number_a_text(self):
        path = ROOT / "out" / "word-index.json"
        if not path.exists():
            self.skipTest("word index not built")
        index = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual([w["number"] for w in index["words"]], list(range(1, 77435)))
        law = index["words"][73950]
        self.assertEqual(law["rasm_uthmani"], "لَّوِ")          # not Ḥafṣ's joined form
        self.assertEqual(law["forms"]["hafs"], "وَأَلَّوِ")
        self.assertEqual(law["hafs"], index["words"][73949]["hafs"])
        self.assertIsNone(index["words"][25684]["hafs"])   # Ḥafṣ lacks مِن
        self.assertEqual(index["words"][25684]["missing"],
                         ["hafs", "shubah", "warsh", "qalun", "duri", "susi"])

    def test_the_ayah_map_answers_what_an_ayah_is_elsewhere(self):
        path = ROOT / "out" / "ayah-map.json"
        if not path.exists():
            self.skipTest("ayah map not built")
        rows = json.loads(path.read_text(encoding="utf-8"))["ayahs"]
        self.assertEqual(len(rows), 6236)
        at = {(r["surah"], r["ayah"]): r for r in rows}
        # The basmalah is 1:1 in Ḥafṣ and unnumbered in Warsh.
        self.assertEqual(at[(1, 1)]["warsh"],
                         {"surah": 1, "ayah": 0, "relation": "unnumbered"})
        # 67:9 is one āyah in Ḥafṣ and two in Sūsī.
        self.assertEqual(at[(67, 9)]["susi"]["relation"], "split")
        self.assertEqual(at[(67, 9)]["duri"]["relation"], "same")
        # Everything Ḥafṣ maps onto itself unchanged.
        self.assertTrue(all(r["hafs"] == {"surah": r["surah"], "ayah": r["ayah"],
                                          "relation": "same"} for r in rows))


class TestRasmImlaiPairing(unittest.TestCase):
    """Bringing an āyah-level column down to the word."""

    def test_equal_counts_pair_across(self):
        self.assertEqual(_pair(["ا", "ب"], ["a", "b"]), ["a", "b"])

    def test_one_rasm_uthmani_word_written_as_two_rasm_imlai_ones_is_joined(self):
        # أَوَلَا is one word on the line and two in plain spelling.
        got = _pair(["أَوَلَا", "يَعۡلَمُونَ"], ["أو", "لا", "يعلمون"])
        self.assertEqual(got, ["أو لا", "يعلمون"])

    def test_fewer_rasm_imlai_tokens_is_refused_rather_than_guessed(self):
        self.assertIsNone(_pair(["ا", "ب", "ج"], ["a", "b"]))


class TestTokenPlacement(unittest.TestCase):
    """A word has to keep its place on the page through the mark-peeling."""

    def test_a_word_takes_the_place_of_its_own_token(self):
        toks = tokenize_ayah(1, 1, "بِسۡمِ ٱللَّهِ",
                             [Place(1, 2), Place(1, 3)])
        self.assertEqual([(t.page, t.line) for t in toks], [(1, 2), (1, 3)])

    def test_a_standalone_symbol_does_not_consume_a_place(self):
        # ۞ stands between words and produces no token, so the word after it
        # must still take the position that belongs to it.
        toks = tokenize_ayah(2, 26, "۞ إِنَّ ٱللَّهَ",
                             [Place(5, 1), Place(5, 1), Place(5, 2)])
        self.assertEqual(len(toks), 2)
        self.assertTrue(toks[0].division)
        self.assertEqual([(t.page, t.line) for t in toks], [(5, 1), (5, 2)])

    def test_no_places_means_no_placement_rather_than_a_wrong_one(self):
        toks = tokenize_ayah(1, 1, "بِسۡمِ ٱللَّهِ")
        self.assertEqual([(t.page, t.line) for t in toks], [(0, 0), (0, 0)])


if __name__ == "__main__":
    unittest.main()
