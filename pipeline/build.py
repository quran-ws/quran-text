#!/usr/bin/env python3
"""Build the word index, the seven muṣḥaf files and every derived artefact.

    python3 pipeline/build.py
"""

import sys
import time
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit(
        f"build.py needs Python 3.11 or newer; this is {sys.version.split()[0]}.\n"
        f"Try: python3.11 pipeline/build.py"
    )

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from qurantext import counting                   # noqa: E402
from qurantext.ayah_map import write_ayah_map    # noqa: E402
from qurantext.build import build_words          # noqa: E402
from qurantext.catalog import write_catalog      # noqa: E402
from qurantext.mushaf import write_manifest, write_mushafs  # noqa: E402
from qurantext.report import write_report        # noqa: E402
from qurantext.sources import load_all           # noqa: E402
from qurantext.validate import (check_ayah_numbers, check_index,  # noqa: E402
                               check_layout_alignment,
                               check_mushaf_roundtrip,
                               check_numbering, check_positions,
                               check_release_policy, check_schema_fields)
from qurantext.viewer import write_viewer        # noqa: E402
from qurantext.views import write_csv, write_nested, write_sqlite  # noqa: E402
from qurantext.word_index import write_differences, write_word_index  # noqa: E402


#: The client libraries under lib/ ship Ḥafṣ and its font; keep the copies in step.
BUNDLES = [
    "lib/python/quran_text_data", "lib/js/data", "lib/php/data", "lib/dart/assets",
    "lib/swift/Sources/QuranText/Resources", "lib/kotlin/src/main/resources",
]


def sync_bundled_hafs(doc: dict) -> None:
    """The same document as data/mushaf/hafs.json, minified: nobody reads the
    bundled copy, so the one-word-per-line layout that makes data/ reviewable
    would only cost the packages 1.5 MB."""
    import json
    import shutil
    text = json.dumps(doc, ensure_ascii=False, separators=(",", ":"))
    font = ROOT / "data" / "fonts" / doc["font"]["file"]
    for d in BUNDLES:
        dest = ROOT / d
        if dest.is_dir():
            (dest / "hafs.json").write_text(text, encoding="utf-8")
            shutil.copy(font, dest / font.name)


def main() -> int:
    t0 = time.time()
    print("loading sources ...")
    riwayahs = load_all()
    for r in riwayahs:
        print(f"  {r.key:8s} {sum(1 for a in r.ayahs if a.ayah > 0):5d} āyāt  {r.source}")

    print("aligning ...")
    words = build_words(riwayahs)
    print(f"  {len(words):,} canonical words")

    print("writing the word index ...")
    word_index = write_word_index(words)
    write_differences(words)
    write_ayah_map(words)

    print("publishing each muṣḥaf ...")
    docs = write_mushafs(words, riwayahs)
    for key, doc in docs.items():
        line = doc["layers"]["derived"]["line"]
        scored = (f"{line['ayahs_agreeing']}/{line['ayahs_checked']} lines"
                  if line.get("validated") else "lines unvalidated")
        c = doc["counting"]
        open_ = f", {len(c['unexplained'])} unexplained" if c["unexplained"] else ""
        print(f"  {key:8s} {doc['mushaf']['word_count']:,} words, "
              f"{len(doc.get('page_starts', []))} pages, {scored}, "
              f"{len(doc['resegmentation'])} re-segmented, "
              f"{c['ayah_count']} āyāt = {c['system']}{open_}")
    counting.write_counting(words, docs)
    write_nested(docs)
    write_csv(docs)
    write_sqlite(docs, word_index)

    print("writing the reports ...")
    write_report(words, riwayahs, docs)
    write_viewer(words, riwayahs)
    write_catalog(words, riwayahs, docs)
    write_manifest(docs)
    sync_bundled_hafs(docs["hafs"])

    problems = (check_index(words, riwayahs)
                + check_ayah_numbers(riwayahs)
                + check_release_policy(riwayahs)
                + check_layout_alignment(riwayahs)
                + check_mushaf_roundtrip(words, riwayahs)
                + check_numbering(docs)
                + check_positions(docs)
                + counting.check_unexplained(docs)
                + check_schema_fields(docs))
    print(f"checks: {len(problems)} finding(s)")
    for p in problems:
        print(f"  - [{p['check']}] {p.get('riwayah', '')} {p['detail']}")
    print(f"done in {time.time() - t0:.0f}s -> data/")
    # A finding means the build wrote data/ but could not vouch for it, so the
    # exit status has to say so: CI and any caller chaining on `&&` are entitled
    # to treat a non-zero status as "do not publish this".
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
