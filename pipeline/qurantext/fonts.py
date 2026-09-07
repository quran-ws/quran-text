"""The font each muṣḥaf needs, taken from the same KFGQPC package as its text.

Every v3.0 release ships one ``.ttf`` beside its ``.docx``, and the text uses
codepoints — Arabic Extended-B alefs, open tanwīn, the waqf signs — that only
that font is guaranteed to draw.  A muṣḥaf file therefore names its font, with
the family name read from the font's own ``name`` table, and the build copies
the file to ``out/fonts/`` so the link inside the JSON resolves.
"""

from __future__ import annotations

import hashlib
import struct
import zipfile
from pathlib import Path

from .build import OUT
from .sources import DATA, SourceSpec

FONT_DIR = OUT / "fonts"

#: Where KFGQPC publishes the fonts themselves.
KFGQPC_FONTS = "https://fonts.qurancomplex.gov.sa/"


def family(ttf: bytes) -> str:
    """The font family name (``name`` table id 1, Windows/English)."""
    count = struct.unpack(">H", ttf[4:6])[0]
    for i in range(count):
        tag, _, off, _ = struct.unpack(">4sIII", ttf[12 + 16 * i:28 + 16 * i])
        if tag != b"name":
            continue
        _, records, strings = struct.unpack(">HHH", ttf[off:off + 6])
        for j in range(records):
            pid, _, lid, nid, ln, so = struct.unpack(
                ">HHHHHH", ttf[off + 6 + 12 * j:off + 18 + 12 * j])
            if pid == 3 and nid == 1 and lid == 0x409:
                start = off + strings + so
                return ttf[start:start + ln].decode("utf-16-be")
    raise ValueError("no family name in font")


def describe(spec: SourceSpec) -> dict:
    """The ``font`` block of a muṣḥaf file, and the font written to ``out/fonts/``."""
    with zipfile.ZipFile(DATA / f"{spec.primary_zip}.zip") as z:
        data = z.read(spec.font_member)
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    name = Path(spec.font_member).name.replace(" ", "-")
    (FONT_DIR / name).write_bytes(data)
    return {
        "family": family(data),
        "file": f"out/fonts/{name}",
        "package": f"{spec.primary_zip}.zip",
        "member": spec.font_member,
        "sha256": hashlib.sha256(data).hexdigest(),
        "publisher": KFGQPC_FONTS,
        "note": "The text uses codepoints only this font is guaranteed to draw "
                "(Arabic Extended-B alefs, open tanwīn, the waqf signs). Ship it "
                "with the text; a general Arabic font will show gaps.",
    }
