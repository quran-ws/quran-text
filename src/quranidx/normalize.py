"""Normalisation layers.

Five forms are derived from every raw token, each answering a different
question:

``uthmani``  the word as printed, minus pause marks and structural symbols.
             This is the canonical display form.
``folded``   ``uthmani`` with release-specific notation unified, so that the
             2022 and 2026 spellings of one reading compare equal.
``pointed``  the consonantal skeleton *with* its dots: what a modern reader
             would call the letters of the word.
``rasm``     the bare ʿUthmānic skeleton — undotted, no hamza, no vowels.  This
             is the alignment key and the identity of a word across riwāyāt.
``simple``   plain modern spelling, for search and for human-readable diffs.

``pointed`` and ``rasm`` are separate because the difference between them is
itself a category of variation.  تَعۡمَلُونَ and يَعۡمَلُونَ have different pointed
forms but one rasm: the codices were written undotted, so a single skeleton
carries both readings on purpose.  Calling that a "rasm variant" would be a
category error; calling it a mere vowelling difference would hide a real
reading.  It gets its own name, ``dotting_variant``.
"""

from __future__ import annotations

import re
import unicodedata

from . import chars


def strip_controls(text: str) -> str:
    """Drop invisible controls and kashida, and normalise NBSP to a space."""
    out = []
    for ch in text:
        if ch in chars.CONTROLS or ch == chars.TATWEEL:
            continue
        out.append(" " if ch in (" ", " ") else ch)
    return "".join(out)


def split_trailing_waqf(token: str) -> tuple[str, str]:
    """Peel pause marks off the end of a token.

    Returns ``(word, waqf)``.  Only *trailing* marks are peeled: U+06EC and
    friends double as orthographic cues in the Warsh family when they sit on an
    interior alif, and those must stay with the word.
    """
    i = len(token)
    while i > 0 and token[i - 1] in chars.WAQF_MARKS:
        i -= 1
    return token[:i], token[i:]


def uthmani(word: str) -> str:
    """Canonical display form: NFC, no controls, no structural symbols."""
    cleaned = "".join(
        ch for ch in strip_controls(word)
        if ch not in chars.STRUCTURAL and ch not in chars.ARABIC_DIGITS
    )
    return unicodedata.normalize("NFC", cleaned).strip()


#: A tanwīn written before the alif it sits on, rather than after it.  The two
#: orders are the same reading: ``حَطَبࣰا`` and ``حَطَباࣰ`` are one word.
_TANWEEN_BEFORE_ALEF = re.compile("([ًࣰٌࣱٍࣲ])(ا)")


def fold_notation(word: str) -> str:
    """Unify the spellings of one reading across releases and typesettings.

    Three kinds of difference are neutralised: the v2 (2022) and v3.0 (2026)
    codepoints for the same mark; the several ways the packages write an alef
    and its vowel (a bare alef plus a ḥaraka, an alef-waṣla, or one of the
    Arabic Extended-B attached-alef letters); and the order in which a tanwīn
    and its alef seat are stored.
    """
    folded = "".join(chars.NOTATION_FOLD.get(ch, ch) for ch in word)
    folded = _TANWEEN_BEFORE_ALEF.sub(r"\2\1", folded)
    return unicodedata.normalize("NFC", folded)


def pointed(word: str) -> str:
    """Consonantal skeleton keeping the dots: the letters as read today.

    The dagger alif becomes a written alef, since the two spell one ā and the
    packages disagree only about which to print.  It is *not* added when an
    alef is already there — ``ءَا`` and ``اٰ`` are both a single ā, and the
    doubling would be an artefact.  The test has to be this local: collapsing
    every run of alefs afterwards would also weld Bazzī's ``لَأُاْقۡسِمُ`` into one
    alef and break the re-segmentation of 75:1.
    """
    out: list[str] = []
    from_dagger = False          # did the alef just emitted come from a dagger?
    for ch in uthmani(word):
        if ch == chars.SUPERSCRIPT_ALEF:
            # ``اٰ``: the alef on the line already carries this ā.
            if not out or out[-1] != "ا":
                out.append("ا")
                from_dagger = True
            continue
        if ch in chars.RASM_KEEP_MARKS_FOLD:
            out.append(chars.RASM_KEEP_MARKS_FOLD[ch])
            from_dagger = False
            continue
        if ch in chars.ALL_MARKS:
            continue             # a mark does not interrupt the pair
        letter = chars.RASM_FOLD.get(ch, ch)
        if not letter:
            continue             # hamza: dropped, and no letter intervenes
        if letter == "ا" and from_dagger:
            from_dagger = False  # ``ٰا``: the dagger already supplied this ā
            continue
        from_dagger = False
        out.append(letter)
    return "".join(out)


def rasm(word: str) -> str:
    """The bare ʿUthmānic skeleton — the cross-riwāyah alignment key.

    Undotted, unvowelled, and without hamza, because that is what the codices
    were: everything added later to disambiguate a reading is exactly what the
    riwāyāt are allowed to disagree about.  Two words with the same rasm are
    one word in the index, however differently they are read.
    """
    letters = pointed(word)
    last = len(letters) - 1
    out = []
    for i, ch in enumerate(letters):
        ch = chars.DOT_FOLD_ALWAYS.get(ch, ch)
        table = chars.DOT_FOLD_FINAL if i == last else chars.DOT_FOLD_MEDIAL
        out.append(table.get(ch, ch))
    return "".join(out)


#: Marks kept when producing the plain-spelling form.
_SIMPLE_DROP = chars.ALL_MARKS - {"ّ"}

_SIMPLE_FOLD = {
    "ٱ": "ا",
    "ے": "ي",
    "ۑ": "ي",
    "ࢇ": "",
}
_SIMPLE_FOLD.update({c: "ا" for c in chars.ATTACHED_ALEF})


def simple(word: str) -> str:
    """Plain modern spelling: no diacritics, superscript alif made explicit."""
    text = uthmani(word)
    out = []
    for ch in text:
        if ch == "ٰ":         # superscript alif -> written alif
            out.append("ا")
            continue
        if ch in _SIMPLE_DROP:
            continue
        out.append(_SIMPLE_FOLD.get(ch, ch))
    return "".join(out)


def forms(word: str) -> dict[str, str]:
    """All derived forms of one word."""
    u = uthmani(word)
    return {
        "uthmani": u,
        "folded": fold_notation(u),
        "pointed": pointed(u),
        "rasm": rasm(u),
        "simple": simple(u),
    }


def contributes_to_rasm(ch: str) -> bool:
    """True when ``ch`` can produce a letter in the rasm.

    A *can*, not a *does*: an alef that follows another alef collapses away, so
    :func:`split_by_rasm` measures prefixes rather than trusting this per
    character.  It is used only to decide where the marks trailing a letter end.
    """
    if ch in chars.ALL_MARKS and ch not in chars.RASM_KEEP_MARKS:
        return False
    return bool(chars.RASM_FOLD.get(ch, ch))


def split_by_rasm(word: str, lengths: list[int]) -> list[str]:
    """Cut ``word`` into pieces whose rasms have the given lengths.

    Used to repair words that a source printed without the space between them
    (``كَانُواْيَعۡمَلُونَ``).  The cut falls *after* any marks trailing the last
    letter of a piece, since a mark belongs to the letter it sits on.

    Piece boundaries are found by measuring the rasm of the prefix rather than
    by counting characters, because a rasm letter is not always one character:
    hamza contributes nothing and a doubled alef collapses to one.
    """
    pieces: list[str] = []
    start = 0
    for length in lengths[:-1]:
        cut = start
        while cut < len(word) and len(rasm(word[start:cut])) < length:
            cut += 1
        # Carry the marks trailing the last letter into the piece just closed.
        while cut < len(word) and not contributes_to_rasm(word[cut]):
            cut += 1
        pieces.append(word[start:cut])
        start = cut
    pieces.append(word[start:])
    return pieces
