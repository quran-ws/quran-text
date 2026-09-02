"""Publish each muṣḥaf on its own, keyed to the shared word index.

``out/`` already answers *how do the muṣḥafs differ?*  It does not answer *give
me Warsh*: a consumer who wants one muṣḥaf has to take the comparison and
project it back out.  This module writes the other view — one self-contained
file per muṣḥaf, every word carrying the global ID that means the same word in
all seven.

The shape is flat.  A muṣḥaf is an ordered list of words, and the structures
above a word — āyah, juz, page — are lists of boundaries over word IDs rather
than levels of nesting.  That is the same model as ``out/fawasil.json`` and it
is what keeps the seven files comparable while they count 6,214 to 6,236 āyāt:
nesting words under āyāt would make one path mean a different word in each
muṣḥaf, which is exactly what the global ID exists to prevent.

Only ``out/mushaf/<key>.json`` is normative.  The nested, sharded, CSV and
SQLite forms in :mod:`quranidx.views` are generated from the same build and are
labelled views, so that whichever one turns out to be most convenient cannot
quietly become the standard.

``w`` is not unique within a document: a muṣḥaf with a word Ḥafṣ does not have
carries it on the same ``w`` with a sub-index, so a word is addressed by
``(w, x)``.  The format version stays at 1.0 while nothing is released — there
is no published version to be compatible with, and a number that moves before
anyone can depend on it says nothing.

Nothing here is asserted that the packages do not say.  Where a fact is derived
rather than read it is marked derived, where it is unavailable the field is
absent and the absence is explained, and where this build departs from the
source's own word spacing every instance is listed in the file itself.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

from .build import OUT, Word
from .output import boundary_events
from .sources import DATA, RELEASE_POLICY, Riwaya
from .suras import names

FORMAT = "quran-mushaf"
FORMAT_VERSION = "1.0"

MUSHAF_DIR = OUT / "mushaf"

#: Signs that can attach to a word, with the Unicode name of each.  Emitted in
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


def _provenance(r: Riwaya) -> dict:
    """Which KFGQPC release every part of this file came from.

    Recorded in the file itself and not only in the manifest, because a muṣḥaf
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


def _marks(w: Word, key: str) -> list[dict]:
    """Every sign printed against this word, with the side it sits on."""
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
    """Collapse ``(value, word_id)`` into ``{n, words:[first,last]}`` runs."""
    out: list[dict] = []
    for value, wid in pairs:
        if out and out[-1]["n"] == value:
            out[-1]["words"][1] = wid
        else:
            out.append({"n": value, "words": [wid, wid]})
    return out


def _suras(key: str, mine: list[Word], r: Riwaya) -> list[dict]:
    """The 114-row sūrah header, in full, in every muṣḥaf's own file.

    Duplicated across the seven rather than shared, because a file that needs a
    second download before it can name a sūrah is not a muṣḥaf that ships alone.
    It costs 114 rows against 77,000 words.
    """
    printed = {a.sura for a in r.ayat if a.aya == 0} | {1}
    by_sura: dict[int, list[Word]] = defaultdict(list)
    for w in mine:
        by_sura[w.sura].append(w)

    out = []
    for sura, ws in sorted(by_sura.items()):
        info = names()[sura]
        pages = [w.place[key][0] for w in ws if key in w.place]
        row = {
            "n": sura,
            "name_ar": info["name_ar"],
            "name_en": info["name_en"],
            "revelation": info["revelation"],
            "basmalah": sura in printed,
            "ayat": max(w.aya.get(key, 0) for w in ws),
            "words": [ws[0].id, ws[-1].id],
        }
        if pages:
            row["pages"] = [min(pages), max(pages)]
        out.append(row)
    return out


def _resegmentation(key: str, words: list[Word]) -> list[dict]:
    """Every place this build changed the source's own word spacing.

    A global word ID is only stable because the alignment occasionally overrides
    a package's spacing — joining what one muṣḥaf splits, or splitting what it
    joins — so a file claiming to *be* that muṣḥaf has to say where it did so.
    The list is present even when empty, so silence is never ambiguous.
    """
    out = []
    for event in boundary_events(words):
        if key not in event["riwayat"]:
            continue
        ids = [i for i in event["word_ids"]]
        mine = [w for w in words if w.id in set(ids) and key in w.forms]
        source = next((t for t, ks in event["texts"].items() if key in ks), "")
        out.append({
            "words": ids,
            "sura": event["sura"],
            "ayah": event["aya"],
            "kind": event["kind"],
            "source_text": source,
            "emitted": [w.forms[key] for w in mine],
            "riwayat_agree": event["agree"],
        })
    return out


def _line_check(key: str, mine: list[Word], r: Riwaya) -> dict:
    """Re-check the reconstructed lines against the release that states them.

    The page is read from the document; the line is inferred from its flow (see
    :mod:`quranidx.layout`).  The v2 CSV states the line of every āyah, so the
    inference can be scored rather than merely asserted — and the āyāt it gets
    wrong are listed, so a consumer can exclude them instead of discovering them.
    Bazzī has no v2 release, so its lines cannot be checked at all.
    """
    if not r.meta:
        return {"validated": False,
                "reason": "no v2 package released for this riwāyah"}

    by_ayah: dict[tuple[int, int], list[Word]] = defaultdict(list)
    for w in mine:
        by_ayah[(w.sura, w.aya[key])].append(w)

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
            wrong.append({"sura": k[0], "ayah": k[1], "derived": got, "source": want})
    return {
        "validated": True,
        "against": r.crosscheck_source,
        "ayat_checked": checked,
        "ayat_agreeing": agreed,
        "disagreements": wrong,
    }


def _layers(key: str, r: Riwaya, line_check: dict) -> dict:
    """What this file carries, and why it lacks whatever it lacks."""
    present = ["suras", "ayat", "pages", "marks"]
    absent: dict[str, str] = {}
    if r.meta:
        present.append("juz")
    else:
        absent["juz"] = "no v2 package released for this riwāyah"
    absent["imlaei"] = "column not present in this riwāyah's release"

    return {
        "present": present,
        "absent": absent,
        "derived": {
            "line": {
                "how": "reconstructed from the document's line breaks, "
                       "paragraph boundaries and sūrah headings; printed lines "
                       "are not encoded in the release",
                **{k: v for k, v in line_check.items() if k != "disagreements"},
            },
        },
        "notes": {
            "page": "read from explicit page breaks in the release, not inferred",
            "waqf": "pause-mark conventions differ by muṣḥaf and are not "
                    "comparable across them: Warsh and Qālūn print one general "
                    "sign where Ḥafṣ, Dūrī and Sūsī print seven distinct ones",
            "hizb": "the ۞ symbol is emitted exactly as the release prints it. "
                    "The releases disagree about how often to print it — 199 "
                    "times in Ḥafṣ, Shuʿbah and Bazzī against 433–437 in the "
                    "others — and nothing here reconciles them",
        },
    }


def _word(w: Word, key: str, imlaei: dict[tuple[int, int], str] | None) -> dict:
    rec: dict = {"w": w.id, "t": w.forms[key]}
    if w.sub:
        # This muṣḥaf writes a word the shared text does not have, so it hangs
        # off the previous word's ID rather than taking one of its own.  Absent
        # on every other word, so its presence is the signal.
        rec["x"] = w.sub
    if key in w.place:
        page, line = w.place[key]
        rec["pg"] = page
        rec["ln"] = line
    if imlaei and (w.id, w.sub) in imlaei:
        rec["e"] = imlaei[(w.id, w.sub)]
    marks = _marks(w, key)
    if marks:
        rec["marks"] = marks
    if key in w.boundary:
        rec["resegmented"] = True
    return rec


def document(words: list[Word], r: Riwaya,
             imlaei: dict[tuple[int, int], str] | None = None) -> dict:
    """The whole of one muṣḥaf, in the canonical shape."""
    key = r.key
    mine = [w for w in words if key in w.forms]

    line_check = _line_check(key, mine, r)
    ayat = _spans([(w.aya[key], w.id) for w in mine])
    sura_of = {w.id: w.sura for w in mine}
    for span in ayat:
        span["sura"] = sura_of[span["words"][0]]

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
            "ayah_count": sum(1 for a in r.ayat if a.aya > 0),
            "word_count": len(mine),
        },
        "provenance": _provenance(r),
        "spine": {
            "word_id_range": [words[0].id, words[-1].id],
            "note": "`w` is the global word ID. The same `w` is the same word "
                    "in every muṣḥaf that has it. Words absent from this muṣḥaf "
                    "leave gaps in the sequence.",
        },
        "layers": _layers(key, r, line_check),
        "mark_signs": {s: {"cp": f"U+{ord(s):04X}", "unicode_name": n}
                       for s, n in MARK_NAMES.items()},
        "suras": _suras(key, mine, r),
        "ayat": [{"sura": s["sura"], "n": s["n"], "words": s["words"]}
                 for s in ayat],
        "pages": _spans([(w.place[key][0], w.id) for w in mine if key in w.place]),
        "resegmentation": _resegmentation(key, words),
        "line_disagreements": line_check.get("disagreements", []),
        "words": [_word(w, key, imlaei) for w in mine],
    }
    if r.meta:
        doc["juz"] = _spans([(int(r.meta[(w.sura, w.aya[key])]["jozz"]), w.id)
                             for w in mine
                             if (w.sura, w.aya[key]) in r.meta
                             and r.meta[(w.sura, w.aya[key])]["jozz"].isdigit()])
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
        "suras": [{k: v for k, v in s.items() if k != "pages"}
                  for s in doc["suras"]],
        "ayat": doc["ayat"],
        "resegmentation": doc["resegmentation"],
        "words": [{k: w[k] for k in ("w", "x", "t") if k in w}
                  for w in doc["words"]],
    }


def _dump(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1),
                    encoding="utf-8")


def write_mushafs(words: list[Word], riwayat: list[Riwaya],
                  imlaei: dict[str, dict[tuple[int, int], str]] | None = None,
                  reports: dict | None = None) -> dict:
    """Write every muṣḥaf's own file, and return what was written."""
    MUSHAF_DIR.mkdir(parents=True, exist_ok=True)
    imlaei = imlaei or {}
    docs = {}
    for r in riwayat:
        doc = document(words, r, imlaei.get(r.key))
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
