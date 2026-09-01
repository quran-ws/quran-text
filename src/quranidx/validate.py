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

#: Āyah totals of the classical counting traditions, for checking the parsed
#: sources against something external to them.
COUNTING_TOTALS = {"kufi": 6236, "madani": 6214, "basri": 6217}


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
    out = []
    for r in riwayat:
        total = sum(1 for a in r.ayat if a.aya > 0)
        expected = COUNTING_TOTALS.get(r.counting)
        if expected is not None and total != expected:
            out.append({"check": "counting_total", "riwaya": r.key,
                        "detail": f"the {r.counting} tradition totals {expected} "
                                  f"āyāt; this release has {total}"})
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
