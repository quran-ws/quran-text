#!/usr/bin/env python3
"""Build the flat Qur'anic word index from the packages in ``data/``.

    python3 build.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from quranidx.build import build_words          # noqa: E402
from quranidx.output import write_all           # noqa: E402
from quranidx.report import write_report        # noqa: E402
from quranidx.viewer import write_viewer        # noqa: E402
from quranidx.sources import load_all           # noqa: E402
from quranidx.validate import (check_counting, check_index,  # noqa: E402
                               check_release_policy)


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
    write_report(words, riwayat)
    write_viewer(words, riwayat)

    problems = (check_index(words, riwayat) + check_counting(riwayat)
                + check_release_policy(riwayat))
    print(f"checks: {len(problems)} finding(s)")
    for p in problems:
        print(f"  - [{p['check']}] {p.get('riwaya', '')} {p['detail']}")
    print(f"done in {time.time() - t0:.0f}s -> out/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
