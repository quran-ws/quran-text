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
STATUS_BOUNDARY = "word_boundary"
STATUS_PARTIAL = "partial"
STATUS_DIACRITIC = "diacritic_variant"
STATUS_IDENTICAL = "identical"


@dataclass
class Word:
    id: int
    sura: int
    index: int            # 1-based position within the sūrah
    key: str              # rebuild-stable identity: "sura:rasm#occurrence"
    rasm: str
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
    present = [k for k in all_keys if k in col.tokens]
    if col.boundary:
        # A boundary disagreement explains any absence here, so it is reported
        # ahead of "partial" — otherwise the cause is hidden by its effect.
        return STATUS_BOUNDARY
    if len(present) < len(all_keys):
        return STATUS_PARTIAL
    if len({col.tokens[k].rasm for k in present}) > 1:
        return STATUS_RASM
    if len({col.tokens[k].folded for k in present}) > 1:
        return STATUS_DIACRITIC
    return STATUS_IDENTICAL


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
            seen[col.rasm] += 1
            forms = {k: col.tokens[k].uthmani for k in present}
            words.append(Word(
                id=next_id,
                sura=sura,
                index=index,
                key=f"{sura}:{col.rasm}#{seen[col.rasm]}",
                rasm=col.rasm,
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
