"""Surah names, taken from the KFGQPC v2 releases rather than hard-coded."""

from __future__ import annotations

import csv
import functools

from .sources import _extract

_CSV = ("UthmanicHafs_v2-0", "UthmanicHafs_v2-0 data/hafsData_v2-0.csv")

#: Where each surah was revealed.  Not present in any shipped file.
MAKKI = {
    1, 6, 7, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27,
    28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
    50, 51, 52, 53, 54, 55, 56, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
    78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,
    96, 97, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114,
}


@functools.cache
def names() -> dict[int, dict[str, str]]:
    path = _extract(*_CSV)
    out: dict[int, dict[str, str]] = {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            n = int(row["sura_no"])
            if n not in out:
                out[n] = {
                    "name_ar": row["sura_name_ar"].strip(),
                    "name_en": row["sura_name_en"].strip(),
                    "revelation": "makki" if n in MAKKI else "madani",
                }
    return out
