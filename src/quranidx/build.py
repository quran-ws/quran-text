"""Build the flat word index and every derived artefact.

The output model is deliberately *flat*: a sūrah is a list of words, and the
āyah number is an attribute of a word rather than a level of nesting.  That is
what makes one number usable across all seven riwāyāt — the editions disagree
about where āyāt end (6,214 to 6,236 of them) but they agree, almost
everywhere, about the sequence of words.

The numbering counts the finest division any muṣḥaf prints.  It is a property
of the format, fixed by ``format_version``, not a per-file choice: see
``docs/MUSHAF-FORMAT.md``, *Numbering*.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from .align import WRITTEN_JOINED, Column, build_spine
from .sources import Riwaya, load_all
from .tokenize import Token, tokenize

OUT = Path("out")

#: Ḥafṣ first because it is the most widely published text and the best
#: starting spine; the rest follow so that the closest relatives merge early.
ORDER = ["hafs", "shuba", "bazzi", "qaloun", "warsh", "douri", "sousi"]

# Status of a canonical word, most specific first.
STATUS_RASM = "rasm_variant"
STATUS_ALIF = "alif_variant"
STATUS_PARTIAL = "partial"
STATUS_BOUNDARY = "word_boundary"
STATUS_DOTTING = "dotting_variant"
STATUS_DIACRITIC = "diacritic_variant"
STATUS_IDENTICAL = "identical"


@dataclass
class Word:
    #: The shared number, ``1 … total``: the same integer is the same word in
    #: every muṣḥaf that has it.
    id: int
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
    #: Riwāyāt whose printed word here is the *same* printed word as at the
    #: previous number — they write the two as one.  Present, not missing,
    #: but not a word of their own at this position.
    continuation: list[str] = field(default_factory=list)


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
    present = [k for k in all_keys if col.present(k)]
    # A riwāyah that writes this word joined to its neighbour carries the
    # letters of two words; it is compared on nothing and counted as present.
    apart = [k for k in present if col.boundary.get(k) != WRITTEN_JOINED]
    if len({col.tokens[k].rasm for k in apart}) > 1:
        if len({col.tokens[k].rasm_plene for k in apart}) > 1:
            return STATUS_RASM
        return STATUS_ALIF
    if len(present) < len(all_keys):
        return STATUS_PARTIAL
    if col.boundary:
        return STATUS_BOUNDARY
    if len({col.tokens[k].pointed for k in apart}) > 1:
        return STATUS_DOTTING
    if len({col.tokens[k].folded for k in apart}) > 1:
        return STATUS_DIACRITIC
    return STATUS_IDENTICAL


def ayah_ends(words: list[Word], key: str) -> list[int]:
    """The ID of the last word of every āyah, for one riwāyah's muṣḥaf."""
    ends: list[int] = []
    run = [w for w in words if w.aya.get(key, 0) > 0]
    # A number covered by the previous printed word cannot end an āyah of its
    # own; the āyah ends after the printed word, i.e. after the *last* number
    # it covers.  Both numbers share the āyah, so the last one is what ends it.
    for i, w in enumerate(run):
        nxt = run[i + 1] if i + 1 < len(run) else None
        if nxt is None or (nxt.sura, nxt.aya[key]) != (w.sura, w.aya[key]):
            ends.append(w.id)
    return ends


def canonical_form(col: Column) -> Token:
    """The token whose spelling represents the column.

    Ḥafṣ when it has the word, since it is the reference text most consumers
    expect; otherwise the most common spelling, then the earliest riwāyah.  A
    riwāyah that writes the word joined to its neighbour is passed over: its
    spelling is of two words, and the number is for one.
    """
    apart = {k: t for k, t in col.tokens.items()
             if col.boundary.get(k) != WRITTEN_JOINED} or dict(col.tokens)
    if "hafs" in apart:
        return apart["hafs"]
    counts = Counter(t.uthmani for t in apart.values())
    best = counts.most_common(1)[0][0]
    for key in ORDER:
        tok = apart.get(key)
        if tok and tok.uthmani == best:
            return tok
    return next(iter(apart.values()))


def build_words(riwayat: list[Riwaya]) -> list[Word]:
    streams = streams_for(riwayat)
    keys = [r.key for r in riwayat]

    words: list[Word] = []
    next_id = 1
    for sura in range(1, 115):
        per_sura = {k: [t for t in streams[k] if t.sura == sura] for k in ORDER}
        spine = build_spine(per_sura, ORDER)

        seen: Counter[str] = Counter()
        for index, col in enumerate(spine, start=1):
            canon = canonical_form(col)
            present = [k for k in keys if col.present(k)]
            # The key is built from the *pointed* skeleton, not the bare rasm:
            # `2:تعملون#1` is legible where `2:ٮعملوں#1` is not, and it is just
            # as stable, since it comes from one canonical spelling.
            seen[canon.pointed] += 1
            tokens = {k: col.token(k) for k in present}
            forms = {k: tokens[k].uthmani for k in present}
            words.append(Word(
                id=next_id,
                sura=sura,
                index=index,
                key=f"{sura}:{canon.pointed}#{seen[canon.pointed]}",
                rasm=col.rasm,
                pointed=canon.pointed,
                uthmani=canon.uthmani,
                simple=canon.simple,
                status=classify(col, keys),
                present=present,
                missing=[k for k in keys if not col.present(k)],
                forms=forms,
                aya={k: tokens[k].aya for k in present},
                waqf={k: tokens[k].waqf for k in present if tokens[k].waqf},
                boundary=dict(col.boundary),
                hizb=[k for k in present if tokens[k].hizb],
                sajdah=[k for k in present if tokens[k].sajdah],
                place={k: (tokens[k].page, tokens[k].line)
                       for k in present if tokens[k].page},
                continuation=[k for k in keys if k in col.covers],
            ))
            next_id += 1
    return words
