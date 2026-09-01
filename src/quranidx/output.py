"""Write the flat index and its companion tables to ``out/``."""

from __future__ import annotations

import csv
import gzip
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from .build import ORDER, OUT, Kalimah, fasilahs
from .sources import Riwayah
from .surahs import names

SCHEMA_VERSION = "3.0"


def _riwayah_meta(riwayahs: list[Riwayah]) -> list[dict]:
    return [{
        "key": r.key,
        "name_en": r.name_en,
        "name_ar": r.name_ar,
        "qari_en": r.qari_en,
        "qari_ar": r.qari_ar,
        "counting": r.counting,
        "ayah_count": sum(1 for a in r.ayahs if a.ayah > 0),
        "source": r.source,
        "crosscheck_source": r.crosscheck_source,
    } for r in riwayahs]


def _groups(w: Kalimah) -> list[dict]:
    """The distinct spellings of one kalimah, each with the riwayahs that use it.

    Ordered by :data:`ORDER`, so the first group is the one Ḥafṣ belongs to
    wherever Ḥafṣ has the kalimah.
    """
    seen: dict[str, list[str]] = {}
    for k in ORDER:
        if k in w.forms:
            seen.setdefault(w.forms[k], []).append(k)
    return [{"text": t, "riwayahs": ks} for t, ks in seen.items()]


def _kalimah_json(w: Kalimah) -> dict:
    """One kalimah.

    ``forms`` always lists every riwayah that has the kalimah, so a consumer never
    has to fall back to another record to resolve a spelling.  ``groups`` says
    the same thing the other way round — one entry per *distinct* spelling —
    and appears only when there is more than one, so its presence is itself the
    signal that the riwayahs part company here.
    """
    rec = {
        "id": w.id,
        "i": w.index,
        "key": w.key,
        "rasm": w.rasm,
        "pointed": w.pointed,
        "uthmani": w.uthmani,
        "simple": w.simple,
        "status": w.status,
        "ayah": w.ayah,
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


def write_all(kalimahs: list[Kalimah], riwayahs: list[Riwayah]) -> dict:
    OUT.mkdir(exist_ok=True)
    (OUT / "surahs").mkdir(exist_ok=True)

    by_surah: dict[int, list[Kalimah]] = defaultdict(list)
    for w in kalimahs:
        by_surah[w.surah].append(w)

    meta = {
        "schema_version": SCHEMA_VERSION,
        "generated": date.today().isoformat(),
        "kalimah_count": len(kalimahs),
        "surah_count": len(by_surah),
        "riwayahs": _riwayah_meta(riwayahs),
        "model": (
            "A surah is a flat list of kalimahs.  One ID means one kalimah in every "
            "riwayah that has it, because kalimahs are identified by their bare "
            "Uthmani rasm — undotted, unvowelled, no hamza — which is what "
            "the seven riwayahs actually share.  How each riwayah spells that "
            "kalimah is in `forms`; where each counting tradition ends its ayahs "
            "is in `fasilahs.json`."
        ),
    }

    # --- per-surah files --------------------------------------------------
    index = []
    for surah, ws in sorted(by_surah.items()):
        info = names()[surah]
        doc = {
            "surah": surah,
            **info,
            "kalimah_count": len(ws),
            "first_kalimah_id": ws[0].id,
            "last_kalimah_id": ws[-1].id,
            "ayah_count": {r.key: max((w.ayah.get(r.key, 0) for w in ws), default=0)
                           for r in riwayahs},
            "kalimahs": [_kalimah_json(w) for w in ws],
        }
        (OUT / "surahs" / f"{surah:03d}.json").write_text(
            json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        index.append({k: v for k, v in doc.items() if k != "kalimahs"})

    # The whole corpus in one file.  Gzipped: it is 36 MB of largely repetitive
    # JSON, and every consumer that wants it can decompress in one line.
    whole = json.dumps({**meta, "surahs": [
        {"surah": s, **names()[s], "kalimahs": [_kalimah_json(w) for w in ws]}
        for s, ws in sorted(by_surah.items())]}, ensure_ascii=False)
    with gzip.open(OUT / "quran-kalimahs.json.gz", "wt", encoding="utf-8",
                   compresslevel=9) as fh:
        fh.write(whole)

    (OUT / "index.json").write_text(
        json.dumps({**meta, "surahs": index}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    # --- flat kalimah table --------------------------------------------------
    keys = [r.key for r in riwayahs]
    with (OUT / "kalimahs.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kalimah_id", "surah", "kalimah_index", "key", "rasm", "pointed",
                     "uthmani", "simple", "status", "present_count"]
                    + [f"ayah_{k}" for k in keys] + [f"form_{k}" for k in keys])
        for w in kalimahs:
            wr.writerow([w.id, w.surah, w.index, w.key, w.rasm, w.pointed,
                         w.uthmani, w.simple, w.status, len(w.present)]
                        + [w.ayah.get(k, "") for k in keys]
                        + [w.forms.get(k, "") for k in keys])

    # --- variants: only where a riwayah departs from the canonical form ----
    with (OUT / "variants.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kalimah_id", "surah", "kalimah_index", "riwayah", "ayah",
                     "canonical_uthmani", "riwayah_uthmani", "same_rasm", "status"])
        for w in kalimahs:
            for k in keys:
                form = w.forms.get(k)
                if form is None or form == w.uthmani:
                    continue
                wr.writerow([w.id, w.surah, w.index, k, w.ayah.get(k, ""),
                             w.uthmani, form,
                             int(w.rasm == _rasm_of(w, k)), w.status])

    # --- conflicts / issues ------------------------------------------------
    flagged = [w for w in kalimahs
               if w.status in ("rasm_variant", "alif_variant", "partial",
                               "kalimah_boundary")]
    with (OUT / "conflicts.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kalimah_id", "surah", "kalimah_index", "ayah_hafs", "status",
                     "rasm", "missing_in", "joined_in", "distinct_forms", "forms"])
        for w in flagged:
            groups = _groups(w)
            wr.writerow([
                w.id, w.surah, w.index, w.ayah.get("hafs", ""), w.status, w.rasm,
                "|".join(w.missing), "|".join(sorted(w.boundary)), len(groups),
                "  ||  ".join(f"{g['text']} [{','.join(g['riwayahs'])}]"
                              for g in groups),
            ])

    (OUT / "conflicts.json").write_text(
        json.dumps({"count": len(flagged),
                    "by_status": Counter(w.status for w in flagged),
                    "kalimahs": [_kalimah_json(w) for w in flagged]},
                   ensure_ascii=False, indent=1), encoding="utf-8")

    # --- fasilahs: the ayah boundaries, as a layer over the kalimah index -------
    systems = fasilahs(kalimahs)
    (OUT / "fasilahs.json").write_text(
        json.dumps({
            "generated": date.today().isoformat(),
            "model": (
                "Each system lists the ID of the last kalimah of every ayah, in "
                "order. The riwayahs following one system agree on all of them."
            ),
            "systems": systems,
        }, ensure_ascii=False, indent=1), encoding="utf-8")

    # --- kalimah-boundary events ----------------------------------------------
    with (OUT / "boundaries.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kalimah_ids", "surah", "ayah_hafs", "kind", "riwayahs",
                     "riwayahs_agree", "forms"])
        for event in boundary_events(kalimahs):
            wr.writerow([
                "|".join(str(i) for i in event["kalimah_ids"]), event["surah"],
                event["ayah"], event["kind"], "|".join(event["riwayahs"]),
                int(event["agree"]),
                "  ||  ".join(f"{t} [{','.join(ks)}]"
                              for t, ks in event["texts"].items()),
            ])
    return meta


def boundary_events(kalimahs: list[Kalimah]) -> list[dict]:
    """Group boundary-flagged kalimahs into the events they belong to.

    A boundary disagreement is never about one kalimah: it is about the space
    between two.  ``agree`` says whether the riwayahs read the run identically
    once it has been re-segmented — which is how a source that merely lost a
    space is told apart from a mushaf that really does print the kalimahs joined.
    """
    events: list[dict] = []
    run: list[Kalimah] = []
    for w in kalimahs:
        if w.boundary and run and w.id == run[-1].id + 1:
            run.append(w)
            continue
        if run:
            events.append(_event(run))
        run = [w] if w.boundary else []
    if run:
        events.append(_event(run))
    return events


def _event(run: list[Kalimah]) -> dict:
    texts: dict[str, list[str]] = defaultdict(list)
    for k in ORDER:
        parts = [w.forms[k] for w in run if k in w.forms]
        if parts:
            texts[" ".join(parts)].append(k)
    kinds = {kind for w in run for kind in w.boundary.values()}
    return {
        "kalimah_ids": [w.id for w in run],
        "surah": run[0].surah,
        "ayah": run[0].ayah.get("hafs", next(iter(run[0].ayah.values()), "")),
        "kind": "|".join(sorted(kinds)),
        "riwayahs": sorted({k for w in run for k in w.boundary}),
        "agree": all(len({w.rasm} | {_rasm_of(w, k) for k in w.forms}) == 1
                     for w in run),
        "texts": dict(texts),
    }


def _rasm_of(w: Kalimah, key: str) -> str:
    """Rasm of one riwayah's form, recomputed from the stored spelling."""
    from .normalize import rasm
    form = w.forms.get(key)
    return rasm(form) if form else ""
