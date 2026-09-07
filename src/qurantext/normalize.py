"""Normalisation layers.

Five forms are derived from every raw token, each answering a different
question:

``rasm_uthmani``  the word as printed, minus waqf marks and structural symbols.
             This is the canonical display form.
``folded``   ``rasm_uthmani`` with release-specific notation unified, so that the
             2022 and 2026 spellings of one qiraah compare equal.
``pointed``  the consonantal skeleton *with* its dots: what a modern reader
             would call the letters of the word.
``rasm``     the bare ʿUthmānic skeleton — undotted, no hamzah, no vowels.  This
             is the alignment key and the identity of a word across riwāyāt.
``plain``   plain modern spelling, for search and for human-readable diffs.

``pointed`` and ``rasm`` are separate because the difference between them is
itself a category of variation.  تَعۡمَلُونَ and يَعۡمَلُونَ have different pointed
forms but one rasm: the codices were written undotted, so a single skeleton
carries both qiraahs on purpose.  Calling that a "rasm variant" would be a
category error; calling it a mere vowelling difference would hide a real
qiraah.  It gets its own name, ``dotting_variant``.
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
    """Peel waqf marks off the end of a token.

    Returns ``(word, waqf)``.  Only *trailing* marks are peeled: U+06EC and
    friends double as orthographic cues in the Warsh family when they sit on an
    interior alif, and those must stay with the word.
    """
    i = len(token)
    while i > 0 and token[i - 1] in chars.WAQF_MARKS:
        i -= 1
    return token[:i], token[i:]


def rasm_uthmani(word: str) -> str:
    """Canonical display form: NFC, no controls, no structural symbols."""
    cleaned = "".join(
        ch for ch in strip_controls(word)
        if ch not in chars.STRUCTURAL and ch not in chars.ARABIC_DIGITS
    )
    return unicodedata.normalize("NFC", cleaned).strip()


#: A tanwīn written before the alif it sits on, rather than after it.  The two
#: orders are the same qiraah: ``حَطَبࣰا`` and ``حَطَباࣰ`` are one word.
_TANWIN_BEFORE_ALEF = re.compile("([ًࣰٌࣱٍࣲ])(ا)")


def fold_notation(word: str) -> str:
    """Unify the spellings of one qiraah across releases and typesettings.

    Three kinds of difference are neutralised: the v2 (2022) and v3.0 (2026)
    codepoints for the same mark; the several ways the packages write an alef
    and its vowel (a bare alef plus a ḥaraka, an alef-waṣla, or one of the
    Arabic Extended-B attached-alef letters); and the order in which a tanwīn
    and its alef seat are stored.
    """
    folded = "".join(chars.NOTATION_FOLD.get(ch, ch) for ch in word)
    folded = _TANWIN_BEFORE_ALEF.sub(r"\2\1", folded)
    return unicodedata.normalize("NFC", folded)


def _is_suppressed_hamzah(text: str, i: int) -> bool:
    """True when the dagger alif at ``text[i]`` stands in for a hamzah.

    ``ٰٓ`` — or ``ٰ۬``, which the Warsh/Qālūn set writes for the same thing — is a
    madd over a hamzah.  Warsh's tashīl suppresses the hamzah itself
    and leaves the madd behind, so a dagger-plus-maddah with no hamzah after it
    is notating a hamzah rather than a written ā — and hamzah is not rasm.  With
    the hamzah still present (``إِسۡرَٰٓءِيلَ``, ``مَلَٰٓئِكَةِ``) or with nothing after
    it at all (``عَلَىٰٓ``), the dagger is a genuine ā that other packages print
    as an alef on the line.

    Deciding this needs the *word*, not the character: the two cases are
    identical up to and including the dagger, and differ only in what follows.
    """
    if i + 1 >= len(text) or text[i + 1] not in chars.HAMZAH_MADD_MARKS:
        return False
    for j, ch in enumerate(text[i + 2:], start=i + 2):
        if ch in chars.HAMZAH_ANY:
            return False         # the madd has its hamzah; the dagger is an ā
        if ch in chars.ALL_MARKS:
            continue
        # A plain letter — but a madd over a *doubled* one is madd lāzim, a
        # genuine long ā before a shaddah (``تَتَّبِعَٰٓنِّ``, ``فَذَٰٓنِّكَ``), not a
        # hamzah.  Only an undoubled letter leaves the madd with nothing to be
        # over, and that is the tashīl case.
        return not _carries_shaddah(text, j)
    return False                 # nothing follows; keep the ā (``عَلَىٰٓ``)


def _carries_shaddah(text: str, i: int) -> bool:
    """True when the letter at ``text[i]`` is written doubled."""
    for ch in text[i + 1:]:
        if ch == "ّ":
            return True
        if ch not in chars.ALL_MARKS:
            return False
    return False


def _letters(text: str, *, dagger_on_the_line: bool) -> str:
    """The letters of ``text``, hamzah dropped and every carrier reduced to its seat.

    ``dagger_on_the_line`` decides the one question the two KFGQPC typesettings
    answer differently: whether a superscript alef counts as a letter.  It does
    for :func:`pointed`, which spells the word as it is *read*; it does not for
    :func:`rasm`, which is what the codex has on the line.

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
            if _is_suppressed_hamzah(text, i):
                continue         # the dagger *is* the hamzah; hamzah is not rasm
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
            continue             # hamzah: dropped, and no letter intervenes
        if letter == "ا" and from_dagger:
            from_dagger = False  # ``ٰا``: the dagger already supplied this ā
            continue
        from_dagger = False
        out.append(letter)
    return "".join(out)


def _undot(letters: str) -> str:
    """Merge the letter shapes that the codices did not tell apart."""
    last = len(letters) - 1
    out = []
    for i, ch in enumerate(letters):
        ch = chars.DOT_FOLD_ALWAYS.get(ch, ch)
        table = chars.DOT_FOLD_FINAL if i == last else chars.DOT_FOLD_MEDIAL
        out.append(table.get(ch, ch))
    return "".join(out)


def pointed(word: str) -> str:
    """Consonantal skeleton keeping the dots: the letters as the word is read.

    Here the dagger alif *is* an alef, because this form spells the qiraah and
    the qiraah has the ā however the typesetter chose to print it.  That is the
    opposite of :func:`rasm`, and deliberately so: it is what lets ``مَٰلِكِ`` and
    ``مَلِكِ`` be one rasm read two ways rather than two rasms.
    """
    return _letters(rasm_uthmani(word), dagger_on_the_line=True)


def rasm(word: str) -> str:
    """The bare ʿUthmānic skeleton — the cross-riwāyah alignment key.

    Undotted, unvowelled, without hamzah, and **without the dagger alif**,
    because that is what the codices were: a superscript alef is by definition
    an alef the scribe did not write on the line, and everything added later to
    disambiguate a qiraah is exactly what the riwāyāt are allowed to disagree
    about.  Counting it as a letter is what used to report ``مَٰلِكِ``/``مَلِكِ``,
    ``دِفَٰعُ``/``دَفۡعُ`` and ``طَٰٓئِراً``/``طَيۡرًا`` as differences between the
    codices, when ملك, دفع and طير are precisely the skeletons that carry both
    qiraahs — the ḥadhf al-alif that makes one muṣḥaf serve seven riwāyāt.

    Two words with the same rasm are one word in the index, however differently
    they are read.
    """
    return _undot(_letters(rasm_uthmani(word), dagger_on_the_line=False))


def rasm_plene(word: str) -> str:
    """The skeleton with every ā spelled out, dagger alifs included.

    The two KFGQPC typesettings do not agree on which ā to put on the line: the
    Warsh/Qālūn set prints ``هَارُوتَ`` and ``مُبَٰرَك`` where the Kūfī set prints
    ``هَٰرُوتَ`` and ``مُبَارَك``.  Spelling every ā out makes those two hands
    comparable, which is what tells a plene/defective spelling apart from a
    disagreement about the letters themselves.  See :func:`build.classify`.
    """
    return _undot(pointed(word))


def unpositioned(skeleton: str) -> str:
    """A rasm with the final shapes folded back into their class.

    ``ں`` and ``ى`` are a nūn and a yāʾ that happen to end a word; medially the
    same letters are ``ٮ``.  Two skeletons that differ by a suffix therefore
    differ in the letter before it too, which makes an added letter look like an
    added *and* a substituted one.  Folding the final shapes is what lets
    ``ٮسٮهى``/``ٮسٮهٮه`` (تشتهي/تشتهيه) be read as the one added hāʾ it is.

    For describing a difference only.  The rasm keeps the final shapes, because
    the codices did: ``ٮعملوں`` ends in a nūn's own curve.
    """
    return "".join(chars.FINAL_SHAPE_FOLD.get(c, c) for c in skeleton)


#: Marks kept when producing the plain-spelling form.
_PLAIN_DROP = chars.ALL_MARKS - {"ّ"}

_PLAIN_FOLD = {
    "ٱ": "ا",
    "ے": "ي",
    "ۑ": "ي",
    "ࢇ": "",
}
_PLAIN_FOLD.update({c: "ا" for c in chars.ATTACHED_ALEF})


def plain(word: str) -> str:
    """Plain modern spelling: no harakah, superscript alif made explicit."""
    text = rasm_uthmani(word)
    out = []
    for ch in text:
        if ch == "ٰ":         # superscript alif -> written alif
            out.append("ا")
            continue
        if ch in _PLAIN_DROP:
            continue
        out.append(_PLAIN_FOLD.get(ch, ch))
    return "".join(out)


def forms(word: str) -> dict[str, str]:
    """All derived forms of one word."""
    u = rasm_uthmani(word)
    return {
        "rasm_uthmani": u,
        "folded": fold_notation(u),
        "pointed": pointed(u),
        "rasm": rasm(u),
        "rasm_plene": rasm_plene(u),
        "plain": plain(u),
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
    hamzah contributes nothing and a doubled alef collapses to one.
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
