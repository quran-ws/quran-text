"""Write the flat index and its companion tables to ``out/``."""

from __future__ import annotations

import csv
import gzip
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from .build import ORDER, OUT, Word, fawasil
from .sources import Riwaya
from .suras import names

SCHEMA_VERSION = "2.1"


def _riwaya_meta(riwayat: list[Riwaya]) -> list[dict]:
    return [{
        "key": r.key,
        "name_en": r.name_en,
        "name_ar": r.name_ar,
        "qari_en": r.qari_en,
        "qari_ar": r.qari_ar,
        "counting": r.counting,
        "ayah_count": sum(1 for a in r.ayat if a.aya > 0),
        "source": r.source,
        "crosscheck_source": r.crosscheck_source,
    } for r in riwayat]


def _groups(w: Word) -> list[dict]:
    """The distinct spellings of one word, each with the riwāyāt that use it.

    Ordered by :data:`ORDER`, so the first group is the one Ḥafṣ belongs to
    wherever Ḥafṣ has the word.
    """
    seen: dict[str, list[str]] = {}
    for k in ORDER:
        if k in w.forms:
            seen.setdefault(w.forms[k], []).append(k)
    return [{"text": t, "riwayat": ks} for t, ks in seen.items()]


def _word_json(w: Word) -> dict:
    """One word.

    ``forms`` always lists every riwāyah that has the word, so a consumer never
    has to fall back to another record to resolve a spelling.  ``groups`` says
    the same thing the other way round — one entry per *distinct* spelling —
    and appears only when there is more than one, so its presence is itself the
    signal that the riwāyāt part company here.
    """
    rec = {
        "id": w.id,
        "slot_id": w.id,
        "i": w.index,
        "key": w.key,
        "rasm": w.rasm,
        "pointed": w.pointed,
        "uthmani": w.uthmani,
        "simple": w.simple,
        "status": w.status,
        "aya": w.aya,
        "position": w.position,
        "forms": w.forms,
    }
    groups = _groups(w)
    if len(groups) > 1:
        rec["groups"] = groups
    if w.missing:
        rec["missing"] = w.missing
    if w.waqf:
        rec["waqf"] = w.waqf
    if w.boundary:
        rec["boundary"] = w.boundary
    if w.hizb:
        rec["hizb"] = w.hizb
    if w.sajdah:
        rec["sajdah"] = w.sajdah
    return rec


def write_all(words: list[Word], riwayat: list[Riwaya]) -> dict:
    OUT.mkdir(exist_ok=True)
    (OUT / "suras").mkdir(exist_ok=True)

    by_sura: dict[int, list[Word]] = defaultdict(list)
    for w in words:
        by_sura[w.sura].append(w)

    meta = {
        "schema_version": SCHEMA_VERSION,
        "generated": date.today().isoformat(),
        "word_count": len(words),
        "slot_count": len(words),
        "sura_count": len(by_sura),
        "riwayat": _riwaya_meta(riwayat),
        "model": (
            "A sūrah is a flat list of shared slots. `slot_id` is the explicit "
            "name of the cross-riwāyah coordinate and `id` is its compatibility "
            "alias. `position` gives each present token's dense ordinal in its "
            "own muṣḥaf, so an absent token leaves a slot gap but no position "
            "gap. How each riwāyah spells the token is in `forms`; rare unequal "
            "wordings are inventoried as alignment spans in slot-model.json; "
            "fawāṣil remain a layer over the slots in fawasil.json."
        ),
    }

    # --- per-sūrah files --------------------------------------------------
    index = []
    for sura, ws in sorted(by_sura.items()):
        info = names()[sura]
        doc = {
            "sura": sura,
            **info,
            "word_count": len(ws),
            "first_word_id": ws[0].id,
            "last_word_id": ws[-1].id,
            "ayah_count": {r.key: max((w.aya.get(r.key, 0) for w in ws), default=0)
                           for r in riwayat},
            "words": [_word_json(w) for w in ws],
        }
        (OUT / "suras" / f"{sura:03d}.json").write_text(
            json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        index.append({k: v for k, v in doc.items() if k != "words"})

    # The whole corpus in one file.  Gzipped: it is 36 MB of largely repetitive
    # JSON, and every consumer that wants it can decompress in one line.
    whole = json.dumps({**meta, "suras": [
        {"sura": s, **names()[s], "words": [_word_json(w) for w in ws]}
        for s, ws in sorted(by_sura.items())]}, ensure_ascii=False)
    with gzip.open(OUT / "quran-words.json.gz", "wt", encoding="utf-8",
                   compresslevel=9) as fh:
        fh.write(whole)

    (OUT / "index.json").write_text(
        json.dumps({**meta, "suras": index}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    # --- flat word table --------------------------------------------------
    keys = [r.key for r in riwayat]
    with (OUT / "words.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["word_id", "sura", "word_index", "key", "rasm", "pointed",
                     "uthmani", "simple", "status", "present_count"]
                    + [f"aya_{k}" for k in keys] + [f"form_{k}" for k in keys]
                    + ["slot_id"] + [f"position_{k}" for k in keys])
        for w in words:
            wr.writerow([w.id, w.sura, w.index, w.key, w.rasm, w.pointed,
                         w.uthmani, w.simple, w.status, len(w.present)]
                        + [w.aya.get(k, "") for k in keys]
                        + [w.forms.get(k, "") for k in keys]
                        + [w.id] + [w.position.get(k, "") for k in keys])

    # --- variants: only where a riwāyah departs from the canonical form ----
    with (OUT / "variants.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["word_id", "sura", "word_index", "riwaya", "aya",
                     "canonical_uthmani", "riwaya_uthmani", "same_rasm", "status",
                     "slot_id", "position"])
        for w in words:
            for k in keys:
                form = w.forms.get(k)
                if form is None or form == w.uthmani:
                    continue
                wr.writerow([w.id, w.sura, w.index, k, w.aya.get(k, ""),
                             w.uthmani, form,
                             int(w.rasm == _rasm_of(w, k)), w.status,
                             w.id, w.position[k]])

    # --- conflicts / issues ------------------------------------------------
    flagged = [w for w in words
               if w.status in ("rasm_variant", "alif_variant", "partial",
                               "word_boundary")]
    with (OUT / "conflicts.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["word_id", "sura", "word_index", "aya_hafs", "status",
                     "rasm", "missing_in", "joined_in", "distinct_forms", "forms",
                     "slot_id", "positions"])
        for w in flagged:
            groups = _groups(w)
            wr.writerow([
                w.id, w.sura, w.index, w.aya.get("hafs", ""), w.status, w.rasm,
                "|".join(w.missing), "|".join(sorted(w.boundary)), len(groups),
                "  ||  ".join(f"{g['text']} [{','.join(g['riwayat'])}]"
                              for g in groups),
                w.id, "|".join(f"{k}:{w.position[k]}" for k in keys
                               if k in w.position),
            ])

    (OUT / "conflicts.json").write_text(
        json.dumps({"count": len(flagged),
                    "by_status": Counter(w.status for w in flagged),
                    "words": [_word_json(w) for w in flagged]},
                   ensure_ascii=False, indent=1), encoding="utf-8")

    # --- fawāṣil: the āyah boundaries, as a layer over the word index -------
    systems = fawasil(words)
    (OUT / "fawasil.json").write_text(
        json.dumps({
            "generated": date.today().isoformat(),
            "model": (
                "Each system lists the slot ID (legacy word ID) of the last "
                "word of every āyah, in "
                "order. The riwāyāt following one system agree on all of them."
            ),
            "systems": systems,
        }, ensure_ascii=False, indent=1), encoding="utf-8")

    # --- word-boundary events ----------------------------------------------
    with (OUT / "boundaries.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["word_ids", "sura", "aya_hafs", "kind", "riwayat",
                     "riwayat_agree", "forms", "slot_ids"])
        for event in boundary_events(words):
            wr.writerow([
                "|".join(str(i) for i in event["word_ids"]), event["sura"],
                event["aya"], event["kind"], "|".join(event["riwayat"]),
                int(event["agree"]),
                "  ||  ".join(f"{t} [{','.join(ks)}]"
                              for t, ks in event["texts"].items()),
                "|".join(str(i) for i in event["word_ids"]),
            ])
    return meta


def boundary_events(words: list[Word]) -> list[dict]:
    """Group boundary-flagged words into the events they belong to.

    A boundary disagreement is never about one word: it is about the space
    between two.  ``agree`` says whether the riwāyāt read the run identically
    once it has been re-segmented — which is how a source that merely lost a
    space is told apart from a muṣḥaf that really does print the words joined.
    """
    events: list[dict] = []
    run: list[Word] = []
    for w in words:
        if w.boundary and run and w.id == run[-1].id + 1:
            run.append(w)
            continue
        if run:
            events.append(_event(run))
        run = [w] if w.boundary else []
    if run:
        events.append(_event(run))
    return events


def _event(run: list[Word]) -> dict:
    texts: dict[str, list[str]] = defaultdict(list)
    for k in ORDER:
        parts = [w.forms[k] for w in run if k in w.forms]
        if parts:
            texts[" ".join(parts)].append(k)
    kinds = {kind for w in run for kind in w.boundary.values()}
    return {
        "word_ids": [w.id for w in run],
        "sura": run[0].sura,
        "aya": run[0].aya.get("hafs", next(iter(run[0].aya.values()), "")),
        "kind": "|".join(sorted(kinds)),
        "riwayat": sorted({k for w in run for k in w.boundary}),
        "agree": all(len({w.rasm} | {_rasm_of(w, k) for k in w.forms}) == 1
                     for w in run),
        "texts": dict(texts),
    }


def _rasm_of(w: Word, key: str) -> str:
    """Rasm of one riwāyah's form, recomputed from the stored spelling."""
    from .normalize import rasm
    form = w.forms.get(key)
    return rasm(form) if form else ""
