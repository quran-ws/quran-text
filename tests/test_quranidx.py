"""Unit tests for the pieces where a silent mistake would corrupt the index.

Run with:  python3 -m unittest discover -s tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from quranidx.align import Column, _distribute, merge          # noqa: E402
from quranidx.build import (STATUS_ALIF, STATUS_IDENTICAL,     # noqa: E402
                            STATUS_RASM, Kalimah,
                            classify)
from quranidx.normalize import (forms, pointed, rasm, rasm_plene,  # noqa: E402
                                simple, split_by_rasm, split_trailing_waqf,
                                unpositioned)
from quranidx.report import _difference_is_length                 # noqa: E402
from quranidx.validate import check_alif_splits                    # noqa: E402
from quranidx.tokenize import Token, tokenize_ayah             # noqa: E402
from quranidx.imlaei import _pair                              # noqa: E402
from quranidx.layout import Place                              # noqa: E402
from quranidx.mushaf import _marks, _spans, minimal            # noqa: E402


def tok(rasm_: str) -> Token:
    return Token(surah=1, ayah=1, pos=1, uthmani=rasm_, folded=rasm_,
                 pointed=rasm_, rasm=rasm_, rasm_plene=rasm_, simple=rasm_)


def real(kalimah: str) -> Token:
    """A token with every form derived from ``kalimah``, as the build makes it."""
    f = forms(kalimah)
    return Token(surah=1, ayah=1, pos=1, uthmani=f["uthmani"], folded=f["folded"],
                 pointed=f["pointed"], rasm=f["rasm"],
                 rasm_plene=f["rasm_plene"], simple=f["simple"])


class TestNormalize(unittest.TestCase):
    def test_rasm_folds_alef_forms(self):
        # Every alif spelling must collapse, or the riwayahs will not align.
        for kalimah in ["ٱللَّهِ", "اِ۬للَّهِ", "ࡴ۬للَّهِ", "ࡵ۬للَّهِ"]:
            self.assertEqual(rasm(kalimah), "الله", kalimah)

    def test_rasm_drops_the_dots(self):
        # The mushafs were undotted, so one rasm carries both qira'ahs and the
        # kalimah keeps one ID.  The qira'ah itself survives in `pointed`.
        self.assertEqual(rasm("تَعۡمَلُونَ"), rasm("يَعۡمَلُونَ"))
        self.assertEqual(rasm("تَعۡمَلُونَ"), "ٮعملوں")
        self.assertNotEqual(pointed("تَعۡمَلُونَ"), pointed("يَعۡمَلُونَ"))

    def test_dots_part_company_at_the_end_of_a_kalimah(self):
        # ب ت ث ن ي share a tooth medially only; final ن and ي keep their tails.
        self.assertEqual(rasm("نَبَتَ")[:-1], "ٮٮ")
        self.assertNotEqual(rasm("مِن"), rasm("مِي"))

    def test_rasm_drops_hamza(self):
        # Hamza is 8th-century notation, not part of the mushafs.  Warsh's
        # yeh-barree-with-hamza and Ḥafṣ's hamza-on-yeh are one kalimah.
        self.assertEqual(rasm("يَسۡتَهۡزِئُ"), rasm("يَسْتَهْزِۓُ"))
        self.assertEqual(rasm("هَٰٓؤُلَآءِ"), rasm("هَٰؤُلَآࢇ"))

    def test_the_dagger_alif_is_not_on_the_line(self):
        # A superscript alef is by definition an alef the scribe did not write.
        # ملك is the skeleton that carries both مَٰلِكِ and مَلِكِ — the ḥadhf
        # al-alif that lets one mushaf serve seven riwayahs — so folding it to a
        # harf invents a disagreement between mushafs that agree.
        self.assertEqual(rasm("مَٰلِكِ"), rasm("مَلِكِ"))
        self.assertEqual(rasm("دِفَٰعُ"), rasm("دَفۡعُ"))
        self.assertEqual(rasm("ٱلرِّيَٰحَ"), rasm("ٱلرِّيحَ"))
        self.assertEqual(rasm("طَٰٓئِراَۢ"), rasm("طَيۡرَۢا"))

    def test_the_reading_keeps_the_a_that_the_line_does_not(self):
        # The ā is real, it is just not written: `pointed` spells the kalimah as
        # it is read, so مَٰلِكِ and مَلِكِ stay two qira'ahs of one rasm.
        self.assertNotEqual(pointed("مَٰلِكِ"), pointed("مَلِكِ"))
        self.assertEqual(pointed("مَٰلِكِ"), "مالك")

    def test_a_dagger_on_an_alef_already_there_adds_nothing(self):
        self.assertEqual(pointed("ءَامَنُواْ"), pointed("اٰمَنُواْ"))
        self.assertEqual(rasm("ءَامَنُواْ"), rasm("اٰمَنُواْ"))

    def test_plene_and_defective_are_told_apart_from_a_real_difference(self):
        # The two typesettings disagree in both directions about which ā to put
        # on the line, so the bare rasm alone cannot tell that difference of
        # hand from a difference of mushaf.  `rasm_plene` is what does.
        self.assertNotEqual(rasm("هَٰرُوتَ"), rasm("هَارُوتَ"))
        self.assertEqual(rasm_plene("هَٰرُوتَ"), rasm_plene("هَارُوتَ"))
        self.assertEqual(rasm_plene("مُبَٰرَك"), rasm_plene("مُبَارَك"))
        # A harf one mushaf has and another does not survives both.
        self.assertNotEqual(rasm("قُلۡ"), rasm("قَالَ"))
        self.assertNotEqual(rasm_plene("قُلۡ"), rasm_plene("قَالَ"))

    def test_adjacent_alefs_are_not_welded(self):
        # Bazzī's لَأُاْقۡسِمُ is لَآ + أُقۡسِمُ printed as one kalimah: the two alefs are
        # separate harfs, and collapsing them would break 75:1.
        self.assertEqual(rasm("لَأُاْقۡسِمُ"), rasm("لَآ") + rasm("أُقۡسِمُ"))

    def test_dagger_standing_in_for_a_suppressed_hamza_is_not_an_alef(self):
        # Warsh's tashīl drops the hamza of أَرَءَيۡتَ and leaves its madd on a
        # dagger alif.  A madd with no hamza after it is notating a hamza, not
        # an ā — so it is not a harf even in the form that spells the qira'ah.
        self.assertEqual(rasm("أَرَءَيۡتَ"), rasm("ࡰرَٰٓيْتَ"))
        self.assertEqual(pointed("أَرَءَيۡتَ"), pointed("ࡰرَٰٓيْتَ"))
        self.assertEqual(rasm("أَرَءَيۡتَكُمۡ"), rasm("أَرَٰ۬يْتَكُمْ"))

    def test_a_madd_that_does_have_its_hamza_is_still_an_alef(self):
        # Where the hamza is present the dagger is a genuine ā, so it belongs
        # to the qira'ah — and to `rasm_plene`, which is what makes Ḥafṣ's
        # إِسۡرَٰٓءِيلَ and Warsh's إِسْرَآءِيلَ one spelling of one kalimah.
        self.assertEqual(pointed("إِسۡرَٰٓءِيلَ"), pointed("إِسْرَآءِيلَ"))
        self.assertEqual(rasm_plene("إِسۡرَٰٓءِيلَ"), rasm_plene("إِسْرَآءِيلَ"))
        self.assertEqual(rasm("هَٰٓؤُلَآءِ"), rasm("هَٰؤُلَآࢇ"))

    def test_madd_lazim_over_a_shadda_is_still_an_alef(self):
        # تَتَّبِعَٰٓنِّ and فَذَٰٓنِّكَ put the madd over a doubled harf, not a
        # hamza: a real long ā, which other packages write on the line.
        self.assertEqual(pointed("تَتَّبِعَآنِّ"), pointed("تَتَّبِعَٰٓنِّ"))
        self.assertEqual(rasm_plene("فَذَٰنِكَ"), rasm_plene("فَذَٰٓنِّكَ"))

    def test_a_kalimah_final_madd_is_not_a_harf_of_its_own(self):
        # عَلَىٰٓ is ʿalā and عَلَيَّ is ʿalayya — a real variant at 7:105, and a
        # variant of *qira'ah*: both are written على, which is the point of the
        # skeleton.  Emitting the dagger as an extra alef made the kalimah علىا.
        self.assertEqual(rasm("عَلَىٰٓ"), "على")
        self.assertEqual(rasm("عَلَىٰٓ"), rasm("عَلَيَّ"))
        self.assertNotEqual(pointed("عَلَىٰٓ"), pointed("عَلَيَّ"))
        # 34:17 نُجَٰزِي / يُجَٰزَىٰ: four harfs, whichever way it is read.
        self.assertEqual(rasm("يُجَٰزَىٰ"), rasm("نُجَٰزِيٓ"))
        self.assertEqual(rasm("يُجَٰزَىٰ"), "ٮحرى")

    def test_rasm_keeps_real_harf_differences(self):
        # Bazzī reads قَالَ where the others read قُلۡ: different harfs.
        self.assertNotEqual(rasm("قُلۡ"), rasm("قَالَ"))

    def test_silah_is_a_vowel_not_a_harf(self):
        # Bazzī's ṣilat al-mīm is written superscript, so it is not part of the
        # rasm: عَلَيۡهِمُۥ and عَلَيۡهِمۡ are one kalimah read two ways, and must align.
        self.assertEqual(rasm("عَلَيۡهِمُۥ"), rasm("عَلَيۡهِمۡ"))
        self.assertEqual(pointed("عَلَيۡهِمُۥ"), "عليهم")

    def test_superscript_yeh_is_a_harf_others_write_on_the_line(self):
        # ٱلنَّبِيِّۧنَ writes its second yāʾ superscript; Warsh prints it as ۑ.
        self.assertEqual(rasm("ٱلنَّبِيِّۧنَ"), rasm("ࡰ۬لنَّبِيِٕٓۑنَ"))

    def test_simple_spelling_expands_superscript_alef(self):
        self.assertEqual(simple("مَٰلِكِ"), "مالك")

    def test_waqf_is_peeled_not_dropped(self):
        kalimah, waqf = split_trailing_waqf("رَيۡبَۛ")
        self.assertEqual(waqf, "ۛ")
        self.assertEqual(pointed(kalimah), "ريب")

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
    def test_splits_a_kalimah_printed_without_its_space(self):
        pieces = split_by_rasm("كَانُواْيَعۡمَلُونَ", [5, 7])
        self.assertEqual([pointed(p) for p in pieces], ["كانوا", "يعملون"])

    def test_marks_stay_with_the_harf_they_sit_on(self):
        pieces = split_by_rasm("قَتَرٞوَلَا", [3, 3])
        self.assertEqual(pieces[0], "قَتَرٞ")      # the tanwīn belongs to قتر
        self.assertEqual(pieces[1], "وَلَا")

    def test_round_trips(self):
        kalimah = "وَمَالِيَ"
        self.assertEqual("".join(split_by_rasm(kalimah, [3, 2])), kalimah)


class TestTokenize(unittest.TestCase):
    def test_hizb_symbol_is_not_a_kalimah(self):
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

    def test_a_joined_kalimah_is_resegmented_into_its_columns(self):
        spine = [Column(tokens={"a": tok("كانوا")}), Column(tokens={"a": tok("يعملون")})]
        out = merge(spine, "b", [tok("كانوايعملون")])
        self.assertEqual(len(out), 2)
        # Both columns keep riwayah b, so no kalimah is reported missing.
        self.assertTrue(all("b" in c.tokens for c in out))
        self.assertEqual([c.boundary["b"] for c in out],
                         ["joined_in_source"] * 2)

    def test_an_inserted_kalimah_gets_its_own_column(self):
        spine = [Column(tokens={"a": tok("تجري")}), Column(tokens={"a": tok("تحتها")})]
        out = merge(spine, "b", [tok("تجري"), tok("من"), tok("تحتها")])
        self.assertEqual([c.rasm for c in out], ["تجري", "من", "تحتها"])
        self.assertNotIn("a", out[1].tokens)      # only Bazzī has مِن at 9:101

    def test_distribute_groups_by_harfs_not_by_position(self):
        cols = [Column(tokens={"a": tok("ما")}), Column(tokens={"a": tok("لي")})]
        groups = _distribute(cols, [tok("مالي")])
        self.assertEqual(len(groups), 1)
        self.assertEqual((len(groups[0][0]), len(groups[0][1])), (2, 1))


class TestClassify(unittest.TestCase):
    """A difference of hand and a difference of mushaf are not one label."""

    KEYS = ["hafs", "warsh"]

    def column(self, hafs: str, warsh: str) -> Column:
        return Column(tokens={"hafs": real(hafs), "warsh": real(warsh)})

    def test_plene_against_defective_is_its_own_status(self):
        # هَٰرُوتَ against هَارُوتَ is a difference of hand, not of mushaf: the two
        # typesettings disagree in both directions and every such kalimah in the
        # corpus splits the seven the same single way.  It is reported, but
        # apart from the harfs the mushafs actually disagree about.
        self.assertEqual(classify(self.column("هَٰرُوتَ", "هَارُوتَ"), self.KEYS),
                         STATUS_ALIF)
        self.assertEqual(classify(self.column("مُبَارَكࣰا", "مُبَٰرَكاࣰ"), self.KEYS),
                         STATUS_ALIF)
        self.assertEqual(rasm_plene("هَٰرُوتَ"), rasm_plene("هَارُوتَ"))
        # The bare rasm still keeps it: within one mushaf it is that mushaf's
        # own ḥadhf.
        self.assertNotEqual(rasm("هَٰرُوتَ"), rasm("هَارُوتَ"))

    def test_a_harf_one_mushaf_lacks_is_a_rasm_variant(self):
        self.assertEqual(classify(self.column("قُلۡ", "قَالَ"), self.KEYS),
                         STATUS_RASM)

    def test_a_harf_added_is_a_rasm_variant_not_an_alif_one(self):
        # 5:54 يَرۡتَدَّ / يَرۡتَدِدۡ and 43:71 تَشۡتَهِيهِ / تَشۡتَهِي: a harf on the line
        # that the other mushaf does not have at all.
        self.assertEqual(classify(self.column("يَرۡتَدَّ", "يَرۡتَدِدۡ"), self.KEYS),
                         STATUS_RASM)
        self.assertEqual(classify(self.column("تَشۡتَهِيهِ", "تَشۡتَهِي"), self.KEYS),
                         STATUS_RASM)

    def test_a_dagger_against_nothing_is_not_a_rasm_variant(self):
        # 1:4 — ملك in every mushaf, read مالك by Ḥafṣ.  The qira'ah survives in
        # `pointed`, so this is a dotting/vowelling difference, not a rasm one.
        self.assertNotEqual(classify(self.column("مَٰلِكِ", "مَلِكِ"), self.KEYS),
                            STATUS_RASM)
        self.assertNotEqual(classify(self.column("مَٰلِكِ", "مَلِكِ"), self.KEYS),
                            STATUS_IDENTICAL)


class TestAlifSplitsOneWay(unittest.TestCase):
    """The one fact `alif_variant` rests on, asserted rather than assumed."""

    def kalimah(self, id_: int, **forms_: str) -> Kalimah:
        return Kalimah(id=id_, surah=1, index=id_, key=f"k{id_}", rasm="", pointed="",
                       uthmani="", simple="", status="alif_variant",
                       present=list(forms_), missing=[], forms=forms_, ayah={},
                       waqf={}, boundary={}, hizb=[], sajdah=[])

    def test_one_partition_passes(self):
        # Both directions are fine — what matters is who is on each side.
        kalimahs = [self.kalimah(1, hafs="هَٰرُوتَ", bazzi="هَٰرُوتَ", warsh="هَارُوتَ"),
                    self.kalimah(2, hafs="مُبَارَك", bazzi="مُبَارَك", warsh="مُبَٰرَك")]
        self.assertEqual(check_alif_splits(kalimahs), [])

    def test_makkah_leaving_the_kufi_side_is_reported(self):
        # Bazzī is Makkī.  A plene/defective kalimah that puts it with Madinah is a
        # khilāf of the amṣār, not a house style, and the status would no longer
        # be warranted.
        kalimahs = [self.kalimah(1, hafs="هَٰرُوتَ", bazzi="هَٰرُوتَ", warsh="هَارُوتَ"),
                    self.kalimah(2, hafs="هَٰرُوتَ", bazzi="هَارُوتَ", warsh="هَارُوتَ")]
        problems = check_alif_splits(kalimahs)
        self.assertEqual([p["check"] for p in problems], ["alif_splits_one_way"])

    def test_other_statuses_are_not_its_business(self):
        kalimahs = [self.kalimah(1, hafs="قُلۡ", warsh="قَالَ")]
        kalimahs[0].status = "rasm_variant"
        self.assertEqual(check_alif_splits(kalimahs), [])


class TestShapeOfDifference(unittest.TestCase):
    """What kind of harf difference a rasm variant is."""

    def kalimah(self, **forms_: str) -> Kalimah:
        return Kalimah(id=1, surah=1, index=1, key="k",
                       rasm=rasm(next(iter(forms_.values()))), pointed="", uthmani="",
                       simple="", status=STATUS_RASM, present=list(forms_),
                       missing=[], forms=forms_, ayah={}, waqf={}, boundary={},
                       hizb=[], sajdah=[])

    def test_final_shapes_fold_to_their_class(self):
        # ں and ى are a nūn and a yāʾ at the end of a kalimah; medially both are ٮ.
        self.assertEqual(unpositioned("ٮسٮهى"), "ٮسٮهٮ")
        self.assertEqual(unpositioned("ٮعملوں"), "ٮعملوٮ")
        self.assertEqual(unpositioned("ٮعملوٮ"), "ٮعملوٮ")

    def test_one_harf_more(self):
        # 5:54 يَرۡتَدَّ/يَرۡتَدِدۡ — a dāl added, nothing exchanged.
        self.assertTrue(_difference_is_length(
            self.kalimah(hafs="يَرۡتَدَّ", warsh="يَرۡتَدِدۡ")))
        # 43:71 تَشۡتَهِيهِ/تَشۡتَهِي — a hāʾ added.  Only the final-shape fold makes
        # that visible: ٮسٮهى against ٮسٮهٮه would otherwise read as a swap too.
        self.assertTrue(_difference_is_length(
            self.kalimah(hafs="تَشۡتَهِيهِ", warsh="تَشۡتَهِي")))

    def test_one_harf_for_another(self):
        # 91:15 وَلَا/فَلَا and 7:137 كَلِمَتُ/كَلِمَةُ — exchanged, not added.
        self.assertFalse(_difference_is_length(
            self.kalimah(hafs="وَلَا", warsh="فَلَا")))
        self.assertFalse(_difference_is_length(
            self.kalimah(hafs="كَلِمَتُ", warsh="كَلِمَةُ")))


class TestSpans(unittest.TestCase):
    """Boundaries over kalimah IDs, which is how every layer is expressed."""

    def test_consecutive_equal_values_collapse(self):
        self.assertEqual(
            _spans([(1, 10), (1, 11), (1, 12), (2, 13), (2, 14)]),
            [{"n": 1, "kalimahs": [10, 12]}, {"n": 2, "kalimahs": [13, 14]}])

    def test_a_single_kalimah_span_is_first_and_last_alike(self):
        self.assertEqual(_spans([(7, 99)]), [{"n": 7, "kalimahs": [99, 99]}])

    def test_a_repeated_value_that_is_not_adjacent_stays_two_spans(self):
        # Ayah numbers restart every surah, so 1 follows 1 across a boundary
        # without the two being the same ayah.
        self.assertEqual(
            _spans([(1, 5), (2, 6), (1, 7)]),
            [{"n": 1, "kalimahs": [5, 5]},
             {"n": 2, "kalimahs": [6, 6]},
             {"n": 1, "kalimahs": [7, 7]}])


class TestMarks(unittest.TestCase):
    """A mark says which side of the kalimah it is printed on."""

    def kalimah(self, **kw):
        return Kalimah(id=1, surah=1, index=1, key="k", rasm="r", pointed="p",
                       uthmani="u", simple="s", status=STATUS_IDENTICAL,
                       present=["hafs"], missing=[], forms={"hafs": "u"},
                       ayah={"hafs": 1}, waqf=kw.get("waqf", {}), boundary={},
                       hizb=kw.get("hizb", []), sajdah=kw.get("sajdah", []),
                       place={})

    def test_rub_el_hizb_sits_before_the_kalimah(self):
        self.assertEqual(_marks(self.kalimah(hizb=["hafs"]), "hafs"),
                         [{"k": "hizb", "at": "before", "sign": "۞"}])

    def test_a_pause_mark_sits_after_it(self):
        self.assertEqual(_marks(self.kalimah(waqf={"hafs": "ۖ"}), "hafs"),
                         [{"k": "waqf", "at": "after", "sign": "ۖ"}])

    def test_sajdah_is_its_own_kind_not_a_pause_mark(self):
        # ۩ arrives through the same channel as the pause marks and must not
        # also be reported as one.
        marks = _marks(self.kalimah(waqf={"hafs": "۩"}, sajdah=["hafs"]), "hafs")
        self.assertEqual(marks, [{"k": "sajdah", "at": "after", "sign": "۩"}])

    def test_a_kalimah_of_another_riwaya_carries_none_of_them(self):
        self.assertEqual(_marks(self.kalimah(hizb=["hafs"]), "warsh"), [])


class TestMinimalVariant(unittest.TestCase):
    """The small file drops conveniences, never disclosures."""

    DOC = {
        "format": "quran-mushaf", "format_version": "2.0",
        "generated": "2026-09-01", "mushaf": {}, "provenance": {}, "spine": {},
        "surahs": [{"n": 1, "name_ar": "a", "ayahs": 7, "kalimahs": [1, 29],
                   "safhahs": [1, 1]}],
        "ayahs": [{"surah": 1, "n": 1, "kalimahs": [1, 4]}],
        "resegmentation": [{"kalimahs": [1, 2], "kind": "joined_in_source"}],
        "line_disagreements": [{"surah": 1, "ayah": 1}],
        "kalimahs": [{"w": 1, "t": "بِسۡمِ", "pg": 1, "ln": 3, "e": "بسم",
                      "marks": [{"k": "waqf", "at": "after", "sign": "ۖ"}]}],
    }

    def test_a_kalimah_keeps_only_its_id_and_its_text(self):
        self.assertEqual(minimal(self.DOC)["kalimahs"], [{"w": 1, "t": "بِسۡمِ"}])

    def test_resegmentation_survives(self):
        # It is a disclosure about the text itself; dropping it would make the
        # small file quietly less honest than the large one.
        self.assertEqual(minimal(self.DOC)["resegmentation"],
                         self.DOC["resegmentation"])

    def test_layout_does_not(self):
        self.assertNotIn("safhahs", minimal(self.DOC)["surahs"][0])


class TestImlaeiPairing(unittest.TestCase):
    """Bringing an ayah-level column down to the kalimah."""

    def test_equal_counts_pair_across(self):
        self.assertEqual(_pair(["ا", "ب"], ["a", "b"]), ["a", "b"])

    def test_one_uthmani_kalimah_written_as_two_imlaei_ones_is_joined(self):
        # أَوَلَا is one kalimah on the line and two in plain spelling.
        got = _pair(["أَوَلَا", "يَعۡلَمُونَ"], ["أو", "لا", "يعلمون"])
        self.assertEqual(got, ["أو لا", "يعلمون"])

    def test_fewer_imlaei_tokens_is_refused_rather_than_guessed(self):
        self.assertIsNone(_pair(["ا", "ب", "ج"], ["a", "b"]))


class TestTokenPlacement(unittest.TestCase):
    """A kalimah has to keep its place on the safhah through the mark-peeling."""

    def test_a_kalimah_takes_the_place_of_its_own_token(self):
        toks = tokenize_ayah(1, 1, "بِسۡمِ ٱللَّهِ",
                             [Place(1, 2), Place(1, 3)])
        self.assertEqual([(t.safhah, t.line) for t in toks], [(1, 2), (1, 3)])

    def test_a_standalone_symbol_does_not_consume_a_place(self):
        # ۞ stands between kalimahs and produces no token, so the kalimah after it
        # must still take the position that belongs to it.
        toks = tokenize_ayah(2, 26, "۞ إِنَّ ٱللَّهَ",
                             [Place(5, 1), Place(5, 1), Place(5, 2)])
        self.assertEqual(len(toks), 2)
        self.assertTrue(toks[0].hizb)
        self.assertEqual([(t.safhah, t.line) for t in toks], [(5, 1), (5, 2)])

    def test_no_places_means_no_placement_rather_than_a_wrong_one(self):
        toks = tokenize_ayah(1, 1, "بِسۡمِ ٱللَّهِ")
        self.assertEqual([(t.safhah, t.line) for t in toks], [(0, 0), (0, 0)])


if __name__ == "__main__":
    unittest.main()
