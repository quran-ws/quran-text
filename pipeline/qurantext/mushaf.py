"""Publish each muṣḥaf on its own, as words by position with layers over them.

``data/`` already answers *how do the muṣḥafs differ?*  It does not answer *give
me Warsh*: a consumer who wants one muṣḥaf has to take the comparison and
project it back out.  This module writes the other view — one self-contained
file per muṣḥaf.

**A muṣḥaf is an ordered array of word strings.  Everything else is a layer over
that array, addressed by position.**  ``words[i]`` is the *i*-th word of this
muṣḥaf; ``ayah_starts``, ``page_starts``, ``line_starts``, ``juz_starts`` and
``surah_starts`` are sorted lists of positions, so unit *k* of any layer is
``words[starts[k]:starts[k+1]]`` — a slice, correct in all seven files.

Two kinds of integer appear and are kept apart.  A **position** is an index
into ``words`` of *this* muṣḥaf; every key ending in ``_starts`` holds
positions, as do ``marks[][0]`` and ``resegmentation[].positions``.  A
**number** is the shared numbering that means the same word in all seven; only
the ``numbering`` block holds numbers.  A consumer who works in one muṣḥaf
never reads it.

Only ``data/mushaf/<key>.json`` and ``data/word-index.json`` are normative.  The
nested, CSV and SQLite forms in :mod:`qurantext.views` are generated from the
same build and are labelled views, so that whichever one turns out to
be most convenient cannot quietly become the standard.

Nothing here is asserted that the packages do not say.  Where a fact is derived
rather than read it is marked derived, where it is unavailable the field is
absent and the absence is explained, and where this build departs from the
source's own word spacing every instance is listed in the file itself.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from . import chars, counting, fonts, rasm_imlai
from . import paths, stamp
from .build import DATA, Word
from .word_index import boundary_events
from .sources import PACKAGES, RELEASE_POLICY, Riwayah
from .surahs import names

FORMAT = "quran-mushaf"
FORMAT_VERSION = "1.0"

MUSHAF_DIR = DATA / "mushaf"

#: Signs that can attach to a word, with the Unicode name of each.  Emitted in
#: every file so a consumer never has to hard-code a codepoint table.
MARK_NAMES = {
    "ۖ": "ARABIC SMALL HIGH LIGATURE SAD WITH LAM WITH ALEF MAKSURA",
    "ۗ": "ARABIC SMALL HIGH LIGATURE QAF WITH LAM WITH ALEF MAKSURA",
    "ۘ": "ARABIC SMALL HIGH MEEM INITIAL FORM",
    "ۙ": "ARABIC SMALL HIGH LAM ALEF",
    "ۚ": "ARABIC SMALL HIGH JEEM",
    "ۛ": "ARABIC SMALL HIGH THREE DOTS",
    "ۜ": "ARABIC SMALL HIGH SEEN",
    "۞": "ARABIC START OF RUB EL HIZB",
    "۩": "ARABIC PLACE OF SAJDAH",
    "ۤ": "ARABIC SMALL HIGH MADDA",
}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _provenance(r: Riwayah) -> dict:
    """Which KFGQPC release every part of this file came from.

    Recorded in the file itself and not only in the manifest, because a muṣḥaf
    file will be copied, mirrored and vendored on its own, and a text whose
    edition cannot be named is not a citable one.
    """
    spec = r.spec
    text = PACKAGES / f"{spec.primary_zip}.zip"
    out = {
        "text": {
            "package": text.name,
            "member": spec.primary_member,
            "release_year": spec.primary_year,
            "sha256": _sha256(text),
        },
        "policy": RELEASE_POLICY,
    }
    if spec.csv_zip:
        layout = PACKAGES / f"{spec.csv_zip}.zip"
        out["layout"] = {
            "package": layout.name,
            "member": spec.csv_member,
            "release_year": spec.csv_year,
            "sha256": _sha256(layout),
            "used_for": ["juz", "line_check"],
        }
    return out


def _marks(w: Word, key: str) -> list[dict]:
    """Every sign printed against this word, with the side it sits on."""
    out = []
    if key in w.division:
        out.append({"kind": "division", "side": "before", "sign": "۞"})
    for sign in w.waqf.get(key, ""):
        if sign == "۩":
            continue                       # emitted below, as its own kind
        out.append({"kind": "waqf", "side": "after", "sign": sign})
    # Order matters: where a word carries both — ``يَسۡجُدُونَۤ۩`` at 7:206 and
    # 84:21 — the release writes the line inside the sign, and re-attaching the
    # marks in the order emitted has to reproduce the printed token.
    if key in w.sajdah_line:
        out.append({"kind": "sajdah_line", "side": "after",
                    "sign": chars.SAJDAH_LINE})
    if key in w.sajdah:
        out.append({"kind": "sajdah", "side": "after", "sign": "۩"})
    return out


def _starts(values: list) -> list[int]:
    """Positions at which a per-position value changes — one per unit."""
    out: list[int] = []
    prev = object()
    for i, v in enumerate(values):
        if v != prev:
            out.append(i)
            prev = v
    return out


class Printed:
    """One printed word of one muṣḥaf: its position, and the numbers it covers.

    Almost every printed word covers one number.  At 72:16 and 73:20 a muṣḥaf
    that writes ``وَأَلَّوِ`` or ``أَلَّن`` as one word covers two.  ``word`` is the
    :class:`Word` of the first number, which carries the text, the āyah and
    the place; the covered numbers carry the same token and add nothing.
    """

    __slots__ = ("position", "first", "last", "word")

    def __init__(self, position: int, word: Word):
        self.position = position
        self.first = self.last = word.id
        self.word = word


def printed_words(words: list[Word], key: str) -> tuple[list[Printed], list[int]]:
    """Walk the numbering and return this muṣḥaf's printed words and its gaps."""
    printed: list[Printed] = []
    missing: list[int] = []
    for w in words:
        if key not in w.forms:
            missing.append(w.id)
        elif key in w.continuation:
            printed[-1].last = w.id
        else:
            printed.append(Printed(len(printed), w))
    return printed, missing


def numbering(printed: list[Printed], missing: list[int], total: int) -> dict:
    """How this muṣḥaf's positions map onto the shared numbering.

    ``missing`` lists the numbers this muṣḥaf does not read — the only way a
    number can fail to be covered.  ``written_joined`` lists the printed words
    that cover more than one number — the only way a position can cover more
    than one.  Everything else is one word, one number, in step, and is not
    stored.  See ``docs/format.md``, *Numbering*, for the invariants.
    """
    return {
        "total": total,
        "missing": missing,
        "written_joined": [{"position": p.position, "numbers": [p.first, p.last]}
                           for p in printed if p.last > p.first],
    }


def numbers_of(doc: dict) -> list[tuple[int, int]]:
    """position -> ``(first, last)`` run of shared numbers, for a published file.

    The one-pass walk the spec describes: advance one per word, skip
    ``missing``, advance by the run length at a ``written_joined`` position.
    Raises ``AssertionError`` where the block does not tile ``1 … total``.
    """
    key = doc["mushaf"]["key"]
    block = doc["numbering"]
    missing = set(block["missing"])
    joined = {j["position"]: j["numbers"] for j in block["written_joined"]}
    runs, n = [], 1
    for position in range(len(doc["words"])):
        while n in missing:
            n += 1
        first, last = joined.get(position, (n, n))
        if first != n:
            raise AssertionError(f"{key}: run at {position} starts {first}, expected {n}")
        if last < first:
            raise AssertionError(f"{key}: run at {position} is empty")
        runs.append((first, last))
        n = last + 1
    while n in missing:
        n += 1
    if n != block["total"] + 1:
        raise AssertionError(f"{key}: runs and missing do not tile 1…total")
    return runs


def _surahs(key: str, printed: list[Printed], ayah_starts: list[int],
           r: Riwayah) -> list[dict]:
    """The 114-row sūrah header, in full, in every muṣḥaf's own file.

    Duplicated across the seven rather than shared, because a file that needs a
    second download before it can name a sūrah is not a muṣḥaf that ships alone.
    It costs 114 rows against 77,000 words.
    """
    basmalah_printed = {a.surah for a in r.ayahs if a.ayah == 0} | {1}
    by_surah: dict[int, list[Printed]] = defaultdict(list)
    for p in printed:
        by_surah[p.word.surah].append(p)
    first_ayah_of: dict[int, int] = {}
    for k, position in enumerate(ayah_starts):
        first_ayah_of.setdefault(printed[position].word.surah, k)

    out = []
    for surah, ps in sorted(by_surah.items()):
        info = names()[surah]
        out.append({
            "number": surah,
            "name_ar": info["name_ar"],
            "name_en": info["name_en"],
            "revelation": info["revelation"],
            "has_basmalah": surah in basmalah_printed,
            "ayah_count": max(p.word.ayah.get(key, 0) for p in ps),
            "first_ayah": first_ayah_of[surah],
        })
    return out


def _resegmentation(key: str, words: list[Word], at: dict[int, int]) -> list[dict]:
    """Every place this build changed the source's own word spacing.

    A shared numbering is only stable because the alignment occasionally
    overrides a package's spacing — splitting what one source printed joined —
    so a file claiming to *be* that muṣḥaf has to say where it did so.  The
    list is present even when empty, so silence is never ambiguous.

    A word a muṣḥaf *really* prints joined — ``written_joined`` in
    ``numbering`` — is not here: that is a fact about the muṣḥaf, not a
    departure from it.
    """
    out = []
    for event in boundary_events(words):
        if key not in event["riwayahs"]:
            continue
        ids = event["word_ids"]
        mine = [w for w in words if w.id in set(ids) and key in w.forms]
        source = next((t for t, ks in event["texts"].items() if key in ks), "")
        out.append({
            "positions": sorted({at[i] for i in ids if i in at}),
            "surah": event["surah"],
            "ayah": event["ayah"],
            "kind": event["kind"],
            "source_text": source,
            "emitted": [w.forms[key] for w in mine],
            "riwayahs_agree": event["agree"],
        })
    return out


def _line_check(key: str, printed: list[Printed], r: Riwayah) -> dict:
    """Re-check the reconstructed lines against the release that states them.

    The page is read from the document; the line is inferred from its flow (see
    :mod:`qurantext.layout`).  The v2 CSV states the line of every āyah, so the
    inference can be scored rather than merely asserted — and the āyāt it gets
    wrong are listed, so a consumer can exclude them instead of discovering them.

    Bazzī has no v2 release, so it is not scored here.  That is a gap in the
    *check*, not in the data: its lines are identical, word for word, to Ḥafṣ's
    (``docs/known-issues.md`` §6), so they carry Ḥafṣ's accuracy.
    """
    if not r.meta:
        return {"validated": False,
                "reason": "no v2 package released for this riwāyah"}

    by_ayah: dict[tuple[int, int], list[Word]] = defaultdict(list)
    for p in printed:
        by_ayah[(p.word.surah, p.word.ayah[key])].append(p.word)

    checked = agreed = 0
    wrong = []
    for k, meta in r.meta.items():
        ws = by_ayah.get(k)
        if not ws or not meta["line_end"].isdigit():
            continue
        checked += 1
        got = max(w.place[key][1] for w in ws if key in w.place)
        want = int(meta["line_end"])
        if got == want:
            agreed += 1
        else:
            wrong.append({"surah": k[0], "ayah": k[1], "derived": got, "source": want})
    return {
        "validated": True,
        "against": r.crosscheck_source,
        "ayahs_checked": checked,
        "ayahs_agreeing": agreed,
        "disagreements": wrong,
    }


def _layers(r: Riwayah, line_check: dict, has_juz: bool) -> dict:
    """What this file carries, and why it lacks whatever it lacks."""
    present = ["surahs", "ayahs", "pages", "lines", "marks"]
    absent: dict[str, str] = {}
    if has_juz:
        present.append("juz")
    else:
        absent["juz"] = "no v2 package released for this riwāyah"
    absent["rasm_imlai"] = "column not present in this riwāyah's release"

    return {
        "present": present,
        "absent": absent,
        "derived": {
            "line": {
                "how": "reconstructed from the document's line breaks, "
                       "paragraph boundaries and sūrah headings; printed lines "
                       "are not encoded in the release",
                **{k: v for k, v in line_check.items() if k != "disagreements"},
            },
        },
        "notes": {
            "page": "read from explicit page breaks in the release, not inferred",
            "waqf": "waqf-mark conventions differ by muṣḥaf and are not "
                    "comparable across them: Warsh and Qālūn print one general "
                    "sign where Ḥafṣ, Dūrī and Sūsī print seven distinct ones",
            "division": "the ۞ symbol is emitted exactly as the release prints it. "
                    "The releases disagree about how often to print it — 199 "
                    "times in Ḥafṣ, Shuʿbah and Bazzī against 433–437 in the "
                    "others — and nothing here reconciles them",
        },
    }


def _juz_per_position(printed: list[Printed], key: str, r: Riwayah) -> list[int] | None:
    """The juz of every printed word, from the v2 CSV, or ``None`` without one.

    The CSV is per numbered āyah.  The unnumbered basmalah of Al-Fātiḥah has no
    row, so its words take the juz of the āyah that follows them.
    """
    if not r.meta:
        return None
    out: list[int | None] = []
    for p in printed:
        meta = r.meta.get((p.word.surah, p.word.ayah[key]))
        jozz = meta["jozz"] if meta and meta["jozz"].isdigit() else None
        out.append(int(jozz) if jozz else None)
    for i in range(len(out) - 2, -1, -1):        # fill gaps from the right
        if out[i] is None:
            out[i] = out[i + 1]
    for i in range(1, len(out)):                  # then from the left
        if out[i] is None:
            out[i] = out[i - 1]
    return out                                    # type: ignore[return-value]


def document(words: list[Word], r: Riwayah,
             rasm_imlai: dict[int, str] | None = None) -> dict:
    """The whole of one muṣḥaf, in the canonical shape.

    The ``counting`` block is filled in by :func:`qurantext.counting.derive`
    once the file's own āyah layer exists, since it is derived from it.
    """
    key = r.key
    printed, missing = printed_words(words, key)
    at = {}                                      # number -> position
    for p in printed:
        for n in range(p.first, p.last + 1):
            at[n] = p.position

    line_check = _line_check(key, printed, r)
    ayahs = [(p.word.surah, p.word.ayah[key]) for p in printed]
    ayah_starts = [i for i in _starts(ayahs) if ayahs[i][1] > 0]
    surah_starts = _starts([p.word.surah for p in printed])
    places = [p.word.place.get(key) for p in printed]
    page_starts = _starts([pl[0] for pl in places]) if all(places) else None
    line_starts = _starts([pl for pl in places]) if all(places) else None
    juz = _juz_per_position(printed, key, r)

    mark_types: list[dict] = []
    type_index: dict[tuple, int] = {}
    marks: list[list[int]] = []
    for p in printed:
        for m in _marks(p.word, key):
            sig = (m["kind"], m["side"], m["sign"])
            if sig not in type_index:
                type_index[sig] = len(mark_types)
                mark_types.append(m)
            marks.append([p.position, type_index[sig]])

    doc = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "generated": stamp.generated(),
        "mushaf": {
            "key": key,
            "name_en": r.name_en,
            "name_ar": r.name_ar,
            "qiraah_en": r.qiraah_en,
            "qiraah_ar": r.qiraah_ar,
            "word_count": len(printed),
        },
        "counting": None,
        "provenance": _provenance(r),
        "font": fonts.describe(r.spec),
        "layers": _layers(r, line_check, juz is not None),
        "words": [p.word.forms[key] for p in printed],
        "rasm_imlai": ([rasm_imlai.get(p.first, rasm_imlai.get(p.last)) for p in printed]
                   if rasm_imlai else None),
        "numbering": numbering(printed, missing, words[-1].id),
        "surah_starts": surah_starts,
        "ayah_starts": ayah_starts,
        "page_starts": page_starts,
        "line_starts": line_starts,
        "juz_starts": _starts(juz) if juz else None,
        "surahs": _surahs(key, printed, ayah_starts, r),
        "marks": marks,
        "mark_types": mark_types,
        "mark_signs": {s: {"cp": f"U+{ord(s):04X}", "unicode_name": n}
                       for s, n in MARK_NAMES.items()},
        "resegmentation": _resegmentation(key, words, at),
        "line_disagreements": line_check.get("disagreements", []),
    }
    for layer in ("page_starts", "line_starts", "juz_starts"):
        if doc[layer] is None:
            del doc[layer]
    return doc


def _dump(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1),
                    encoding="utf-8")


def write_mushafs(words: list[Word], riwayahs: list[Riwayah]) -> dict[str, dict]:
    """Write every muṣḥaf's own file, and return the documents by key.

    Imlāʾī is derived here for whichever release supplies it, and the
    ``counting`` block once the file's own āyah layer exists.
    """
    MUSHAF_DIR.mkdir(parents=True, exist_ok=True)
    for stale in MUSHAF_DIR.glob("*.min.json"):
        stale.unlink()
    docs = {}
    for r in riwayahs:
        mapping, report = rasm_imlai.derive(words, r)
        doc = document(words, r, mapping if report.get("available") else None)
        if report.get("available"):
            doc["layers"]["derived"]["rasm_imlai"] = report
            doc["layers"]["present"].append("rasm_imlai")
            doc["layers"]["absent"].pop("rasm_imlai", None)
        doc["counting"] = counting.derive(doc, words)
        _dump(MUSHAF_DIR / f"{r.key}.json", doc)
        docs[r.key] = doc
    return docs


def write_manifest(docs: dict[str, dict]) -> dict:
    """Every emitted file and every source package, each with its SHA-256.

    A dataset becomes citable when a reader can prove which release a file came
    from without trusting the person who published it.  The manifest is that
    proof: the source hashes let anyone re-derive the build, and the output
    hashes let anyone check that the copy they hold is the one described here.
    """
    files = sorted(p for p in DATA.rglob("*")
                   if p.is_file() and p.name != "manifest.json")

    manifest = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "generated": stamp.generated(),
        "normative": [f"data/mushaf/{k}.json" for k in docs]
                     + ["data/word-index.json", "data/word-index.csv"],
        "note": "Only the files listed under `normative` define the format. "
                "Everything else is a generated view of them.",
        "sources": {
            **{k: {n: {kk: vv for kk, vv in part.items() if kk != "used_for"}
                   for n, part in doc["provenance"].items()
                   if isinstance(part, dict)}
               for k, doc in docs.items()},
            "qiraat-ayah-map": counting.provenance(),
        },
        "files": [
            {"path": p.relative_to(paths.ROOT).as_posix(),
             "bytes": p.stat().st_size,
             "sha256": _sha256(p)}
            for p in files
        ],
    }
    _dump(DATA / "manifest.json", manifest)
    return manifest
