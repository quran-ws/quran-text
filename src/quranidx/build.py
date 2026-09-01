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
from dataclasses import dataclass
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
        keep = [a for a in r.ayat if a.aya > 0 or a.sura == 1]
        out[r.key] = tokenize(keep)
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

    Any difference in the letters on the line is a ``rasm_variant``, including
    the 198 words where the two typesettings disagree only about whether to put
    an ā on the line or above it.  That sub-class is worth knowing about — see
    :func:`normalize.rasm_plene`, which is what identifies it, and the report
    section that lists it — but it is not a separate verdict: a written alef is
    part of the bare rasm whichever hand wrote it.
    """
    present = [k for k in all_keys if k in col.tokens]
    if len({col.tokens[k].rasm for k in present}) > 1:
        return STATUS_RASM
    if len(present) < len(all_keys):
        return STATUS_PARTIAL
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
            present = [k for k in keys if k in col.tokens]
            # The key is built from the *pointed* skeleton, not the bare rasm:
            # `2:تعملون#1` is legible where `2:ٮعملوں#1` is not, and it is just
            # as stable, since it comes from one canonical spelling.
            seen[canon.pointed] += 1
            forms = {k: col.tokens[k].uthmani for k in present}
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
                missing=[k for k in keys if k not in col.tokens],
                forms=forms,
                aya={k: col.tokens[k].aya for k in present},
                waqf={k: col.tokens[k].waqf for k in present if col.tokens[k].waqf},
                boundary=dict(col.boundary),
                hizb=[k for k in present if col.tokens[k].hizb],
                sajdah=[k for k in present if col.tokens[k].sajdah],
            ))
            next_id += 1
    return words
