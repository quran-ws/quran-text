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

import json
from collections import Counter, defaultdict
from pathlib import Path

from . import paths
from .build import Word
from .normalize import fold_notation, rasm, rasm_uthmani
from .sources import Riwayah
from .tokenize import tokenize

# There is deliberately no table of expected āyah totals here.
#
# An earlier version asserted {"kufi": 6236, "madani": 6214, "basri": 6217} and
# reported Sūsī's 6,218 as a defect.  Both the premise and the conclusion were
# wrong.  Many fawāṣil are مختلف فيها, so a printed muṣḥaf has to choose, and
# the riwāyah does not determine the choice: KFGQPC's own Dūrī printings state
# they follow المدني الأول and yet total 6,218 (1429 AH), 6,217 (1436) and
# 6,214 (1443).  Mulk 67:9 «قد جاءنا نذير» is one such point — al-Dānī has
# it counted by المدني الأخير والمكي and by Shayba — and four of the seven
# packages here count it.  Sūsī was never an outlier.
#
# Asserting a total per tradition therefore measures the assumption, not the
# data.  What is still worth asserting is that the numbering is *internally*
# coherent, which is what remains below.


def check_index(words: list[Word], riwayahs: list[Riwayah]) -> list[dict]:
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

    by_surah: dict[int, list[Word]] = defaultdict(list)
    for w in words:
        by_surah[w.surah].append(w)
    for surah, ws in sorted(by_surah.items()):
        if [w.index for w in ws] != list(range(1, len(ws) + 1)):
            problems.append({"check": "index_contiguous", "surah": surah,
                             "detail": "word_index is not 1..n"})

    # Every letter of every riwāyah must survive into the index, in order.
    # Comparing the concatenated rasm rather than the word count makes the
    # check indifferent to words the builder re-segmented.
    for r in riwayahs:
        source = [a for a in r.ayahs if a.ayah > 0 or a.surah == 1]
        got = "".join(rasm(w.forms[r.key]) for w in words
                      if r.key in w.forms and r.key not in w.continuation)
        want = "".join(t.rasm for t in tokenize(source))
        if got != want:
            at = next((i for i, (x, y) in enumerate(zip(got, want)) if x != y),
                      min(len(got), len(want)))
            problems.append({
                "check": "roundtrip_rasm", "riwayah": r.key,
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


def check_release_policy(riwayahs: list[Riwayah]) -> list[dict]:
    """The text must come from each riwāyah's *latest* release.

    KFGQPC revises these documents deliberately — the 2026 Ḥafṣ separates
    ``مَا لِيَ`` where the 2022 CSV joins it as ``مَالِيَ`` — so where two releases
    of one riwāyah disagree, the later one is the text and the earlier one is a
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


def check_ayah_numbers(riwayahs: list[Riwayah]) -> list[dict]:
    """Each muṣḥaf's āyah numbers must run 1..n in every sūrah — nothing more.

    See the note above on why no total is asserted.
    """
    out = []
    for r in riwayahs:
        for surah, n in Counter(a.surah for a in r.ayahs if a.ayah > 0).items():
            nums = sorted(a.ayah for a in r.ayahs if a.surah == surah and a.ayah > 0)
            if nums != list(range(1, n + 1)):
                out.append({"check": "ayah_contiguous", "riwayah": r.key,
                            "surah": surah, "detail": "āyah numbers are not 1..n"})
    return out


def cross_release(riwayahs: list[Riwayah]) -> dict[str, dict]:
    """Compare each riwāyah's primary release against its other release.

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
            a, b = rasm_uthmani(primary[ref]), rasm_uthmani(r.crosscheck[ref])
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
    """The typesetting positions must line up with the words they position.

    :func:`qurantext.layout.word_places` walks the document a second time, for
    positions rather than for text.  Everything downstream zips the two streams
    by index, which is only sound if they are the same stream — so assert it
    rather than trust it.  A future release that moved a heading into the flow
    would otherwise slide every later word onto the wrong line in silence.
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


#: What a published file is allowed *not* to contain, and why.  Everything
#: else the release writes has to survive into ``words`` or into ``marks``.
DECLARED_ABSENT = {
    "\u06dd": "āyah mark; the āyah layer says the same thing",
    "\u06de": "۞; published in marks",
    "\u06e9": "۩; published in marks",
    "\u00a0": "no-break space; folded to a plain space",
    " ": "word separator",
    **{chr(0x0660 + i): "āyah number digit; the āyah layer says the same thing"
       for i in range(10)},
}


def check_nothing_dropped(docs: dict[str, dict], riwayahs) -> list[dict]:
    """No codepoint of a release may vanish without being declared.

    Twice now a whole class of character has been deleted on the reading that
    it was not text — the kashida, which is usually a seat for a hamzah, and
    the ṣaḥḥa, which is 9,950 signs the Warsh release prints — and neither
    deletion was visible to any check, because both sides of every comparison
    had been through the same stripping.  This one compares against the
    *package*: every codepoint in the source has to appear in the published
    words, in the published marks, or in :data:`DECLARED_ABSENT`.

    Codepoints, not occurrences.  A sign that moved from the word to a mark is
    still present; a sign that is gone from both is the failure this catches,
    and it is always a whole class at once.
    """
    out = []
    by_key = {r.key: r for r in riwayahs}
    for key, doc in sorted(docs.items()):
        r = by_key.get(key)
        if r is None:
            continue
        source = {ch for a in r.ayahs for ch in a.text}
        published = {ch for w in doc["words"] for ch in w}
        published |= {t["sign"] for t in doc["mark_types"]}
        gone = source - published - set(DECLARED_ABSENT)
        if gone:
            named = ", ".join(f"U+{ord(c):04X}" for c in sorted(gone))
            out.append({"check": "nothing_dropped", "riwayah": key,
                        "detail": f"codepoint(s) in the release and in no "
                                  f"published field: {named}"})
    return out


def check_mushaf_roundtrip(words, riwayahs) -> list[dict]:
    """Each muṣḥaf's published words must be that muṣḥaf's words.

    The same invariant :func:`check_index` asserts for the word index, asserted again
    for the per-muṣḥaf files: concatenating what is published for one muṣḥaf has
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
        mine = [w for w in words if key in w.forms and key not in w.continuation]
        published = "".join(rasm(w.forms[key]) for w in mine)
        source = "".join(t.rasm for t in streams[key])
        if published != source:
            out.append({"check": "mushaf_roundtrip", "riwayah": key,
                        "detail": "published text does not reproduce the source"})

        from .align import WRITTEN_JOINED
        from .word_index import boundary_events
        declared = {i for e in boundary_events(words) if key in e["riwayahs"]
                    for i in e["word_ids"] if key in next(
                        w for w in words if w.id == i).forms}
        flagged = {w.id for w in mine
                   if w.boundary.get(key) not in (None, WRITTEN_JOINED)}
        if declared != flagged:
            out.append({"check": "mushaf_resegmentation", "riwayah": key,
                        "detail": f"{len(flagged - declared)} re-segmented "
                                  f"word(s) not declared"})

        stray = {n for t in streams[key] for n in t.notes} - {"resegmented"}
        if stray:
            out.append({"check": "mushaf_tokenizer_notes", "riwayah": key,
                        "detail": f"undeclared tokenizer departure(s): "
                                  f"{sorted(stray)}"})
    return out


# --------------------------------------------------------------------------
# the published files
# --------------------------------------------------------------------------

SCHEMA = paths.SCHEMA / "mushaf-1.0.json"


def check_numbering(docs: dict[str, dict]) -> list[dict]:
    """The invariants of the shared numbering, over all seven files at once.

    1. every number in ``1 … total`` is covered by exactly one word or listed
       in ``missing``, never both, never neither;
    2. ``len(words) + Σ(len(run) − 1) + len(missing) == total``;
    3. ``total`` is identical across the seven;
    4. every ``written_joined`` run is length ≥ 2, and every ``missing`` number
       is read by at least one *other* muṣḥaf — otherwise it would not be in
       the numbering at all.
    """
    problems: list[dict] = []
    totals = {d["numbering"]["total"] for d in docs.values()}
    if len(totals) != 1:
        problems.append({"check": "numbering_total",
                         "detail": f"files disagree about total: {sorted(totals)}"})
    covered: dict[int, set[str]] = defaultdict(set)
    for key, doc in docs.items():
        try:
            from .mushaf import numbers_of
            runs = numbers_of(doc)
        except AssertionError as e:
            problems.append({"check": "numbering_tiles", "riwayah": key, "detail": str(e)})
            continue
        n = doc["numbering"]
        if len(doc["words"]) + sum(l - f for f, l in runs) + len(n["missing"]) != n["total"]:
            problems.append({"check": "numbering_sum", "riwayah": key,
                             "detail": "len(words) + joined + missing != total"})
        for j in n["written_joined"]:
            if j["numbers"][1] <= j["numbers"][0]:
                problems.append({"check": "numbering_joined_run", "riwayah": key,
                                 "detail": f"run at {j['position']} is not ≥ 2"})
        for f, l in runs:
            for k in range(f, l + 1):
                covered[k].add(key)
    total = max(totals)
    nobody = [k for k in range(1, total + 1) if not covered.get(k)]
    if nobody:
        problems.append({"check": "numbering_read_by_nobody",
                         "detail": f"{len(nobody)} number(s) no muṣḥaf reads, "
                                   f"e.g. {nobody[:3]}"})
    return problems


def check_positions(docs: dict[str, dict]) -> list[dict]:
    """Every ``*_starts`` layer is a strictly increasing list of positions
    inside ``words``, and the sūrah header agrees with the āyah layer."""
    problems: list[dict] = []
    for key, doc in docs.items():
        n = len(doc["words"])
        for layer in ("surah_starts", "ayah_starts", "page_starts",
                      "line_starts", "juz_starts"):
            starts = doc.get(layer)
            if starts is None:
                continue
            if starts != sorted(set(starts)) or starts[0] < 0 or starts[-1] >= n:
                problems.append({"check": "positions_sorted", "riwayah": key,
                                 "detail": f"{layer} is not strictly increasing "
                                           f"within 0 … {n - 1}"})
        if doc["surah_starts"][0] != 0 or len(doc["surah_starts"]) != 114:
            problems.append({"check": "positions_surahs", "riwayah": key,
                             "detail": "surah_starts must be 114 entries from 0"})
        if len(doc["ayah_starts"]) != doc["counting"]["ayah_count"]:
            problems.append({"check": "positions_ayah_count", "riwayah": key,
                             "detail": "len(ayah_starts) != counting.ayah_count"})
        if doc["mushaf"]["word_count"] != n:
            problems.append({"check": "positions_word_count", "riwayah": key,
                             "detail": "mushaf.word_count != len(words)"})
        expect = 0
        for row in doc["surahs"]:
            if row["first_ayah"] != expect:
                problems.append({"check": "positions_first_ayah", "riwayah": key,
                                 "detail": f"sūrah {row['number']}: first_ayah "
                                           f"{row['first_ayah']} != {expect}"})
                break
            expect += row["ayah_count"]
        if doc.get("rasm_imlai") is not None and len(doc["rasm_imlai"]) != n:
            problems.append({"check": "positions_rasm_imlai", "riwayah": key,
                             "detail": "rasm_imlai is not parallel to words"})
        for position, t in doc["marks"]:
            if not (0 <= position < n and 0 <= t < len(doc["mark_types"])):
                problems.append({"check": "positions_marks", "riwayah": key,
                                 "detail": f"mark [{position}, {t}] out of range"})
                break
    return problems


def check_schema_fields(docs: dict[str, dict], schema: Path = SCHEMA) -> list[dict]:
    """The muṣḥaf documents and the JSON Schema must agree on the field set.

    ``schema/mushaf-1.0.json`` is published as the checkable specification and
    sets ``additionalProperties: false``.  A full JSON Schema validation would
    need a dependency this project does not take; comparing the field *names*
    needs none, and catches the drift that actually happens — a field emitted
    by the build and never declared, or declared, required, and not emitted.
    """
    if not schema.exists():
        return [{"check": "schema_present",
                 "detail": f"{schema} is referenced by the docs but missing"}]
    spec = json.loads(schema.read_text(encoding="utf-8"))
    declared = set(spec["properties"])
    required = set(spec.get("required", []))
    problems: list[dict] = []
    for key, doc in sorted(docs.items()):
        undeclared = set(doc) - declared
        if undeclared:
            problems.append({"check": "schema_fields", "riwayah": key,
                             "detail": f"document fields not in the schema: "
                                       f"{sorted(undeclared)}"})
        lacking = required - set(doc)
        if lacking:
            problems.append({"check": "schema_fields", "riwayah": key,
                             "detail": f"required fields missing: {sorted(lacking)}"})
        for name, sub in spec["properties"].items():
            if name in doc and isinstance(doc[name], dict) and "properties" in sub \
                    and sub.get("additionalProperties") is False:
                extra = set(doc[name]) - set(sub["properties"])
                if extra:
                    problems.append({"check": "schema_fields", "riwayah": key,
                                     "detail": f"{name} has fields not in the "
                                               f"schema: {sorted(extra)}"})
    return problems
