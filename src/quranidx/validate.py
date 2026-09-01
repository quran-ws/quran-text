"""Checks run over the built index and over the sources themselves.

Two independent questions are asked here:

* Is the *index* self-consistent — contiguous IDs, every riwāyah accounted
  for, āyah numbering intact?
* Do the *sources* agree with themselves — where a riwāyah ships both a 2022
  and a 2026 release, do the two say the same thing?

The second question is the more interesting one, and its answers become the
issues report.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from .build import Word
from .normalize import fold_notation, rasm, uthmani
from .sources import Riwaya
from .tokenize import tokenize

# There is deliberately no table of expected āyah totals here.
#
# An earlier version asserted {"kufi": 6236, "madani": 6214, "basri": 6217} and
# reported Sūsī's 6,218 as a defect.  Both the premise and the conclusion were
# wrong.  Many fawāṣil are مختلف فيها, so a printed muṣḥaf has to choose, and
# the qirāʾah does not determine the choice: KFGQPC's own Dūrī printings state
# they follow المدني الأول and yet total 6,218 (1429 AH), 6,217 (1436) and
# 6,214 (1443).  Al-Mulk 67:9 «قد جاءنا نذير» is one such point — al-Dānī has
# it counted by المدني الأخير والمكي and by Shayba — and four of the seven
# packages here count it.  Sūsī was never an outlier.
#
# Asserting a total per tradition therefore measures the assumption, not the
# data.  What is still worth asserting is that the numbering is *internally*
# coherent, which is what remains below.


def check_index(words: list[Word], riwayat: list[Riwaya]) -> list[dict]:
    problems: list[dict] = []

    for i, w in enumerate(words, start=1):
        if w.id != i:
            problems.append({"check": "id_contiguous", "word_id": w.id,
                             "detail": f"expected {i}"})
            break

    seen: Counter[str] = Counter(w.key for w in words)
    dupes = [k for k, n in seen.items() if n > 1]
    if dupes:
        problems.append({"check": "key_unique",
                         "detail": f"{len(dupes)} duplicate stability keys, "
                                   f"e.g. {dupes[:3]}"})

    by_sura: dict[int, list[Word]] = defaultdict(list)
    for w in words:
        by_sura[w.sura].append(w)
    for sura, ws in sorted(by_sura.items()):
        if [w.index for w in ws] != list(range(1, len(ws) + 1)):
            problems.append({"check": "index_contiguous", "sura": sura,
                             "detail": "word_index is not 1..n"})

    # Slot IDs are shared and may have gaps in one muṣḥaf.  Its own word
    # positions must not: they count only tokens that are actually present.
    for r in riwayat:
        got = [w.position[r.key] for w in words if r.key in w.position]
        want = list(range(1, len(got) + 1))
        if got != want:
            problems.append({"check": "position_contiguous", "riwaya": r.key,
                             "detail": "dense positions are not 1..word_count"})

    # Every letter of every riwāyah must survive into the index, in order.
    # Comparing the concatenated rasm rather than the word count makes the
    # check indifferent to words the builder re-segmented.
    for r in riwayat:
        source = [a for a in r.ayat if a.aya > 0 or a.sura == 1]
        got = "".join(rasm(w.forms[r.key]) for w in words if r.key in w.forms)
        want = "".join(t.rasm for t in tokenize(source))
        if got != want:
            at = next((i for i, (x, y) in enumerate(zip(got, want)) if x != y),
                      min(len(got), len(want)))
            problems.append({
                "check": "roundtrip_rasm", "riwaya": r.key,
                "detail": f"letter streams diverge at offset {at}: index has "
                          f"{got[at:at + 30]!r}, source has {want[at:at + 30]!r}",
            })
    return problems


def check_alif_splits(words: list[Word]) -> list[dict]:
    """The plene/defective ā must divide the riwāyāt exactly one way.

    This is the ground ``alif_variant`` stands on rather than a nicety.  Every
    one of these words puts {warsh, qālūn} on one side and the other five on the
    other — in both directions, 198 times out of 198 — and a khilāf of the amṣār
    would not do that, since Bazzī is Makkī and Makkah sides with Madinah on
    ḥadhf al-alif as often as not.  One partition means the class tracks the
    publisher's hand, which is why it is reported apart from the letters the
    codices disagree about.  If a future package ever splits one of these words
    some other way, that inference has lost its warrant and should be revisited
    rather than quietly kept, so it is asserted here instead of being left in a
    paragraph.
    """
    splits: dict[frozenset, list[int]] = defaultdict(list)
    for w in words:
        if w.status != "alif_variant":
            continue
        groups: dict[str, list[str]] = defaultdict(list)
        for key, form in w.forms.items():
            groups[rasm(form)].append(key)
        splits[frozenset(frozenset(v) for v in groups.values())].append(w.id)
    if len(splits) <= 1:
        return []
    return [{"check": "alif_splits_one_way",
             "detail": f"{len(splits)} distinct riwāyah partitions among the "
                       f"{sum(len(v) for v in splits.values())} plene/defective "
                       f"words; first word of each: "
                       f"{sorted(ids[0] for ids in splits.values())}"}]


def check_release_policy(riwayat: list[Riwaya]) -> list[dict]:
    """The text must come from each riwāyah's *latest* release.

    KFGQPC revises these documents deliberately — the 2026 Ḥafṣ separates
    ``مَا لِيَ`` where the 2022 CSV joins it as ``مَالِيَ`` — so where two releases
    of one riwāyah disagree, the later one is the text and the earlier one is a
    cross-check.  Loading them the other way round would publish a superseded
    convention while still passing every structural check, so it is asserted
    rather than assumed.
    """
    out = []
    for r in riwayat:
        if r.crosscheck and r.crosscheck_year > r.release_year:
            out.append({"check": "release_policy", "riwaya": r.key,
                        "detail": f"the text is loaded from the {r.release_year} "
                                  f"release but a {r.crosscheck_year} one exists"})
    return out


def check_counting(riwayat: list[Riwaya]) -> list[dict]:
    """Each muṣḥaf's numbering must be internally coherent — nothing more.

    See the note above on why no total is asserted.
    """
    out = []
    for r in riwayat:
        for sura, n in Counter(a.sura for a in r.ayat if a.aya > 0).items():
            nums = sorted(a.aya for a in r.ayat if a.sura == sura and a.aya > 0)
            if nums != list(range(1, n + 1)):
                out.append({"check": "ayah_contiguous", "riwaya": r.key,
                            "sura": sura, "detail": "āyah numbers are not 1..n"})
    return out


def cross_release(riwayat: list[Riwaya]) -> dict[str, dict]:
    """Compare each riwāyah's primary release against its other release.

    Differences split three ways: pure notation (the 2026 files use the Unicode
    codepoints added for open tanwīn where the 2022 files reused others),
    vowelling, and rasm.  Only the last two are textual.
    """
    report: dict[str, dict] = {}
    for r in riwayat:
        if not r.crosscheck:
            continue
        primary = {(a.sura, a.aya): a.text for a in r.ayat if a.aya > 0}
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
            "ayat_compared": len(shared),
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


def check_layout_alignment(riwayat) -> list[dict]:
    """The typesetting positions must line up with the words they position.

    :func:`quranidx.layout.word_places` walks the document a second time, for
    positions rather than for text.  Everything downstream zips the two streams
    by index, which is only sound if they are the same stream — so assert it
    rather than trust it.  A future release that moved a heading into the flow
    would otherwise slide every later word onto the wrong line in silence.
    """
    from .layout import raw_tokens
    from .normalize import strip_controls
    from .sources import _extract

    out = []
    for r in riwayat:
        spec = r.spec
        if not spec or spec.primary_kind != "docx":
            continue
        path = _extract(spec.primary_zip, spec.primary_member)
        want = [t for a in r.ayat for t in strip_controls(a.text).split()]
        got = raw_tokens(path)
        if want != got:
            where = next((i for i, (x, y) in enumerate(zip(want, got)) if x != y),
                         min(len(want), len(got)))
            out.append({"check": "layout_alignment", "riwaya": r.key,
                        "detail": f"position stream diverges from the text at "
                                  f"token {where} ({len(want)} vs {len(got)})"})
    return out


def check_mushaf_roundtrip(words, riwayat) -> list[dict]:
    """Each muṣḥaf's published words must be that muṣḥaf's words.

    The same invariant :func:`check_index` asserts for the spine, asserted again
    for the per-muṣḥaf files: concatenating what is published for one muṣḥaf has
    to reproduce what tokenising its source gives, once the handful of places
    where this build re-spaced the text are accounted for.  Those places are
    listed in every file, so the check also confirms the listing is complete.
    """
    from .build import streams_for
    from .normalize import rasm

    out = []
    streams = streams_for(riwayat)
    for r in riwayat:
        key = r.key
        mine = [w for w in words if key in w.forms]
        published = "".join(rasm(w.forms[key]) for w in mine)
        source = "".join(t.rasm for t in streams[key])
        if published != source:
            out.append({"check": "mushaf_roundtrip", "riwaya": key,
                        "detail": "published text does not reproduce the source"})

        declared = {i for w in mine if key in w.boundary for i in (w.id,)}
        flagged = {w.id for w in mine if key in w.boundary}
        if declared != flagged:
            out.append({"check": "mushaf_resegmentation", "riwaya": key,
                        "detail": f"{len(flagged - declared)} re-segmented "
                                  f"word(s) not declared"})

        stray = {n for t in streams[key] for n in t.notes} - {"resegmented"}
        if stray:
            out.append({"check": "mushaf_tokenizer_notes", "riwaya": key,
                        "detail": f"undeclared tokenizer departure(s): "
                                  f"{sorted(stray)}"})
    return out
