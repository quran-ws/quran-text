#!/usr/bin/env python3
"""Extract the glyph stream of an islamweb HQPB muṣḥaf PDF.

    .venv/bin/python pipeline/tools/hqpb_extract.py <slug> [<slug> ...]

Reads ``sources/islamweb/<slug>/quran.pdf`` and writes, beside it,
``glyphs.json.gz`` (the glyph stream the build decodes) and ``SOURCE.json``
(what the file is: URL, SHA-256, size, the PDF's own metadata, and the
version of this extractor).  The PDF itself is not committed.

**What a glyph stream is.**  These PDFs are Word documents set in the KFGQPC
"HQPB" symbol fonts of 2005–2018: each glyph is a letter form, a mark or a
sign, addressed by its glyph id in one of the fonts HQPB1–5/7, MSH-Quraan1 or
Hamd2.  The PDF's text layer (ToUnicode) is unreliable — it is missing in
whole sections and maps two different glyphs to one character — so the
stream keys every glyph on ``(font family, glyph id)`` and nothing else.
Decoding glyph ids to Unicode happens in :mod:`qurantext.hqpb` with the
table that ``hqpb_calibrate.py`` learns; this tool only recovers the
*structure*: pages, lines, words, which glyph is a mark on which letter,
āyah medallions and their numbers, the basmalah ligature and the ۞ sign.

**Why a separate one-off tool.**  It needs PyMuPDF (``pip install pymupdf``
into ``.venv``), because poppler cannot report glyph ids.  The build never
reads a PDF: it reads the committed stream, so CI stays dependency-free and
the published text is reproducible from the repository alone.

Geometry conventions (all in PDF points × 1.5, the pixel space pdftohtml
uses, so the thresholds below read as pixels at 108 dpi):

* a *line* is a cluster of glyph baselines within ``LINE_TOL``;
* within a line glyphs are read right to left by their x origin;
* a zero-advance mark is drawn at its base letter's origin, so a mark attaches
  to the base whose origin x it shares, else to the base whose extent
  contains it, else to the nearest base;
* words are separated by the space glyphs the document carries; a word is
  split where an āyah medallion begins or ends, and ۞ stands alone, as it
  does in the KFGQPC packages.

Stream tokens: ``w`` word, ``m`` āyah medallion (``n`` = the printed number),
``b`` the basmalah ligature, ``h`` ۞, ``s`` a sūrah header (its text is not
kept: the name and āyah count printed there are not scripture).  Each glyph is
``[font index, glyph id, colour index, 1 if a mark else 0]``.
"""

from __future__ import annotations

import datetime as _dt
import gzip
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:  # pragma: no cover - older wheels
    import fitz  # type: ignore

ROOT = Path(__file__).resolve().parents[2]
ISLAMWEB = ROOT / "sources" / "islamweb"
URL = "https://dl2.islamweb.net/Audio_Path/quran_list/{slug}/quran.pdf"

EXTRACTOR_VERSION = 15
SCALE = 1.5
LINE_TOL = 8
#: The fonts whose glyphs are text.  «Hamdy2/4/5» are a second sign family a
#: few of the files reach for (a dagger alef in the Ruways file, a sign after
#: ٱئۡتِنَا in Ibn Jammāz's); their ids are not Hamd2's, so they stay distinct.
BODY = re.compile(r"HQPB\d|MSH-Quraan1|Hamd2|Hamdy\d")
#: No file sets a body glyph below 18 (scaled): the smallest are one line of
#: the Isḥāq file at 19 (p. 566) and a word of the Khalaf file at 18 (p. 483),
#: squeezed to fit the page.  A cut at 20 silently lost both.
MIN_BODY_SIZE = 18
MARK_FONT = re.compile(r"HQPB[45]")
#: the sign fonts, whose glyphs the typists overprint to make them bold
SIGN_FONT = re.compile(r"MSH-Quraan1|Hamd2|Hamdy\d")

#: Structural glyphs, by (family, glyph id).  Read off the Qālūn PDF and
#: confirmed on every other file; they do not depend on the ToUnicode map.
MEDALLION = {("HQPB2", 167), ("HQPB2", 168)}
DIGIT_GID = {("HQPB2", 169 + d): d for d in range(10)}
DIGIT_GID.update({("MSH-Quraan1", 19 + d): d for d in range(10)})
#: The basmalah ligature: three glyphs in HQPB3 (2005–2018 files) or in Hamd2 (Khalaf, Khallād,
#: Isḥāq, Idrīs).
BASMALAH_GIDS = ({("HQPB3", 72), ("HQPB3", 73), ("HQPB3", 74)}, {("Hamd2", 198), ("Hamd2", 199), ("Hamd2", 200)})
HIZB_GID = ("HQPB4", 13)
#: The ornamental brackets around a sūrah name: «﴿ ﴾» in MSH-Quraan1, or the HQPB2 pair the Khalaf
#: file uses.  The 2017 files (Abū Jaʿfar, Yaʿqūb, Khalaf al-ʿĀshir) print no sūrah header at all.
HEADER_GIDS = {("MSH-Quraan1", 155), ("MSH-Quraan1", 156), ("HQPB2", 193), ("HQPB2", 194)}
_DIGIT_OR_PAREN = re.compile(r"[\d()]")


_FAMILY_ALIASES = {"MshQuraan1": "MSH-Quraan1"}


def fam(name: str) -> str:
    """The font family without its subset prefix, under one spelling.

    The Isḥāq and Idrīs files (produced by Ghostscript, not Acrobat) carry the
    sign font as «MshQuraan1»; the glyph ids are the same font's."""
    family = name.split("+", 1)[-1]
    return _FAMILY_ALIASES.get(family, family)


# --------------------------------------------------------------------------
# reading the PDF
# --------------------------------------------------------------------------

def page_items(page) -> list[dict]:
    """One dict per drawn glyph, with its font family, glyph id, colour and geometry."""
    items = []
    for sp in page.get_texttrace():
        family = fam(sp["font"])
        r, g, b = (sp["color"][:3] if sp.get("color") else (0, 0, 0))
        color = "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))
        size = round(sp["size"] * SCALE)
        for uc, gid, origin, bbox in sp["chars"]:
            x0, y0, x1, y1 = bbox
            items.append(dict(
                family=family, gid=gid, ch=chr(uc), color=color, size=size,
                top=round(y0 * SCALE), ox=origin[0] * SCALE,
                width=(x1 - x0) * SCALE,
            ))
    return items


def _is_header_item(i: dict) -> bool:
    return (i["family"], i["gid"]) in HEADER_GIDS


def _is_count_item(i: dict) -> bool:
    """A Latin-font digit or parenthesis: the «(n)» of the header's second line."""
    return not BODY.search(i["family"]) and bool(_DIGIT_OR_PAREN.search(i["ch"]))


def lines_of(items: list[dict]) -> list[tuple[bool, list[dict]]]:
    """Body glyphs grouped into lines, each flagged ``(is_header, glyphs)``.

    A sūrah header is two lines — «﴿ سُورَةُ … ﴾» and «مكية/مدنية وآياتها (n)» —
    recognised by the MSH-Quraan1 bracket glyphs and the Latin-font digits,
    never by font size: one whole page of the Warsh file is set at the
    header size."""
    # the «(n)» of a header's count line is set small in some files, so count
    # items are kept regardless of size; a page number on a line of its own is
    # harmless, since a line with no body glyph emits nothing
    rel = [i for i in items
           if (i["size"] >= MIN_BODY_SIZE and (BODY.search(i["family"]) or is_space(i)))
           or _is_header_item(i) or _is_count_item(i)]
    rel.sort(key=lambda i: i["top"])
    # A line is a run of tops with no gap wider than LINE_TOL between
    # neighbours: a sign set a little above its line (the HQPB7 signs sit 9 px
    # up) must not open a line of its own and take the word spaces with it,
    # which once left a whole line of the Isḥāq file unsplit.  Lines are some
    # 50 px apart, so the runs never bridge two of them.
    lines: list[list[dict]] = []
    cur: list[dict] = []
    prev_top = None
    for i in rel:
        if prev_top is None or i["top"] - prev_top <= LINE_TOL:
            cur.append(i)
        else:
            lines.append(cur)
            cur = [i]
        prev_top = i["top"]
    if cur:
        lines.append(cur)
    out = []
    for line in lines:
        if all(is_space(i) for i in line):
            continue                              # a blank line (spaces only) is not a line
        glyphs = [i for i in line if BODY.search(i["family"]) or is_space(i)]
        # only the bracket ornaments mark a header here; the name and count lines
        # under them are recognised by what they decode to (qurantext.hqpb)
        out.append((any(_is_header_item(i) for i in line), glyphs))
    return out


def is_space(it: dict) -> bool:
    """A word separator: a blank character drawn from a text font.

    A blank character from a *body* font is a glyph whose ToUnicode entry
    happens to be a space — the sīn of إِسۡرَٰٓءِيلَ maps to U+00A0 — and is text.
    Even glyph 3, the fonts' own space glyph, is kept: the Khalaf file uses it
    as a hair space *inside* words around coloured glyphs, and the table reads
    it as nothing."""
    return it["ch"].strip() == "" and not BODY.search(it["family"])


def glyphs_of_line(line: list[dict]) -> list[dict]:
    gl = []
    for it in line:
        if is_space(it):
            gl.append(dict(kind="space", x=it["ox"] + it["width"] / 2))
            continue
        x0, x1 = it["ox"], it["ox"] + it["width"]
        gl.append(dict(
            kind="mark" if MARK_FONT.match(it["family"]) else "base",
            x=(x0 + x1) / 2, x0=x0, x1=x1,
            family=it["family"], gid=it["gid"], color=it["color"],
        ))
    gl.sort(key=lambda g: (-round(g["x"]), 0 if g["kind"] != "mark" else 1))
    return gl


def dedupe(word: list[dict]) -> list[dict]:
    """Drop a glyph printed again on the same spot.

    The Khalaf, Khallād and Abū al-Ḥārith files overprint a coloured sign up to
    six times to make it bold — six imālah dots on one letter — and some files
    repeat a vowel or a stroke the same way (the Abū Jaʿfar files print a small
    yāʾ three times).  One glyph at one place is one sign."""
    out: list[dict] = []
    for g in word:
        k = (g["family"], g["gid"])
        overprintable = g["kind"] == "mark" or SIGN_FONT.match(g["family"])
        if overprintable and k not in MEDALLION and k not in DIGIT_GID \
                and any((o["family"], o["gid"]) == k and abs(o["x"] - g["x"]) <= 1.5 for o in out):
            continue
        out.append(g)
    return out


def attach_marks(word: list[dict]) -> list[dict]:
    """Order a word as base, its marks, base, its marks … by geometry."""
    bases = [g for g in word if g["kind"] != "mark"]
    marks = [g for g in word if g["kind"] == "mark"]
    if not bases:
        return word
    slots: dict[int, list[dict]] = {id(b): [] for b in bases}
    for m in marks:
        cand = [b for b in bases if abs(b["x0"] - m["x0"]) <= 1]
        if not cand:
            cand = [b for b in bases if b["x0"] - 1.5 <= m["x"] <= b["x1"] + 1.5]
        if not cand:
            cand = [min(bases, key=lambda b: abs(b["x"] - m["x"]))]
        slots[id(cand[0])].append(m)
    out = []
    for b in bases:
        out.append(b)
        out.extend(sorted(slots[id(b)], key=lambda m: -m["x"]))
    return out


def words_of_line(line: list[dict]) -> list[list[dict]]:
    words: list[list[dict]] = []
    cur: list[dict] = []
    in_med = False
    opened_with = None          # which half opened the medallion
    just_closed = None          # the half that closed the last medallion

    def flush():
        nonlocal cur
        if cur:
            words.append(attach_marks(dedupe(cur)))
            cur = []

    for g in glyphs_of_line(line):
        if g["kind"] == "space":
            if not in_med:
                flush()
            continue
        k = (g["family"], g["gid"])
        if k in MEDALLION:
            # The Hishām file doubles the halves of some medallions («∪∪٦∩∩»);
            # a repeated half belongs to the medallion it repeats.
            if in_med and k == opened_with:
                cur.append(g)
            elif not in_med and just_closed == k and words and not cur:
                words[-1].append(g)
            elif not in_med:
                flush()
                cur = [g]
                in_med, opened_with = True, k
            else:
                cur.append(g)
                flush()
                in_med, just_closed = False, k
            continue
        just_closed = None
        if k == HIZB_GID:
            flush()
            words.append([g])
        else:
            cur.append(g)
    flush()
    return words


def marker_number(word: list[dict]) -> int | None:
    digits = []
    for g in word:
        k = (g["family"], g["gid"])
        if k in MEDALLION:
            continue
        if k in DIGIT_GID:
            digits.append(DIGIT_GID[k])
        else:
            return None
    if not digits:
        return None
    # the number is read left to right while the line is read right to left
    return int("".join(str(d) for d in reversed(digits)))


def classify(word: list[dict]) -> str:
    ks = [(g["family"], g["gid"]) for g in word]
    if MEDALLION & set(ks):
        return "marker"
    if set(ks) in BASMALAH_GIDS:
        return "basmalah"
    if ks == [HIZB_GID]:
        return "hizb"
    if all(g["kind"] == "mark" for g in word):
        return "marks"
    return "word"


# --------------------------------------------------------------------------
# the stream
# --------------------------------------------------------------------------

def extract(pdf_path: Path) -> dict:
    doc = fitz.open(pdf_path)
    fonts: list[str] = []
    colors: list[str] = []
    f_idx: dict[str, int] = {}
    c_idx: dict[str, int] = {}

    def fi(f):
        if f not in f_idx:
            f_idx[f] = len(fonts)
            fonts.append(f)
        return f_idx[f]

    def ci(c):
        if c not in c_idx:
            c_idx[c] = len(colors)
            colors.append(c)
        return c_idx[c]

    pages = []
    stats = Counter()
    for pno in range(doc.page_count):
        lines_out = []
        prev_header = False
        for is_header, line in lines_of(page_items(doc[pno])):
            if is_header:
                if not prev_header:            # one token per header block, not per header line
                    lines_out.append([{"k": "s", "g": []}])
                    stats["surah"] += 1
                prev_header = True
                continue
            prev_header = False
            toks = []
            for w in words_of_line(line):
                kind = classify(w)
                if kind == "marks" and toks and toks[-1]["k"] == "w":
                    # a sign set off by spaces belongs to the word before it
                    toks[-1]["g"].extend([fi(g["family"]), g["gid"], ci(g["color"]), 1] for g in w)
                    continue
                tok = {"k": {"word": "w", "marker": "m", "basmalah": "b", "hizb": "h", "marks": "w"}[kind],
                       "g": [[fi(g["family"]), g["gid"], ci(g["color"]), 0 if g["kind"] == "base" else 1] for g in w]}
                if kind == "marker":
                    tok["n"] = marker_number(w)
                toks.append(tok)
                stats[kind] += 1
            if toks:
                lines_out.append(toks)
        pages.append({"n": pno + 1, "lines": lines_out})
    return {
        "format": "hqpb-glyphs",
        "version": EXTRACTOR_VERSION,
        "fonts": fonts,
        "colors": colors,
        "pages": pages,
        "counts": dict(stats),
    }


def source_record(slug: str, pdf_path: Path, doc_meta: dict) -> dict:
    data = pdf_path.read_bytes()
    return {
        "slug": slug,
        "url": URL.format(slug=slug),
        "file": "quran.pdf",
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "fetched": _dt.date.today().isoformat(),
        "pdf": {k: v for k, v in doc_meta.items() if v},
        "extractor": {"tool": "pipeline/tools/hqpb_extract.py", "version": EXTRACTOR_VERSION,
                      "pymupdf": fitz.version[0]},
    }


def main(slugs: list[str]) -> None:
    for slug in slugs:
        d = ISLAMWEB / slug
        pdf = d / "quran.pdf"
        if not pdf.exists():
            raise SystemExit(f"{pdf} is missing; download it from {URL.format(slug=slug)}")
        stream = extract(pdf)
        doc = fitz.open(pdf)
        src = source_record(slug, pdf, doc.metadata)
        src["pages"] = doc.page_count
        stream["source"] = {k: src[k] for k in ("slug", "url", "sha256")}
        with gzip.open(d / "glyphs.json.gz", "wt", encoding="utf-8") as fh:
            json.dump(stream, fh, ensure_ascii=False, separators=(",", ":"))
        (d / "SOURCE.json").write_text(json.dumps(src, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        c = stream["counts"]
        print(f"{slug:9s} pages={doc.page_count} surahs={c.get('surah', 0)} words={c.get('word', 0)} "
              f"markers={c.get('marker', 0)} basmalah={c.get('basmalah', 0)} hizb={c.get('hizb', 0)} "
              f"-> {(d / 'glyphs.json.gz').stat().st_size // 1024} KB", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or sorted(p.name for p in ISLAMWEB.iterdir() if (p / "quran.pdf").exists()))
