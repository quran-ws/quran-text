"""Generated views of the muṣḥaf files.

None of these is normative.  ``out/mushaf/<key>.json`` is the format of record;
everything here is written from the same build so it cannot drift from it, and
exists only to meet consumers where they already are — a nested tree for people
arriving from verse-level XML, a flat table for pandas and R, and one SQLite
file for anyone who would rather answer a question in SQL than write a program.

The distinction is kept explicit, in ``docs/MUSHAF-FORMAT.md`` and in a
``view_of`` field on every file, because the alternative is that whichever form
turns out to be handiest silently becomes the standard.
"""

from __future__ import annotations

import csv
import gzip
import json
import shutil
import sqlite3
from bisect import bisect_right
from pathlib import Path

from .build import OUT
from .mushaf import FORMAT, FORMAT_VERSION, MUSHAF_DIR, numbers_of


# --------------------------------------------------------------------------
# reading the layers
# --------------------------------------------------------------------------

def unit_of(starts: list[int], pos: int) -> int:
    """Index of the unit (āyah, page, …) that position ``pos`` falls in.

    ``-1`` before the first start — the unnumbered basmalah, which precedes
    the first āyah in the muṣḥafs that do not count it.
    """
    return bisect_right(starts, pos) - 1


class Coords:
    """Per-position coordinates of one muṣḥaf, read off its layers once."""

    def __init__(self, doc: dict):
        self.doc = doc
        self.sura_starts = doc["sura_starts"]
        self.ayah_starts = doc["ayah_starts"]
        self.page_starts = doc.get("page_starts")
        self.line_starts = doc.get("line_starts")
        self.juz_starts = doc.get("juz_starts")
        self.numbers = numbers_of(doc)
        self.first_ayah = {s["number"]: s["first_ayah"] for s in doc["suras"]}
        self.marks: dict[int, list[dict]] = {}
        for pos, t in doc["marks"]:
            self.marks.setdefault(pos, []).append(doc["mark_types"][t])

    def sura(self, pos: int) -> int:
        return self.doc["suras"][unit_of(self.sura_starts, pos)]["number"]

    def ayah(self, pos: int) -> tuple[int, int]:
        """``(āyah number in this muṣḥaf, position within the āyah)``.

        Āyah ``0`` is the unnumbered basmalah, before the sūrah's first āyah.
        """
        sura = self.sura(pos)
        k = unit_of(self.ayah_starts, pos)
        if k < 0 or self.sura(self.ayah_starts[k]) != sura:
            return 0, pos - self.sura_starts[unit_of(self.sura_starts, pos)] + 1
        return k - self.first_ayah[sura] + 1, pos - self.ayah_starts[k] + 1

    def page(self, pos: int) -> int | None:
        return unit_of(self.page_starts, pos) + 1 if self.page_starts else None

    def line(self, pos: int) -> int | None:
        """Line within the page, counted from the page's first line."""
        if not self.line_starts or not self.page_starts:
            return None
        page_start = self.page_starts[unit_of(self.page_starts, pos)]
        return unit_of(self.line_starts, pos) - unit_of(self.line_starts, page_start) + 1

    def juz(self, pos: int) -> int | None:
        return unit_of(self.juz_starts, pos) + 1 if self.juz_starts else None

    def imlaei(self, pos: int) -> str | None:
        return self.doc["imlaei"][pos] if self.doc.get("imlaei") else None

    def resegmented(self) -> set[int]:
        return {p for e in self.doc["resegmentation"] for p in e["positions"]}


def _write_gz(path: Path, text: str) -> None:
    """Write one gzipped text file.

    The views are compressed and the normative files are not.  A view is
    fetched, decompressed and loaded by a program; the file of record is also
    read by people, and a standard whose canonical artefact cannot be opened in
    an editor is a worse standard for the few megabytes it saves.
    """
    with gzip.open(path, "wt", encoding="utf-8", compresslevel=9) as fh:
        fh.write(text)


def _mark_text(marks: list[dict]) -> str:
    return "|".join(f"{m['kind']}:{m['side']}:{m['sign']}" for m in marks)


def _word_record(c: Coords, pos: int) -> dict:
    """One word of a view, with every layer's value repeated on it."""
    first, last = c.numbers[pos]
    ayah, pos_in_ayah = c.ayah(pos)
    rec = {"pos": pos, "text": c.doc["words"][pos], "number": first}
    if last > first:
        rec["number_last"] = last
    rec.update({"sura": c.sura(pos), "ayah": ayah, "pos_in_ayah": pos_in_ayah})
    for name, value in (("page", c.page(pos)), ("line", c.line(pos)),
                        ("juz", c.juz(pos)), ("imlaei", c.imlaei(pos))):
        if value is not None:
            rec[name] = value
    if pos in c.marks:
        rec["marks"] = c.marks[pos]
    return rec


# --------------------------------------------------------------------------
# nested
# --------------------------------------------------------------------------

def write_nested(docs: dict[str, dict]) -> None:
    """sūrah -> āyah -> words, for consumers migrating off verse-level formats.

    The coordinates it repeats on every word are the reason this is a view and
    not the format: the same path names a different word in each muṣḥaf, because
    the muṣḥafs count āyāt differently.  The shared ``number`` is carried on
    every word here too, so a consumer who starts in the tree can still leave.
    The unnumbered basmalah of Al-Fātiḥah sits under ``"basmalah"`` rather
    than under an āyah number it does not have.
    """
    for key, doc in docs.items():
        c = Coords(doc)
        resegmented = c.resegmented()
        tree: dict[str, dict] = {}
        for pos in range(len(doc["words"])):
            rec = _word_record(c, pos)
            if pos in resegmented:
                rec["resegmented"] = True
            s = tree.setdefault(str(rec["sura"]), {"ayat": {}})
            slot = str(rec["ayah"]) if rec["ayah"] else "basmalah"
            s["ayat"].setdefault(slot, {"words": []})["words"].append(rec)
        for row in doc["suras"]:
            head = {k: v for k, v in row.items() if k not in ("number", "first_ayah")}
            tree[str(row["number"])] = {**head, "ayat": tree[str(row["number"])]["ayat"]}
        _write_gz(MUSHAF_DIR / f"{key}.nested.json.gz", json.dumps({
            "format": FORMAT,
            "format_version": FORMAT_VERSION,
            "view_of": f"out/mushaf/{key}.json",
            "view": "nested",
            "note": "Generated view. The normative file is the flat one; an "
                    "āyah path is not stable across muṣḥafs, `number` is.",
            "mushaf": doc["mushaf"],
            "counting": {k: doc["counting"][k] for k in
                         ("system", "ayah_count", "basmalah_counted")},
            "provenance": doc["provenance"],
            "suras": tree,
        }, ensure_ascii=False, indent=1))


# --------------------------------------------------------------------------
# flat table
# --------------------------------------------------------------------------

COLUMNS = ["pos", "sura", "ayah", "pos_in_ayah", "page", "line", "juz",
           "number", "number_last", "text", "imlaei", "marks", "resegmented"]


def write_csv(docs: dict[str, dict]) -> None:
    """One row per printed word.  ``number_last`` equals ``number`` except where
    the word covers a run, so the table stays one-row-per-word."""
    for key, doc in docs.items():
        c = Coords(doc)
        resegmented = c.resegmented()
        with gzip.open(MUSHAF_DIR / f"{key}.csv.gz", "wt", encoding="utf-8",
                       newline="", compresslevel=9) as fh:
            wr = csv.writer(fh)
            wr.writerow(COLUMNS)
            for pos in range(len(doc["words"])):
                first, last = c.numbers[pos]
                ayah, pos_in_ayah = c.ayah(pos)
                wr.writerow([pos, c.sura(pos), ayah, pos_in_ayah,
                             c.page(pos) or "", c.line(pos) or "", c.juz(pos) or "",
                             first, last, doc["words"][pos], c.imlaei(pos) or "",
                             _mark_text(c.marks.get(pos, [])),
                             int(pos in resegmented)])


# --------------------------------------------------------------------------
# SQLite
# --------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE mushaf (
  key TEXT PRIMARY KEY, name_en TEXT, name_ar TEXT, qari_en TEXT, qari_ar TEXT,
  counting_system TEXT, ayah_count INTEGER, basmalah_counted INTEGER,
  word_count INTEGER,
  text_package TEXT, text_sha256 TEXT, layout_package TEXT);
CREATE TABLE sura (
  mushaf TEXT, n INTEGER, name_ar TEXT, name_en TEXT, revelation TEXT,
  basmalah INTEGER, ayat INTEGER, first_pos INTEGER, last_pos INTEGER,
  PRIMARY KEY (mushaf, n));
CREATE TABLE word (
  mushaf TEXT, pos INTEGER, sura INTEGER, ayah INTEGER, pos_in_ayah INTEGER,
  number INTEGER, number_last INTEGER,
  uthmani TEXT, imlaei TEXT, page INTEGER, line INTEGER, juz INTEGER,
  resegmented INTEGER,
  PRIMARY KEY (mushaf, pos));
CREATE TABLE word_index (
  number INTEGER PRIMARY KEY, sura INTEGER, rasm TEXT, pointed TEXT,
  uthmani TEXT, simple TEXT, status TEXT,
  hafs_sura INTEGER, hafs_ayah INTEGER, hafs_pos INTEGER);
CREATE TABLE mark (
  mushaf TEXT, pos INTEGER, kind TEXT, side TEXT, sign TEXT);
CREATE TABLE resegmentation (
  mushaf TEXT, positions TEXT, sura INTEGER, ayah INTEGER, kind TEXT,
  source_text TEXT, emitted TEXT, riwayat_agree INTEGER);
CREATE TABLE line_disagreement (
  mushaf TEXT, sura INTEGER, ayah INTEGER, derived INTEGER, source INTEGER);
CREATE INDEX word_by_number ON word (number);
CREATE INDEX word_by_ref ON word (mushaf, sura, ayah);
CREATE INDEX mark_by_word ON mark (mushaf, pos);
"""


def write_sqlite(docs: dict[str, dict], word_index: dict,
                 path: Path = OUT / "quran.sqlite") -> None:
    """All seven muṣḥafs and the word index in one queryable file.

    ``word.number`` is the shared number, indexed on its own, so comparing two
    muṣḥafs is a self-join rather than a program:

        SELECT a.number, a.uthmani, b.uthmani
        FROM word a LEFT JOIN word b
          ON b.number = a.number AND b.mushaf = 'warsh'
        WHERE a.mushaf = 'hafs' AND (b.uthmani IS NULL OR b.uthmani <> a.uthmani);

    ``LEFT JOIN`` rather than ``JOIN`` because the answer is sometimes *no row*:
    Warsh does not recite ``هُوَ`` at 57:24, and a word-level dataset projected
    from Ḥafṣ has to see that rather than skip silently past it.  Where a word
    covers a run of numbers, ``number`` is the first and ``number_last`` the
    last; join on ``b.number BETWEEN a.number AND a.number_last`` to catch
    those too.
    """
    for stale in (path, path.with_suffix(path.suffix + ".gz")):
        if stale.exists():
            stale.unlink()
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    db.executemany("INSERT INTO word_index VALUES (?,?,?,?,?,?,?,?,?,?)", [
        (w["number"], w["sura"], w["rasm"], w["pointed"], w["uthmani"], w["simple"],
         w["status"], *((w["hafs"]["sura"], w["hafs"]["ayah"], w["hafs"]["pos"])
                        if w["hafs"] else (None, None, None)))
        for w in word_index["words"]])
    for key, doc in docs.items():
        m, prov, cnt = doc["mushaf"], doc["provenance"], doc["counting"]
        db.execute("INSERT INTO mushaf VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
            key, m["name_en"], m["name_ar"], m["qari_en"], m["qari_ar"],
            cnt["system"], cnt["ayah_count"], int(cnt["basmalah_counted"]),
            m["word_count"],
            prov["text"]["package"], prov["text"]["sha256"],
            prov.get("layout", {}).get("package")))
        starts = doc["sura_starts"] + [len(doc["words"])]
        db.executemany("INSERT INTO sura VALUES (?,?,?,?,?,?,?,?,?)", [
            (key, r["number"], r["name_ar"], r["name_en"], r["revelation"],
             int(r["has_basmalah"]), r["ayah_count"], starts[i], starts[i + 1] - 1)
            for i, r in enumerate(doc["suras"])])

        c = Coords(doc)
        resegmented = c.resegmented()
        rows = []
        for pos in range(len(doc["words"])):
            first, last = c.numbers[pos]
            ayah, pos_in_ayah = c.ayah(pos)
            rows.append((key, pos, c.sura(pos), ayah, pos_in_ayah, first, last,
                         doc["words"][pos], c.imlaei(pos), c.page(pos),
                         c.line(pos), c.juz(pos), int(pos in resegmented)))
        db.executemany("INSERT INTO word VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
        db.executemany("INSERT INTO mark VALUES (?,?,?,?,?)", [
            (key, pos, mk["kind"], mk["side"], mk["sign"])
            for pos, t in doc["marks"] for mk in [doc["mark_types"][t]]])
        db.executemany("INSERT INTO resegmentation VALUES (?,?,?,?,?,?,?,?)", [
            (key, "|".join(str(i) for i in e["positions"]), e["sura"], e["ayah"],
             e["kind"], e["source_text"], " ".join(e["emitted"]),
             int(e["riwayat_agree"]))
            for e in doc["resegmentation"]])
        db.executemany("INSERT INTO line_disagreement VALUES (?,?,?,?,?)", [
            (key, d["sura"], d["ayah"], d["derived"], d["source"])
            for d in doc["line_disagreements"]])
    db.commit()
    db.execute("VACUUM")
    db.close()

    # Shipped compressed: it is a view, and an uncompressed one is tens of
    # megabytes of binary that git can neither diff nor pack.
    with path.open("rb") as raw, gzip.open(
            path.with_suffix(path.suffix + ".gz"), "wb", compresslevel=9) as gz:
        shutil.copyfileobj(raw, gz)
    path.unlink()
