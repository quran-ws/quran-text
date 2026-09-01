"""Publish each mushaf on its own, keyed to the shared kalimah index.

``out/`` already answers *how do the mushafs differ?*  It does not answer *give
me Warsh*: a consumer who wants one mushaf has to take the comparison and
project it back out.  This module writes the other view — one self-contained
file per mushaf, every kalimah carrying the global ID that means the same kalimah in
all seven.

The shape is flat.  A mushaf is an ordered list of kalimahs, and the structures
above a kalimah — ayah, juz, safhah — are lists of boundaries over kalimah IDs rather
than levels of nesting.  That is the same model as ``out/fasilahs.json`` and it
is what keeps the seven files comparable while they count 6,214 to 6,236 ayahs:
nesting kalimahs under ayahs would make one path mean a different kalimah in each
mushaf, which is exactly what the global ID exists to prevent.

Only ``out/mushaf/<key>.json`` is normative.  The nested, sharded, CSV and
SQLite forms in :mod:`quranidx.views` are generated from the same build and are
labelled views, so that whichever one turns out to be most convenient cannot
quietly become the standard.

Nothing here is asserted that the packages do not say.  Where a fact is derived
rather than read it is marked derived, where it is unavailable the field is
absent and the absence is explained, and where this build departs from the
source's own kalimah spacing every instance is listed in the file itself.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

from .build import OUT, Kalimah
from .output import boundary_events
from .sources import DATA, RELEASE_POLICY, Riwayah
from .surahs import names

FORMAT = "quran-mushaf"
FORMAT_VERSION = "2.0"

MUSHAF_DIR = OUT / "mushaf"

#: Signs that can attach to a kalimah, with the Unicode name of each.  Emitted in
#: every file so a consumer never has to hard-code a codepoint table.
MARK_NAMES = {
    "ۖ": "ARABIC SMALL HIGH LIGATURE SAD WITH LAM WITH ALEF MAKSURA",
    "ۗ": "ARABIC SMALL HIGH LIGATURE QAF WITH LAM WITH ALEF MAKSURA",
    "ۘ": "ARABIC SMALL HIGH MEEM INITIAL FORM",
    "ۙ": "ARABIC SMALL HIGH LAM ALEF",
    "ۚ": "ARABIC SMALL HIGH JEEM",
    "ۛ": "ARABIC SMALL HIGH THREE DOTS",
    "ۜ": "ARABIC SMALL HIGH SEEN",
    "۞": "ARABIC START OF RUB EL HIZB",
    "۩": "ARABIC PLACE OF SAJDAH",
}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _provenance(r: Riwayah) -> dict:
    """Which KFGQPC release every part of this file came from.

    Recorded in the file itself and not only in the manifest, because a mushaf
    file will be copied, mirrored and vendored on its own, and a text whose
    edition cannot be named is not a citable one.
    """
    spec = r.spec
    text = DATA / f"{spec.primary_zip}.zip"
    out = {
        "text": {
            "package": text.name,
            "member": spec.primary_member,
            "release_year": spec.primary_year,
            "sha256": _sha256(text),
        },
        "policy": RELEASE_POLICY,
    }
    if spec.csv_zip:
        layout = DATA / f"{spec.csv_zip}.zip"
        out["layout"] = {
            "package": layout.name,
            "member": spec.csv_member,
            "release_year": spec.csv_year,
            "sha256": _sha256(layout),
            "used_for": ["juz", "line_check"],
        }
    return out


def _marks(w: Kalimah, key: str) -> list[dict]:
    """Every sign printed against this kalimah, with the side it sits on."""
    out = []
    if key in w.hizb:
        out.append({"k": "hizb", "at": "before", "sign": "۞"})
    for sign in w.waqf.get(key, ""):
        if sign == "۩":
            continue                       # emitted below, as its own kind
        out.append({"k": "waqf", "at": "after", "sign": sign})
    if key in w.sajdah:
        out.append({"k": "sajdah", "at": "after", "sign": "۩"})
    return out


def _spans(pairs: list[tuple[int, int]]) -> list[dict]:
    """Collapse ``(value, kalimah_id)`` into ``{n, kalimahs:[first,last]}`` runs."""
    out: list[dict] = []
    for value, wid in pairs:
        if out and out[-1]["n"] == value:
            out[-1]["kalimahs"][1] = wid
        else:
            out.append({"n": value, "kalimahs": [wid, wid]})
    return out


def _surahs(key: str, mine: list[Kalimah], r: Riwayah) -> list[dict]:
    """The 114-row surah header, in full, in every mushaf's own file.

    Duplicated across the seven rather than shared, because a file that needs a
    second download before it can name a surah is not a mushaf that ships alone.
    It costs 114 rows against 77,000 kalimahs.
    """
    printed = {a.surah for a in r.ayahs if a.ayah == 0} | {1}
    by_surah: dict[int, list[Kalimah]] = defaultdict(list)
    for w in mine:
        by_surah[w.surah].append(w)

    out = []
    for surah, ws in sorted(by_surah.items()):
        info = names()[surah]
        safhahs = [w.place[key][0] for w in ws if key in w.place]
        row = {
            "n": surah,
            "name_ar": info["name_ar"],
            "name_en": info["name_en"],
            "revelation": info["revelation"],
            "basmalah": surah in printed,
            "ayahs": max(w.ayah.get(key, 0) for w in ws),
            "kalimahs": [ws[0].id, ws[-1].id],
        }
        if safhahs:
            row["safhahs"] = [min(safhahs), max(safhahs)]
        out.append(row)
    return out


def _resegmentation(key: str, kalimahs: list[Kalimah]) -> list[dict]:
    """Every place this build changed the source's own kalimah spacing.

    A global kalimah ID is only stable because the alignment occasionally overrides
    a package's spacing — joining what one mushaf splits, or splitting what it
    joins — so a file claiming to *be* that mushaf has to say where it did so.
    The list is present even when empty, so silence is never ambiguous.
    """
    out = []
    for event in boundary_events(kalimahs):
        if key not in event["riwayahs"]:
            continue
        ids = [i for i in event["kalimah_ids"]]
        mine = [w for w in kalimahs if w.id in set(ids) and key in w.forms]
        source = next((t for t, ks in event["texts"].items() if key in ks), "")
        out.append({
            "kalimahs": ids,
            "surah": event["surah"],
            "ayah": event["ayah"],
            "kind": event["kind"],
            "source_text": source,
            "emitted": [w.forms[key] for w in mine],
            "riwayahs_agree": event["agree"],
        })
    return out


def _line_check(key: str, mine: list[Kalimah], r: Riwayah) -> dict:
    """Re-check the reconstructed lines against the release that states them.

    The safhah is read from the document; the line is inferred from its flow (see
    :mod:`quranidx.layout`).  The v2 CSV states the line of every ayah, so the
    inference can be scored rather than merely asserted — and the ayahs it gets
    wrong are listed, so a consumer can exclude them instead of discovering them.
    Bazzī has no v2 release, so its lines cannot be checked at all.
    """
    if not r.meta:
        return {"validated": False,
                "reason": "no v2 package released for this riwayah"}

    by_ayah: dict[tuple[int, int], list[Kalimah]] = defaultdict(list)
    for w in mine:
        by_ayah[(w.surah, w.ayah[key])].append(w)

    checked = agreed = 0
    wrong = []
    for k, meta in r.meta.items():
        ws = by_ayah.get(k)
        if not ws or not meta["line_end"].isdigit():
            continue
        checked += 1
        got = max(w.place[key][1] for w in ws if key in w.place)
        want = int(meta["line_end"])
        if got == want:
            agreed += 1
        else:
            wrong.append({"surah": k[0], "ayah": k[1], "derived": got, "source": want})
    return {
        "validated": True,
        "against": r.crosscheck_source,
        "ayahs_checked": checked,
        "ayahs_agreeing": agreed,
        "disagreements": wrong,
    }


def _layers(key: str, r: Riwayah, line_check: dict) -> dict:
    """What this file carries, and why it lacks whatever it lacks."""
    present = ["surahs", "ayahs", "safhahs", "marks"]
    absent: dict[str, str] = {}
    if r.meta:
        present.append("juz")
    else:
        absent["juz"] = "no v2 package released for this riwayah"
    absent["imlaei"] = "column not present in this riwayah's release"

    return {
        "present": present,
        "absent": absent,
        "derived": {
            "line": {
                "how": "reconstructed from the document's line breaks, "
                       "paragraph boundaries and surah headings; printed lines "
                       "are not encoded in the release",
                **{k: v for k, v in line_check.items() if k != "disagreements"},
            },
        },
        "notes": {
            "safhah": "read from explicit safhah breaks in the release, not inferred",
            "waqf": "pause-mark conventions differ by mushaf and are not "
                    "comparable across them: Warsh and Qālūn print one general "
                    "sign where Ḥafṣ, Dūrī and Sūsī print seven distinct ones",
            "hizb": "the ۞ symbol is emitted exactly as the release prints it. "
                    "The releases disagree about how often to print it — 199 "
                    "times in Ḥafṣ, Shuʿbah and Bazzī against 433–437 in the "
                    "others — and nothing here reconciles them",
        },
    }


def _kalimah(w: Kalimah, key: str, imlaei: dict[int, str] | None) -> dict:
    rec: dict = {"w": w.id, "t": w.forms[key]}
    if key in w.place:
        safhah, line = w.place[key]
        rec["pg"] = safhah
        rec["ln"] = line
    if imlaei and w.id in imlaei:
        rec["e"] = imlaei[w.id]
    marks = _marks(w, key)
    if marks:
        rec["marks"] = marks
    if key in w.boundary:
        rec["resegmented"] = True
    return rec


def document(kalimahs: list[Kalimah], r: Riwayah,
             imlaei: dict[int, str] | None = None) -> dict:
    """The whole of one mushaf, in the canonical shape."""
    key = r.key
    mine = [w for w in kalimahs if key in w.forms]

    line_check = _line_check(key, mine, r)
    ayahs = _spans([(w.ayah[key], w.id) for w in mine])
    surah_of = {w.id: w.surah for w in mine}
    for span in ayahs:
        span["surah"] = surah_of[span["kalimahs"][0]]

    doc = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "generated": date.today().isoformat(),
        "mushaf": {
            "key": key,
            "name_en": r.name_en,
            "name_ar": r.name_ar,
            "qari_en": r.qari_en,
            "qari_ar": r.qari_ar,
            "counting": r.counting,
            "ayah_count": sum(1 for a in r.ayahs if a.ayah > 0),
            "kalimah_count": len(mine),
        },
        "provenance": _provenance(r),
        "spine": {
            "kalimah_id_range": [kalimahs[0].id, kalimahs[-1].id],
            "note": "`w` is the global kalimah ID. The same `w` is the same kalimah "
                    "in every mushaf that has it. Kalimahs absent from this mushaf "
                    "leave gaps in the sequence.",
        },
        "layers": _layers(key, r, line_check),
        "mark_signs": {s: {"cp": f"U+{ord(s):04X}", "unicode_name": n}
                       for s, n in MARK_NAMES.items()},
        "surahs": _surahs(key, mine, r),
        "ayahs": [{"surah": s["surah"], "n": s["n"], "kalimahs": s["kalimahs"]}
                  for s in ayahs],
        "safhahs": _spans([(w.place[key][0], w.id) for w in mine if key in w.place]),
        "resegmentation": _resegmentation(key, kalimahs),
        "line_disagreements": line_check.get("disagreements", []),
        "kalimahs": [_kalimah(w, key, imlaei) for w in mine],
    }
    if r.meta:
        doc["juz"] = _spans([(int(r.meta[(w.surah, w.ayah[key])]["jozz"]), w.id)
                             for w in mine
                             if (w.surah, w.ayah[key]) in r.meta
                             and r.meta[(w.surah, w.ayah[key])]["jozz"].isdigit()])
    return doc


def minimal(doc: dict) -> dict:
    """The text and the IDs, and nothing else.

    ``resegmentation`` stays: it is a disclosure about the text itself, so
    dropping it would make the small file quietly less honest than the large one.
    """
    return {
        **{k: doc[k] for k in ("format", "format_version", "generated",
                               "mushaf", "provenance", "spine")},
        "variant": "minimal",
        "surahs": [{k: v for k, v in s.items() if k != "safhahs"}
                   for s in doc["surahs"]],
        "ayahs": doc["ayahs"],
        "resegmentation": doc["resegmentation"],
        "kalimahs": [{"w": w["w"], "t": w["t"]} for w in doc["kalimahs"]],
    }


def _dump(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1),
                    encoding="utf-8")


def write_mushafs(kalimahs: list[Kalimah], riwayahs: list[Riwayah],
                  imlaei: dict[str, dict[int, str]] | None = None,
                  reports: dict | None = None) -> dict:
    """Write every mushaf's own file, and return what was written."""
    MUSHAF_DIR.mkdir(parents=True, exist_ok=True)
    imlaei = imlaei or {}
    docs = {}
    for r in riwayahs:
        doc = document(kalimahs, r, imlaei.get(r.key))
        if reports and r.key in reports:
            doc["layers"]["derived"]["imlaei"] = reports[r.key]
            if reports[r.key].get("available"):
                doc["layers"]["present"].append("imlaei")
                doc["layers"]["absent"].pop("imlaei", None)
        _dump(MUSHAF_DIR / f"{r.key}.json", doc)
        _dump(MUSHAF_DIR / f"{r.key}.min.json", minimal(doc))
        docs[r.key] = doc
    return docs


def write_manifest(docs: dict[str, dict]) -> dict:
    """Every emitted file and every source package, each with its SHA-256.

    A dataset becomes citable when a reader can prove which release a file came
    from without trusting the person who published it.  The manifest is that
    proof: the source hashes let anyone re-derive the build, and the output
    hashes let anyone check that the copy they hold is the one described here.
    """
    files = sorted(p for p in MUSHAF_DIR.rglob("*")
                   if p.is_file() and p.name != "manifest.json")
    extra = [OUT / "quran.sqlite"]

    manifest = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "generated": date.today().isoformat(),
        "normative": [f"out/mushaf/{k}.json" for k in docs],
        "note": "Only the files listed under `normative` define the format. "
                "Everything else is a generated view of them.",
        "sources": {
            k: {n: {kk: vv for kk, vv in part.items() if kk != "used_for"}
                for n, part in doc["provenance"].items()
                if isinstance(part, dict)}
            for k, doc in docs.items()
        },
        "files": [
            {"path": str(p).replace("\\", "/"),
             "bytes": p.stat().st_size,
             "sha256": _sha256(p)}
            for p in files + [x for x in extra if x.exists()]
        ],
    }
    _dump(MUSHAF_DIR / "manifest.json", manifest)
    return manifest
