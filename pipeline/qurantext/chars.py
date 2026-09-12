"""Character classification tables for KFGQPC Uthmanic text.

Derived from a full codepoint inventory of every source shipped in ``sources/``
(see ``docs/CHARSET.md``).  The tables below are the single place where a
codepoint's role is decided; everything downstream asks these sets.
"""

# --- structural / non-text ------------------------------------------------

AYAH_MARK = "۝"          # ۝  ARABIC END OF AYAH (v3 docx)
RUBU_AL_HIZB = "۞"          # ۞  ARABIC START OF RUB EL HIZB
SAJDAH      = "۩"          # ۩  ARABIC PLACE OF SAJDAH

#: The horizontal line drawn over the words that make the sajdah due — خط
#: السجدة, the mark the terminology standard calls ``sajdah_line``.  The
#: packages encode it as U+06E4 ARABIC SMALL HIGH MADDA, which is not what that
#: codepoint names: it is a line over a phrase, not a maddah over a letter.
#: The corpus says so outright.  U+06E4 occurs 26 times in the Hafs release and
#: nowhere else in it; every occurrence is the last character of its word; the
#: 26 words are the sajdah phrases of all 15 sajdah places and nothing else
#: (``yasjudun``, ``kharru sujjadan``, ``wa-lillahi yasjudu`` ...), and five of
#: the seven releases carry the same 26 while Warsh and Qalun, whose typesetting
#: draws no such line, carry none.  A maddah would not distribute that way, and
#: would not sit after a final ``nun`` with its fathah already written.
#: So it is peeled off the word like the waqf marks and published as a mark of
#: its own kind: see :func:`normalize.split_trailing_signs`.
SAJDAH_LINE = "ۤ"          # ۤ  ARABIC SMALL HIGH MADDA (used as the sajdah line)

ARABIC_DIGITS = {chr(0x0660 + i): str(i) for i in range(10)}

#: The ṣaḥḥa U+08CC ("correct as written") and its raised-dot companion U+0888.
#: They are annotation rather than letters — not pronounced, and written by one
#: release where the others write nothing — but they *are* printed, 9,950 and
#: 91 times in the v3.0 Warsh document, word-final in all but four places.  So
#: they are peeled off the word like a waqf mark and published in ``marks`` as
#: the kinds ``sah`` and ``raised_dot``, rather than deleted: a sign the release
#: prints is not this repository's to remove.  They stay out of the alignment
#: key, which is what kept them from being the largest single source of
#: spurious differences in the corpus.
EDITORIAL = {"࣌", "࢈"}

#: Standalone symbols that mark structure, never part of a word.
STRUCTURAL = {AYAH_MARK, RUBU_AL_HIZB, SAJDAH}

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

#: Kashida.  **Not stripped.**  It was, on the reading that a kashida only
#: stretches a join, and that reading does not survive the corpus: in the v3.0
#: documents almost every one is a *seat*.  535 of Ḥafṣ's 536 carry a hamzah, a
#: small high yeh or a dagger alif that has no letter of its own — ``يَطَـُٔونَ``
#: is ``ط`` with its fatḥah, then the kashida carrying ``ٔ``, then the ḍammah
#: that belongs to the hamzah — and deleting it leaves two marks in one run
#: with nothing to say which is whose, lets NFC compose ``سَيِّـَٔاتِ`` into a
#: ``ئ`` no muṣḥaf prints, and changes what the font draws.  The rest are
#: printed inside a word too (``لِّـجِبۡرِيلَ``, ``إِبۡرَٰهِـيمَ``).  The text
#: published here is the release's, so the kashida stays where the release put
#: it (``docs/known-issues.md`` §4).
#:
#: It is ink, not a letter: :func:`is_letter` excludes it, and the rasm,
#: pointed, plain and folded forms drop it, so nothing downstream sees a new
#: word.
TATWEEL = "ـ"

# --- waqf marks ---------------------------------------------------
# These sit after the last letter of a word with no intervening space.  They
# annotate recitation, not rasm, so they are peeled off the word and
# recorded separately.

WAQF_MARKS = {
    "ۖ",  # ۖ  ṣlā   - preferable to continue
    "ۗ",  # ۗ  qlā   - waqf preferred
    "ۘ",  # ۘ  mīm   - waqf lāzim
    "ۙ",  # ۙ  lā    - waqf prohibited
    "ۚ",  # ۚ  jīm   - waqf permitted
    "ۛ",  # ۛ  three dots - mu'ānaqah (waqf at one of two)
    "ۜ",  # ۜ  small high seen  (KFGQPC: saktah / sīn recitation cue)
    "۩",  # ۩  place of sajdah
    "۪",  # ۪  ARABIC EMPTY CENTRE LOW STOP
    "۫",  # ۫  ARABIC EMPTY CENTRE HIGH STOP
    "۬",  # ۬  ARABIC ROUNDED HIGH STOP WITH FILLED CENTRE
}

#: Waqf marks that are *not* peeled in every riwāyah.  U+06EC is used by the
#: Warsh/Qālūn/Dūrī/Sūsī sets as an orthographic hamzat-waṣl cue on alif rather
#: than as a waqf sign, so it is only treated as waqf when it trails a word.
CONTEXTUAL_WAQF = {"۬", "۪", "۫"}

# --- vowels, tanwīn, and recitation marks ----------------------------

HARAKAHS = {
    "ً",  # ً tanwīn al-fatḥ
    "ٌ",  # ٌ tanwīn al-ḍamm
    "ٍ",  # ٍ tanwīn al-kasr
    "َ",  # َ fathah
    "ُ",  # ُ dammah
    "ِ",  # ِ kasrah
    "ّ",  # ّ shaddah
    "ْ",  # ْ sukun
    "ۡ",  # ۡ small high dotless head of khah (KFGQPC sukun)
}

#: "Open" tanwīn (iẓhār/idghām notation).  The v2 data sets encode these with
#: repurposed combining marks; the v3.0 sets use the dedicated Arabic Extended-A
#: codepoints added in Unicode 9.  :data:`NOTATION_FOLD` unifies them.
OPEN_TANWIN = {"ࣰ", "ࣱ", "ࣲ"}

#: Orthographic marks that belong to the word (madd, small letters, rounded
#: zeros, iqlāb mīm, ...).  Kept in the Uthmānī form, dropped from the rasm.
ORTHOGRAPHIC_MARKS = {
    "ٓ",  # ٓ maddah above
    "ٔ",  # ٔ hamzah above
    "ٕ",  # ٕ hamzah below
    "ٖ",  # ٖ subscript alef      (v2 open tanwīn al-kasr)
    "ٗ",  # ٗ inverted dammah      (v2 open tanwīn al-ḍamm)
    "ٜ",  # ٜ vowel sign dot below
    "ٞ",  # ٞ fathah with two dots (v2 open tanwīn al-fatḥ)
    "ٰ",  # ٰ superscript alef
    "۟",  # ۟ small high rounded zero
    "۠",  # ۠ small high upright rectangular zero
    "ۢ",  # ۢ small high meem isolated (iqlāb)
    "ۣ",  # ۣ small low seen
    "ۥ",  # ۥ small waw   (ṣilah)
    "ۦ",  # ۦ small yeh   (ṣilah)
    "ۧ",  # ۧ small high yeh
    "ۨ",  # ۨ small high noon
    "ۭ",  # ۭ small low meem (iqlāb)
    "࢈",  # ࢈ raised round dot
    "࣌",  # small high word ṣaḥ
} | OPEN_TANWIN

#: Everything that is a mark rather than a letter.
ALL_MARKS = HARAKAHS | ORTHOGRAPHIC_MARKS | WAQF_MARKS | {SAJDAH_LINE}

# --- notation folding -----------------------------------------------------
# The 2022 (v2 / V20) and 2026 (v3.0) releases spell the *same* qiraah with
# different codepoints.  Folding them is what keeps the comparison from
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
    "ٞ": "ࣰ",  # fathah with two dots  -> open tanwīn al-fatḥ
    "ٗ": "ࣱ",  # inverted dammah       -> open tanwīn al-ḍamm
    "ٖ": "ࣲ",  # subscript alef       -> open tanwīn al-kasr
    "ۡ": "ْ",  # KFGQPC sukun head    -> sukun
    "۟": "۠",  # rounded zero         -> rectangular zero
    # --- glyph choices that say nothing about the qiraah ------------------
    "ے": "ي",  # yeh barree: the Warsh/Qālūn fonts' final yāʾ
    "ۑ": "ي",  # yeh with three dots below: likewise
    "ۓ": "ئ",  # yeh barree with hamzah above
    "ࢇ": "ء",  # baseline round dot: the v3.0 sets' standalone hamzah
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
    "ؤ": "و",               # ؤ -> و   hamzah on a wāw seat: the seat is the letter
    "ئ": "ي",               # ئ -> ي
    "ى": "ي",               # ى -> ي
    "ے": "ي",               # ے yeh barree -> ي
    "ۑ": "ي",               # ۑ yeh w/ three dots below -> ي
    "ۓ": "ي",               # ۓ yeh barree with hamzah -> ي
    "ة": "ه",               # ة -> ه
    "ٮ": "ب",               # ٮ dotless beh -> ب
    "ء": "",                # hamzah is not a rasm letter (see below)
    "ࢇ": "",                # baseline round dot: the same hamzah, another glyph
})

# Hamzah is post-ʿUthmānic: it was devised by al-Khalīl in the 8th century, two
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

#: Dagger alif.  A superscript alef is, by definition, an alef the scribe did
#: *not* write on the line: it is the reader's cue for ḥadhf al-alif.  So it is
#: an ā for the qiraah — :func:`normalize.pointed` counts it — and no letter at
#: all for the rasm.  Counting it as a rasm letter reported مَٰلِكِ against مَلِكِ,
#: دِفَٰعُ against دَفۡعُ and طَٰٓئِراً against طَيۡرًا as disagreements between the
#: codices, when ملك, دفع and طير are exactly the skeletons written to carry
#: both qiraahs at once.
#:
#: What the two typesettings *do* disagree about is which ā to put on the line —
#: the Warsh/Qālūn set prints هَارُوتَ and مُبَٰرَك where the Kūfī set prints هَٰرُوتَ
#: and مُبَارَك.  That is a difference of hand, not of codex — the corpus says so
#: outright: all 198 such words split the seven riwāyāt along exactly one line,
#: {warsh, qālūn} against the other five, in both directions and without a
#: single exception, while the 62 real letter differences split fourteen
#: different ways.  Ḥadhf/ithbāt khilāf between the amṣār does not partition by
#: publisher; a house style does.  :func:`normalize.rasm_plene` is what tells
#: the two apart, and :data:`build.STATUS_ALIF` is what it is called.
SUPERSCRIPT_ALEF = "ٰ"

#: Marks a dagger alif can carry that make it a madd *over something* — the
#: maddah, and the rounded high sign the Warsh/Qālūn family uses for the same
#: job.  What the madd is over decides whether the dagger is a written ā at
#: all: see :data:`HAMZAH_ANY`.
HAMZAH_MADD_MARKS = {"ٓ", "۬"}

#: Hamzah in every form it is written: bare, on a seat, and combining.  Used to
#: read the one context where a dagger alif is not an ā.
#:
#: ``ٰٓ`` marks a madd over a hamzah.  Where the hamzah is there — ``إِسۡرَٰٓءِيلَ``,
#: ``هَٰٓؤُلَآءِ``, ``مَلَٰٓئِكَةِ`` — the dagger is a genuine written ā and Warsh
#: prints an alef in its place.  Where a plain letter follows instead, there is
#: no hamzah for the madd to be over, because the qiraah has suppressed it: in
#: Warsh's ``ࡰرَٰٓيْتَ`` the dagger *is* the tashīl'd hamzah of Ḥafṣ's ``أَرَءَيۡتَ``.
#: Hamzah is not part of the rasm, so neither is that dagger.
HAMZAH_ANY = {"ء", "أ", "إ", "ؤ", "ئ", "آ", "ٱ", "ࢇ", "ٔ", "ٕ", "ۓ"}

# --- iʿjām (pointing) -----------------------------------------------------
# The ʿUthmānic codices were written without dots.  One skeleton therefore
# carries several qiraahs by design: تَعۡمَلُونَ and يَعۡمَلُونَ are not two rasms,
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

#: The final shapes above, folded back to the class they belong to.  Position is
#: not identity: the yāʾ of ``ٮسٮهى`` and the yāʾ of ``ٮسٮهٮه`` are the same
#: letter, and it is only the suffix that moves one of them off the end of the
#: word.  Comparing two skeletons of different length letter by letter needs
#: that undone first, or every added suffix reads as a substitution as well.
#: Used only for describing a difference, never for the rasm itself.
FINAL_SHAPE_FOLD = {"ں": "ٮ", "ى": "ٮ", "ٯ": "ڡ"}

#: Marks that survive into the rasm, because in these packages they stand in
#: for a letter another package writes on the line.  See
#: :data:`RASM_KEEP_MARKS_FOLD` for what each becomes.  The dagger alif is not
#: among them: see :data:`SUPERSCRIPT_ALEF`.
RASM_KEEP_MARKS: frozenset[str] = frozenset(RASM_KEEP_MARKS_FOLD)

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
        and ch not in EDITORIAL and ch != TATWEEL and not ch.isspace() \
        and ch not in ARABIC_DIGITS
