#!/usr/bin/env python3
"""Build the word index, the seven muṣḥaf files and every derived artefact.

    python3 build.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from quranidx import counting                   # noqa: E402
from quranidx.build import build_words          # noqa: E402
from quranidx.mushaf import write_manifest, write_mushafs  # noqa: E402
from quranidx.output import write_index         # noqa: E402
from quranidx.report import write_report        # noqa: E402
from quranidx.sources import load_all           # noqa: E402
from quranidx.spine import write_spine          # noqa: E402
from quranidx.validate import (check_ayah_numbers, check_index,  # noqa: E402
                               check_layout_alignment,
                               check_mushaf_roundtrip,
                               check_numbering, check_positions,
                               check_release_policy, check_schema_fields)
from quranidx.viewer import write_viewer        # noqa: E402
from quranidx.views import (write_csv, write_nested,  # noqa: E402
                            write_shards, write_sqlite)


def main() -> int:
    t0 = time.time()
    print("loading sources ...")
    riwayat = load_all()
    for r in riwayat:
        print(f"  {r.key:8s} {sum(1 for a in r.ayat if a.aya > 0):5d} āyāt  {r.source}")

    print("aligning ...")
    words = build_words(riwayat)
    print(f"  {len(words):,} canonical words")

    print("writing ...")
    write_index(words, riwayat)
    spine = write_spine(words)
    write_viewer(words, riwayat)

    print("publishing each muṣḥaf ...")
    docs = write_mushafs(words, riwayat)
    for key, doc in docs.items():
        line = doc["layers"]["derived"]["line"]
        scored = (f"{line['ayat_agreeing']}/{line['ayat_checked']} lines"
                  if line.get("validated") else "lines unvalidated")
        c = doc["counting"]
        open_ = f", {len(c['unexplained'])} unexplained" if c["unexplained"] else ""
        print(f"  {key:8s} {doc['mushaf']['word_count']:,} words, "
              f"{len(doc.get('page_starts', []))} pages, {scored}, "
              f"{len(doc['resegmentation'])} re-segmented, "
              f"{c['ayah_count']} āyāt = {c['system']}{open_}")
    counting.write_fawasil(words, docs)
    write_report(words, riwayat, docs)
    write_nested(docs)
    write_shards(docs)
    write_csv(docs)
    write_sqlite(docs, spine)
    write_manifest(docs)

    problems = (check_index(words, riwayat)
                + check_ayah_numbers(riwayat)
                + check_release_policy(riwayat)
                + check_layout_alignment(riwayat)
                + check_mushaf_roundtrip(words, riwayat)
                + check_numbering(docs)
                + check_positions(docs)
                + counting.check_unexplained(docs)
                + check_schema_fields(docs))
    print(f"checks: {len(problems)} finding(s)")
    for p in problems:
        print(f"  - [{p['check']}] {p.get('riwaya', '')} {p['detail']}")
    print(f"done in {time.time() - t0:.0f}s -> out/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
