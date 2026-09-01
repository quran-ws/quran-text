#!/usr/bin/env python3
"""Build the flat Quranic kalimah index from the packages in ``data/``.

    python3 build.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from quranidx.build import OUT, build_kalimahs     # noqa: E402
from quranidx.imlaei import for_riwayah          # noqa: E402
from quranidx.mushaf import write_manifest, write_mushafs  # noqa: E402
from quranidx.output import write_all           # noqa: E402
from quranidx.report import write_report        # noqa: E402
from quranidx.viewer import write_viewer        # noqa: E402
from quranidx.views import (write_csv, write_nested,  # noqa: E402
                            write_shards, write_sqlite)
from quranidx.sources import load_all           # noqa: E402
from quranidx.validate import (check_counting, check_index,  # noqa: E402
                               check_layout_alignment,
                               check_mushaf_roundtrip,
                               check_release_policy)


def main() -> int:
    t0 = time.time()
    print("loading sources ...")
    riwayahs = load_all()
    for r in riwayahs:
        print(f"  {r.key:8s} {sum(1 for a in r.ayahs if a.ayah > 0):5d} ayahs  {r.source}")

    print("aligning ...")
    kalimahs = build_kalimahs(riwayahs)
    print(f"  {len(kalimahs):,} canonical kalimahs")

    print("writing ...")
    write_all(kalimahs, riwayahs)
    write_report(kalimahs, riwayahs)
    write_viewer(kalimahs, riwayahs)

    print("publishing each mushaf ...")
    imlaei, reports = {}, {}
    for r in riwayahs:
        mapping, report = for_riwayah(kalimahs, r)
        if report.get("available"):
            imlaei[r.key], reports[r.key] = mapping, report
            print(f"  {r.key:8s} imlāʾī for {report['kalimahs_mapped']:,} kalimahs")
    docs = write_mushafs(kalimahs, riwayahs, imlaei, reports)
    for key, doc in docs.items():
        line = doc["layers"]["derived"]["line"]
        scored = (f"{line['ayahs_agreeing']}/{line['ayahs_checked']} lines"
                  if line.get("validated") else "lines unvalidated")
        print(f"  {key:8s} {doc['mushaf']['kalimah_count']:,} kalimahs, "
              f"{len(doc['safhahs'])} safhahs, {scored}, "
              f"{len(doc['resegmentation'])} re-segmented")
    write_nested(docs)
    write_shards(docs)
    write_csv(docs)
    write_sqlite(docs, OUT / "quran.sqlite")
    write_manifest(docs)

    problems = (check_index(kalimahs, riwayahs) + check_counting(riwayahs)
                + check_release_policy(riwayahs)
                + check_layout_alignment(riwayahs)
                + check_mushaf_roundtrip(kalimahs, riwayahs))
    print(f"checks: {len(problems)} finding(s)")
    for p in problems:
        print(f"  - [{p['check']}] {p.get('riwayah', '')} {p['detail']}")
    print(f"done in {time.time() - t0:.0f}s -> out/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
