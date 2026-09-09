"""quran-text — read the muṣḥaf files of the quran-text dataset.

    from quran_text import Mushaf
    m = Mushaf.hafs()                         # bundled; or Mushaf.load("data/mushaf/warsh.json")
    m.ayah(2, 255).text                       # plain words
    m.ayah(2, 255).render(marks=True, ayah_marks=True)
    m.page(3).lines                           # the printed lines
    m.juz(30).first_ayah.key                  # "78:1"

Everything is a slice of one ``words`` array.  A :class:`Span` is a slice with
``text`` and ``render``; :class:`Surah`, :class:`Ayah`, :class:`Page`,
:class:`Line` and :class:`Juz` are spans that know their place.  Positions are
0-based indices into ``words``; sūrah, āyah, page, line and juz numbers are
1-based, as printed.  Āyah numbers are in *this edition's own count*; use
:class:`AyahMap` to convert between editions.

No dependencies.  Python 3.9+.
"""

from __future__ import annotations

import json
from pathlib import Path
from bisect import bisect_right
from dataclasses import dataclass
from typing import Iterable, Optional, Union

__all__ = ["Mushaf", "Surah", "Ayah", "Page", "Line", "Juz", "Word", "Mark", "Font", "AyahMatch",
           "Span", "AyahMap", "MappedAyah", "WordIndex", "IndexedWord",
           "ayah_mark", "fold", "Layer"]

AYAH_MARK = "۝"
Layer = str  # "surahs" | "ayahs" | "pages" | "lines" | "juz" | "marks" | "rasm_imlai"


# --- text helpers ------------------------------------------------------------

_ARABIC_INDIC = "٠١٢٣٤٥٦٧٨٩"


def ayah_mark(number: int) -> str:
    """The end-of-āyah sign with its number, as the muṣḥaf prints it: ``۝٢٥٥``."""
    return AYAH_MARK + "".join(_ARABIC_INDIC[int(d)] for d in str(number))


_FOLD_ALEF = "ٱأإآ" + "".join(chr(c) for c in range(0x0870, 0x0883))
_FOLD_YEH = "ےۑى"


def fold(text: str) -> str:
    """Reduce a word to plain letters for matching: no harakah, no waqf marks,
    one alif, one yāʾ.  For search only — it is not a spelling of anything."""
    out = []
    for ch in text:
        cp = ord(ch)
        if ch == "ٰ":                  # superscript alif -> alif
            out.append("ا")
        elif ch in _FOLD_ALEF:
            out.append("ا")
        elif ch in _FOLD_YEH:
            out.append("ي")
        elif ch == "ـ":                # tatweel
            continue
        elif (0x0610 <= cp <= 0x061A or 0x064B <= cp <= 0x065F
              or 0x06D6 <= cp <= 0x06DC or 0x06DF <= cp <= 0x06E8
              or 0x06EA <= cp <= 0x06ED or 0x08CA <= cp <= 0x08FF
              or cp == 0x0888):
            continue
        else:
            out.append(ch)
    return "".join(out)


def _index_of(starts: list, position: int) -> int:
    """Index of the unit that contains ``position`` (-1 before the first)."""
    return bisect_right(starts, position) - 1


# --- records -----------------------------------------------------------------

@dataclass(frozen=True)
class Font:
    """The KFGQPC font this muṣḥaf's text is set in — the only one guaranteed
    to draw every codepoint the words use.  ``path`` is the file when the
    library has it (bundled for Ḥafṣ, or ``data/fonts/`` next to a loaded
    file); ``None`` otherwise."""
    family: str
    file: str
    sha256: str
    publisher: str
    path: Optional[Path] = None


@dataclass(frozen=True)
class Mark:
    """A sign printed against a word: ``kind`` is waqf, division, sajdah or
    sajdah_line; ``side`` is where it is printed."""
    kind: str
    side: str
    sign: str


class Word:
    """One printed word and everything the muṣḥaf says about it."""

    __slots__ = ("_m", "position")

    def __init__(self, mushaf: "Mushaf", position: int):
        if not 0 <= position < len(mushaf.words):
            raise IndexError(f"position {position} is outside the muṣḥaf")
        self._m = mushaf
        self.position = position

    @property
    def text(self) -> str:
        return self._m.words[self.position]

    @property
    def rasm_imlai(self) -> Optional[str]:
        """Plain modern spelling, Ḥafṣ only; ``None`` elsewhere."""
        col = self._m._doc["rasm_imlai"]
        return col[self.position] if col else None

    @property
    def surah(self) -> "Surah":
        return self._m.surahs[_index_of(self._m._doc["surah_starts"], self.position)]

    @property
    def ayah(self) -> Optional["Ayah"]:
        """The āyah this word is in; ``None`` for the unnumbered basmalah."""
        return self._m.ayah_at(self.position)

    @property
    def index(self) -> Optional[int]:
        """1-based position within the āyah; ``None`` when unnumbered."""
        a = self.ayah
        return None if a is None else self.position - a.start + 1

    @property
    def page(self) -> "Page":
        return self._m.page_at(self.position)

    @property
    def line(self) -> Optional["Line"]:
        return self._m.line_at(self.position)

    @property
    def juz(self) -> Optional["Juz"]:
        return self._m.juz_at(self.position)

    @property
    def number(self) -> int:
        """The shared number: the same word in every riwāyah."""
        return self._m._numbers[self.position][0]

    @property
    def number_last(self) -> int:
        """Equal to ``number`` except where this muṣḥaf writes two numbers as one word."""
        return self._m._numbers[self.position][1]

    @property
    def marks(self) -> list[Mark]:
        return self._m._marks_at.get(self.position, [])

    def has_mark(self, kind: str) -> bool:
        return any(mk.kind == kind for mk in self.marks)

    def to(self, other: "Mushaf") -> Optional["Word"]:
        """The same word in another riwāyah, by the shared number; ``None``
        where that riwāyah does not read it."""
        return other.word_by_number(self.number)

    def render(self, marks: Union[bool, Iterable[str]] = True) -> str:
        """The word with its signs: ``۞`` before, waqf, the sajdah line and
        ``۩`` after."""
        kinds = _mark_kinds(marks)
        before = "".join(mk.sign + " " for mk in self.marks
                         if mk.side == "before" and mk.kind in kinds)
        after = "".join(mk.sign for mk in self.marks
                        if mk.side == "after" and mk.kind in kinds)
        return before + self.text + after

    def __repr__(self) -> str:
        return f"Word({self.position}, {self.text!r})"

    def __str__(self) -> str:
        return self.text


_ALL_KINDS = frozenset({"waqf", "division", "sajdah", "sajdah_line"})


def _mark_kinds(marks: Union[bool, Iterable[str]]) -> frozenset:
    if marks is True:
        return _ALL_KINDS
    if not marks:
        return frozenset()
    return frozenset(marks)


class Span:
    """A run of positions ``start … end-1`` of one muṣḥaf."""

    def __init__(self, mushaf: "Mushaf", start: int, end: int):
        self._m = mushaf
        self.start = start
        self.end = end

    @property
    def mushaf(self) -> "Mushaf":
        return self._m

    @property
    def words(self) -> list[str]:
        return self._m.words[self.start:self.end]

    @property
    def word_list(self) -> list[Word]:
        return [Word(self._m, p) for p in range(self.start, self.end)]

    @property
    def text(self) -> str:
        """The words joined with spaces, without any sign."""
        return " ".join(self.words)

    def render(self, marks: Union[bool, Iterable[str]] = False,
               ayah_marks: bool = False, lines: bool = False) -> str:
        """The text as the muṣḥaf prints it, with what you ask for.

        ``marks``: ``True`` for every sign, or a set of kinds among
        ``"waqf"``, ``"division"``, ``"sajdah"``, ``"sajdah_line"``.
        ``ayah_marks`` appends
        ``۝`` with the āyah number after each āyah that ends inside the span.
        ``lines`` breaks the text where the printed lines break.
        """
        m = self._m
        kinds = _mark_kinds(marks)
        ayah_ends = m._ayah_ends if ayah_marks else None
        line_starts = set(m._doc.get("line_starts") or []) if lines else None
        out: list[str] = []
        for position in range(self.start, self.end):
            if line_starts is not None and position in line_starts and position != self.start:
                out.append("\n")
            elif out:
                out.append(" ")
            token = m.words[position]
            for mk in m._marks_at.get(position, ()):
                if mk.kind not in kinds:
                    continue
                if mk.side == "before":
                    token = mk.sign + " " + token
                else:
                    token = token + mk.sign
            out.append(token)
            if ayah_ends is not None:
                k = ayah_ends.get(position)
                if k is not None:
                    out.append(" " + ayah_mark(m._ayah_number(k)))
        return "".join(out)

    @property
    def ayahs(self) -> list["Ayah"]:
        """Every numbered āyah with at least one word in the span."""
        m = self._m
        first = _index_of(m._doc["ayah_starts"], self.start)
        last = _index_of(m._doc["ayah_starts"], self.end - 1)
        return [Ayah._from_index(m, k) for k in range(max(first, 0), last + 1)]

    @property
    def first_ayah(self) -> Optional["Ayah"]:
        a = self.ayahs
        return a[0] if a else None

    @property
    def last_ayah(self) -> Optional["Ayah"]:
        a = self.ayahs
        return a[-1] if a else None

    @property
    def surahs(self) -> list["Surah"]:
        s = self._m.surahs
        first = _index_of(self._m._doc["surah_starts"], self.start)
        last = _index_of(self._m._doc["surah_starts"], self.end - 1)
        return s[first:last + 1]

    @property
    def pages(self) -> list["Page"]:
        m = self._m
        first = _index_of(m._doc["page_starts"], self.start)
        last = _index_of(m._doc["page_starts"], self.end - 1)
        return [Page(m, n + 1) for n in range(first, last + 1)]

    @property
    def page(self) -> "Page":
        """The page the span starts on."""
        return self._m.page_at(self.start)

    @property
    def juz(self) -> Optional["Juz"]:
        return self._m.juz_at(self.start)

    @property
    def marks(self) -> list[tuple[Word, Mark]]:
        """Every sign inside the span, with the word it is printed on."""
        m = self._m
        return [(Word(m, p), mk) for p in range(self.start, self.end)
                for mk in m._marks_at.get(p, ())]

    def word(self, index: int) -> Word:
        """The ``index``-th word of the span, 1-based."""
        if not 1 <= index <= len(self):
            raise IndexError(f"word {index} of {self!r}: it has {len(self)} words")
        return Word(self._m, self.start + index - 1)

    def __len__(self) -> int:
        return self.end - self.start

    def __iter__(self):
        return iter(self.word_list)

    def __repr__(self) -> str:
        return f"Span({self.start}, {self.end})"


@dataclass(frozen=True)
class AyahMatch:
    """Where an āyah falls in another riwāyah.  ``relation``: ``same`` (one
    āyah, the same words), ``merged`` (one āyah holding more), ``split``
    (several āyāt), ``shifted`` (one āyah, boundaries crossing), ``unnumbered``
    (the basmalah printed without a number), ``missing`` (no word of it)."""
    ayahs: tuple
    relation: str

    @property
    def first(self) -> Optional["Ayah"]:
        return self.ayahs[0] if self.ayahs else None

    @property
    def last(self) -> Optional["Ayah"]:
        return self.ayahs[-1] if self.ayahs else None

    @property
    def key(self) -> str:
        """``"2:253-254"``."""
        if not self.ayahs:
            return ""
        a, b = self.ayahs[0], self.ayahs[-1]
        return a.key if a is b or a == b else f"{a.key}-{b.number}"

    def __repr__(self) -> str:
        return f"AyahMatch({self.key or '-'}, {self.relation})"


class Ayah(Span):
    """One numbered āyah, in this edition's own count."""

    def __init__(self, mushaf: "Mushaf", surah: int, number: int):
        s = mushaf.surah(surah)
        if not 1 <= number <= s.ayah_count:
            raise IndexError(f"{s.name_en} has {s.ayah_count} āyāt in "
                             f"{mushaf.name_en}, not {number}")
        self.surah = s
        self.number = number
        self._k = s._first_ayah + number - 1
        starts = mushaf._doc["ayah_starts"]
        end = starts[self._k + 1] if self._k + 1 < len(starts) else len(mushaf.words)
        super().__init__(mushaf, starts[self._k], end)

    @classmethod
    def _from_index(cls, mushaf: "Mushaf", k: int) -> "Ayah":
        s = mushaf.surahs[mushaf._surah_of_ayah_index(k)]
        return cls(mushaf, s.number, k - s._first_ayah + 1)

    @property
    def key(self) -> str:
        """``"2:255"``."""
        return f"{self.surah.number}:{self.number}"

    @property
    def index(self) -> int:
        """0-based index into ``ayah_starts``: the āyah's ordinal in the muṣḥaf."""
        return self._k

    @property
    def line(self) -> Optional[Line]:
        """The printed line the āyah starts on."""
        return self._m.line_at(self.start)

    @property
    def lines(self) -> list[Line]:
        """Every printed line the āyah touches."""
        m = self._m
        if not m.has("lines"):
            return []
        starts = m._doc["line_starts"]
        first = _index_of(starts, self.start)
        last = _index_of(starts, self.end - 1)
        return [Line._from_index(m, i) for i in range(first, last + 1)]

    @property
    def rasm_imlai(self) -> Optional[list[Optional[str]]]:
        col = self._m._doc["rasm_imlai"]
        return col[self.start:self.end] if col else None

    @property
    def has_sajdah(self) -> bool:
        return any(mk.kind == "sajdah" for _, mk in self.marks)

    @property
    def marker(self) -> str:
        """``۝٢٥٥``."""
        return ayah_mark(self.number)

    @property
    def numbers(self) -> frozenset:
        """The shared numbers of this āyah's words."""
        m = self._m
        first, last = m._numbers[self.start][0], m._numbers[self.end - 1][1]
        return frozenset(range(first, last + 1)) - m.missing_numbers

    def to(self, other: "Mushaf") -> AyahMatch:
        """This āyah in another riwāyah: ``hafs.ayah(2, 255).to(warsh)`` →
        ``AyahMatch(2:253-254, split)``.  Computed from the shared numbering,
        so it works between any two riwāyāt and agrees with ``ayah-map.json``."""
        mine = self.numbers
        hits: list = []
        unnumbered = False
        for n in sorted(mine):
            w = other.word_by_number(n)
            if w is None:
                continue
            a = w.ayah
            if a is None:
                unnumbered = True
            elif not hits or hits[-1] != a:
                hits.append(a)
        if unnumbered and not hits:
            return AyahMatch((), "unnumbered")
        if not hits:
            return AyahMatch((), "missing")
        if len(hits) > 1:
            return AyahMatch(tuple(hits), "split")
        theirs = hits[0].numbers
        relation = "same" if theirs == mine else "merged" if theirs > mine else "shifted"
        return AyahMatch(tuple(hits), relation)

    def next(self) -> Optional["Ayah"]:
        k = self._k + 1
        return Ayah._from_index(self._m, k) if k < self._m.ayah_count else None

    def previous(self) -> Optional["Ayah"]:
        k = self._k - 1
        return Ayah._from_index(self._m, k) if k >= 0 else None

    def __eq__(self, other) -> bool:
        return (isinstance(other, Ayah) and other._m is self._m
                and other._k == self._k)

    def __hash__(self) -> int:
        return hash((id(self._m), self._k))

    def __repr__(self) -> str:
        return f"Ayah({self.key})"


class Surah(Span):
    def __init__(self, mushaf: "Mushaf", number: int):
        if not 1 <= number <= 114:
            raise IndexError(f"sūrah {number}: there are 114")
        info = mushaf._doc["surahs"][number - 1]
        starts = mushaf._doc["surah_starts"]
        end = starts[number] if number < len(starts) else len(mushaf.words)
        super().__init__(mushaf, starts[number - 1], end)
        self.number = number
        self.name_ar: str = info["name_ar"]
        self.name_en: str = info["name_en"]
        self.revelation: str = info["revelation"]
        self.has_basmalah: bool = info["has_basmalah"]
        self.ayah_count: int = info["ayah_count"]
        self._first_ayah: int = info["first_ayah"]

    @property
    def ayahs(self) -> list[Ayah]:
        return [Ayah(self._m, self.number, n) for n in range(1, self.ayah_count + 1)]

    def ayah(self, number: int) -> Ayah:
        return Ayah(self._m, self.number, number)

    @property
    def basmalah(self) -> Optional[Span]:
        """The basmalah where it is printed unnumbered before āyah 1 (Warsh,
        Qālūn, Dūrī, Sūsī at al-Fātiḥah); ``None`` otherwise."""
        first = self._m._doc["ayah_starts"][self._first_ayah]
        return Span(self._m, self.start, first) if first > self.start else None

    @property
    def first_page(self) -> Page:
        return self.page

    @property
    def last_page(self) -> Page:
        return self._m.page_at(self.end - 1)

    def __repr__(self) -> str:
        return f"Surah({self.number}, {self.name_en})"


class Page(Span):
    def __init__(self, mushaf: "Mushaf", number: int):
        starts = mushaf._doc["page_starts"]
        if not 1 <= number <= len(starts):
            raise IndexError(f"page {number}: {mushaf.name_en} has {len(starts)} pages")
        end = starts[number] if number < len(starts) else len(mushaf.words)
        super().__init__(mushaf, starts[number - 1], end)
        self.number = number

    @property
    def lines(self) -> list[Line]:
        m = self._m
        if not m.has("lines"):
            return []
        starts = m._doc["line_starts"]
        first = _index_of(starts, self.start)
        last = _index_of(starts, self.end - 1)
        return [Line._from_index(m, i) for i in range(first, last + 1)]

    def line(self, number: int) -> Line:
        lines = self.lines
        if not 1 <= number <= len(lines):
            raise IndexError(f"line {number}: page {self.number} has {len(lines)} lines")
        return lines[number - 1]

    def next(self) -> Optional["Page"]:
        n = self.number + 1
        return Page(self._m, n) if n <= self._m.page_count else None

    def previous(self) -> Optional["Page"]:
        n = self.number - 1
        return Page(self._m, n) if n >= 1 else None

    def __repr__(self) -> str:
        return f"Page({self.number})"


class Line(Span):
    """One printed line.  Reconstructed, not read: see ``layers.derived.line``."""

    def __init__(self, mushaf: "Mushaf", page: Page, number: int, index: int):
        starts = mushaf._doc["line_starts"]
        end = starts[index + 1] if index + 1 < len(starts) else len(mushaf.words)
        super().__init__(mushaf, starts[index], end)
        self._page = page
        self.number = number          # within the page, 1-based
        self.index = index            # within the muṣḥaf, 0-based

    @property
    def page(self) -> Page:
        return self._page

    @classmethod
    def _from_index(cls, mushaf: "Mushaf", index: int) -> "Line":
        starts = mushaf._doc["line_starts"]
        page = mushaf.page_at(starts[index])
        first = _index_of(starts, page.start)
        return cls(mushaf, page, index - first + 1, index)

    def __repr__(self) -> str:
        return f"Line(page {self.page.number}, line {self.number})"


class Juz(Span):
    def __init__(self, mushaf: "Mushaf", number: int):
        starts = mushaf._doc.get("juz_starts")
        if not starts:
            raise KeyError(mushaf._absent("juz"))
        if not 1 <= number <= len(starts):
            raise IndexError(f"juz {number}: there are {len(starts)}")
        end = starts[number] if number < len(starts) else len(mushaf.words)
        super().__init__(mushaf, starts[number - 1], end)
        self.number = number

    def __repr__(self) -> str:
        return f"Juz({self.number})"


# --- the muṣḥaf ---------------------------------------------------------------

class Mushaf:
    """One muṣḥaf file, ``data/mushaf/<key>.json``."""

    def __init__(self, doc: dict):
        if doc.get("format") != "quran-mushaf":
            raise ValueError("not a quran-mushaf file")
        self._doc = doc
        self.words: list[str] = doc["words"]
        info = doc["mushaf"]
        self.key: str = info["key"]
        self.name_en: str = info["name_en"]
        self.name_ar: str = info["name_ar"]
        self.qiraah_en: Optional[str] = info.get("qiraah_en")
        self.qiraah_ar: Optional[str] = info.get("qiraah_ar")
        self.counting_system: str = doc["counting"]["system"]
        self.basmalah_counted: bool = doc["counting"]["basmalah_counted"]
        self.surahs: list[Surah] = [Surah(self, n) for n in range(1, 115)]
        self._surah_first_ayah = [s._first_ayah for s in self.surahs]
        self._ayah_ends = {}
        starts = doc["ayah_starts"]
        for k, st in enumerate(starts):
            end = starts[k + 1] if k + 1 < len(starts) else len(self.words)
            self._ayah_ends[end - 1] = k
        types = [Mark(t["kind"], t["side"], t["sign"]) for t in doc["mark_types"]]
        self._marks_at: dict[int, list[Mark]] = {}
        for position, t in doc["marks"]:
            self._marks_at.setdefault(position, []).append(types[t])
        self._numbers_cache: Optional[list[tuple[int, int]]] = None

    # -- loading --

    @classmethod
    def hafs(cls) -> "Mushaf":
        """Ḥafṣ, the riwāyah nearly every app uses, bundled with the library
        together with its font."""
        return cls.load(Path(__file__).parent / "quran_text_data" / "hafs.json")

    @classmethod
    def load(cls, path) -> "Mushaf":
        """Any of the seven riwāyāt: ``data/mushaf/<key>.json``."""
        with open(path, encoding="utf-8") as f:
            m = cls(json.load(f))
        m._dir = Path(path).resolve().parent
        return m

    _dir: Optional[Path] = None

    @property
    def font(self) -> Font:
        """The font to ship with this text; see :class:`Font`."""
        f = self._doc["font"]
        name = f["file"].rsplit("/", 1)[-1]
        path = None
        if self._dir is not None:
            for candidate in (self._dir / name, self._dir.parent / "fonts" / name):
                if candidate.exists():
                    path = candidate
                    break
        return Font(f["family"], f["file"], f["sha256"], f["publisher"], path)

    @classmethod
    def from_json(cls, data: Union[str, bytes, dict]) -> "Mushaf":
        if isinstance(data, (str, bytes)):
            data = json.loads(data)
        return cls(data)

    # -- what the file carries --

    @property
    def layers(self) -> list[str]:
        return list(self._doc["layers"]["present"])

    def has(self, layer: Layer) -> bool:
        """``has("juz")``, ``has("rasm_imlai")``, ``has("lines")`` …"""
        return layer in self._doc["layers"]["present"]

    def _absent(self, layer: str) -> str:
        why = self._doc["layers"]["absent"].get(layer, "not in this file")
        return f"{self.name_en} has no {layer} layer: {why}"

    @property
    def counting(self) -> dict:
        return self._doc["counting"]

    @property
    def provenance(self) -> dict:
        return self._doc["provenance"]

    @property
    def word_count(self) -> int:
        return len(self.words)

    @property
    def ayah_count(self) -> int:
        return len(self._doc["ayah_starts"])

    @property
    def page_count(self) -> int:
        return len(self._doc["page_starts"])

    @property
    def line_count(self) -> int:
        return len(self._doc.get("line_starts") or [])

    @property
    def juz_count(self) -> int:
        return len(self._doc.get("juz_starts") or [])

    # -- units by number --

    def surah(self, number: int) -> Surah:
        if not 1 <= number <= 114:
            raise IndexError(f"sūrah {number}: there are 114")
        return self.surahs[number - 1]

    def ayah(self, surah: int, number: int) -> Ayah:
        """Āyah ``number`` of ``surah`` in this edition's own count."""
        return Ayah(self, surah, number)

    def page(self, number: int) -> Page:
        return Page(self, number)

    def juz(self, number: int) -> Juz:
        return Juz(self, number)

    def line(self, page: int, number: int) -> Line:
        return Page(self, page).line(number)

    def word(self, surah: int, ayah: int, index: int) -> Word:
        """Word ``index`` (1-based) of an āyah."""
        return Ayah(self, surah, ayah).word(index)

    def span(self, start: int, end: int) -> Span:
        """Any run of positions, e.g. to render a selection."""
        if not 0 <= start < end <= len(self.words):
            raise IndexError(f"span {start}:{end} is outside the muṣḥaf")
        return Span(self, start, end)

    @property
    def all(self) -> Span:
        return Span(self, 0, len(self.words))

    @property
    def ayahs(self) -> list[Ayah]:
        return [Ayah._from_index(self, k) for k in range(self.ayah_count)]

    @property
    def pages(self) -> list[Page]:
        return [Page(self, n) for n in range(1, self.page_count + 1)]

    @property
    def ajza(self) -> list[Juz]:
        return [Juz(self, n) for n in range(1, self.juz_count + 1)]

    # -- units by position --

    def word_at(self, position: int) -> Word:
        return Word(self, position)

    def ayah_at(self, position: int) -> Optional[Ayah]:
        k = _index_of(self._doc["ayah_starts"], position)
        return Ayah._from_index(self, k) if k >= 0 else None

    def surah_at(self, position: int) -> Surah:
        return self.surahs[_index_of(self._doc["surah_starts"], position)]

    def page_at(self, position: int) -> Page:
        return Page(self, _index_of(self._doc["page_starts"], position) + 1)

    def line_at(self, position: int) -> Optional[Line]:
        starts = self._doc.get("line_starts")
        return Line._from_index(self, _index_of(starts, position)) if starts else None

    def juz_at(self, position: int) -> Optional[Juz]:
        starts = self._doc.get("juz_starts")
        return Juz(self, _index_of(starts, position) + 1) if starts else None

    # -- the shared numbering --

    @property
    def _numbers(self) -> list[tuple[int, int]]:
        if self._numbers_cache is None:
            block = self._doc["numbering"]
            missing = set(block["missing"])
            joined = {j["position"]: tuple(j["numbers"]) for j in block["written_joined"]}
            runs, n = [], 1
            for position in range(len(self.words)):
                while n in missing:
                    n += 1
                first, last = joined.get(position, (n, n))
                runs.append((first, last))
                n = last + 1
            self._numbers_cache = runs
        return self._numbers_cache

    @property
    def missing_numbers(self) -> frozenset:
        """The shared numbers this riwāyah does not read."""
        return frozenset(self._doc["numbering"]["missing"])

    def number_at(self, position: int) -> int:
        """The shared number of the word at ``position``."""
        return self._numbers[position][0]

    def word_by_number(self, number: int) -> Optional[Word]:
        """The printed word carrying a shared number; ``None`` where this
        muṣḥaf does not read it."""
        runs = self._numbers
        i = bisect_right(runs, (number, float("inf"))) - 1
        if i >= 0 and runs[i][0] <= number <= runs[i][1]:
            return Word(self, i)
        return None

    # -- signs and search --

    def sajdat(self) -> list[Ayah]:
        """Every āyah printed with ``۩``."""
        return [Word(self, p).ayah for p, ms in sorted(self._marks_at.items())
                if any(mk.kind == "sajdah" for mk in ms)]

    def division_marks(self) -> list[Word]:
        """Every word printed with ``۞`` before it, as the release prints them."""
        return [Word(self, p) for p, ms in sorted(self._marks_at.items())
                if any(mk.kind == "division" for mk in ms)]

    def search(self, text: str) -> list[Span]:
        """Every place the words of ``text`` occur in sequence, matched on
        :func:`fold` — harakah and hamzah forms do not matter."""
        query = [fold(t) for t in text.split()]
        if not query or not all(query):
            return []
        if self._fold_cache is None:
            self._fold_cache = [fold(w) for w in self.words]
        folded = self._fold_cache
        n, first = len(query), query[0]
        return [Span(self, i, i + n) for i in range(len(folded) - n + 1)
                if folded[i] == first and folded[i:i + n] == query]

    _fold_cache: Optional[list[str]] = None

    # -- internals --

    def _surah_of_ayah_index(self, k: int) -> int:
        return bisect_right(self._surah_first_ayah, k) - 1

    def _ayah_number(self, k: int) -> int:
        return k - self._surah_first_ayah[self._surah_of_ayah_index(k)] + 1

    def __repr__(self) -> str:
        return f"Mushaf({self.key})"


# --- āyah map ----------------------------------------------------------------

@dataclass(frozen=True)
class MappedAyah:
    """Where a Kūfī āyah falls in one edition.  ``relation`` is ``same``,
    ``merged``, ``split`` (then ``ayah_last`` is set), ``shifted`` or
    ``unnumbered`` (``ayah`` is 0)."""
    surah: int
    ayah: int
    relation: str
    ayah_last: Optional[int] = None

    @property
    def key(self) -> str:
        if self.ayah_last:
            return f"{self.surah}:{self.ayah}-{self.ayah_last}"
        return f"{self.surah}:{self.ayah}"


class AyahMap:
    """``data/ayah-map.json``: what a Ḥafṣ (Kūfī) reference is in every edition."""

    def __init__(self, doc: dict):
        if doc.get("format") != "quran-ayah-map":
            raise ValueError("not a quran-ayah-map file")
        self.editions: list[str] = doc["editions"]
        self._rows = {(r["surah"], r["ayah"]): r for r in doc["ayahs"]}

    @classmethod
    def load(cls, path) -> "AyahMap":
        with open(path, encoding="utf-8") as f:
            return cls(json.load(f))

    @classmethod
    def from_json(cls, data: Union[str, bytes, dict]) -> "AyahMap":
        if isinstance(data, (str, bytes)):
            data = json.loads(data)
        return cls(data)

    def convert(self, surah: int, ayah: int, to: str) -> MappedAyah:
        """``convert(2, 255, "warsh")`` → ``MappedAyah(2, 253, "split", 254)``."""
        row = self._rows.get((surah, ayah))
        if row is None:
            raise KeyError(f"{surah}:{ayah} is not a Kūfī āyah")
        if to not in row:
            raise KeyError(f"no edition {to!r}; editions are {self.editions}")
        r = row[to]
        return MappedAyah(r["surah"], r["ayah"], r["relation"], r.get("ayah_last"))

    def all(self, surah: int, ayah: int) -> dict[str, MappedAyah]:
        """The reference in every edition."""
        return {e: self.convert(surah, ayah, e) for e in self.editions}


# --- word index --------------------------------------------------------------

class IndexedWord:
    """One record of ``data/word-index.json``: a shared number and what it is."""

    __slots__ = ("_r",)

    def __init__(self, record: dict):
        self._r = record

    number = property(lambda s: s._r["number"])
    surah = property(lambda s: s._r["surah"])
    index = property(lambda s: s._r["index"])
    key = property(lambda s: s._r["key"])
    rasm_uthmani = property(lambda s: s._r["rasm_uthmani"])
    plain = property(lambda s: s._r["plain"])
    rasm = property(lambda s: s._r["rasm"])
    pointed = property(lambda s: s._r["pointed"])
    status = property(lambda s: s._r["status"])
    hafs = property(lambda s: s._r["hafs"])
    ayah = property(lambda s: s._r["ayah"])
    forms = property(lambda s: s._r["forms"])
    groups = property(lambda s: s._r.get("groups", []))
    missing = property(lambda s: s._r.get("missing", []))
    written_joined = property(lambda s: s._r.get("written_joined", []))

    def form(self, riwayah: str) -> Optional[str]:
        """How one riwāyah spells it; ``None`` where it does not read the word."""
        return self._r["forms"].get(riwayah)

    @property
    def raw(self) -> dict:
        return self._r

    def __repr__(self) -> str:
        return f"IndexedWord({self.number}, {self.rasm_uthmani!r})"


class WordIndex:
    """``data/word-index.json``: the numbering shared by all seven muṣḥafs."""

    def __init__(self, doc: dict):
        if doc.get("format") != "quran-word-index":
            raise ValueError("not a quran-word-index file")
        self.mushafs: list[str] = doc["mushafs"]
        self.total: int = doc["total"]
        self._words = doc["words"]
        self._by_hafs: Optional[dict] = None
        self._by_plain: Optional[dict] = None

    @classmethod
    def load(cls, path) -> "WordIndex":
        with open(path, encoding="utf-8") as f:
            return cls(json.load(f))

    @classmethod
    def from_json(cls, data: Union[str, bytes, dict]) -> "WordIndex":
        if isinstance(data, (str, bytes)):
            data = json.loads(data)
        return cls(data)

    def word(self, number: int) -> IndexedWord:
        if not 1 <= number <= self.total:
            raise IndexError(f"number {number}: the numbering is 1 … {self.total}")
        return IndexedWord(self._words[number - 1])

    def find(self, surah: int, ayah: int, index: int) -> Optional[IndexedWord]:
        """By Ḥafṣ coordinates: sūrah, āyah in the Kūfī count, 1-based word."""
        if self._by_hafs is None:
            self._by_hafs = {}
            for r in self._words:
                h = r["hafs"]
                if h:
                    self._by_hafs.setdefault((h["surah"], h["ayah"], h["position"]), r)
        r = self._by_hafs.get((surah, ayah, index))
        return IndexedWord(r) if r else None

    def search(self, text: str) -> list[IndexedWord]:
        """Every number whose folded spelling equals ``text``, folded."""
        q = fold(text)
        if self._by_plain is None:
            self._by_plain = {}
            for r in self._words:
                self._by_plain.setdefault(fold(r["rasm_uthmani"]), []).append(r)
        return [IndexedWord(r) for r in self._by_plain.get(q, [])]

    def differing(self) -> list[IndexedWord]:
        """Every number the riwāyāt spell in more than one way."""
        return [IndexedWord(r) for r in self._words if "groups" in r]

    def __len__(self) -> int:
        return self.total

    def __iter__(self):
        return (IndexedWord(r) for r in self._words)
