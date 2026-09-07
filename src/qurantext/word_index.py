"""The word index: every number of the shared numbering, with a text and who reads it.

The numbering counts the finest division of the text any of the seven muṣḥafs
prints, so it is a division nobody prints and no muṣḥaf file can stand in for
it.  This file is where a number gets a text.  The muṣḥaf files are where a
text gets a position.  Neither is derivable from the other alone, so both are
normative.

Every number carries its Ḥafṣ coordinates ``{surah, ayah, position}`` in the Kūfī
count, because almost every existing word-level dataset — the corpus.quran.com
morphology, quran.com's word audio segments, word by word translations — is
keyed that way, and this column is what lets them attach in one lookup.  At
72:16 two numbers carry the same coordinates, which is the honest statement
that Ḥafṣ writes them as one word.

``differences.json`` beside it is the same records filtered to the words where
the riwāyāt actually disagree.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import date

from .align import WRITTEN_JOINED
from .build import ORDER, OUT, Word

FORMAT = "quran-word-index"
FORMAT_VERSION = "1.0"

#: The statuses that mean the riwāyāt part company on more than vowelling.
DIFFERENCE_STATUSES = ("rasm_variant", "alif_variant", "partial", "word_boundary")


def hafs_coordinates(words: list[Word]) -> dict[int, dict]:
    """number -> ``{surah, ayah, position}`` in Ḥafṣ, where it has the word.

    The position counts *printed* words: a number Ḥafṣ covers with the same
    printed word as the number before it takes that word's position.
    """
    out: dict[int, dict] = {}
    position = 0
    at: tuple[int, int] | None = None
    for w in words:
        if "hafs" not in w.forms:
            continue
        if "hafs" in w.continuation:
            out[w.id] = out[w.id - 1]
            continue
        here = (w.surah, w.ayah["hafs"])
        if here != at:
            at, position = here, 0
        position += 1
        out[w.id] = {"surah": w.surah, "ayah": w.ayah["hafs"], "position": position}
    return out


def groups(w: Word) -> list[dict]:
    """The distinct spellings of one word, each with the riwāyāt that use it.

    Ordered by :data:`ORDER`, so the first group is the one Ḥafṣ belongs to
    wherever Ḥafṣ has the word.
    """
    seen: dict[str, list[str]] = {}
    for k in ORDER:
        if k in w.forms:
            seen.setdefault(w.forms[k], []).append(k)
    return [{"text": t, "riwayahs": ks} for t, ks in seen.items()]


def word_record(w: Word, hafs: dict[int, dict]) -> dict:
    """One number of the index.

    ``forms`` always lists every riwāyah that has the word, so a consumer never
    has to fall back to another record to resolve a spelling.  ``groups`` says
    the same thing the other way round — one entry per *distinct* spelling —
    and appears only when there is more than one, so its presence is itself the
    signal that the riwāyāt part company here.  Optional fields are omitted
    when empty.
    """
    rec = {
        "number": w.id,
        "surah": w.surah,
        "index": w.index,
        "key": w.key,
        "rasm": w.rasm,
        "pointed": w.pointed,
        "rasm_uthmani": w.rasm_uthmani,
        "plain": w.plain,
        "status": w.status,
        "hafs": hafs.get(w.id),
        "ayah": {k: w.ayah[k] for k in ORDER if k in w.ayah},
        "forms": {k: w.forms[k] for k in ORDER if k in w.forms},
    }
    spellings = groups(w)
    if len(spellings) > 1:
        rec["groups"] = spellings
    if w.missing:
        rec["missing"] = w.missing
    joined = [k for k in ORDER if w.boundary.get(k) == WRITTEN_JOINED]
    if joined:
        rec["written_joined"] = joined
    resegmented = {k: v for k, v in w.boundary.items() if v != WRITTEN_JOINED}
    if resegmented:
        rec["resegmented"] = resegmented
    if w.waqf:
        rec["waqf"] = w.waqf
    if w.division:
        rec["division"] = w.division
    if w.sajdah:
        rec["sajdah"] = w.sajdah
    return rec


def _write_records(path, head: dict, records: list[dict]) -> None:
    """One record per line: readable in an editor and diffable by git, without
    the 3× cost of indenting 77,000 small objects."""
    with path.open("w", encoding="utf-8") as fh:
        text = json.dumps(head, ensure_ascii=False, indent=1)
        fh.write(text[:-2] + ',\n "words": [\n')
        fh.write(",\n".join("  " + json.dumps(r, ensure_ascii=False, separators=(",", ":"))
                            for r in records))
        fh.write("\n ]\n}\n")


CSV_COLUMNS = (["number", "surah", "index", "key", "rasm", "pointed", "rasm_uthmani",
                "plain", "status", "hafs_surah", "hafs_ayah", "hafs_position",
                "missing", "written_joined"]
               + [f"ayah_{k}" for k in ORDER] + [f"form_{k}" for k in ORDER])


def _csv_row(w: Word, hafs: dict[int, dict]) -> list:
    h = hafs.get(w.id)
    return ([w.id, w.surah, w.index, w.key, w.rasm, w.pointed, w.rasm_uthmani, w.plain,
             w.status, *((h["surah"], h["ayah"], h["position"]) if h else ("", "", "")),
             "|".join(w.missing),
             "|".join(k for k in ORDER if w.boundary.get(k) == WRITTEN_JOINED)]
            + [w.ayah.get(k, "") for k in ORDER]
            + [w.forms.get(k, "") for k in ORDER])


def write_word_index(words: list[Word]) -> dict:
    """Write ``out/word-index.json`` and ``out/word-index.csv``; return the document."""
    hafs = hafs_coordinates(words)
    doc = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "generated": date.today().isoformat(),
        "total": words[-1].id,
        "mushafs": ORDER,
        "note": "`number` is the shared number, dense 1 … total, the same "
                "integer every muṣḥaf file maps its positions onto. `forms[key]` "
                "is absent where that muṣḥaf does not read the word; where a "
                "muṣḥaf writes the number joined with its neighbour the form is "
                "the joined word, repeated on both numbers, and `written_joined` "
                "names those muṣḥafs. `hafs` is the word's sūrah, āyah and "
                "position in the āyah in the Kūfī count, null where Ḥafṣ lacks it.",
        "words": [word_record(w, hafs) for w in words],
    }
    _write_records(OUT / "word-index.json", {k: v for k, v in doc.items() if k != "words"},
                   doc["words"])
    with (OUT / "word-index.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(CSV_COLUMNS)
        for w in words:
            wr.writerow(_csv_row(w, hafs))
    return doc


def write_differences(words: list[Word]) -> dict:
    """``out/differences.json`` and ``.csv``: only the numbers where the
    riwāyāt disagree about the letters, the ā, a word's presence, or its
    boundary — the same records as the word index, filtered."""
    hafs = hafs_coordinates(words)
    flagged = [w for w in words if w.status in DIFFERENCE_STATUSES]
    doc = {
        "format": "quran-differences",
        "format_version": FORMAT_VERSION,
        "generated": date.today().isoformat(),
        "count": len(flagged),
        "by_status": dict(Counter(w.status for w in flagged)),
        "note": "The word-index records whose status is one of "
                + ", ".join(DIFFERENCE_STATUSES)
                + ". Vowelling and pointing differences are in the word index "
                  "itself, under `groups`.",
        "words": [word_record(w, hafs) for w in flagged],
    }
    _write_records(OUT / "differences.json", {k: v for k, v in doc.items() if k != "words"},
                   doc["words"])
    with (OUT / "differences.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["number", "surah", "index", "ayah_hafs", "status", "rasm",
                     "missing_in", "written_joined_by", "resegmented_in",
                     "distinct_forms", "forms"])
        for w in flagged:
            spellings = groups(w)
            wr.writerow([
                w.id, w.surah, w.index, w.ayah.get("hafs", ""), w.status, w.rasm,
                "|".join(w.missing),
                "|".join(k for k in ORDER if w.boundary.get(k) == WRITTEN_JOINED),
                "|".join(k for k in ORDER if w.boundary.get(k) not in (None, WRITTEN_JOINED)),
                len(spellings),
                "  ||  ".join(f"{g['text']} [{','.join(g['riwayahs'])}]" for g in spellings),
            ])
    return doc


# --------------------------------------------------------------------------
# word-boundary events (shared by the muṣḥaf files and the reports)
# --------------------------------------------------------------------------

def boundary_events(words: list[Word]) -> list[dict]:
    """Group boundary-flagged words into the events they belong to.

    A boundary disagreement is never about one word: it is about the space
    between two.  ``agree`` says whether the riwāyāt read the run identically
    once it has been re-segmented — which is how a source that merely lost a
    space is told apart from a muṣḥaf that really does print the words joined.

    A *declared* joined word (``written_joined``) is not an event here: it is
    the muṣḥaf's own rasm, carried in ``numbering`` and the word index,
    not a departure this build made from it.
    """
    def resegmented(w: Word) -> bool:
        return any(v != WRITTEN_JOINED for v in w.boundary.values())

    events: list[dict] = []
    run: list[Word] = []
    for w in words:
        if resegmented(w) and run and w.id == run[-1].id + 1:
            run.append(w)
            continue
        if run:
            events.append(_event(run))
        run = [w] if resegmented(w) else []
    if run:
        events.append(_event(run))
    return events


def _event(run: list[Word]) -> dict:
    texts: dict[str, list[str]] = defaultdict(list)
    for k in ORDER:
        parts = [w.forms[k] for w in run if k in w.forms and k not in w.continuation]
        if parts:
            texts[" ".join(parts)].append(k)
    kinds = {kind for w in run for kind in w.boundary.values()} - {WRITTEN_JOINED}
    return {
        "word_ids": [w.id for w in run],
        "surah": run[0].surah,
        "ayah": run[0].ayah.get("hafs", next(iter(run[0].ayah.values()), "")),
        "kind": "|".join(sorted(kinds)),
        "riwayahs": sorted({k for w in run for k, v in w.boundary.items()
                           if v != WRITTEN_JOINED}),
        "agree": all(len({w.rasm} | {rasm_of(w, k) for k in w.forms}) == 1
                     for w in run),
        "texts": dict(texts),
    }


def rasm_of(w: Word, key: str) -> str:
    """Rasm of one riwāyah's form, recomputed from the stored spelling."""
    from .normalize import rasm
    form = w.forms.get(key)
    return rasm(form) if form else ""
