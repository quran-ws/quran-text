"""Normalisation layers.

Four forms are derived from every raw token, each answering a different
question:

``uthmani``  the word as printed, minus pause marks and structural symbols.
             This is the canonical display form.
``folded``   ``uthmani`` with release-specific notation unified, so that the
             2022 and 2026 spellings of one reading compare equal.
``rasm``     the consonantal skeleton: the alignment key and the boundary
             between "same word, different vowelling" and "different word".
``simple``   plain modern spelling, for search and for human-readable diffs.
"""

from __future__ import annotations

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


def fold_notation(word: str) -> str:
    """Unify the v2 (2022) and v3.0 (2026) spellings of the same reading."""
    return "".join(chars.NOTATION_FOLD.get(ch, ch) for ch in word)


def rasm(word: str) -> str:
    """Consonantal skeleton — the cross-riwāyah alignment key."""
    out = []
    for ch in uthmani(word):
        if ch in chars.ALL_MARKS and ch not in chars.RASM_KEEP_MARKS:
            continue
        out.append(chars.RASM_FOLD.get(ch, ch))
    return "".join(out)


#: Marks kept when producing the plain-spelling form.
_SIMPLE_DROP = chars.ALL_MARKS - {"ّ"}

_SIMPLE_FOLD = {
    "ٱ": "ا",
    "ى": "ى",
    "ۥ": "ه",
    "ۦ": "ه",
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
        "rasm": rasm(u),
        "simple": simple(u),
    }
