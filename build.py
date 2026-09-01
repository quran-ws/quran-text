#!/usr/bin/env python3
"""Build the flat Qur'anic word index from the packages in ``data/``.

    python3 build.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from quranidx.build import OUT, build_index     # noqa: E402
from quranidx.imlaei import for_riwaya          # noqa: E402
from quranidx.mushaf import write_manifest, write_mushafs  # noqa: E402
from quranidx.output import write_all           # noqa: E402
from quranidx.report import write_report        # noqa: E402
from quranidx.viewer import write_viewer        # noqa: E402
from quranidx.views import (write_csv, write_nested,  # noqa: E402
                            write_shards, write_sqlite)
from quranidx.sources import load_all           # noqa: E402
from quranidx.slots import write_slot_model     # noqa: E402
from quranidx.validate import (check_counting, check_index,  # noqa: E402
                               check_layout_alignment,
                               check_mushaf_roundtrip,
                               check_release_policy)


def main() -> int:
    t0 = time.time()
    print("loading sources ...")
    riwayat = load_all()
    for r in riwayat:
        print(f"  {r.key:8s} {sum(1 for a in r.ayat if a.aya > 0):5d} āyāt  {r.source}")

    print("aligning ...")
    result = build_index(riwayat)
    words = result.words
    print(f"  {len(words):,} canonical word slots")

    print("writing ...")
    write_all(words, riwayat)
    write_report(words, riwayat)
    write_viewer(words, riwayat)
    slot_model = write_slot_model(words, result.alignment_spans)
    print(f"  {slot_model['alignment_span_count']} n:m alignment span(s)")

    print("publishing each muṣḥaf ...")
    imlaei, reports = {}, {}
    for r in riwayat:
        mapping, report = for_riwaya(words, r)
        if report.get("available"):
            imlaei[r.key], reports[r.key] = mapping, report
            print(f"  {r.key:8s} imlāʾī for {report['words_mapped']:,} words")
    docs = write_mushafs(words, riwayat, imlaei, reports)
    for key, doc in docs.items():
        line = doc["layers"]["derived"]["line"]
        scored = (f"{line['ayat_agreeing']}/{line['ayat_checked']} lines"
                  if line.get("validated") else "lines unvalidated")
        print(f"  {key:8s} {doc['mushaf']['word_count']:,} words, "
              f"{len(doc['pages'])} pages, {scored}, "
              f"{len(doc['resegmentation'])} re-segmented")
    write_nested(docs)
    write_shards(docs)
    write_csv(docs)
    write_sqlite(docs, OUT / "quran.sqlite")
    write_manifest(docs)

    problems = (check_index(words, riwayat) + check_counting(riwayat)
                + check_release_policy(riwayat)
                + check_layout_alignment(riwayat)
                + check_mushaf_roundtrip(words, riwayat))
    print(f"checks: {len(problems)} finding(s)")
    for p in problems:
        print(f"  - [{p['check']}] {p.get('riwaya', '')} {p['detail']}")
    print(f"done in {time.time() - t0:.0f}s -> out/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
