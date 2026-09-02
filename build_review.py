#!/usr/bin/env python3
"""Render the HTML review page by injecting the payload into the template."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from quranidx.build import build_words          # noqa: E402
from quranidx.sources import load_all           # noqa: E402
from quranidx.webdata import payload            # noqa: E402

TEMPLATE = Path("web/review.template.html")
TARGET = Path("out/review.html")


def main() -> int:
    riwayat = load_all()
    words = build_words(riwayat)
    data = json.dumps(payload(words, riwayat), ensure_ascii=False,
                      separators=(",", ":"))
    # The payload sits in a <script type="application/json">, so the only
    # sequence that could break out of it is a literal "</".
    data = data.replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("__DATA__", data)
    TARGET.write_text(html, encoding="utf-8")
    print(f"{TARGET} — {len(html):,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
