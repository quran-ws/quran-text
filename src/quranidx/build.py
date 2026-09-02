"""Build the flat word index and every derived artefact.

The output model is deliberately *flat*: a sūrah is a list of words, and the
āyah number is an attribute of a word rather than a level of nesting.  That is
what makes one ID usable across all seven riwāyāt — the riwāyāt disagree about
where āyāt end (Kūfī counts 6236, Madanī 6214, Baṣrī 6217, Makkī 6220) but they
agree, almost everywhere, about the sequence of words.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from .align import Column, build_spine
from .sources import Riwaya, load_all
from .tokenize import Token, tokenize

OUT = Path("out")

#: Ḥafṣ first because it is the most widely published text and the best
#: starting spine; the rest follow so that the closest relatives merge early.
ORDER = ["hafs", "shuba", "bazzi", "qaloun", "warsh", "douri", "sousi"]

# Status of a canonical word, most specific first.
STATUS_RASM = "rasm_variant"
STATUS_ALIF = "alif_variant"
STATUS_ADDITION = "addition"
STATUS_PARTIAL = "partial"
STATUS_BOUNDARY = "word_boundary"
STATUS_DOTTING = "dotting_variant"
STATUS_DIACRITIC = "diacritic_variant"
STATUS_IDENTICAL = "identical"

#: Traditions of ʿadd al-āy, for reference only.  They are *not* the identity
#: of a fawāṣil system: see :func:`fawasil`.
COUNTING_TRADITIONS = {"kufi": "Kūfī", "madani": "Madanī",
                       "basri": "Baṣrī", "makki": "Makkī"}


@dataclass
class Word:
    id: int
    #: 0 for a spine word — that is, for every word Ḥafṣ has.  A word Ḥafṣ does
    #: not have takes no ID of its own: it hangs off the preceding spine word
    #: with a sub-index of 1, 2, …  So Ḥafṣ's own IDs are `1 … n` exactly, with
    #: no repeat and no gap, and a muṣḥaf without the extra word simply does not
    #: carry that sub-index.
    sub: int
    sura: int
    index: int            # 1-based position within the sūrah
    key: str              # rebuild-stable identity: "sura:pointed#occurrence"
    rasm: str             # bare ʿUthmānic skeleton, shared by every riwāyah
    pointed: str          # canonical word's dotted skeleton
    uthmani: str
    simple: str
    status: str
    present: list[str]
    missing: list[str]
    forms: dict[str, str]
    aya: dict[str, int]
    waqf: dict[str, str]
    boundary: dict[str, str]
    hizb: list[str]
    sajdah: list[str]
    #: riwāyah -> (page, line) in that muṣḥaf's own typesetting.  The page is
    #: read from the release; the line is reconstructed.  See ``layout.py``.
    place: dict[str, tuple[int, int]] = field(default_factory=dict)


def streams_for(riwayat: list[Riwaya]) -> dict[str, list[Token]]:
    """Tokenise each riwāyah, keeping only words that some riwāyah numbers.

    Every sūrah but at-Tawbah is printed with a basmalah above it.  Only
    Al-Fātiḥah's is *numbered* as an āyah, and only by Ḥafṣ, Shuʿbah and Bazzī.
    A word belongs in the index when any riwāyah numbers it, so Al-Fātiḥah's
    basmalah is in (for all seven, unnumbered where it is unnumbered) and the
    other 112 openings stay out, recorded as sūrah metadata instead.
    """
    out = {}
    for r in riwayat:
        # Tokenise the *whole* stream before filtering.  The typesetting
        # positions are a flat list over every āyah the document prints,
        # including the 112 unnumbered basmalahs, so dropping āyāt first would
        # slide every later word onto the wrong line.
        toks = tokenize(r.ayat, r.places or None)
        out[r.key] = [t for t in toks if t.aya > 0 or t.sura == 1]
    return out


def ref(w: Word) -> str:
    """How a word's ID is written: ``25684`` for a spine word, ``25684.1`` for
    an addition.

    The data keeps ``id`` and ``sub`` as two integers, because the ranges in
    ``ayat``, ``pages`` and ``juz`` are compared numerically and a string could
    not be — and because ``25684.1`` as a JSON *number* is a float, which
    round-trips as ``25684.099999999999`` and is no kind of identifier.  This is
    the one canonical way to write the pair, so that everything a person reads
    says the same thing.
    """
    return f"{w.id}.{w.sub}" if w.sub else str(w.id)


def is_addition(col: Column) -> bool:
    """Is this a word the base muṣḥaf does not have?

    **The spine is Ḥafṣ's own word sequence**, and *added* and *lacking* are
    said with respect to it.  That is a declared frame of reference, not a claim
    that Ḥafṣ reads correctly and the others do not: at 72:16 four muṣḥafs write
    ``لَّوِ`` and three do not, and it is still an addition here, because Ḥafṣ is
    where the counting starts.

    Naming the frame is what makes both directions sayable at all.  Without one,
    ``هُوَ`` at 57:23 has no answer to *was it added by five or dropped by two?*

    The test is a membership check rather than a count because
    :func:`quranidx.align.build_spine` starts from :data:`ORDER`'s first muṣḥaf
    and never revisits it, so a column it has no token in is exactly a column
    some later riwāyah brought.
    """
    return ORDER[0] not in col.tokens


def classify(col: Column, all_keys: list[str]) -> str:
    """Name the strongest kind of disagreement this word carries.

    The order matters and used to be wrong: ``word_boundary`` was returned
    before the words were compared at all, so five of the six boundary events
    in the corpus were reported as disagreements when in fact all seven riwāyāt
    read them identically and one *source* had merely lost a space.  Content is
    now decided first; the boundary stays on the word as an annotation either
    way, and ``word_boundary`` is reserved for a word that is otherwise in
    agreement but printed joined somewhere.

    A difference in the letters on the line is a ``rasm_variant`` — unless the
    only letter in question is an ā that one hand puts on the line and the other
    puts above it, which is ``alif_variant``.  The split is not a matter of
    taste.  The corpus decides it: all 198 plene/defective words partition the
    seven riwāyāt along exactly one line, {warsh, qālūn} against the other five,
    in both directions and without a single exception, while the 62 words whose
    skeletons differ once every ā is spelled out partition them fourteen
    different ways — Bazzī alone seven times, Ḥafṣ+Shuʿbah alone six, Qālūn
    alone five.  Ḥadhf/ithbāt al-alif between the codices of the amṣār would not
    put Makkah with Madinah 198 times out of 198; a publisher's house style
    would, and does.  So the ā is reported, but not as the codices disagreeing.

    ``rasm_plene`` is what draws the line: it spells every ā out, so two words
    that agree there and differ in ``rasm`` differ only about where the ā was
    written.  The bare ``rasm`` keeps the distinction, because inside any one
    muṣḥaf it is real — Ḥafṣ writes قال plene 412 times and defective 4, and
    that is its own ḥadhf, faithfully carried.
    """
    present = [k for k in all_keys if k in col.tokens]
    if len({col.tokens[k].rasm for k in present}) > 1:
        if len({col.tokens[k].rasm_plene for k in present}) > 1:
            return STATUS_RASM
        return STATUS_ALIF
    if len(present) < len(all_keys):
        # Two different facts, and conflating them was the old bug.  Both are
        # said with respect to Ḥafṣ: a word Ḥafṣ has and another muṣḥaf does not
        # is ``partial``; a word Ḥafṣ does not have is an ``addition``, and the
        # muṣḥafs without it are not missing anything.
        return STATUS_ADDITION if is_addition(col) else STATUS_PARTIAL
    if col.boundary:
        return STATUS_BOUNDARY
    if len({col.tokens[k].pointed for k in present}) > 1:
        return STATUS_DOTTING
    if len({col.tokens[k].folded for k in present}) > 1:
        return STATUS_DIACRITIC
    return STATUS_IDENTICAL


def ayah_ends(words: list[Word], key: str) -> list[int]:
    """The ID of the last word of every āyah, for one riwāyah's muṣḥaf."""
    ends: list[int] = []
    run = [w for w in words if w.aya.get(key, 0) > 0]
    for i, w in enumerate(run):
        nxt = run[i + 1] if i + 1 < len(run) else None
        if nxt is None or (nxt.sura, nxt.aya[key]) != (w.sura, w.aya[key]):
            ends.append(w.id)
    return ends


def fawasil(words: list[Word]) -> dict[str, dict]:
    """Where each muṣḥaf ends its āyāt, as canonical word IDs.

    **The fawāṣil belong to the printed muṣḥaf, not to the qirāʾah.**  This is
    not a nicety.  Many fawāṣil are مختلف فيها — al-Dānī records 67:9
    «قد جاءنا نذير» as counted by المدني الأخير والمكي and by Shayba, and not
    counted by the rest — so an edition has to *choose*, and different editions
    of the same riwāyah choose differently.  KFGQPC's own Dūrī printings show
    it plainly: 1429 AH and 1443 AH split 67:9 and give a colophon total of
    6214, while 1436 AH does not split it and states 6217.  Same publisher,
    same riwāyah, three printings, two different divisions.

    So a system is not named for a counting tradition and is not derived from
    one.  It is read off the packages themselves, and riwāyāt are grouped only
    where their fawāṣil turn out to be identical.  If a future package moves a
    single fāṣilah, it splits into its own system here rather than being
    quietly averaged into a tradition it does not actually follow.
    """
    ends = {key: ayah_ends(words, key) for key in ORDER}
    systems: dict[str, dict] = {}
    for key in ORDER:
        for system in systems.values():
            if system["ends"] == ends[key]:
                system["mushaf"].append(key)
                break
        else:
            systems[key] = {"mushaf": [key], "ayah_count": len(ends[key]),
                            "ends": ends[key]}
    # Name each system after the muṣḥaf(s) that use it, not after a tradition.
    return {"+".join(s["mushaf"]): s for s in systems.values()}


def canonical_form(col: Column) -> Token:
    """The token whose spelling represents the column.

    Ḥafṣ when it has the word, since it is the reference text most consumers
    expect; otherwise the most common spelling, then the earliest riwāyah.
    """
    if "hafs" in col.tokens:
        return col.tokens["hafs"]
    counts = Counter(t.uthmani for t in col.tokens.values())
    best = counts.most_common(1)[0][0]
    for key in ORDER:
        tok = col.tokens.get(key)
        if tok and tok.uthmani == best:
            return tok
    return next(iter(col.tokens.values()))


def build_words(riwayat: list[Riwaya]) -> list[Word]:
    """The whole index, numbered.

    A spine word takes the next ID and a ``sub`` of 0.  An addition takes the
    *preceding* spine word's ID with the next sub-index, which is what keeps the
    spine's numbering unbroken while still placing the extra word in reading
    order: Bazzī's ``مِن`` at 9:101 sits at ``تَجۡرِي``'s ID with ``sub`` 1, and the
    six muṣḥafs without it have no hole to explain.
    """
    streams = streams_for(riwayat)
    keys = [r.key for r in riwayat]

    words: list[Word] = []
    next_id = 1
    for sura in range(1, 115):
        per_sura = {k: [t for t in streams[k] if t.sura == sura] for k in ORDER}
        spine = build_spine(per_sura, ORDER)

        seen: Counter[str] = Counter()
        # Reset per sūrah: an addition attaches to the spine word before it, and
        # the last word of the previous sūrah is not that word.
        spine_id = spine_index = sub = index = 0
        for col in spine:
            # An addition before any spine word has nothing to hang on, so it
            # becomes a spine word itself — the one case that would put a gap in
            # Ḥafṣ.  It does not occur in this corpus; the fallback is here so
            # that it could never pass silently.
            if is_addition(col) and spine_id:
                sub += 1
            else:
                spine_id, next_id = next_id, next_id + 1
                index += 1
                spine_index, sub = index, 0
            canon = canonical_form(col)
            present = [k for k in keys if k in col.tokens]
            # The key is built from the *pointed* skeleton, not the bare rasm:
            # `2:تعملون#1` is legible where `2:ٮعملوں#1` is not, and it is just
            # as stable, since it comes from one canonical spelling.
            seen[canon.pointed] += 1
            forms = {k: col.tokens[k].uthmani for k in present}
            words.append(Word(
                id=spine_id,
                sub=sub,
                sura=sura,
                index=spine_index,
                key=f"{sura}:{canon.pointed}#{seen[canon.pointed]}",
                rasm=col.rasm,
                pointed=canon.pointed,
                uthmani=canon.uthmani,
                simple=canon.simple,
                status=classify(col, keys),
                present=present,
                # Nobody is *missing* an addition: the word is not part of the
                # shared text, so a muṣḥaf without it has dropped nothing.  Who
                # does write it is in `present` and `forms`.
                missing=[] if sub else [k for k in keys if k not in col.tokens],
                forms=forms,
                aya={k: col.tokens[k].aya for k in present},
                waqf={k: col.tokens[k].waqf for k in present if col.tokens[k].waqf},
                boundary=dict(col.boundary),
                hizb=[k for k in present if col.tokens[k].hizb],
                sajdah=[k for k in present if col.tokens[k].sajdah],
                place={k: (col.tokens[k].page, col.tokens[k].line)
                       for k in present if col.tokens[k].page},
            ))
    return words
