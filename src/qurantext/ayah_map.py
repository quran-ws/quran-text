"""The āyah map: what a Kūfī āyah reference is in every edition.

"What is 2:255 in Warsh?" is the single most common question a consumer
switching a reader between riwāyāt has to answer, and it is derivable from the
word index — an āyah is a run of numbers, and each edition says which of its
own āyāt those numbers fall in — but derivable is not the same as shipped.

The reference is the Kūfī count as Ḥafṣ prints it, because that is what
almost every existing dataset is keyed to.  For every Kūfī āyah, each edition
gets the āyah (or run of āyāt) its words fall in and how the two relate:

| relation | meaning |
|---|---|
| ``same`` | the edition's āyah has exactly these words |
| ``merged`` | the edition's āyah also contains words of a neighbouring Kūfī āyah |
| ``split`` | the Kūfī āyah's words fall in more than one edition āyah |
| ``shifted`` | the āyah boundaries cross: neither contains the other |
| ``unnumbered`` | the words are printed but not numbered — the basmalah of Al-Fātiḥah |
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date

from .build import ORDER, OUT, Word

FORMAT = "quran-ayah-map"
FORMAT_VERSION = "1.0"
REFERENCE = "hafs"


def _runs(words: list[Word], key: str) -> dict[tuple[int, int], set[int]]:
    """``(surah, ayah)`` in one edition -> the numbers it contains."""
    out: dict[tuple[int, int], set[int]] = defaultdict(set)
    for w in words:
        if key in w.ayah:
            out[(w.surah, w.ayah[key])].add(w.id)
    return out


def _relation(kufi: set[int], edition: set[int], spans: int) -> str:
    if spans > 1:
        return "split"
    if edition == kufi:
        return "same"
    if edition > kufi:
        return "merged"
    return "shifted"


def ayah_map(words: list[Word]) -> list[dict]:
    reference = _runs(words, REFERENCE)
    editions = {k: _runs(words, k) for k in ORDER}
    number_to_ayah = {k: {n: sa for sa, ns in runs.items() for n in ns}
                      for k, runs in editions.items()}

    out = []
    for (surah, ayah), numbers in sorted(reference.items()):
        entry: dict = {"surah": surah, "ayah": ayah}
        for k in ORDER:
            hits = sorted({number_to_ayah[k][n] for n in numbers if n in number_to_ayah[k]})
            if not hits:
                continue                       # no word of this āyah in that edition
            first, last = hits[0], hits[-1]
            cell = {"surah": first[0], "ayah": first[1]}
            if last != first:
                cell["ayah_last"] = last[1]
            if first[1] == 0:
                cell["relation"] = "unnumbered"
            else:
                cell["relation"] = _relation(numbers, editions[k][first], len(hits))
            entry[k] = cell
        out.append(entry)
    return out


def _cell_text(cell: dict | None) -> str:
    if not cell:
        return ""
    text = f"{cell['surah']}:{cell['ayah']}"
    if "ayah_last" in cell:
        text += f"-{cell['ayah_last']}"
    return text


def write_ayah_map(words: list[Word]) -> dict:
    """Write ``out/ayah-map.json`` and ``out/ayah-map.csv``; return the document."""
    rows = ayah_map(words)
    doc = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "generated": date.today().isoformat(),
        "reference": REFERENCE,
        "editions": ORDER,
        "note": "One entry per āyah of the Kūfī count as Ḥafṣ prints it. For "
                "each edition: the āyah its words fall in (`ayah_last` when they "
                "span more than one) and `relation` — same, merged, split, "
                "shifted, or unnumbered for the basmalah of Al-Fātiḥah. An "
                "edition is absent from an entry only where it reads none of "
                "the āyah's words, which does not occur in the current sources.",
        "ayahs": rows,
    }
    with (OUT / "ayah-map.json").open("w", encoding="utf-8") as fh:
        head = {k: v for k, v in doc.items() if k != "ayahs"}
        text = json.dumps(head, ensure_ascii=False, indent=1)
        fh.write(text[:-2] + ',\n "ayahs": [\n')
        fh.write(",\n".join("  " + json.dumps(r, ensure_ascii=False, separators=(",", ":"))
                            for r in rows))
        fh.write("\n ]\n}\n")
    with (OUT / "ayah-map.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["surah", "ayah"] + ORDER + [f"{k}_relation" for k in ORDER])
        for r in rows:
            wr.writerow([r["surah"], r["ayah"]]
                        + [_cell_text(r.get(k)) for k in ORDER]
                        + [r.get(k, {}).get("relation", "") for k in ORDER])
    return doc
