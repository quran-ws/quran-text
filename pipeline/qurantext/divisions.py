"""The ḥizb and its subdivisions: ``hizb_starts`` and ``rubu_al_hizb_starts`` or ``thumn_starts``.

The releases cannot supply this layer alone.  A ``.docx`` prints the ۞ inline
and nothing else, and no ۞ is printed where a sūrah heading takes its place:
Ḥafṣ prints 199 of its 240 rubu_al_hizbs, Qālūn 437 marks for 480 thumns
(docs/known-issues.md §7).  The printed muṣḥaf marks every division in its
outer margin, so the ones the docx lacks were read from the print and recorded
in ``sources/divisions/``, one file per muṣḥaf, keyed by āyah.

This module puts the two together:

    the opening of the Qurʾān at 1:1
  + every inline ۞ of the docx, less any the evidence names in ``not_a_division``
  + every entry of ``margin_division_marks``

and refuses to publish unless the grid closes: the stated total, 60 ḥizbs of
4 or 8, every margin entry on a word that carries no ۞, on the page the
evidence states, and juz boundaries that differ from the layout CSV exactly
where the evidence says they do.  A muṣḥaf with no evidence file gets no
layer, and ``layers.absent`` says why.

``juz_starts`` is not touched.  It is read from the v2 CSV, because that is
what the package states (docs/known-issues.md §11).
"""

from __future__ import annotations

import hashlib
import json
from bisect import bisect_right

from .paths import ROOT, SOURCES

DIVISIONS = SOURCES / "divisions"
HIZB_COUNT = 60
#: The subdivision a muṣḥaf prints, and how many of it make one ḥizb.
PER_HIZB = {"rubu_al_hizb": 4, "thumn": 8}

NO_PRINT = ("no printed muṣḥaf of this riwāyah was read: the release prints "
            "199 of the 240 inline, and the rest are marked only in the margin")


class DivisionError(ValueError):
    """The evidence and the data do not make a closed grid."""


def evidence_path(key: str):
    found = sorted(DIVISIONS.glob(f"{key}-*.json"))
    if len(found) > 1:
        raise DivisionError(f"{key}: more than one evidence file: {[p.name for p in found]}")
    return found[0] if found else None


def _ayah_start(doc: dict, ref: str) -> int:
    surah, ayah = (int(part) for part in ref.split(":"))
    return doc["ayah_starts"][doc["surahs"][surah - 1]["first_ayah"] + ayah - 1]


def _ref(doc: dict, position: int) -> str:
    surah = bisect_right(doc["surah_starts"], position)
    ayah = bisect_right(doc["ayah_starts"], position) - doc["surahs"][surah - 1]["first_ayah"]
    return f"{surah}:{max(ayah, 1)}"     # an uncounted basmalah stands before āyah 1


def grid(doc: dict, evidence: dict) -> tuple[list[int], dict]:
    """Every division start of one muṣḥaf, in order, and how many came from where."""
    key = doc["mushaf"]["key"]
    unit, total = evidence["unit"], evidence["total"]
    if unit not in PER_HIZB or total != HIZB_COUNT * PER_HIZB[unit]:
        raise DivisionError(f"{key}: {total} {unit}s is not {HIZB_COUNT} ḥizbs")

    division = {i for i, mark in enumerate(doc["mark_types"]) if mark["kind"] == "division"}
    inline = {position for position, kind in doc["marks"] if kind in division}

    for entry in evidence.get("not_a_division", []):
        position = _ayah_start(doc, entry["ayah"])
        if position not in inline:
            raise DivisionError(f"{key}: not_a_division {entry['ayah']} carries no ۞")
        inline.discard(position)

    margin = set()
    for entry in evidence["margin_division_marks"]:
        position = _ayah_start(doc, entry["ayah"])
        if position in inline:
            raise DivisionError(f"{key}: {entry['ayah']} is listed as a margin mark "
                                "but the docx prints a ۞ there")
        page = bisect_right(doc["page_starts"], position)
        if page != entry["page"]:
            raise DivisionError(f"{key}: {entry['ayah']} is on page {page}, "
                                f"the evidence says {entry['page']}")
        margin.add(position)
    if len(margin) != len(evidence["margin_division_marks"]):
        raise DivisionError(f"{key}: an āyah is listed twice in margin_division_marks")

    starts = sorted({0} | inline | margin)
    if 0 in inline | margin or len(starts) != total:
        raise DivisionError(
            f"{key}: 1 + {len(inline)} inline + {len(margin)} margin = {len(starts)}, "
            f"not {total}")
    return starts, {"opening": 1, "inline_division_marks": len(inline),
                    "margin_division_marks": len(margin)}


def _juz_differences(doc: dict, hizb_starts: list[int]) -> list[dict]:
    """Where the print's juz, every second ḥizb, is not where the layout CSV starts one."""
    layout = doc.get("juz_starts")
    if not layout:
        return []
    return [{"juz": j + 1, "print": _ref(doc, hizb_starts[2 * j]), "layout": _ref(doc, start)}
            for j, start in enumerate(layout) if hizb_starts[2 * j] != start]


def apply(doc: dict) -> None:
    """Add the division layers to one muṣḥaf document, or say why it has none."""
    key = doc["mushaf"]["key"]
    layers = doc["layers"]
    path = evidence_path(key)
    if path is None:
        for layer in ("hizb", *PER_HIZB):
            layers["absent"][layer] = NO_PRINT
        return

    raw = path.read_bytes()
    evidence = json.loads(raw)
    if evidence["mushaf"] != key:
        raise DivisionError(f"{path.name} is for {evidence['mushaf']}, not {key}")
    unit = evidence["unit"]
    per = PER_HIZB[unit]
    starts, counts = grid(doc, evidence)
    hizb_starts = starts[::per]

    differs = _juz_differences(doc, hizb_starts)
    if differs != evidence.get("juz_differs_from_layout", []):
        raise DivisionError(
            f"{key}: the print and the layout CSV disagree about juz at {differs}, "
            f"the evidence says {evidence.get('juz_differs_from_layout', [])}")

    # Beside juz_starts, where a reader looks for it.
    ordered = {}
    for name, value in doc.items():
        ordered[name] = value
        if name == ("juz_starts" if "juz_starts" in doc else "line_starts"):
            ordered["hizb_starts"] = hizb_starts
            ordered[f"{unit}_starts"] = starts
    doc.clear()
    doc.update(ordered)

    layers["present"] += ["hizb", unit]
    other = next(name for name in PER_HIZB if name != unit)
    layers["absent"][other] = (
        f"this muṣḥaf divides the ḥizb into {per} {unit}s, not {PER_HIZB[other]} {other}s")
    layers["derived"]["divisions"] = {
        "how": "the opening at 1:1, every inline ۞ of the release, and the divisions "
               "the printed muṣḥaf marks only in its margin, read from the print and "
               "recorded in the evidence file. The build fails unless they total "
               f"{evidence['total']}. hizb_starts is every {per}th of {unit}_starts.",
        **counts,
        "not_a_division": [entry["ayah"] for entry in evidence.get("not_a_division", [])],
        "juz_differs_from_layout": differs,
    }
    if differs:
        layers["notes"]["juz"] = (
            "juz_starts is the layout CSV's; hizb_starts is the printed muṣḥaf's. "
            "They disagree at juz " + ", ".join(str(d["juz"]) for d in differs)
            + ": there hizb_starts[2·(juz−1)] is where the print starts the juz "
              "(layers.derived.divisions.juz_differs_from_layout).")
    doc["provenance"]["divisions"] = {
        "evidence": path.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "print": {name: evidence["print"][name] for name in ("file", "sha256", "from")},
        "used_for": ["hizb", unit],
    }
