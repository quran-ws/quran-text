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

#: Standalone symbols that mark structure, never part of a word.
STRUCTURAL = {END_OF_AYAH, RUB_EL_HIZB, SAJDAH}

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

NOTATION_FOLD = {
    "ٞ": "ࣰ",  # fatha with two dots  -> open fathatan
    "ٗ": "ࣱ",  # inverted damma       -> open dammatan
    "ٖ": "ࣲ",  # subscript alef       -> open kasratan
    "ۡ": "ْ",  # KFGQPC sukun head    -> sukun
    "۟": "۠",  # rounded zero         -> rectangular zero
}

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
    "ؤ": "و",               # ؤ -> و
    "ئ": "ي",               # ئ -> ي
    "ى": "ي",               # ى -> ي
    "ے": "ي",               # ے yeh barree -> ي
    "ۑ": "ي",               # ۑ yeh w/ three dots below -> ي
    "ة": "ه",               # ة -> ه
    "ٮ": "ب",               # ٮ dotless beh -> ب
    "ࢇ": "",                     # baseline round dot: not a consonant
})

# The ṣilah waw and yeh (ۥ ۦ), the small high yeh (ۧ) and the small farsi yeh
# (ࣉ) are superscript: they mark a vowel that is pronounced but *not* written
# on the line, so they are marks rather than letters and never enter the rasm.
# That is what lets Bazzī's عَلَيۡهِمُۥ align with عَلَيۡهِمۡ as one word read two
# ways, instead of splitting into two unrelated words.

#: Marks that survive into the rasm because they stand for an elided letter.
#: (Superscript alif is *not* one of them: the rasm is defined by what is
#: written on the line.)
RASM_KEEP_MARKS: frozenset[str] = frozenset()

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
