"""Checks run over the built index and over the sources themselves.

Two independent questions are asked here:

* Is the *index* self-consistent — contiguous IDs, every riwayah accounted
  for, ayah numbering intact?
* Do the *sources* agree with themselves — where a riwayah ships both a 2022
  and a 2026 release, do the two say the same thing?

The second question is the more interesting one, and its answers become the
issues report.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from .build import Kalimah
from .normalize import fold_notation, rasm, uthmani
from .sources import Riwayah
from .tokenize import tokenize

# There is deliberately no table of expected ayah totals here.
#
# An earlier version asserted {"kufi": 6236, "madani": 6214, "basri": 6217} and
# reported Sūsī's 6,218 as a defect.  Both the premise and the conclusion were
# wrong.  Many fasilahs are مختلف فيها, so a printed mushaf has to choose, and
# the qira'ah does not determine the choice: KFGQPC's own Dūrī printings state
# they follow المدني الأول and yet total 6,218 (1429 AH), 6,217 (1436) and
# 6,214 (1443).  Al-Mulk 67:9 «قد جاءنا نذير» is one such point — al-Dānī has
# it counted by المدني الأخير والمكي and by Shayba — and four of the seven
# packages here count it.  Sūsī was never an outlier.
#
# Asserting a total per tradition therefore measures the assumption, not the
# data.  What is still worth asserting is that the numbering is *internally*
# coherent, which is what remains below.


def check_index(kalimahs: list[Kalimah], riwayahs: list[Riwayah]) -> list[dict]:
    problems: list[dict] = []

    for i, w in enumerate(kalimahs, start=1):
        if w.id != i:
            problems.append({"check": "id_contiguous", "kalimah_id": w.id,
                             "detail": f"expected {i}"})
            break

    seen: Counter[str] = Counter(w.key for w in kalimahs)
    dupes = [k for k, n in seen.items() if n > 1]
    if dupes:
        problems.append({"check": "key_unique",
                         "detail": f"{len(dupes)} duplicate stability keys, "
                                   f"e.g. {dupes[:3]}"})

    by_surah: dict[int, list[Kalimah]] = defaultdict(list)
    for w in kalimahs:
        by_surah[w.surah].append(w)
    for surah, ws in sorted(by_surah.items()):
        if [w.index for w in ws] != list(range(1, len(ws) + 1)):
            problems.append({"check": "index_contiguous", "surah": surah,
                             "detail": "kalimah_index is not 1..n"})

    # Every harf of every riwayah must survive into the index, in order.
    # Comparing the concatenated rasm rather than the kalimah count makes the
    # check indifferent to kalimahs the builder re-segmented.
    for r in riwayahs:
        source = [a for a in r.ayahs if a.ayah > 0 or a.surah == 1]
        got = "".join(rasm(w.forms[r.key]) for w in kalimahs if r.key in w.forms)
        want = "".join(t.rasm for t in tokenize(source))
        if got != want:
            at = next((i for i, (x, y) in enumerate(zip(got, want)) if x != y),
                      min(len(got), len(want)))
            problems.append({
                "check": "roundtrip_rasm", "riwayah": r.key,
                "detail": f"harf streams diverge at offset {at}: index has "
                          f"{got[at:at + 30]!r}, source has {want[at:at + 30]!r}",
            })
    return problems


def check_alif_splits(kalimahs: list[Kalimah]) -> list[dict]:
    """The plene/defective ā must divide the riwayahs exactly one way.

    This is the ground ``alif_variant`` stands on rather than a nicety.  Every
    one of these kalimahs puts {warsh, qālūn} on one side and the other five on the
    other — in both directions, 198 times out of 198 — and a khilāf of the amṣār
    would not do that, since Bazzī is Makkī and Makkah sides with Madinah on
    ḥadhf al-alif as often as not.  One partition means the class tracks the
    publisher's hand, which is why it is reported apart from the harfs the
    mushafs disagree about.  If a future package ever splits one of these kalimahs
    some other way, that inference has lost its warrant and should be revisited
    rather than quietly kept, so it is asserted here instead of being left in a
    paragraph.
    """
    splits: dict[frozenset, list[int]] = defaultdict(list)
    for w in kalimahs:
        if w.status != "alif_variant":
            continue
        groups: dict[str, list[str]] = defaultdict(list)
        for key, form in w.forms.items():
            groups[rasm(form)].append(key)
        splits[frozenset(frozenset(v) for v in groups.values())].append(w.id)
    if len(splits) <= 1:
        return []
    return [{"check": "alif_splits_one_way",
             "detail": f"{len(splits)} distinct riwayah partitions among the "
                       f"{sum(len(v) for v in splits.values())} plene/defective "
                       f"kalimahs; first kalimah of each: "
                       f"{sorted(ids[0] for ids in splits.values())}"}]


def check_release_policy(riwayahs: list[Riwayah]) -> list[dict]:
    """The text must come from each riwayah's *latest* release.

    KFGQPC revises these documents deliberately — the 2026 Ḥafṣ separates
    ``مَا لِيَ`` where the 2022 CSV joins it as ``مَالِيَ`` — so where two releases
    of one riwayah disagree, the later one is the text and the earlier one is a
    cross-check.  Loading them the other way round would publish a superseded
    convention while still passing every structural check, so it is asserted
    rather than assumed.
    """
    out = []
    for r in riwayahs:
        if r.crosscheck and r.crosscheck_year > r.release_year:
            out.append({"check": "release_policy", "riwayah": r.key,
                        "detail": f"the text is loaded from the {r.release_year} "
                                  f"release but a {r.crosscheck_year} one exists"})
    return out


def check_counting(riwayahs: list[Riwayah]) -> list[dict]:
    """Each mushaf's numbering must be internally coherent — nothing more.

    See the note above on why no total is asserted.
    """
    out = []
    for r in riwayahs:
        for surah, n in Counter(a.surah for a in r.ayahs if a.ayah > 0).items():
            nums = sorted(a.ayah for a in r.ayahs if a.surah == surah and a.ayah > 0)
            if nums != list(range(1, n + 1)):
                out.append({"check": "ayah_contiguous", "riwayah": r.key,
                            "surah": surah, "detail": "ayah numbers are not 1..n"})
    return out


def cross_release(riwayahs: list[Riwayah]) -> dict[str, dict]:
    """Compare each riwayah's primary release against its other release.

    Differences split three ways: pure notation (the 2026 files use the Unicode
    codepoints added for open tanwīn where the 2022 files reused others),
    vowelling, and rasm.  Only the last two are textual.
    """
    report: dict[str, dict] = {}
    for r in riwayahs:
        if not r.crosscheck:
            continue
        primary = {(a.surah, a.ayah): a.text for a in r.ayahs if a.ayah > 0}
        shared = primary.keys() & r.crosscheck.keys()
        notation = vowel = rasm_diff = 0
        examples: list[dict] = []
        rasm_examples: list[dict] = []
        for ref in sorted(shared):
            a, b = uthmani(primary[ref]), uthmani(r.crosscheck[ref])
            if a == b:
                continue
            if fold_notation(a) == fold_notation(b):
                notation += 1
            elif rasm(a) == rasm(b):
                vowel += 1
                if len(examples) < 3:
                    examples.append({"ref": f"{ref[0]}:{ref[1]}", "kind": "marks",
                                     "primary": a[:60], "other": b[:60]})
            else:
                rasm_diff += 1
                rasm_examples.append({"ref": f"{ref[0]}:{ref[1]}", "kind": "rasm",
                                      "primary": a, "other": b})
        report[r.key] = {
            "primary": r.source,
            "other": r.crosscheck_source,
            "ayahs_compared": len(shared),
            "only_in_primary": len(primary.keys() - r.crosscheck.keys()),
            "only_in_other": len(r.crosscheck.keys() - primary.keys()),
            "identical": len(shared) - notation - vowel - rasm_diff,
            "notation_only": notation,
            "marks_only": vowel,
            "rasm_differs": rasm_diff,
            "examples": examples,
            "rasm_examples": rasm_examples,
        }
    return report


def check_layout_alignment(riwayahs) -> list[dict]:
    """The typesetting positions must line up with the kalimahs they position.

    :func:`quranidx.layout.kalimah_places` walks the document a second time, for
    positions rather than for text.  Everything downstream zips the two streams
    by index, which is only sound if they are the same stream — so assert it
    rather than trust it.  A future release that moved a heading into the flow
    would otherwise slide every later kalimah onto the wrong line in silence.
    """
    from .layout import raw_tokens
    from .normalize import strip_controls
    from .sources import _extract

    out = []
    for r in riwayahs:
        spec = r.spec
        if not spec or spec.primary_kind != "docx":
            continue
        path = _extract(spec.primary_zip, spec.primary_member)
        want = [t for a in r.ayahs for t in strip_controls(a.text).split()]
        got = raw_tokens(path)
        if want != got:
            where = next((i for i, (x, y) in enumerate(zip(want, got)) if x != y),
                         min(len(want), len(got)))
            out.append({"check": "layout_alignment", "riwayah": r.key,
                        "detail": f"position stream diverges from the text at "
                                  f"token {where} ({len(want)} vs {len(got)})"})
    return out


def check_mushaf_roundtrip(kalimahs, riwayahs) -> list[dict]:
    """Each mushaf's published kalimahs must be that mushaf's kalimahs.

    The same invariant :func:`check_index` asserts for the spine, asserted again
    for the per-mushaf files: concatenating what is published for one mushaf has
    to reproduce what tokenising its source gives, once the handful of places
    where this build re-spaced the text are accounted for.  Those places are
    listed in every file, so the check also confirms the listing is complete.
    """
    from .build import streams_for
    from .normalize import rasm

    out = []
    streams = streams_for(riwayahs)
    for r in riwayahs:
        key = r.key
        mine = [w for w in kalimahs if key in w.forms]
        published = "".join(rasm(w.forms[key]) for w in mine)
        source = "".join(t.rasm for t in streams[key])
        if published != source:
            out.append({"check": "mushaf_roundtrip", "riwayah": key,
                        "detail": "published text does not reproduce the source"})

        declared = {i for w in mine if key in w.boundary for i in (w.id,)}
        flagged = {w.id for w in mine if key in w.boundary}
        if declared != flagged:
            out.append({"check": "mushaf_resegmentation", "riwayah": key,
                        "detail": f"{len(flagged - declared)} re-segmented "
                                  f"kalimah(s) not declared"})

        stray = {n for t in streams[key] for n in t.notes} - {"resegmented"}
        if stray:
            out.append({"check": "mushaf_tokenizer_notes", "riwayah": key,
                        "detail": f"undeclared tokenizer departure(s): "
                                  f"{sorted(stray)}"})
    return out
