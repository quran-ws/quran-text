"""``out/catalog.json``: what is in ``out/``, and where to start.

The front door.  A developer reads this one small file and knows which
riwāyāt are here, what each one counts, how big the corpus is, and which file
answers which question — without opening anything else.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import date

from .build import OUT, Word
from .sources import Riwaya
from .suras import names

FORMAT = "quran-catalog"
FORMAT_VERSION = "1.0"

#: Every file group under ``out/``, with the question it answers.
FILES = [
    {"path": "out/mushaf/<key>.json", "format": "quran-mushaf", "normative": True,
     "answers": "give me one muṣḥaf: its words by position, with āyāt, pages, lines, juz, marks, and the numbering that maps positions onto the shared numbers"},
    {"path": "out/mushaf/<key>.nested.json.gz", "format": "quran-mushaf", "view": "nested",
     "answers": "the same muṣḥaf as sūrah → āyah → words, for consumers coming from verse-level formats"},
    {"path": "out/mushaf/<key>.csv.gz", "format": "csv", "view": "flat",
     "answers": "the same muṣḥaf as one row per word, for pandas, R and spreadsheets"},
    {"path": "out/word-index.json", "format": "quran-word-index", "normative": True,
     "answers": "what word is number n, who reads it and how, and where it is in Ḥafṣ"},
    {"path": "out/word-index.csv", "format": "csv",
     "answers": "the word index as a table"},
    {"path": "out/differences.json", "format": "quran-differences",
     "answers": "only the words where the riwāyāt disagree about letters, the ā, presence or boundary"},
    {"path": "out/ayah-map.json", "format": "quran-ayah-map",
     "answers": "what a Kūfī āyah reference is in every edition"},
    {"path": "out/counting.json", "format": "quran-counting",
     "answers": "the six counting systems, their boundaries as numbers, and which system each edition follows"},
    {"path": "out/quran.sqlite.gz", "format": "sqlite",
     "answers": "all seven muṣḥafs and the word index, queryable in SQL"},
    {"path": "out/manifest.json", "format": "quran-manifest",
     "answers": "the SHA-256 of every source package and every file here"},
    {"path": "out/reports/", "format": "markdown, csv, html",
     "answers": "how the seven compare and how this was built, for reading rather than loading"},
]


def write_catalog(words: list[Word], riwayat: list[Riwaya],
                  docs: dict[str, dict]) -> dict:
    by_sura: dict[int, list[Word]] = defaultdict(list)
    for w in words:
        by_sura[w.sura].append(w)

    doc = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "generated": date.today().isoformat(),
        "word_count": words[-1].id,
        "sura_count": len(by_sura),
        "riwayat": [{
            "key": r.key,
            "name_en": r.name_en,
            "name_ar": r.name_ar,
            "qari_en": r.qari_en,
            "qari_ar": r.qari_ar,
            "counting_system": docs[r.key]["counting"]["system"],
            "ayah_count": docs[r.key]["counting"]["ayah_count"],
            "word_count": docs[r.key]["mushaf"]["word_count"],
            "source": r.source,
            "crosscheck_source": r.crosscheck_source,
            "file": f"out/mushaf/{r.key}.json",
        } for r in riwayat],
        "suras": [{
            "number": sura,
            **names()[sura],
            "word_count": len(ws),
            "first_number": ws[0].id,
            "last_number": ws[-1].id,
            "ayah_count": {r.key: max((w.aya.get(r.key, 0) for w in ws), default=0)
                           for r in riwayat},
        } for sura, ws in sorted(by_sura.items())],
        "files": FILES,
    }
    (OUT / "catalog.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    return doc
