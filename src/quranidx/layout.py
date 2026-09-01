"""Kalimah-level safhah and line, read from the KFGQPC ``.docx`` releases.

The v2 CSVs give ``safhah`` and ``line_start``/``line_end`` per *ayah*, which is
too coarse to place a kalimah: an ayah routinely spans several lines and, at a safhah
turn, two safhahs.  The ``.docx`` releases carry the typesetting itself, so the
position of every kalimah is recoverable from them directly.

Two things are recovered, and they are **not** equally sound:

**Safhah is read.**  Every release marks its safhah turns explicitly — 603
``<w:br w:type="page"/>`` elements, giving 604 safhahs — so a kalimah's safhah is a
fact taken from the file, not a guess.  It agrees with the v2 CSV on all 6,236
Ḥafṣ ayahs, and it is present in all seven packages including Bazzī, which has no
CSV at all.

**Line is reconstructed.**  Printed lines are *not* encoded.  What the document
has is line breaks, paragraph boundaries and headings, from which the printed
line can be inferred but not read:

    line breaks alone .................... 5,079 / 6,236 ayahs
    + paragraph boundaries ............... 6,131 / 6,236 ayahs   ← shipped

The residual 105 overshoot by one or two on safhahs the publisher sets specially —
Al-Fātiḥah above all, whose frame the flow does not describe.  Every emitted
line is therefore marked derived, and :func:`line_disagreements` re-checks the
reconstruction against the CSV so the exact residual travels with the data
rather than living in a commit message.  Bazzī has no CSV, so its lines cannot
be checked at all; that too is stated rather than glossed.

See ``docs/ISSUES.md`` §"Reconstructed lines".
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path

from . import chars
from .sources import _AYAH_MARK, _TRAILING_HEAD, _is_heading

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

#: A surah heading occupies a printed line of its own.  The paragraph carrying
#: it is skipped for text, so the line it uses has to be added back by hand.
HEADING_LINES = 1


@dataclass(frozen=True)
class Place:
    """Where one kalimah sits in the printed mushaf."""

    safhah: int
    line: int


def _placed_paragraphs(path: Path) -> list[list[tuple[str, int, int]]]:
    """Every paragraph as a list of ``(char, safhah, line)``, in document order.

    Position is tracked per *character*, not per paragraph.  These releases set
    the whole mushaf in a few hundred paragraphs — Ḥafṣ uses 342 for 604 safhahs —
    and move the safhah with ``<w:br>`` elements *inside* them, so a paragraph's
    starting safhah says almost nothing about where its kalimahs are printed.
    """
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))

    out: list[list[tuple[str, int, int]]] = []
    state = {"safhah": 1, "line": 1, "first": True}

    def walk(node, sink) -> None:
        for el in node:
            tag = el.tag
            if tag == W + "p":
                if not state["first"]:
                    state["line"] += 1
                state["first"] = False
                para: list[tuple[str, int, int]] = []
                walk(el, para)
                out.append(para)
                if _is_heading("".join(c for c, _, _ in para)):
                    state["line"] += HEADING_LINES
            elif tag == W + "br":
                if el.get(W + "type") == "page":
                    state["safhah"] += 1
                    state["line"] = 1
                    state["first"] = True
                else:
                    state["line"] += 1
            elif tag == W + "t":
                for ch in (el.text or ""):
                    sink.append((ch, state["safhah"], state["line"]))
            else:
                walk(el, sink)

    walk(root[0], [])
    return out


def _clean(para: list[tuple[str, int, int]]) -> list[tuple[str, int, int]]:
    """Apply the same filtering :func:`sources.load_docx` applies, positionally.

    Each transform is done on the ``(char, safhah, line)`` list rather than on a
    string, so a character's position survives every edit.  The regexes are run
    against the string built from the list, whose indices correspond to it
    one-for-one.
    """
    # strip_controls: drop controls and kashida, fold NBSP to a plain space.
    out = [(" " if c in (" ", "\u00a0") else c, p, l)
           for c, p, l in para
           if c not in chars.CONTROLS and c != chars.TATWEEL]

    # A surah heading stranded at the end of a paragraph belongs to no ayah.
    text = "".join(c for c, _, _ in out)
    m = _TRAILING_HEAD.search(text)
    if m:
        out = out[:m.start(1)]

    # Ayah marks are not kalimahs.  Replacing them with a space rather than
    # deleting them keeps the tokens on either side apart.
    text = "".join(c for c, _, _ in out)
    keep: list[tuple[str, int, int]] = []
    at = 0
    for m in _AYAH_MARK.finditer(text):
        keep.extend(out[at:m.start()])
        keep.append((" ", *out[m.start()][1:]))
        at = m.end()
    keep.extend(out[at:])
    return keep


def _tokens_with_places(para: list[tuple[str, int, int]]) -> list[tuple[str, Place]]:
    """Split one cleaned paragraph into tokens, each at its first character."""
    out: list[tuple[str, Place]] = []
    buf: list[str] = []
    start: Place | None = None
    for ch, safhah, line in para:
        if ch.isspace():
            if buf:
                out.append(("".join(buf), start))
                buf, start = [], None
            continue
        if not buf:
            start = Place(safhah, line)
        buf.append(ch)
    if buf:
        out.append(("".join(buf), start))
    return out


def _scripture(path: Path) -> list[tuple[str, Place]]:
    out: list[tuple[str, Place]] = []
    for para in _placed_paragraphs(path):
        if _is_heading("".join(c for c, _, _ in para)):
            continue
        out.extend(_tokens_with_places(_clean(para)))
    return out


def kalimah_places(path: Path) -> list[Place]:
    """A :class:`Place` for every scripture token, in document order.

    The token sequence is the same one :func:`quranidx.sources.load_docx`
    produces, filtered the same way, so the two can be zipped by index.  That
    equivalence is asserted rather than assumed — see
    :func:`quranidx.validate.check_layout_alignment`.
    """
    return [place for _, place in _scripture(path)]


def raw_tokens(path: Path) -> list[str]:
    """The token sequence :func:`kalimah_places` positions, for cross-checking."""
    return [tok for tok, _ in _scripture(path)]
