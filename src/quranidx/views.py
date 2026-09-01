"""Generated views of the muṣḥaf files.

None of these is normative.  ``out/mushaf/<key>.json`` is the format of record;
everything here is written from the same build so it cannot drift from it, and
exists only to meet consumers where they already are — a nested tree for people
arriving from verse-level XML, per-sūrah shards for a page that fetches over
static hosting, a flat table for pandas and R, and one SQLite file for anyone
who would rather answer a question in SQL than write a program.

The distinction is kept explicit, in ``docs/MUSHAF-FORMAT.md`` and in a
``view_of`` field on every file, because the alternative is that whichever form
turns out to be handiest silently becomes the standard and the word ID it was
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
    """slot id -> (sura, ayah, dense token position within the āyah).

    A slot range can contain gaps for words this muṣḥaf lacks.  Counting the
    integers in the range therefore inflates positions after a gap; enumerate
    only this document's actual word records instead.
    """
    out: dict[int, tuple[int, int, int]] = {}
    slot_ids = [w.get("s", w["w"]) for w in doc["words"]]
    at = 0
    for span in doc["ayat"]:
        first, last = span.get("slots", span["words"])
        while at < len(slot_ids) and slot_ids[at] < first:
            at += 1
        pos = 1
        while at < len(slot_ids) and slot_ids[at] <= last:
            out[slot_ids[at]] = (span["sura"], span["n"], pos)
            at += 1
            pos += 1
    return out


def _juz_of(doc: dict) -> dict[int, int]:
    out: dict[int, int] = {}
    for span in doc.get("juz", []):
        for wid in range(span["words"][0], span["words"][1] + 1):
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


def _mark_text(word: dict) -> str:
    return "|".join(f"{m['k']}:{m['at']}:{m['sign']}" for m in word.get("marks", []))


# --------------------------------------------------------------------------
# nested
# --------------------------------------------------------------------------

def write_nested(docs: dict[str, dict]) -> None:
    """sūrah -> āyah -> words, for consumers migrating off verse-level formats.

    The coordinates it repeats on every word are the reason this is a view and
    not the format: the same path names a different word in each muṣḥaf, because
    the muṣḥafs count āyāt differently.  The global ``w`` is carried on every
    word here too, so a consumer who starts in the tree can still leave it.
    """
    out = MUSHAF_DIR / "nested"
    out.mkdir(parents=True, exist_ok=True)
    for key, doc in docs.items():
        coords = _coords(doc)
        tree: dict[str, dict] = {}
        for word in doc["words"]:
            sura, ayah, pos = coords[word["w"]]
            s = tree.setdefault(str(sura), {"ayat": {}})
            s["ayat"].setdefault(str(ayah), {"words": []})["words"].append(
                {**word, "sura": sura, "ayah": ayah, "pos": pos})
        for row in doc["suras"]:
            # `ayat` is the map of āyāt here, so the header's āyah *count* is
            # renamed rather than merged over it.
            head = {("ayah_count" if k == "ayat" else k): v
                    for k, v in row.items() if k != "n"}
            tree[str(row["n"])] = {**head, "ayat": tree[str(row["n"])]["ayat"]}
        _write_gz(out / f"{key}.json.gz", json.dumps({
            "format": FORMAT,
            "format_version": FORMAT_VERSION,
            "view_of": f"out/mushaf/{key}.json",
            "view": "nested",
            "note": "Generated view. The normative file is the flat one; an "
                    "āyah path is not stable across muṣḥafs, `w` is.",
            "mushaf": doc["mushaf"],
            "provenance": doc["provenance"],
            "suras": tree,
        }, ensure_ascii=False, indent=1))


# --------------------------------------------------------------------------
# per-sūrah shards
# --------------------------------------------------------------------------

def write_shards(docs: dict[str, dict]) -> None:
    """The canonical shape, cut to one sūrah, so a page can fetch what it shows."""
    for key, doc in docs.items():
        out = MUSHAF_DIR / "suras" / key
        out.mkdir(parents=True, exist_ok=True)
        words = defaultdict(list)
        coords = _coords(doc)
        for word in doc["words"]:
            words[coords[word["w"]][0]].append(word)
        for row in doc["suras"]:
            sura = row["n"]
            first, last = row["words"]
            (out / f"{sura:03d}.json").write_text(json.dumps({
                "format": FORMAT,
                "format_version": FORMAT_VERSION,
                "view_of": f"out/mushaf/{key}.json",
                "view": "sura-shard",
                "mushaf": doc["mushaf"]["key"],
                "provenance": doc["provenance"],
                "sura": row,
                "ayat": [a for a in doc["ayat"] if a["sura"] == sura],
                "pages": [p for p in doc["pages"]
                          if p["words"][1] >= first and p["words"][0] <= last],
                "words": words[sura],
            }, ensure_ascii=False, indent=1), encoding="utf-8")


# --------------------------------------------------------------------------
# flat table
# --------------------------------------------------------------------------

COLUMNS = ["word_id", "sura", "ayah", "pos", "uthmani", "imlaei",
           "page", "line", "juz", "marks", "resegmented",
           "slot_id", "position"]


def write_csv(docs: dict[str, dict]) -> None:
    for key, doc in docs.items():
        coords = _coords(doc)
        juz = _juz_of(doc)
        with gzip.open(MUSHAF_DIR / f"{key}.csv.gz", "wt", encoding="utf-8",
                       newline="", compresslevel=9) as fh:
            wr = csv.writer(fh)
            wr.writerow(COLUMNS)
            for word in doc["words"]:
                sura, ayah, pos = coords[word["w"]]
                wr.writerow([word["w"], sura, ayah, pos, word["t"],
                             word.get("e", ""), word.get("pg", ""),
                             word.get("ln", ""), juz.get(word["w"], ""),
                             _mark_text(word), int(word.get("resegmented", False)),
                             word.get("s", word["w"]), word["p"]])


# --------------------------------------------------------------------------
# SQLite
# --------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE mushaf (
  key TEXT PRIMARY KEY, name_en TEXT, name_ar TEXT, qari_en TEXT, qari_ar TEXT,
  counting TEXT, ayah_count INTEGER, word_count INTEGER,
  text_package TEXT, text_sha256 TEXT, layout_package TEXT);
CREATE TABLE sura (
  mushaf TEXT, n INTEGER, name_ar TEXT, name_en TEXT, revelation TEXT,
  basmalah INTEGER, ayat INTEGER, first_word INTEGER, last_word INTEGER,
  PRIMARY KEY (mushaf, n));
CREATE TABLE word (
  mushaf TEXT, word_id INTEGER, sura INTEGER, ayah INTEGER, pos INTEGER,
  uthmani TEXT, imlaei TEXT, page INTEGER, line INTEGER, juz INTEGER,
  resegmented INTEGER, slot_id INTEGER, position INTEGER,
  PRIMARY KEY (mushaf, word_id));
CREATE TABLE mark (
  mushaf TEXT, word_id INTEGER, kind TEXT, side TEXT, sign TEXT);
CREATE TABLE resegmentation (
  mushaf TEXT, word_ids TEXT, sura INTEGER, ayah INTEGER, kind TEXT,
  source_text TEXT, emitted TEXT, riwayat_agree INTEGER);
CREATE TABLE line_disagreement (
  mushaf TEXT, sura INTEGER, ayah INTEGER, derived INTEGER, source INTEGER);
CREATE INDEX word_by_id ON word (word_id);
CREATE INDEX word_by_ref ON word (mushaf, sura, ayah);
CREATE INDEX mark_by_word ON mark (mushaf, word_id);
CREATE UNIQUE INDEX word_by_position ON word (mushaf, position);
"""


def write_sqlite(docs: dict[str, dict], path: Path) -> None:
    """All seven muṣḥafs in one queryable file.

    ``word.word_id`` is the global ID, indexed on its own, so comparing two
    muṣḥafs is a self-join rather than a program.
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
            m["counting"], m["ayah_count"], m["word_count"],
            prov["text"]["package"], prov["text"]["sha256"],
            prov.get("layout", {}).get("package")))
        db.executemany("INSERT INTO sura VALUES (?,?,?,?,?,?,?,?,?)", [
            (key, r["n"], r["name_ar"], r["name_en"], r["revelation"],
             int(r["basmalah"]), r["ayat"], r["words"][0], r["words"][1])
            for r in doc["suras"]])

        coords, juz = _coords(doc), _juz_of(doc)
        db.executemany("INSERT INTO word VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", [
            (key, w["w"], *coords[w["w"]], w["t"], w.get("e"), w.get("pg"),
             w.get("ln"), juz.get(w["w"]), int(w.get("resegmented", False)),
             w.get("s", w["w"]), w["p"])
            for w in doc["words"]])
        db.executemany("INSERT INTO mark VALUES (?,?,?,?,?)", [
            (key, w["w"], mk["k"], mk["at"], mk["sign"])
            for w in doc["words"] for mk in w.get("marks", [])])
        db.executemany("INSERT INTO resegmentation VALUES (?,?,?,?,?,?,?,?)", [
            (key, "|".join(str(i) for i in e["words"]), e["sura"], e["ayah"],
             e["kind"], e["source_text"], " ".join(e["emitted"]),
             int(e["riwayat_agree"]))
            for e in doc["resegmentation"]])
        db.executemany("INSERT INTO line_disagreement VALUES (?,?,?,?,?)", [
            (key, d["sura"], d["ayah"], d["derived"], d["source"])
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
