"""Generated views of the mushaf files.

None of these is normative.  ``out/mushaf/<key>.json`` is the format of record;
everything here is written from the same build so it cannot drift from it, and
exists only to meet consumers where they already are — a nested tree for people
arriving from ayah-level XML, per-surah shards for a page that fetches over
static hosting, a flat table for pandas and R, and one SQLite file for anyone
who would rather answer a question in SQL than write a program.

The distinction is kept explicit, in ``docs/MUSHAF-FORMAT.md`` and in a
``view_of`` field on every file, because the alternative is that whichever form
turns out to be handiest silently becomes the standard and the kalimah ID it was
supposed to carry becomes decorative.
"""

from __future__ import annotations

import csv
import gzip
import json
import shutil
import sqlite3
from collections import defaultdict
from pathlib import Path

from .mushaf import FORMAT, FORMAT_VERSION, MUSHAF_DIR


def _coords(doc: dict) -> dict[int, tuple[int, int, int]]:
    """kalimah id -> (surah, ayah, position within the ayah)."""
    out: dict[int, tuple[int, int, int]] = {}
    for span in doc["ayahs"]:
        first, last = span["kalimahs"]
        for pos, wid in enumerate(range(first, last + 1), start=1):
            out[wid] = (span["surah"], span["n"], pos)
    return out


def _juz_of(doc: dict) -> dict[int, int]:
    out: dict[int, int] = {}
    for span in doc.get("juz", []):
        for wid in range(span["kalimahs"][0], span["kalimahs"][1] + 1):
            out[wid] = span["n"]
    return out


def _write_gz(path: Path, text: str) -> None:
    """Write one gzipped text file.

    The views are compressed and the normative files are not.  A view is
    fetched, decompressed and loaded by a program; the file of record is also
    read by people, and a standard whose canonical artefact cannot be opened in
    an editor is a worse standard for the few megabytes it saves.
    """
    with gzip.open(path, "wt", encoding="utf-8", compresslevel=9) as fh:
        fh.write(text)


def _mark_text(kalimah: dict) -> str:
    return "|".join(f"{m['k']}:{m['at']}:{m['sign']}" for m in kalimah.get("marks", []))


# --------------------------------------------------------------------------
# nested
# --------------------------------------------------------------------------

def write_nested(docs: dict[str, dict]) -> None:
    """surah -> ayah -> kalimahs, for consumers migrating off ayah-level formats.

    The coordinates it repeats on every kalimah are the reason this is a view and
    not the format: the same path names a different kalimah in each mushaf, because
    the mushafs count ayahs differently.  The global ``w`` is carried on every
    kalimah here too, so a consumer who starts in the tree can still leave it.
    """
    out = MUSHAF_DIR / "nested"
    out.mkdir(parents=True, exist_ok=True)
    for key, doc in docs.items():
        coords = _coords(doc)
        tree: dict[str, dict] = {}
        for kalimah in doc["kalimahs"]:
            surah, ayah, pos = coords[kalimah["w"]]
            s = tree.setdefault(str(surah), {"ayahs": {}})
            s["ayahs"].setdefault(str(ayah), {"kalimahs": []})["kalimahs"].append(
                {**kalimah, "surah": surah, "ayah": ayah, "pos": pos})
        for row in doc["surahs"]:
            # `ayahs` is the map of ayahs here, so the header's ayah *count* is
            # renamed rather than merged over it.
            head = {("ayah_count" if k == "ayahs" else k): v
                    for k, v in row.items() if k != "n"}
            tree[str(row["n"])] = {**head, "ayahs": tree[str(row["n"])]["ayahs"]}
        _write_gz(out / f"{key}.json.gz", json.dumps({
            "format": FORMAT,
            "format_version": FORMAT_VERSION,
            "view_of": f"out/mushaf/{key}.json",
            "view": "nested",
            "note": "Generated view. The normative file is the flat one; an "
                    "ayah path is not stable across mushafs, `w` is.",
            "mushaf": doc["mushaf"],
            "provenance": doc["provenance"],
            "surahs": tree,
        }, ensure_ascii=False, indent=1))


# --------------------------------------------------------------------------
# per-surah shards
# --------------------------------------------------------------------------

def write_shards(docs: dict[str, dict]) -> None:
    """The canonical shape, cut to one surah, so a page can fetch what it shows."""
    for key, doc in docs.items():
        out = MUSHAF_DIR / "surahs" / key
        out.mkdir(parents=True, exist_ok=True)
        kalimahs = defaultdict(list)
        coords = _coords(doc)
        for kalimah in doc["kalimahs"]:
            kalimahs[coords[kalimah["w"]][0]].append(kalimah)
        for row in doc["surahs"]:
            surah = row["n"]
            first, last = row["kalimahs"]
            (out / f"{surah:03d}.json").write_text(json.dumps({
                "format": FORMAT,
                "format_version": FORMAT_VERSION,
                "view_of": f"out/mushaf/{key}.json",
                "view": "surah-shard",
                "mushaf": doc["mushaf"]["key"],
                "provenance": doc["provenance"],
                "surah": row,
                "ayahs": [a for a in doc["ayahs"] if a["surah"] == surah],
                "safhahs": [p for p in doc["safhahs"]
                            if p["kalimahs"][1] >= first and p["kalimahs"][0] <= last],
                "kalimahs": kalimahs[surah],
            }, ensure_ascii=False, indent=1), encoding="utf-8")


# --------------------------------------------------------------------------
# flat table
# --------------------------------------------------------------------------

COLUMNS = ["kalimah_id", "surah", "ayah", "pos", "uthmani", "imlaei",
           "safhah", "line", "juz", "marks", "resegmented"]


def write_csv(docs: dict[str, dict]) -> None:
    for key, doc in docs.items():
        coords = _coords(doc)
        juz = _juz_of(doc)
        with gzip.open(MUSHAF_DIR / f"{key}.csv.gz", "wt", encoding="utf-8",
                       newline="", compresslevel=9) as fh:
            wr = csv.writer(fh)
            wr.writerow(COLUMNS)
            for kalimah in doc["kalimahs"]:
                surah, ayah, pos = coords[kalimah["w"]]
                wr.writerow([kalimah["w"], surah, ayah, pos, kalimah["t"],
                             kalimah.get("e", ""), kalimah.get("pg", ""),
                             kalimah.get("ln", ""), juz.get(kalimah["w"], ""),
                             _mark_text(kalimah), int(kalimah.get("resegmented", False))])


# --------------------------------------------------------------------------
# SQLite
# --------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE mushaf (
  key TEXT PRIMARY KEY, name_en TEXT, name_ar TEXT, qari_en TEXT, qari_ar TEXT,
  counting TEXT, ayah_count INTEGER, kalimah_count INTEGER,
  text_package TEXT, text_sha256 TEXT, layout_package TEXT);
CREATE TABLE surah (
  mushaf TEXT, n INTEGER, name_ar TEXT, name_en TEXT, revelation TEXT,
  basmalah INTEGER, ayahs INTEGER, first_kalimah INTEGER, last_kalimah INTEGER,
  PRIMARY KEY (mushaf, n));
CREATE TABLE kalimah (
  mushaf TEXT, kalimah_id INTEGER, surah INTEGER, ayah INTEGER, pos INTEGER,
  uthmani TEXT, imlaei TEXT, safhah INTEGER, line INTEGER, juz INTEGER,
  resegmented INTEGER,
  PRIMARY KEY (mushaf, kalimah_id));
CREATE TABLE mark (
  mushaf TEXT, kalimah_id INTEGER, kind TEXT, side TEXT, sign TEXT);
CREATE TABLE resegmentation (
  mushaf TEXT, kalimah_ids TEXT, surah INTEGER, ayah INTEGER, kind TEXT,
  source_text TEXT, emitted TEXT, riwayahs_agree INTEGER);
CREATE TABLE line_disagreement (
  mushaf TEXT, surah INTEGER, ayah INTEGER, derived INTEGER, source INTEGER);
CREATE INDEX kalimah_by_id ON kalimah (kalimah_id);
CREATE INDEX kalimah_by_ref ON kalimah (mushaf, surah, ayah);
CREATE INDEX mark_by_kalimah ON mark (mushaf, kalimah_id);
"""


def write_sqlite(docs: dict[str, dict], path: Path) -> None:
    """All seven mushafs in one queryable file.

    ``kalimah.kalimah_id`` is the global ID, indexed on its own, so comparing two
    mushafs is a self-join rather than a program.
    """
    for stale in (path, path.with_suffix(path.suffix + ".gz")):
        if stale.exists():
            stale.unlink()
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    for key, doc in docs.items():
        m, prov = doc["mushaf"], doc["provenance"]
        db.execute("INSERT INTO mushaf VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
            key, m["name_en"], m["name_ar"], m["qari_en"], m["qari_ar"],
            m["counting"], m["ayah_count"], m["kalimah_count"],
            prov["text"]["package"], prov["text"]["sha256"],
            prov.get("layout", {}).get("package")))
        db.executemany("INSERT INTO surah VALUES (?,?,?,?,?,?,?,?,?)", [
            (key, r["n"], r["name_ar"], r["name_en"], r["revelation"],
             int(r["basmalah"]), r["ayahs"], r["kalimahs"][0], r["kalimahs"][1])
            for r in doc["surahs"]])

        coords, juz = _coords(doc), _juz_of(doc)
        db.executemany("INSERT INTO kalimah VALUES (?,?,?,?,?,?,?,?,?,?,?)", [
            (key, w["w"], *coords[w["w"]], w["t"], w.get("e"), w.get("pg"),
             w.get("ln"), juz.get(w["w"]), int(w.get("resegmented", False)))
            for w in doc["kalimahs"]])
        db.executemany("INSERT INTO mark VALUES (?,?,?,?,?)", [
            (key, w["w"], mk["k"], mk["at"], mk["sign"])
            for w in doc["kalimahs"] for mk in w.get("marks", [])])
        db.executemany("INSERT INTO resegmentation VALUES (?,?,?,?,?,?,?,?)", [
            (key, "|".join(str(i) for i in e["kalimahs"]), e["surah"], e["ayah"],
             e["kind"], e["source_text"], " ".join(e["emitted"]),
             int(e["riwayahs_agree"]))
            for e in doc["resegmentation"]])
        db.executemany("INSERT INTO line_disagreement VALUES (?,?,?,?,?)", [
            (key, d["surah"], d["ayah"], d["derived"], d["source"])
            for d in doc["line_disagreements"]])
    db.commit()
    db.execute("VACUUM")
    db.close()

    # Shipped compressed: it is a view, and an uncompressed one is 56 MB of
    # binary that git can neither diff nor pack.
    with path.open("rb") as raw, gzip.open(
            path.with_suffix(path.suffix + ".gz"), "wb", compresslevel=9) as gz:
        shutil.copyfileobj(raw, gz)
    path.unlink()
