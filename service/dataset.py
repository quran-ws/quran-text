"""The built dataset under ``data/``, loaded once and shared by every request.

    data = Dataset.load()          # QURAN_DATA, default ../data
    data.mushaf("warsh")           # a quran_text.Mushaf
    data.ayah_map                  # a quran_text.AyahMap
    data.word_index                # a quran_text.WordIndex, loaded on first use
    data.kufi_refs("warsh", 2, 253)  # the Kūfī āyāt Warsh 2:253 corresponds to
"""

from __future__ import annotations

import json
import os
import re
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "lib" / "python"))

from quran_text import AyahMap, Mushaf, WordIndex  # noqa: E402

EDITIONS = ["hafs", "shubah", "warsh", "qalun", "duri", "susi", "bazzi"]


class Dataset:
    def __init__(self, root: Path):
        self.root = root
        self.catalog = _read_json(root / "catalog.json")
        self.manifest = _read_json(root / "manifest.json")
        self.mushafs: dict[str, Mushaf] = {
            key: Mushaf.load(root / "mushaf" / f"{key}.json") for key in EDITIONS
        }
        ayah_map_doc = _read_json(root / "ayah-map.json")
        self.ayah_map = AyahMap(ayah_map_doc)
        self._kufi_refs = _invert_ayah_map(ayah_map_doc)
        self._word_index: WordIndex | None = None
        self._lock = threading.Lock()

    @classmethod
    def load(cls, root: str | os.PathLike | None = None) -> "Dataset":
        root = Path(root or os.environ.get("QURAN_DATA") or HERE.parent / "data")
        if not (root / "catalog.json").exists():
            raise FileNotFoundError(
                f"{root} holds no built dataset (catalog.json missing); "
                "run build.py or point QURAN_DATA at data/")
        return cls(root)

    # -- editions --

    def mushaf(self, key: str) -> Mushaf:
        m = self.mushafs.get(key)
        if m is None:
            raise KeyError(f"unknown edition {key!r}; one of {', '.join(EDITIONS)}")
        return m

    def edition_info(self, key: str) -> dict:
        """What the page shows for one riwāyah: names, counts, what it lacks."""
        m = self.mushaf(key)
        entry = next(r for r in self.catalog["riwayahs"] if r["key"] == key)
        marks = {}
        for _, mk in m.all.marks:
            marks[mk.kind] = marks.get(mk.kind, 0) + 1
        return {
            "key": key,
            "name_en": m.name_en, "name_ar": m.name_ar,
            "qiraah_en": m.qiraah_en, "qiraah_ar": m.qiraah_ar,
            "counting_system": m.counting_system,
            "counting_system_en": m.counting.get("system_name_en"),
            "counting_system_ar": m.counting.get("system_name_ar"),
            "ayah_count": m.ayah_count, "word_count": m.word_count,
            "page_count": m.page_count, "juz_count": m.juz_count,
            "basmalah_counted": m.basmalah_counted,
            "has": {layer: m.has(layer) for layer in ("rasm_imlai", "juz", "lines")},
            "absent": m._doc["layers"]["absent"],
            "marks": marks,
            "surah_ayah_counts": [s.ayah_count for s in m.surahs],
            "source": entry["source"],
            "provenance": m.provenance,
            "font": {**m._doc["font"], "url": "/files/fonts/" + m._doc["font"]["file"]},
            "sample": self.sample(m),
        }

    @staticmethod
    def sample(m: Mushaf) -> dict:
        """A stretch of about ten āyāt that carries every kind of sign the
        release prints — waqf marks, ۩ and ۞ — so a preview shows them all."""
        printed = {mk.kind for _, mk in m.all.marks}
        starts = m._doc["ayah_starts"]
        for a in m.sajdat():
            for first in range(max(0, a.index - 9), a.index + 1):
                last = min(first + 9, m.ayah_count - 1)
                span = m.span(starts[first], m.ayahs[last].end)
                kinds = {mk.kind for _, mk in span.marks}
                lo, hi = m.ayahs[first], m.ayahs[last]
                if printed <= kinds and lo.surah.number == hi.surah.number:
                    return {"ayah": f"{lo.key}-{hi.key}", "signs": sorted(kinds)}
        return {"ayah": "1:1-1:7", "signs": sorted(printed)}

    # -- the word index, 50 MB, only when asked for --

    @property
    def word_index(self) -> WordIndex:
        if self._word_index is None:
            with self._lock:
                if self._word_index is None:
                    self._word_index = WordIndex.load(self.root / "word-index.json")
        return self._word_index

    # -- āyah references across editions --

    def kufi_refs(self, edition: str, surah: int, ayah: int) -> list[dict]:
        """The Kūfī (Ḥafṣ) āyāt whose words fall in ``surah:ayah`` of ``edition``,
        each with how the two relate: ``[{"surah": 2, "ayah": 255, "relation": "split"}]``."""
        return self._kufi_refs.get((edition, surah, ayah), [])

    # -- raw files --

    def files(self) -> list[dict]:
        """Every file under ``data/`` with size, SHA-256 and the question it answers."""
        answers = [(re.compile("^" + re.escape(f["path"]).replace(r"<key>", r"[a-z]+").replace(r"<file>", r"[A-Za-z0-9.\-]+")
                               + ("" if f["path"].endswith("/") else "$")), f)
                   for f in self.catalog["files"]]
        out = []
        for entry in self.manifest["files"]:
            path = entry["path"]
            about = next((f for rx, f in answers if rx.match(path)), None)
            if about is None and path.endswith(".csv"):        # the table twin of a JSON file
                twin = next((f for rx, f in answers if rx.match(path[:-4] + ".json")), None)
                about = {"format": "csv", "answers": twin["answers"] + " — as a table"} if twin else None
            about = about or _UNLISTED.get(path, {})
            out.append({
                "path": path.removeprefix("data/"),
                "bytes": entry["bytes"], "sha256": entry["sha256"],
                "format": about.get("format"), "normative": about.get("normative", False),
                "answers": about.get("answers"),
            })
        return out

    def versions(self) -> dict:
        """What a client library compares itself against to spot a new release.

        Deliberately small and free of prose: a client fetches this on a slow
        cadence, so it must stay cheap to serve and cheap to parse.  Identity is
        the KFGQPC package a riwāyah was cut from plus the SHA-256 of the built
        file, because either one moving means the bytes a caller holds are stale.
        """
        sha = {f["path"].removeprefix("data/"): f["sha256"] for f in self.manifest["files"]}
        editions = {}
        for r in self.catalog["riwayahs"]:
            key = r["key"]
            text = (self.mushaf(key).provenance or {}).get("text", {})
            editions[key] = {
                "source": text.get("package"),
                "source_sha256": text.get("sha256"),
                "file": f"mushaf/{key}.json",
                "file_sha256": sha.get(f"mushaf/{key}.json"),
                "ayah_count": r.get("ayah_count"),
                "word_count": r.get("word_count"),
            }
        return {
            "format": "quran-version",
            "format_version": "1.0",
            "dataset": self.catalog["generated"],
            "editions": editions,
        }

    def file_path(self, relative: str) -> Path | None:
        """The on-disk path of a listed file, or ``None`` if it is not one."""
        if any(f["path"] == relative for f in self.files()):
            return self.root / relative
        return None


_UNLISTED = {
    "data/catalog.json": {"format": "quran-catalog",
                         "answers": "start here: the riwāyāt, the sūrahs and every file"},
}


def _read_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _invert_ayah_map(doc: dict) -> dict[tuple[str, int, int], list[dict]]:
    inverse: dict[tuple[str, int, int], list[dict]] = {}
    for row in doc["ayahs"]:
        for edition in doc["editions"]:
            r = row[edition]
            for a in range(r["ayah"], r.get("ayah_last", r["ayah"]) + 1):
                inverse.setdefault((edition, r["surah"], a), []).append(
                    {"surah": row["surah"], "ayah": row["ayah"], "relation": r["relation"]})
    return inverse
