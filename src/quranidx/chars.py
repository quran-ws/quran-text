"""Character classification tables for KFGQPC Uthmanic text.

Derived from a full codepoint inventory of every source shipped in ``data/``
(see ``docs/CHARSET.md``).  The tables below are the single place where a
codepoint's role is decided; everything downstream asks these sets.
"""

# --- structural / non-text ------------------------------------------------

END_OF_AYAH = "۝"          # ۝  ARABIC END OF AYAH (v3 docx)
RUB_EL_HIZB = "۞"          # ۞  ARABIC START OF RUB EL HIZB
SAJDAH      = "۩"          # ۩  ARABIC PLACE OF SAJDAH

ARABIC_DIGITS = {chr(0x0660 + i): str(i) for i in range(10)}

#: Editorial annotation, not text.  U+08CC is the proofreader's *ṣaḥḥa* ("correct
#: as written"); it occurs 8,128 times in the v3.0 Warsh document alone and is
#: the single largest source of spurious differences in the corpus.  U+0888 is
#: its raised-dot companion.  Neither is pronounced or written by any other
#: release, so both are dropped rather than folded.
EDITORIAL = {"࣌", "࢈"}

#: Standalone symbols that mark structure, never part of a word.
STRUCTURAL = {END_OF_AYAH, RUB_EL_HIZB, SAJDAH} | EDITORIAL

#: Invisible controls that carry no textual meaning here.  Their presence in a
#: source is itself reportable (see ``issues.STRAY_CONTROL``).
CONTROLS = {
    "​",  # ZERO WIDTH SPACE
    "‌",  # ZERO WIDTH NON-JOINER
    "‍",  # ZERO WIDTH JOINER
    "‎",  # LEFT-TO-RIGHT MARK
    "‏",  # RIGHT-TO-LEFT MARK
    "﻿",  # ZERO WIDTH NO-BREAK SPACE / BOM
}

TATWEEL = "ـ"  # ـ  kashida: pure typography, never semantic

# --- waqf (pause) marks ---------------------------------------------------
# These sit after the last letter of a word with no intervening space.  They
# annotate recitation, not orthography, so they are peeled off the word and
# recorded separately.

WAQF_MARKS = {
    "ۖ",  # ۖ  ṣlā   - preferable to continue
    "ۗ",  # ۗ  qlā   - preferable to stop
    "ۘ",  # ۘ  mīm   - compulsory stop
    "ۙ",  # ۙ  lā    - prohibited stop
    "ۚ",  # ۚ  jīm   - permissible stop
    "ۛ",  # ۛ  three dots - mu'ānaqah (stop at one of two)
    "ۜ",  # ۜ  small high seen  (KFGQPC: sakta / sīn reading cue)
    "۩",  # ۩  place of sajdah
    "۪",  # ۪  empty centre low stop
    "۫",  # ۫  empty centre high stop
    "۬",  # ۬  rounded high stop with filled centre
}

#: Waqf marks that are *not* peeled in every riwāyah.  U+06EC is used by the
#: Warsh/Qālūn/Dūrī/Sūsī sets as an orthographic hamzat-waṣl cue on alif rather
#: than as a pause sign, so it is only treated as waqf when it trails a word.
CONTEXTUAL_WAQF = {"۬", "۪", "۫"}

# --- vowels, tanwīn, and recitation diacritics ----------------------------

HARAKAT = {
    "ً",  # ً fathatan
    "ٌ",  # ٌ dammatan
    "ٍ",  # ٍ kasratan
    "َ",  # َ fatha
    "ُ",  # ُ damma
    "ِ",  # ِ kasra
    "ّ",  # ّ shadda
    "ْ",  # ْ sukun
    "ۡ",  # ۡ small high dotless head of khah (KFGQPC sukun)
}

#: "Open" tanwīn (iẓhār/idghām notation).  The v2 data sets encode these with
#: repurposed combining marks; the v3.0 sets use the dedicated Arabic Extended-A
#: codepoints added in Unicode 9.  :data:`NOTATION_FOLD` unifies them.
OPEN_TANWEEN = {"ࣰ", "ࣱ", "ࣲ"}

#: Orthographic marks that belong to the word (madd, small letters, rounded
#: zeros, iqlāb mīm, ...).  Kept in the Uthmānī form, dropped from the rasm.
ORTHOGRAPHIC_MARKS = {
    "ٓ",  # ٓ maddah above
    "ٔ",  # ٔ hamza above
    "ٕ",  # ٕ hamza below
    "ٖ",  # ٖ subscript alef      (v2 open kasratan)
    "ٗ",  # ٗ inverted damma      (v2 open dammatan)
    "ٜ",  # ٜ vowel sign dot below
    "ٞ",  # ٞ fatha with two dots (v2 open fathatan)
    "ٰ",  # ٰ superscript alef
    "۟",  # ۟ small high rounded zero
    "۠",  # ۠ small high upright rectangular zero
    "ۢ",  # ۢ small high meem isolated (iqlāb)
    "ۣ",  # ۣ small low seen
    "ۤ",  # ۤ small high madda
    "ۥ",  # ۥ small waw   (ṣilah)
    "ۦ",  # ۦ small yeh   (ṣilah)
    "ۧ",  # ۧ small high yeh
    "ۨ",  # ۨ small high noon
    "ۭ",  # ۭ small low meem (iqlāb)
    "࢈",  # ࢈ raised round dot
    "࣌",  # small high word ṣaḥ
} | OPEN_TANWEEN

#: Everything that is a mark rather than a letter.
ALL_MARKS = HARAKAT | ORTHOGRAPHIC_MARKS | WAQF_MARKS

# --- notation folding -----------------------------------------------------
# The 2022 (v2 / V20) and 2026 (v3.0) releases spell the *same* reading with
# different codepoints.  Folding them is what stops the comparison from
# reporting thousands of false variants between Dūrī and everything else.

#: Alef carrying its vowel in one codepoint (Arabic Extended-B, Unicode 14/16).
#: Used by the v3.0 Warsh/Qālūn/Sūsī/Bazzī sets where the other releases write
#: an alef followed by a separate vowel.  The mapping is not guessed: each
#: codepoint was aligned against the other riwāyāt's spelling of the same word
#: across the whole corpus, and every entry below is the majority correspondence
#: with at least 5,800 confirmations.
ATTACHED_ALEF_DECOMP = {
    "ࡰ": "اَ", "ࡱ": "اَ", "ࡲ": "اُ", "ࡳ": "اُ", "ࡴ": "اِ", "ࡵ": "اِ",
    "ࡶ": "ا",  "ࡷ": "ا",  "ࡸ": "اُ", "ࡹ": "اِ", "ࡺ": "ا",  "ࡻ": "اَ",
    "ࡼ": "اُ", "ࡽ": "اِ", "ࡾ": "اَ", "ࡿ": "اُ", "ࢀ": "اِ", "ࢁ": "ا", "ࢂ": "ا",
}

NOTATION_FOLD = {
    "ٞ": "ࣰ",  # fatha with two dots  -> open fathatan
    "ٗ": "ࣱ",  # inverted damma       -> open dammatan
    "ٖ": "ࣲ",  # subscript alef       -> open kasratan
    "ۡ": "ْ",  # KFGQPC sukun head    -> sukun
    "۟": "۠",  # rounded zero         -> rectangular zero
    # --- glyph choices that say nothing about the reading ------------------
    "ے": "ي",  # yeh barree: the Warsh/Qālūn fonts' final yāʾ
    "ۑ": "ي",  # yeh with three dots below: likewise
    "ۓ": "ئ",  # yeh barree with hamza above
    "ࢇ": "ء",  # baseline round dot: the v3.0 sets' standalone hamza
    # --- hamzat waṣl, written four different ways across the packages -----
    "ٱ": "ا", "أ": "ا", "إ": "ا",
    "۬": "", "۪": "", "۫": "",   # the waṣl vowel cues that ride on an alef
}
NOTATION_FOLD.update(ATTACHED_ALEF_DECOMP)

# --- rasm folding ---------------------------------------------------------
# Reduce a word to its consonantal skeleton.  This is the alignment key: two
# riwāyāt that differ only in vowelling collapse to the same rasm.

#: Alif written as a single codepoint carrying an attached vowel or waṣl cue.
#: Added in Unicode 14/16 and used by the v3.0 Warsh/Qālūn/Sūsī/Bazzī sets.
ATTACHED_ALEF = {chr(c) for c in range(0x0870, 0x087A)}

ALEF_FORMS = {"آ", "أ", "إ", "ا", "ٱ"} | ATTACHED_ALEF

RASM_FOLD = {}
for _c in ALEF_FORMS:
    RASM_FOLD[_c] = "ا"          # every alif -> bare alif
RASM_FOLD.update({
    "ؤ": "و",               # ؤ -> و   hamza on a wāw seat: the seat is the letter
    "ئ": "ي",               # ئ -> ي
    "ى": "ي",               # ى -> ي
    "ے": "ي",               # ے yeh barree -> ي
    "ۑ": "ي",               # ۑ yeh w/ three dots below -> ي
    "ۓ": "ي",               # ۓ yeh barree with hamza -> ي
    "ة": "ه",               # ة -> ه
    "ٮ": "ب",               # ٮ dotless beh -> ب
    "ء": "",                # hamza is not a rasm letter (see below)
    "ࢇ": "",                # baseline round dot: the same hamza, another glyph
})

# Hamza is post-ʿUthmānic: it was devised by al-Khalīl in the 8th century, two
# centuries after the codices were written.  A skeleton that keeps it is not a
# rasm.  Dropping it — and reducing every carrier to its seat — is what makes
# يَسۡتَهۡزِئُ and يَسْتَهْزِۓُ one word, and هَٰٓؤُلَآءِ and هَٰؤُلَآࢇ one word.

#: Superscript letters that stand for a letter the codex *does* write on the
#: line in other packages.  The small high yeh of ٱلنَّبِيِّۧنَ is the same yāʾ that
#: Warsh prints as ۑ; treating it as a mark invented a difference.  The ṣilah
#: waw and yeh (ۥ ۦ) are deliberately *not* here: they stand for a vowel that is
#: pronounced but never written, which is what lets Bazzī's عَلَيۡهِمُۥ align with
#: عَلَيۡهِمۡ as one word read two ways.
RASM_KEEP_MARKS_FOLD = {
    "ۧ": "ي",   # small high yeh
    "ࣉ": "ي",   # small farsi yeh
}

#: Dagger alif.  Written alef and superscript alef are the same ā, spelled two
#: ways by two typesetting traditions: KFGQPC's Warsh/Qālūn set writes هَارُوتَ
#: where the Kūfī set writes هَٰرُوتَ.  Folding them is not merely convenient —
#: keeping them apart *hides* real variants, because the same fold is what
#: separates مَٰلِكِ from مَلِكِ, دِفَٰعُ from دَفۡعُ and ٱلرِّيَٰحُ from ٱلرِّيحُ.
SUPERSCRIPT_ALEF = "ٰ"

# --- iʿjām (pointing) -----------------------------------------------------
# The ʿUthmānic codices were written without dots.  One skeleton therefore
# carries several readings by design: تَعۡمَلُونَ and يَعۡمَلُونَ are not two rasms,
# they are one rasm pointed two ways, and the muṣḥaf accommodates both on
# purpose.  Folding the dots is what makes the index say so.
#
# Letters merge only where their *shapes* merge, which depends on position:
# ب ت ث ن ي share one tooth medially but part company at the end of a word,
# where ب ت ث keep the bowl, ن takes its own curve and ي its own tail.  Every
# letter below is a connector, so "final shape" means simply "last letter".

#: Shapes that coincide in every position.
DOT_FOLD_ALWAYS = {
    "ج": "ح", "خ": "ح",
    "ذ": "د",
    "ز": "ر",
    "ش": "س",
    "ض": "ص",
    "ظ": "ط",
    "غ": "ع",
}

#: Shapes that coincide only when the letter connects to the left.
DOT_FOLD_MEDIAL = {
    "ب": "ٮ", "ت": "ٮ", "ث": "ٮ", "ن": "ٮ", "ي": "ٮ",
    "ف": "ڡ", "ق": "ڡ",
}

#: Shapes at the end of a word, where the tails separate again.
DOT_FOLD_FINAL = {
    "ب": "ٮ", "ت": "ٮ", "ث": "ٮ",
    "ن": "ں",
    "ي": "ى",
    "ف": "ڡ", "ق": "ٯ",
}

#: Marks that survive into the rasm, because in these packages they stand in
#: for a letter another package writes on the line.  See
#: :data:`RASM_KEEP_MARKS_FOLD` for what each becomes, and
#: :data:`SUPERSCRIPT_ALEF` for the dagger alif, which is handled separately
#: because it becomes a letter rather than folding to one.
RASM_KEEP_MARKS: frozenset[str] = frozenset(RASM_KEEP_MARKS_FOLD) | {SUPERSCRIPT_ALEF}

# --- ligature-encoded āyah numbers (v2 CSV only) --------------------------
# The v2 CSV/HTML files abuse the Arabic Presentation Forms-A block: āyah n is
# written as the single codepoint U+FC00 + (n - 1).

AYAH_LIGATURE_BASE = 0xFC00
AYAH_LIGATURE_MAX = 0xFC00 + 285   # sūrah 2 has 286 āyāt


def ayah_number_from_ligature(ch: str) -> int | None:
    """Return the āyah number a presentation-form codepoint stands for."""
    o = ord(ch)
    if AYAH_LIGATURE_BASE <= o <= AYAH_LIGATURE_MAX:
        return o - AYAH_LIGATURE_BASE + 1
    return None


def is_letter(ch: str) -> bool:
    return ch not in ALL_MARKS and ch not in STRUCTURAL and ch not in CONTROLS \
        and ch != TATWEEL and not ch.isspace() and ch not in ARABIC_DIGITS
