"""Decode an islamweb HQPB glyph stream into the paragraphs the loader reads.

The stream (``sources/islamweb/<slug>/glyphs.json.gz``) is what
``pipeline/tools/hqpb_extract.py`` recovered from the PDF: pages, lines and
tokens, each glyph addressed as ``(font family, glyph id)``.  The table
(``sources/islamweb/decoder/table-v1.json``) is what
``pipeline/tools/hqpb_calibrate.py`` learned by aligning the Qālūn, Shuʿbah
and Warsh streams against the KFGQPC texts of the same riwāyāt.  This module
puts the two together with no knowledge of its own: every codepoint it emits
is looked up, never inferred, and a glyph the table does not know is emitted
as U+FFFD and counted, so that the build can refuse to publish it.

Output shape: one paragraph per sūrah, words separated by spaces, each āyah
closed by ``NBSP + U+06DD + Arabic-Indic digits`` exactly as the v3.0 KFGQPC
documents do, so :func:`qurantext.sources.paragraphs_to_ayahs` segments both
kinds of source with one walk.  A basmalah ligature becomes its own paragraph
(the loader turns it into āyah 0); ۞ is its own word.

A sūrah begins at a header token, or — the 2017 files print no headers — at a
basmalah ligature, or where the printed āyah numbers restart at 1, 2, 3 (al-Tawbah
has neither).  A header followed by its basmalah opens one sūrah, not two.

Āyah numbers are assigned by position — the n-th medallion of a sūrah closes
āyah n — because the printed numbers carry typists' slips (the Qālūn file
prints ٢٠ for 5:30).  The printed numbers are kept and compared in
:func:`printed_number_slips`, and the muṣḥaf file lists every disagreement.
"""

from __future__ import annotations

import gzip
import json
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from . import chars, normalize

NBSP = " "
AYAH_SIGN = "۝"
UNKNOWN = "�"
HIZB = "۞"   # ۞
#: The kashida glyph: a word whose last glyph is one continues into the next word —
#: the Hishām file types «قِيلَ» as «ق» + a space + the ishmām sign + «ـيلَ».
KASHIDA = {("HQPB2", 164)}
TANWIN = set("\u064b\u064c\u064d\u08f0\u08f1\u08f2")
LONE_ALEF = set("\u0623\u0625\u0627\u0622\u0671")
#: What a sūrah header says, by rasm: «سورة …» and «مكية/مدنية وآياتها (n)».  A line of
#: up to three such words right under a header ornament is the header, not scripture
#: (24:1 «سُورَةٌ أَنزَلۡنَٰهَا …» is a full line and keeps its place).
def _skeleton(word: str) -> str:
    """The rasm without its alefs: «وَءَايَاتُهَا» and «وَءَايَٰتُهَا» agree here."""
    return "".join(c for c in normalize.rasm(word) if c not in "اٱأإآ")


#: The count line, as one skeleton: the Khalaf file runs its two words together.
HEADER_LINES = {_skeleton(a) + _skeleton(b) for a in ("مَكِّيَّةٌ", "مَدَنِيَّةٌ")
                for b in ("وَءَايَاتُهَا", "ءَايَاتُهَا", "وَآيَاتُهَا", "آيَاتُهَا")}


def _is_header_line(words: list[str]) -> bool:
    if not words or len(words) > 4:
        return False
    line = "".join(_skeleton(w) for w in words)
    return line.startswith(_skeleton("سُورَةُ")) or line in HEADER_LINES
#: Signs that are neither letters nor combining: the sajdah sign, the waqf signs, the small letters.
SIGNS = set("\u06d6\u06d7\u06d8\u06d9\u06da\u06db\u06dc\u06e9\u08cc\u06e5\u06e6")
BASMALAH = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"   # in the decoded (2022) notation: U+0652 sukun

Key = tuple[str, int]


def load_stream(path: Path) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return json.load(fh)


def load_table(path: Path) -> "Table":
    return Table(json.loads(Path(path).read_text(encoding="utf-8")))


class Table:
    """The learned glyph → text table, in lookup form."""

    def __init__(self, doc: dict):
        self.doc = doc
        self.version = doc["version"]
        self.base: dict[Key, str] = {}
        self.ctx: dict[tuple, str] = {}
        self.mark: dict[Key, str] = {}
        self.lig: dict[tuple, str] = {}
        self.marklike: set[Key] = set()
        for e in doc["entries"]:
            k = (e["font"], e["gid"])
            if e["kind"] == "base":
                self.base[k] = e["text"]
            elif e["kind"] == "mark":
                self.mark[k] = e["text"]
            elif e["kind"] == "marklike":
                self.marklike.add(k)
        for e in doc.get("context", []):
            marks = tuple((f, g) for f, g in e["marks"])
            prev = tuple(e["prev"]) if e.get("prev") else None
            self.ctx[(prev, (e["font"], e["gid"]), marks)] = e["text"]
        for e in doc.get("ligatures", []):
            marks = tuple((f, g) for f, g in e["marks"])
            self.lig[((e["font"], e["gid"]), marks)] = e["text"]
        self.order: dict[str, int] = doc.get("mark_order", {})
        joins = doc.get("joins", {})
        self.never_final: set[Key] = {tuple(k) for k in joins.get("never_final", [])}
        self.never_initial: set[Key] = {tuple(k) for k in joins.get("never_initial", [])}

    def letters(self, prev: Key | None, base: Key, marks: tuple[Key, ...]) -> str | None:
        for key in ((prev, base, marks), (None, base, marks)):
            if key in self.ctx:
                return self.ctx[key]
        return self.base.get(base)


@dataclass
class Decoded:
    text: str
    unknown: list[Key] = field(default_factory=list)
    #: colour of each glyph, in reading order, as the stream's colour strings
    colors: list[str] = field(default_factory=list)


def split_units(glyphs: list[tuple[Key, bool]], marklike: set[Key]) -> list[tuple[Key | None, list[Key]]]:
    """Group a word's glyphs into letter units: a base and the marks on it."""
    units: list[tuple[Key | None, list[Key]]] = []
    for k, is_mark in glyphs:
        if is_mark or k in marklike:
            if units:
                units[-1][1].append(k)
            else:
                units.append((None, [k]))
        else:
            units.append((k, []))
    return units


def decode_word(glyphs: list[tuple[Key, bool]], table: Table) -> Decoded:
    out = ""
    unknown: list[Key] = []
    units = split_units(glyphs, table.marklike)
    for i, (base, marks) in enumerate(units):
        prev = units[i - 1][0] if i else None
        mk = tuple(marks)
        if base is not None and (base, mk) in table.lig:
            out += table.lig[(base, mk)]
            continue
        letters = ""
        if base is not None:
            letters = table.letters(prev, base, mk)
            if letters is None:
                unknown.append(base)
                letters = UNKNOWN
        spans = []
        for m in marks:
            t = table.mark.get(m)
            if t is None and m in table.marklike:
                continue                      # a glyph that stands for nothing (a seat, a stroke)
            if t is None:
                unknown.append(m)
                t = UNKNOWN
            spans.append(t)
        letter_list = [c for c in letters if not unicodedata.combining(c)] or [""]
        if len(letter_list) >= 2 and len(spans) >= 2:
            # a ligature glyph (لأ, لا …) with one mark glyph per letter: the marks are
            # in reading order, so the k-th goes on the k-th letter
            groups = [[] for _ in letter_list]
            for k, t in enumerate(spans):
                groups[min(k, len(groups) - 1)].append(t)
            for letter, g in zip(letter_list, groups):
                out += letter + "".join(sorted("".join(g), key=lambda c: table.order.get(c, 99)))
        else:
            out += letters + "".join(sorted("".join(spans), key=lambda c: table.order.get(c, 99)))
    return Decoded(unicodedata.normalize("NFC", out), unknown)


@dataclass
class Surah:
    index: int
    #: decoded words in order; an āyah medallion is the string ``AYAH_SIGN``
    words: list[str]
    printed_numbers: list[int | None]
    basmalah: bool
    #: per word: the set of non-black colours on its glyphs
    colors: list[frozenset[str]]
    pages: list[int]
    lines: list[int]
    unknown: Counter


def decode_stream(stream: dict, table: Table) -> list[Surah]:
    fonts, colors = stream["fonts"], stream["colors"]
    surahs: list[Surah] = []
    cur: Surah | None = None
    pending_basmalah = False
    line_no = 0

    def start(index: int) -> Surah:
        s = Surah(index, [], [], False, [], [], [], Counter())
        surahs.append(s)
        return s

    tokens = [(page["n"], li, tok) for page in stream["pages"] for li, line in enumerate(page["lines"]) for tok in line]
    join_next = False
    markers = [i for i, (_p, _l, t) in enumerate(tokens) if t["k"] == "m"]
    restart_at = set()
    for a, b, c in zip(markers, markers[1:], markers[2:]):
        if (tokens[a][2].get("n"), tokens[b][2].get("n"), tokens[c][2].get("n")) == (1, 2, 3):
            restart_at.add(a)
    # header lines: the two or three lines under a header ornament that name the sūrah
    # and give its āyah count; dropped by what they decode to, never by length
    skip: set[tuple[int, int]] = set()
    by_line: dict[tuple[int, int], list] = {}
    for pno, li, tok in tokens:
        by_line.setdefault((pno, li), []).append(tok)
    line_keys = list(by_line)
    for i, key in enumerate(line_keys):
        if any(t["k"] == "s" for t in by_line[key]):
            skip.add(key)                         # the ornament line carries the sūrah's name
            for nxt in line_keys[i + 1:i + 4]:
                toks = by_line[nxt]
                if any(t["k"] in ("m", "b", "s") for t in toks):
                    break
                words = [decode_word([((fonts[f], gid), bool(m)) for f, gid, _c, m in t["g"]], table).text
                         for t in toks if t["k"] == "w"]
                if _is_header_line(words):
                    skip.add(nxt)
                else:
                    break
    last_page = None
    for idx, (pno, li, tok) in enumerate(tokens):
        if (pno, li) in skip and tok["k"] == "w":
            continue
        if (pno, li) != last_page:
            line_no += 1
            last_page = (pno, li)
        page = {"n": pno}
        if True:
            if True:
                k = tok["k"]
                if k == "s":
                    cur = start(len(surahs) + 1)
                    continue
                if k == "b":
                    if cur is None or cur.words:      # a basmalah opens a sūrah unless a header just did
                        cur = start(len(surahs) + 1)
                    cur.basmalah = True
                    continue
                if k == "m" and idx in restart_at and cur is not None and AYAH_SIGN in cur.words:
                    # the first marker of a sūrah without header or basmalah (al-Tawbah): the
                    # words since the last marker belong to the new sūrah
                    j = len(cur.words) - 1
                    while j >= 0 and cur.words[j] != AYAH_SIGN:
                        j -= 1
                    moved = cur.words[j + 1:], cur.colors[j + 1:], cur.pages[j + 1:], cur.lines[j + 1:]
                    del cur.words[j + 1:], cur.colors[j + 1:], cur.pages[j + 1:], cur.lines[j + 1:]
                    cur = start(len(surahs) + 1)
                    cur.words, cur.colors, cur.pages, cur.lines = [list(x) for x in moved]
                if cur is None:
                    cur = start(1)
                if k == "m":
                    cur.words.append(AYAH_SIGN)
                    cur.printed_numbers.append(tok.get("n"))
                    cur.colors.append(frozenset())
                    cur.pages.append(page["n"]); cur.lines.append(line_no)
                    continue
                if k == "h":
                    cur.words.append(HIZB)
                    cur.colors.append(frozenset())
                    cur.pages.append(page["n"]); cur.lines.append(line_no)
                    continue
                glyphs = [((fonts[f], gid), bool(is_mark)) for f, gid, _c, is_mark in tok["g"]]
                d = decode_word(glyphs, table)
                for u in d.unknown:
                    cur.unknown[u] += 1
                word_colors_ = frozenset(colors[c] for _f, _g, c, _m in tok["g"] if colors[c] != "#000000")
                bases = [k for k, is_mark in glyphs if not is_mark and k not in table.marklike]
                # the typist's spaces inside a word: a medial glyph form at the word's end, a
                # kashida at its end, a lone hamza-alef (never a word), a word opening with a
                # final glyph form or with a mark
                ends_in_stroke = bool(glyphs) and glyphs[-1][0] in KASHIDA
                ends_open = bool(bases) and bases[-1] in table.never_final
                lone_alef = bool(d.text) and d.text[0] in LONE_ALEF \
                    and all(unicodedata.combining(c) for c in d.text[1:])
                opens_closed = (bool(bases) and bases[0] in table.never_initial) \
                    or (bool(d.text) and unicodedata.combining(d.text[0]))
                if (join_next or opens_closed) and cur.words and cur.words[-1] not in (AYAH_SIGN, HIZB):
                    cur.words[-1] = unicodedata.normalize("NFC", cur.words[-1] + d.text)
                    cur.colors[-1] = cur.colors[-1] | word_colors_
                    join_next = ends_in_stroke or ends_open
                    continue
                join_next = ends_in_stroke or ends_open or lone_alef
                hamza_only = bool(d.text) and d.text[0] == "\u0621" \
                    and all(c == "\u0621" or unicodedata.combining(c) for c in d.text)
                if hamza_only and not (set(d.text) & TANWIN):
                    # a hamza typed apart from the word it opens (ءَأَمَنتُم → «ءَ» «مَنتُم»):
                    # the next word completes it
                    join_next = True
                elif hamza_only and cur.words and cur.words[-1] not in (AYAH_SIGN, HIZB):
                    # a hamza with tanwīn typed apart from the word it closes (دِفۡءٌ → «دِفۡ» «ءٌ»)
                    cur.words[-1] = unicodedata.normalize("NFC", cur.words[-1] + d.text)
                    cur.colors[-1] = cur.colors[-1] | word_colors_
                    continue
                if d.text and all(unicodedata.combining(c) or c in SIGNS for c in d.text) \
                        and cur.words and cur.words[-1] not in (AYAH_SIGN, HIZB):
                    # a sign set apart by a space (۩, a waqf sign) belongs to the word
                    # before it, which is where the KFGQPC releases write it
                    cur.words[-1] = unicodedata.normalize("NFC", cur.words[-1] + d.text)
                    cur.colors[-1] = cur.colors[-1] | word_colors_
                    continue
                cur.words.append(d.text)
                cur.colors.append(word_colors_)
                cur.pages.append(page["n"]); cur.lines.append(line_no)
    return surahs


def _ayah_mark(n: int) -> str:
    digits = {v: k for k, v in chars.ARABIC_DIGITS.items()}
    return NBSP + AYAH_SIGN + "".join(digits[d] for d in str(n))


def paragraphs(surahs: list[Surah]) -> list[str]:
    """The paragraph list :func:`qurantext.sources.paragraphs_to_ayahs` expects."""
    out: list[str] = []
    for s in surahs:
        words = list(s.words)
        if s.basmalah:
            out.append(BASMALAH)
        elif s.index == 1 and len(words) > 5 and AYAH_SIGN not in words[:5] \
                and [normalize.rasm(w) for w in words[:4]] == [normalize.rasm(w) for w in BASMALAH.split()]:
            # Al-Fātiḥah's basmalah is spelled out in every file; where the count does
            # not number it there is no medallion after it, so it would fall into
            # āyah 1.  Give it its own paragraph, as the KFGQPC documents do.
            out.append(BASMALAH)
            words = words[4:]
        n = 0
        buf: list[str] = []
        for w in words:
            if w == AYAH_SIGN:
                n += 1
                if buf:
                    buf[-1] = buf[-1] + _ayah_mark(n)
                else:
                    buf.append(_ayah_mark(n).lstrip(NBSP))
            else:
                buf.append(w)
        out.append(" ".join(buf))
    return out


def printed_number_slips(surahs: list[Surah]) -> list[dict]:
    """Where the medallion's printed number is not the āyah's position."""
    slips = []
    for s in surahs:
        n = 0
        for w, printed in zip((w for w in s.words if w == AYAH_SIGN), s.printed_numbers):
            n += 1
            if printed != n:
                slips.append({"surah": s.index, "ayah": n, "printed": printed})
    return slips


def word_colors(surahs: list[Surah]) -> list[tuple[int, int, frozenset[str]]]:
    """``(surah, word position among non-mark words, colours)`` for every coloured word."""
    out = []
    for s in surahs:
        pos = 0
        for w, c in zip(s.words, s.colors):
            if w == AYAH_SIGN:
                continue
            pos += 1
            if c:
                out.append((s.index, pos, c))
    return out
