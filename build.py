#!/usr/bin/env python3
"""Build the flat Qur'anic word index from the packages in ``data/``.

    python3 build.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from quranidx.build import OUT, build_words     # noqa: E402
from quranidx.counting import (check_counting as check_counting_files,  # noqa: E402
                               provenance as counting_provenance,
                               write_fawasil)
from quranidx.imlaei import for_riwaya          # noqa: E402
from quranidx.mushaf import write_manifest, write_mushafs  # noqa: E402
from quranidx.output import write_all           # noqa: E402
from quranidx.report import write_report        # noqa: E402
from quranidx.spine import write_spine          # noqa: E402
from quranidx.viewer import write_viewer        # noqa: E402
from quranidx.views import (write_csv, write_nested,  # noqa: E402
                            write_shards, write_sqlite)
from quranidx.sources import load_all           # noqa: E402
from quranidx.validate import (check_counting, check_index,  # noqa: E402
                               check_layout_alignment,
                               check_mushaf_roundtrip,
                               check_numbering, check_positions,
                               check_release_policy, check_schema_fields)


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
    write_all(words, riwayat)
    spine = write_spine(words)
    write_viewer(words, riwayat)

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
        c = doc["counting"]
        print(f"  {key:8s} {doc['mushaf']['word_count']:,} words, "
              f"{len(doc.get('page_starts', []))} pages, {scored}, "
              f"{len(doc['resegmentation'])} re-segmented, "
              f"{c['ayah_count']} āyāt = {c['system']}"
              f"{' + ' + str(len(c['unexplained'])) + ' unexplained' if c['unexplained'] else ''}")
    write_fawasil(words, docs)
    write_report(words, riwayat, {k: d["counting"] for k, d in docs.items()})
    write_nested(docs)
    write_shards(docs)
    write_csv(docs)
    write_sqlite(docs, spine, OUT / "quran.sqlite")
    write_manifest(docs, {"qiraat-ayah-map": counting_provenance()})

    problems = (check_index(words, riwayat) + check_counting(riwayat)
                + check_release_policy(riwayat)
                + check_layout_alignment(riwayat)
                + check_mushaf_roundtrip(words, riwayat)
                + check_numbering(docs) + check_positions(docs)
                + check_counting_files(docs)
                + check_schema_fields(docs, Path("schema/mushaf-1.0.json")))
    print(f"checks: {len(problems)} finding(s)")
    for p in problems:
        print(f"  - [{p['check']}] {p.get('riwaya', '')} {p['detail']}")
    print(f"done in {time.time() - t0:.0f}s -> out/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
