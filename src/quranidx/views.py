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


def _key(word: dict) -> tuple[int, int]:
    """``(word id, sub)`` — what addresses one word in one muṣḥaf.

    The ID alone does not: a word only a minority of muṣḥafs write has no ID of
    its own and hangs off the previous one, so Ḥafṣ's ``أَوۡ`` at 40:26 shares an
    ID with the ``دِينَكُمۡ`` before it.
    """
    return word["w"], word.get("x", 0)


def _coords(doc: dict) -> dict[tuple[int, int], tuple[int, int, int]]:
    """word -> (sura, ayah, position within the āyah).

    An āyah's ``words`` is a range of *IDs*, and an ID is shared across the
    muṣḥafs, so in one that lacks a word the range has a hole in it — while a
    muṣḥaf that adds one has two words inside a single ID.  Counting the
    integers in the range gets both wrong: Warsh 40:26 has 17 words and used to
    number the last of them 18.  Walk this muṣḥaf's own word list instead, which
    has neither holes nor doubles.
    """
    out: dict[tuple[int, int], tuple[int, int, int]] = {}
    at = 0
    words = doc["words"]
    for span in doc["ayat"]:
        first, last = span["words"]
        while at < len(words) and words[at]["w"] < first:
            at += 1
        pos = 1
        while at < len(words) and words[at]["w"] <= last:
            out[_key(words[at])] = (span["sura"], span["n"], pos)
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
            sura, ayah, pos = coords[_key(word)]
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
            words[coords[_key(word)][0]].append(word)
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

COLUMNS = ["word_id", "sub", "sura", "ayah", "pos", "uthmani", "imlaei",
           "page", "line", "juz", "marks", "resegmented"]


def write_csv(docs: dict[str, dict]) -> None:
    for key, doc in docs.items():
        coords = _coords(doc)
        juz = _juz_of(doc)
        with gzip.open(MUSHAF_DIR / f"{key}.csv.gz", "wt", encoding="utf-8",
                       newline="", compresslevel=9) as fh:
            wr = csv.writer(fh)
            wr.writerow(COLUMNS)
            for word in doc["words"]:
                sura, ayah, pos = coords[_key(word)]
                wr.writerow([word["w"], word.get("x", 0), sura, ayah, pos, word["t"],
                             word.get("e", ""), word.get("pg", ""),
                             word.get("ln", ""), juz.get(word["w"], ""),
                             _mark_text(word), int(word.get("resegmented", False))])


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
  mushaf TEXT, word_id INTEGER, sub INTEGER, sura INTEGER, ayah INTEGER,
  pos INTEGER,
  uthmani TEXT, imlaei TEXT, page INTEGER, line INTEGER, juz INTEGER,
  resegmented INTEGER,
  PRIMARY KEY (mushaf, word_id, sub));
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
"""


def write_sqlite(docs: dict[str, dict], path: Path) -> None:
    """All seven muṣḥafs in one queryable file.

    ``word.word_id`` is the global ID, indexed on its own, so comparing two
    muṣḥafs is a self-join rather than a program:

        SELECT a.word_id, a.uthmani, b.uthmani
        FROM word a LEFT JOIN word b
          ON b.word_id = a.word_id AND b.sub = a.sub AND b.mushaf = 'warsh'
        WHERE a.mushaf = 'hafs' AND (b.uthmani IS NULL OR b.uthmani <> a.uthmani);

    ``LEFT JOIN`` rather than ``JOIN`` because the answer is sometimes *no row*:
    Warsh does not recite ``هُوَ`` at 57:23, and a word-level dataset projected
    from Ḥafṣ has to see that rather than skip silently past it.

    ``(word_id, sub)`` is the key, not ``word_id`` alone — a word only a
    minority of muṣḥafs write hangs off the previous ID.  ``pos`` is the āyah-
    relative word number, which is what audio segments and highlighting address.
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
        db.executemany("INSERT INTO word VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", [
            (key, w["w"], w.get("x", 0), *coords[_key(w)], w["t"], w.get("e"),
             w.get("pg"), w.get("ln"), juz.get(w["w"]),
             int(w.get("resegmented", False)))
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
