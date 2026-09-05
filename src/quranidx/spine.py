"""The spine: every number of the shared numbering, with a text and who reads it.

The numbering counts the finest division of the text any of the seven muṣḥafs
prints, so the master is a division nobody prints and no muṣḥaf file can stand
in for it.  This file is where a number gets a text.  The muṣḥaf files are
where a text gets a position.  Neither is derivable from the other alone, so
both are normative.

Every number carries its Ḥafṣ coordinates ``[sura, ayah, position-in-ayah]``
in the Kūfī count, because almost every existing word-level dataset — the
corpus.quran.com morphology, quran.com's word audio segments, word-by-word
translations — is keyed that way, and this column is what lets them attach in
one lookup.  At 72:16 two numbers carry the same triple, which is the honest
statement that Ḥafṣ writes them as one word.
"""

from __future__ import annotations

import csv
import json
from datetime import date

from .build import ORDER, OUT, Word

FORMAT = "quran-spine"
FORMAT_VERSION = "1.0"


def hafs_coordinates(words: list[Word]) -> dict[int, dict]:
    """number -> ``{sura, ayah, pos}`` in Ḥafṣ, where it has the word.

    The position counts *printed* words: a number Ḥafṣ covers with the same
    printed word as the number before it takes that word's position.
    """
    out: dict[int, dict] = {}
    pos = 0
    at: tuple[int, int] | None = None
    for w in words:
        if "hafs" not in w.forms:
            continue
        if "hafs" in w.continuation:
            out[w.id] = out[w.id - 1]
            continue
        here = (w.sura, w.aya["hafs"])
        if here != at:
            at, pos = here, 0
        pos += 1
        out[w.id] = {"sura": w.sura, "ayah": w.aya["hafs"], "pos": pos}
    return out


def spine_word(w: Word, hafs: dict[int, dict]) -> dict:
    return {
        "number": w.id,
        "sura": w.sura,
        "rasm": w.rasm,
        "pointed": w.pointed,
        "uthmani": w.uthmani,
        "simple": w.simple,
        "status": w.status,
        "hafs": hafs.get(w.id),
        "forms": {k: w.forms[k] for k in ORDER if k in w.forms},
        "ayah": {k: w.aya[k] for k in ORDER if k in w.aya},
        **({"written_joined": [k for k in ORDER if w.boundary.get(k) == "written_joined"]}
           if any(v == "written_joined" for v in w.boundary.values()) else {}),
    }


def write_spine(words: list[Word]) -> dict:
    """Write ``out/spine.json`` and ``out/spine.csv`` and return the document."""
    hafs = hafs_coordinates(words)
    doc = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "generated": date.today().isoformat(),
        "total": words[-1].id,
        "mushafs": ORDER,
        "note": "`number` is the shared number, dense 1 … total. `forms[key]` is "
                "absent where that muṣḥaf does not read the word; where a "
                "muṣḥaf writes the number joined with its neighbour the form "
                "is the joined word, repeated on both numbers, and `written_joined` "
                "names those muṣḥafs. `hafs` is the word's sūrah, āyah and "
                "position in the āyah in the Kūfī count, null where Ḥafṣ lacks it.",
        "words": [spine_word(w, hafs) for w in words],
    }
    # One word per line: readable in an editor and diffable by git, without
    # the 3× cost of indenting 77,000 small objects.
    head = {k: v for k, v in doc.items() if k != "words"}
    with (OUT / "spine.json").open("w", encoding="utf-8") as fh:
        text = json.dumps(head, ensure_ascii=False, indent=1)
        fh.write(text[:-2] + ',\n "words": [\n')
        fh.write(",\n".join("  " + json.dumps(w, ensure_ascii=False, separators=(",", ":"))
                            for w in doc["words"]))
        fh.write("\n ]\n}\n")

    with (OUT / "spine.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["number", "sura", "rasm", "pointed", "uthmani", "simple", "status",
                     "hafs_sura", "hafs_ayah", "hafs_pos", "written_joined"]
                    + [f"ayah_{k}" for k in ORDER] + [f"form_{k}" for k in ORDER])
        for w in words:
            h = hafs.get(w.id)
            wr.writerow([w.id, w.sura, w.rasm, w.pointed, w.uthmani, w.simple,
                         w.status, *((h["sura"], h["ayah"], h["pos"]) if h else ("", "", "")),
                         "|".join(k for k in ORDER
                                  if w.boundary.get(k) == "written_joined")]
                        + [w.aya.get(k, "") for k in ORDER]
                        + [w.forms.get(k, "") for k in ORDER])
    return doc
