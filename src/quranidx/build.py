"""Build the flat kalimah index and every derived artefact.

The output model is deliberately *flat*: a surah is a list of kalimahs, and the
ayah number is an attribute of a kalimah rather than a level of nesting.  That is
what makes one ID usable across all seven riwayahs — the riwayahs disagree about
where ayahs end (Kūfī counts 6236, Madanī 6214, Baṣrī 6217, Makkī 6220) but they
agree, almost everywhere, about the sequence of kalimahs.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from .align import Column, build_spine
from .sources import Riwayah, load_all
from .tokenize import Token, tokenize

OUT = Path("out")

#: Ḥafṣ first because it is the most widely published text and the best
#: starting spine; the rest follow so that the closest relatives merge early.
ORDER = ["hafs", "shuba", "bazzi", "qaloun", "warsh", "douri", "sousi"]

# Status of a canonical kalimah, most specific first.
STATUS_RASM = "rasm_variant"
STATUS_ALIF = "alif_variant"
STATUS_PARTIAL = "partial"
STATUS_BOUNDARY = "kalimah_boundary"
STATUS_DOTTING = "dotting_variant"
STATUS_DIACRITIC = "diacritic_variant"
STATUS_IDENTICAL = "identical"

#: Traditions of ʿadd al-āy, for reference only.  They are *not* the identity
#: of a fasilahs system: see :func:`fasilahs`.
COUNTING_TRADITIONS = {"kufi": "Kūfī", "madani": "Madanī",
                       "basri": "Baṣrī", "makki": "Makkī"}


@dataclass
class Kalimah:
    id: int
    surah: int
    index: int            # 1-based position within the surah
    key: str              # rebuild-stable identity: "surah:pointed#occurrence"
    rasm: str             # bare Uthmani skeleton, shared by every riwayah
    pointed: str          # canonical kalimah's dotted skeleton
    uthmani: str
    simple: str
    status: str
    present: list[str]
    missing: list[str]
    forms: dict[str, str]
    ayah: dict[str, int]
    waqf: dict[str, str]
    boundary: dict[str, str]
    hizb: list[str]
    sajdah: list[str]
    #: riwayah -> (safhah, line) in that mushaf's own typesetting.  The safhah is
    #: read from the release; the line is reconstructed.  See ``layout.py``.
    place: dict[str, tuple[int, int]] = field(default_factory=dict)


def streams_for(riwayahs: list[Riwayah]) -> dict[str, list[Token]]:
    """Tokenise each riwayah, keeping only kalimahs that some riwayah numbers.

    Every surah but at-Tawbah is printed with a basmalah above it.  Only
    Al-Fātiḥah's is *numbered* as an ayah, and only by Ḥafṣ, Shuʿbah and Bazzī.
    A kalimah belongs in the index when any riwayah numbers it, so Al-Fātiḥah's
    basmalah is in (for all seven, unnumbered where it is unnumbered) and the
    other 112 openings stay out, recorded as surah metadata instead.
    """
    out = {}
    for r in riwayahs:
        # Tokenise the *whole* stream before filtering.  The typesetting
        # positions are a flat list over every ayah the document prints,
        # including the 112 unnumbered basmalahs, so dropping ayahs first would
        # slide every later kalimah onto the wrong line.
        toks = tokenize(r.ayahs, r.places or None)
        out[r.key] = [t for t in toks if t.ayah > 0 or t.surah == 1]
    return out


def classify(col: Column, all_keys: list[str]) -> str:
    """Name the strongest kind of disagreement this kalimah carries.

    The order matters and used to be wrong: ``kalimah_boundary`` was returned
    before the kalimahs were compared at all, so five of the six boundary events
    in the corpus were reported as disagreements when in fact all seven riwayahs
    read them identically and one *source* had merely lost a space.  Content is
    now decided first; the boundary stays on the kalimah as an annotation either
    way, and ``kalimah_boundary`` is reserved for a kalimah that is otherwise in
    agreement but printed joined somewhere.

    A difference in the harfs on the line is a ``rasm_variant`` — unless the
    only harf in question is an ā that one hand puts on the line and the other
    puts above it, which is ``alif_variant``.  The split is not a matter of
    taste.  The corpus decides it: all 198 plene/defective kalimahs partition the
    seven riwayahs along exactly one line, {warsh, qālūn} against the other five,
    in both directions and without a single exception, while the 62 kalimahs whose
    skeletons differ once every ā is spelled out partition them fourteen
    different ways — Bazzī alone seven times, Ḥafṣ+Shuʿbah alone six, Qālūn
    alone five.  Ḥadhf/ithbāt al-alif between the mushafs of the amṣār would not
    put Makkah with Madinah 198 times out of 198; a publisher's house style
    would, and does.  So the ā is reported, but not as the mushafs disagreeing.

    ``rasm_plene`` is what draws the line: it spells every ā out, so two kalimahs
    that agree there and differ in ``rasm`` differ only about where the ā was
    written.  The bare ``rasm`` keeps the distinction, because inside any one
    mushaf it is real — Ḥafṣ writes قال plene 412 times and defective 4, and
    that is its own ḥadhf, faithfully carried.
    """
    present = [k for k in all_keys if k in col.tokens]
    if len({col.tokens[k].rasm for k in present}) > 1:
        if len({col.tokens[k].rasm_plene for k in present}) > 1:
            return STATUS_RASM
        return STATUS_ALIF
    if len(present) < len(all_keys):
        return STATUS_PARTIAL
    if col.boundary:
        return STATUS_BOUNDARY
    if len({col.tokens[k].pointed for k in present}) > 1:
        return STATUS_DOTTING
    if len({col.tokens[k].folded for k in present}) > 1:
        return STATUS_DIACRITIC
    return STATUS_IDENTICAL


def ayah_ends(kalimahs: list[Kalimah], key: str) -> list[int]:
    """The ID of the last kalimah of every ayah, for one riwayah's mushaf."""
    ends: list[int] = []
    run = [w for w in kalimahs if w.ayah.get(key, 0) > 0]
    for i, w in enumerate(run):
        nxt = run[i + 1] if i + 1 < len(run) else None
        if nxt is None or (nxt.surah, nxt.ayah[key]) != (w.surah, w.ayah[key]):
            ends.append(w.id)
    return ends


def fasilahs(kalimahs: list[Kalimah]) -> dict[str, dict]:
    """Where each mushaf ends its ayahs, as canonical kalimah IDs.

    **The fasilahs belong to the printed mushaf, not to the qira'ah.**  This is
    not a nicety.  Many fasilahs are مختلف فيها — al-Dānī records 67:9
    «قد جاءنا نذير» as counted by المدني الأخير والمكي and by Shayba, and not
    counted by the rest — so an edition has to *choose*, and different editions
    of the same riwayah choose differently.  KFGQPC's own Dūrī printings show
    it plainly: 1429 AH and 1443 AH split 67:9 and give a colophon total of
    6214, while 1436 AH does not split it and states 6217.  Same publisher,
    same riwayah, three printings, two different divisions.

    So a system is not named for a counting tradition and is not derived from
    one.  It is read off the packages themselves, and riwayahs are grouped only
    where their fasilahs turn out to be identical.  If a future package moves a
    single fasilah, it splits into its own system here rather than being
    quietly averaged into a tradition it does not actually follow.
    """
    ends = {key: ayah_ends(kalimahs, key) for key in ORDER}
    systems: dict[str, dict] = {}
    for key in ORDER:
        for system in systems.values():
            if system["ends"] == ends[key]:
                system["mushaf"].append(key)
                break
        else:
            systems[key] = {"mushaf": [key], "ayah_count": len(ends[key]),
                            "ends": ends[key]}
    # Name each system after the mushaf(s) that use it, not after a tradition.
    return {"+".join(s["mushaf"]): s for s in systems.values()}


def canonical_form(col: Column) -> Token:
    """The token whose spelling represents the column.

    Ḥafṣ when it has the kalimah, since it is the reference text most consumers
    expect; otherwise the most common spelling, then the earliest riwayah.
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


def build_kalimahs(riwayahs: list[Riwayah]) -> list[Kalimah]:
    streams = streams_for(riwayahs)
    keys = [r.key for r in riwayahs]

    kalimahs: list[Kalimah] = []
    next_id = 1
    for surah in range(1, 115):
        per_surah = {k: [t for t in streams[k] if t.surah == surah] for k in ORDER}
        spine = build_spine(per_surah, ORDER)

        seen: Counter[str] = Counter()
        for index, col in enumerate(spine, start=1):
            canon = canonical_form(col)
            present = [k for k in keys if k in col.tokens]
            # The key is built from the *pointed* skeleton, not the bare rasm:
            # `2:تعملون#1` is legible where `2:ٮعملوں#1` is not, and it is just
            # as stable, since it comes from one canonical spelling.
            seen[canon.pointed] += 1
            forms = {k: col.tokens[k].uthmani for k in present}
            kalimahs.append(Kalimah(
                id=next_id,
                surah=surah,
                index=index,
                key=f"{surah}:{canon.pointed}#{seen[canon.pointed]}",
                rasm=col.rasm,
                pointed=canon.pointed,
                uthmani=canon.uthmani,
                simple=canon.simple,
                status=classify(col, keys),
                present=present,
                missing=[k for k in keys if k not in col.tokens],
                forms=forms,
                ayah={k: col.tokens[k].ayah for k in present},
                waqf={k: col.tokens[k].waqf for k in present if col.tokens[k].waqf},
                boundary=dict(col.boundary),
                hizb=[k for k in present if col.tokens[k].hizb],
                sajdah=[k for k in present if col.tokens[k].sajdah],
                place={k: (col.tokens[k].safhah, col.tokens[k].line)
                       for k in present if col.tokens[k].safhah},
            ))
            next_id += 1
    return kalimahs
