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

#: Counting traditions, and the riwāyāt that follow each.  Dūrī and Sūsī are
#: both Baṣrī but part company at exactly one fāṣilah, so they are listed
#: separately rather than pretending to a single Baṣrī system.
FAWASIL_SYSTEMS = {
    "kufi": ["hafs", "shuba"],
    "madani": ["warsh", "qaloun"],
    "basri_douri": ["douri"],
    "basri_sousi": ["sousi"],
    "makki": ["bazzi"],
}


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


def fawasil(words: list[Word]) -> dict[str, dict]:
    """Where each counting tradition ends its āyāt, as canonical word IDs.

    The fawāṣil are a layer *over* the word index, not a property of it: the
    riwāyāt agree about the sequence of words far more than about where the
    āyāt stop.  Recording them separately is what lets one ID mean one word in
    all seven riwāyāt while each tradition keeps its own count.
    """
    out: dict[str, dict] = {}
    for system, keys in FAWASIL_SYSTEMS.items():
        key = keys[0]
        ends: list[int] = []
        run = [w for w in words if w.aya.get(key, 0) > 0]
        for i, w in enumerate(run):
            nxt = run[i + 1] if i + 1 < len(run) else None
            if nxt is None or (nxt.sura, nxt.aya[key]) != (w.sura, w.aya[key]):
                ends.append(w.id)
        out[system] = {"riwayat": keys, "ayah_count": len(ends), "ends": ends}
    return out


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
