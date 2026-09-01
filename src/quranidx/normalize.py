"""Normalisation layers.

Five forms are derived from every raw token, each answering a different
question:

``uthmani``  the kalimah as printed, minus pause marks and structural symbols.
             This is the canonical display form.
``folded``   ``uthmani`` with release-specific notation unified, so that the
             2022 and 2026 spellings of one qira'ah compare equal.
``pointed``  the consonantal skeleton *with* its dots: what a modern reader
             would call the harfs of the kalimah.
``rasm``     the bare Uthmani skeleton — undotted, no hamza, no vowels.  This
             is the alignment key and the identity of a kalimah across riwayahs.
``simple``   plain modern spelling, for search and for human-readable diffs.

``pointed`` and ``rasm`` are separate because the difference between them is
itself a category of variation.  تَعۡمَلُونَ and يَعۡمَلُونَ have different pointed
forms but one rasm: the mushafs were written undotted, so a single skeleton
carries both qira'ahs on purpose.  Calling that a "rasm variant" would be a
category error; calling it a mere vowelling difference would hide a real
qira'ah.  It gets its own name, ``dotting_variant``.
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

    Returns ``(kalimah, waqf)``.  Only *trailing* marks are peeled: U+06EC and
    friends double as orthographic cues in the Warsh family when they sit on an
    interior alif, and those must stay with the kalimah.
    """
    i = len(token)
    while i > 0 and token[i - 1] in chars.WAQF_MARKS:
        i -= 1
    return token[:i], token[i:]


def uthmani(kalimah: str) -> str:
    """Canonical display form: NFC, no controls, no structural symbols."""
    cleaned = "".join(
        ch for ch in strip_controls(kalimah)
        if ch not in chars.STRUCTURAL and ch not in chars.ARABIC_DIGITS
    )
    return unicodedata.normalize("NFC", cleaned).strip()


#: A tanwīn written before the alif it sits on, rather than after it.  The two
#: orders are the same qira'ah: ``حَطَبࣰا`` and ``حَطَباࣰ`` are one kalimah.
_TANWEEN_BEFORE_ALEF = re.compile("([ًࣰٌࣱٍࣲ])(ا)")


def fold_notation(kalimah: str) -> str:
    """Unify the spellings of one qira'ah across releases and typesettings.

    Three kinds of difference are neutralised: the v2 (2022) and v3.0 (2026)
    codepoints for the same mark; the several ways the packages write an alef
    and its vowel (a bare alef plus a ḥaraka, an alef-waṣla, or one of the
    Arabic Extended-B attached-alef harfs); and the order in which a tanwīn
    and its alef seat are stored.
    """
    folded = "".join(chars.NOTATION_FOLD.get(ch, ch) for ch in kalimah)
    folded = _TANWEEN_BEFORE_ALEF.sub(r"\2\1", folded)
    return unicodedata.normalize("NFC", folded)


def _is_suppressed_hamza(text: str, i: int) -> bool:
    """True when the dagger alif at ``text[i]`` stands in for a hamza.

    ``ٰٓ`` — or ``ٰ۬``, which the Warsh/Qālūn set writes for the same thing — is a
    madd over a hamza.  Warsh's tashīl suppresses the hamza itself
    and leaves the madd behind, so a dagger-plus-maddah with no hamza after it
    is notating a hamza rather than a written ā — and hamza is not rasm.  With
    the hamza still present (``إِسۡرَٰٓءِيلَ``, ``مَلَٰٓئِكَةِ``) or with nothing after
    it at all (``عَلَىٰٓ``), the dagger is a genuine ā that other packages print
    as an alef on the line.

    Deciding this needs the *kalimah*, not the character: the two cases are
    identical up to and including the dagger, and differ only in what follows.
    """
    if i + 1 >= len(text) or text[i + 1] not in chars.HAMZA_MADD_MARKS:
        return False
    for j, ch in enumerate(text[i + 2:], start=i + 2):
        if ch in chars.HAMZA_ANY:
            return False         # the madd has its hamza; the dagger is an ā
        if ch in chars.ALL_MARKS:
            continue
        # A plain harf — but a madd over a *doubled* one is madd lāzim, a
        # genuine long ā before a shadda (``تَتَّبِعَٰٓنِّ``, ``فَذَٰٓنِّكَ``), not a
        # hamza.  Only an undoubled harf leaves the madd with nothing to be
        # over, and that is the tashīl case.
        return not _carries_shadda(text, j)
    return False                 # nothing follows; keep the ā (``عَلَىٰٓ``)


def _carries_shadda(text: str, i: int) -> bool:
    """True when the harf at ``text[i]`` is written doubled."""
    for ch in text[i + 1:]:
        if ch == "ّ":
            return True
        if ch not in chars.ALL_MARKS:
            return False
    return False


def _harfs(text: str, *, dagger_on_the_line: bool) -> str:
    """The harfs of ``text``, hamza dropped and every carrier reduced to its seat.

    ``dagger_on_the_line`` decides the one question the two KFGQPC typesettings
    answer differently: whether a superscript alef counts as a harf.  It does
    for :func:`pointed`, which spells the kalimah as it is *read*; it does not for
    :func:`rasm`, which is what the mushaf has on the line.

    When it is counted, it is not added on top of an alef that is already there
    — ``ءَا`` and ``اٰ`` are both a single ā, and the doubling would be an
    artefact.  The test has to be this local: collapsing every run of alefs
    afterwards would also weld Bazzī's ``لَأُاْقۡسِمُ`` into one alef and break the
    re-segmentation of 75:1.
    """
    out: list[str] = []
    from_dagger = False          # did the alef just emitted come from a dagger?
    for i, ch in enumerate(text):
        if ch == chars.SUPERSCRIPT_ALEF:
            if not dagger_on_the_line:
                continue         # a dagger alif is by definition not on the line
            if _is_suppressed_hamza(text, i):
                continue         # the dagger *is* the hamza; hamza is not rasm
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
        harf = chars.RASM_FOLD.get(ch, ch)
        if not harf:
            continue             # hamza: dropped, and no harf intervenes
        if harf == "ا" and from_dagger:
            from_dagger = False  # ``ٰا``: the dagger already supplied this ā
            continue
        from_dagger = False
        out.append(harf)
    return "".join(out)


def _undot(harfs: str) -> str:
    """Merge the harf shapes that the mushafs did not tell apart."""
    last = len(harfs) - 1
    out = []
    for i, ch in enumerate(harfs):
        ch = chars.DOT_FOLD_ALWAYS.get(ch, ch)
        table = chars.DOT_FOLD_FINAL if i == last else chars.DOT_FOLD_MEDIAL
        out.append(table.get(ch, ch))
    return "".join(out)


def pointed(kalimah: str) -> str:
    """Consonantal skeleton keeping the dots: the harfs as the kalimah is read.

    Here the dagger alif *is* an alef, because this form spells the qira'ah and
    the qira'ah has the ā however the typesetter chose to print it.  That is the
    opposite of :func:`rasm`, and deliberately so: it is what lets ``مَٰلِكِ`` and
    ``مَلِكِ`` be one rasm read two ways rather than two rasms.
    """
    return _harfs(uthmani(kalimah), dagger_on_the_line=True)


def rasm(kalimah: str) -> str:
    """The bare Uthmani skeleton — the cross-riwayah alignment key.

    Undotted, unvowelled, without hamza, and **without the dagger alif**,
    because that is what the mushafs were: a superscript alef is by definition
    an alef the scribe did not write on the line, and everything added later to
    disambiguate a qira'ah is exactly what the riwayahs are allowed to disagree
    about.  Counting it as a harf is what used to report ``مَٰلِكِ``/``مَلِكِ``,
    ``دِفَٰعُ``/``دَفۡعُ`` and ``طَٰٓئِراً``/``طَيۡرًا`` as differences between the
    mushafs, when ملك, دفع and طير are precisely the skeletons that carry both
    qira'ahs — the ḥadhf al-alif that makes one mushaf serve seven riwayahs.

    Two kalimahs with the same rasm are one kalimah in the index, however differently
    they are read.
    """
    return _undot(_harfs(uthmani(kalimah), dagger_on_the_line=False))


def rasm_plene(kalimah: str) -> str:
    """The skeleton with every ā spelled out, dagger alifs included.

    The two KFGQPC typesettings do not agree on which ā to put on the line: the
    Warsh/Qālūn set prints ``هَارُوتَ`` and ``مُبَٰرَك`` where the Kūfī set prints
    ``هَٰرُوتَ`` and ``مُبَارَك``.  Spelling every ā out makes those two hands
    comparable, which is what tells a plene/defective spelling apart from a
    disagreement about the harfs themselves.  See :func:`build.classify`.
    """
    return _undot(pointed(kalimah))


def unpositioned(skeleton: str) -> str:
    """A rasm with the final shapes folded back into their class.

    ``ں`` and ``ى`` are a nūn and a yāʾ that happen to end a kalimah; medially the
    same harfs are ``ٮ``.  Two skeletons that differ by a suffix therefore
    differ in the harf before it too, which makes an added harf look like an
    added *and* a substituted one.  Folding the final shapes is what lets
    ``ٮسٮهى``/``ٮسٮهٮه`` (تشتهي/تشتهيه) be read as the one added hāʾ it is.

    For describing a difference only.  The rasm keeps the final shapes, because
    the mushafs did: ``ٮعملوں`` ends in a nūn's own curve.
    """
    return "".join(chars.FINAL_SHAPE_FOLD.get(c, c) for c in skeleton)


#: Marks kept when producing the plain-spelling form.
_SIMPLE_DROP = chars.ALL_MARKS - {"ّ"}

_SIMPLE_FOLD = {
    "ٱ": "ا",
    "ے": "ي",
    "ۑ": "ي",
    "ࢇ": "",
}
_SIMPLE_FOLD.update({c: "ا" for c in chars.ATTACHED_ALEF})


def simple(kalimah: str) -> str:
    """Plain modern spelling: no diacritics, superscript alif made explicit."""
    text = uthmani(kalimah)
    out = []
    for ch in text:
        if ch == "ٰ":         # superscript alif -> written alif
            out.append("ا")
            continue
        if ch in _SIMPLE_DROP:
            continue
        out.append(_SIMPLE_FOLD.get(ch, ch))
    return "".join(out)


def forms(kalimah: str) -> dict[str, str]:
    """All derived forms of one kalimah."""
    u = uthmani(kalimah)
    return {
        "uthmani": u,
        "folded": fold_notation(u),
        "pointed": pointed(u),
        "rasm": rasm(u),
        "rasm_plene": rasm_plene(u),
        "simple": simple(u),
    }


def contributes_to_rasm(ch: str) -> bool:
    """True when ``ch`` can produce a harf in the rasm.

    A *can*, not a *does*: an alef that follows another alef collapses away, so
    :func:`split_by_rasm` measures prefixes rather than trusting this per
    character.  It is used only to decide where the marks trailing a harf end.
    """
    if ch in chars.ALL_MARKS and ch not in chars.RASM_KEEP_MARKS:
        return False
    return bool(chars.RASM_FOLD.get(ch, ch))


def split_by_rasm(kalimah: str, lengths: list[int]) -> list[str]:
    """Cut ``kalimah`` into pieces whose rasms have the given lengths.

    Used to repair kalimahs that a source printed without the space between them
    (``كَانُواْيَعۡمَلُونَ``).  The cut falls *after* any marks trailing the last
    harf of a piece, since a mark belongs to the harf it sits on.

    Piece boundaries are found by measuring the rasm of the prefix rather than
    by counting characters, because a rasm harf is not always one character:
    hamza contributes nothing and a doubled alef collapses to one.
    """
    pieces: list[str] = []
    start = 0
    for length in lengths[:-1]:
        cut = start
        while cut < len(kalimah) and len(rasm(kalimah[start:cut])) < length:
            cut += 1
        # Carry the marks trailing the last harf into the piece just closed.
        while cut < len(kalimah) and not contributes_to_rasm(kalimah[cut]):
            cut += 1
        pieces.append(kalimah[start:cut])
        start = cut
    pieces.append(kalimah[start:])
    return pieces
