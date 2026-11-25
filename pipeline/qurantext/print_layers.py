"""Layers of another printed edition over the words of a muṣḥaf already published.

``data/print/<key>.json`` holds where one printed edition breaks its pages and
lines and which waqf signs it prints, as positions into the ``words`` of a
muṣḥaf file.  It holds no words.  The word list is pinned by count and SHA-256:
if it ever changes, the build fails until the evidence is held against the new
list.

The evidence is ``sources/prints/<key>/``: ``print.json`` says which scans were
read, how, and what was used as a starting point; ``lines.csv`` and
``waqf.csv`` give every line start and every sign with the way it was proved.
A row whose ``proof`` is ``unproved`` is not published.  It is listed in
the document under ``unproved``.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
from bisect import bisect_right
from collections import Counter

from . import paths, stamp

FORMAT = "quran-print-layers"
FORMAT_VERSION = "1.0"

PRINTS = paths.SOURCES / "prints"
OUT = paths.DATA / "print"
REPORTS = paths.DATA / "reports"
SCHEMA = paths.SCHEMA / "print-layers-1.0.json"

UNPROVED = "unproved"
#: The waqf signs looked for.  The saktah seen is not one of them.
WAQF = "ۖۗۘۙۚۛ"
PAGES = 604


class PrintError(ValueError):
    """The evidence does not fit the words it points at."""


def words_sha256(words: list[str]) -> str:
    """SHA-256 of the words joined with a line feed, UTF-8, none trailing."""
    return hashlib.sha256("\n".join(words).encode("utf-8")).hexdigest()


def word_keys(doc: dict) -> list[str]:
    """``surah:ayah:word`` of every position, in the muṣḥaf's own count."""
    out, a = [], -1
    starts = doc["ayah_starts"]
    for position in range(len(doc["words"])):
        if a + 1 < len(starts) and starts[a + 1] == position:
            a += 1
        surah = bisect_right(doc["surah_starts"], position)
        ayah = a - doc["surahs"][surah - 1]["first_ayah"] + 1
        out.append(f"{surah}:{ayah}:{position - starts[a] + 1}")
    return out


def _rows(raw: bytes) -> list[dict]:
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))


def document(key: str, base: dict) -> dict:
    """The layer document of one printed edition over ``base``."""
    folder = PRINTS / key
    raw = {n: (folder / n).read_bytes() for n in ("print.json", "lines.csv", "waqf.csv")}
    info = json.loads(raw["print.json"])
    words, refs = base["words"], word_keys(base)
    digest = words_sha256(words)
    if base["mushaf"]["key"] != info["base"]["mushaf"]:
        raise PrintError(f"{key}: evidence is over {info['base']['mushaf']}")
    if (len(words), digest) != (info["base"]["word_count"], info["base"]["words_sha256"]):
        raise PrintError(f"{key}: the words of {base['mushaf']['key']} are not the ones "
                         "the print was read against")
    if base["counting"]["ayah_count"] != info["base"]["ayah_count"]:
        raise PrintError(f"{key}: āyah count differs from the evidence")
    at = {r: i for i, r in enumerate(refs)}

    lines = _rows(raw["lines.csv"])
    line_starts, page_starts, proof = [], [], Counter()
    row_before, unproved_lines = (0, 0), []
    for r in lines:
        row = (int(r["page"]), int(r["line"]))
        position = at[r["word"]]
        if row <= row_before or (line_starts and position <= line_starts[-1]):
            raise PrintError(f"{key}: lines.csv is out of order at {r['word']}")
        proof[r["proof"]] += 1
        line_starts.append(position)
        if r["proof"] == UNPROVED:
            unproved_lines.append({"position": position, "word": r["word"], "page": row[0], "line": row[1]})
        if row[0] != row_before[0]:
            if row[0] != row_before[0] + 1:
                raise PrintError(f"{key}: page {row_before[0] + 1} has no line")
            page_starts.append(position)
        row_before = row
    if unproved_lines:
        raise PrintError(f"{key}: {len(unproved_lines)} line starts are unproved")
    if line_starts[0] != 0 or len(page_starts) != PAGES:
        raise PrintError(f"{key}: {len(page_starts)} pages from position {line_starts[0]}")

    marks, unproved_waqf, waqf_proof, by_sign = [], [], Counter(), Counter()
    types: list[dict] = []
    for r in _rows(raw["waqf.csv"]):
        position, sign = at[r["word"]], r["sign"]
        if len(sign) != 1 or sign not in WAQF:
            raise PrintError(f"{key}: {sign!r} at {r['word']} is not a waqf sign")
        waqf_proof[r["proof"]] += 1
        if r["proof"] == UNPROVED:
            unproved_waqf.append({"position": position, "word": r["word"], "candidate": sign, "note": r["note"]})
            continue
        if marks and marks[-1][0] >= position:
            raise PrintError(f"{key}: waqf.csv is out of order at {r['word']}")
        kind = {"kind": "waqf", "side": "after", "sign": sign}
        if kind not in types:
            types.append(kind)
        marks.append([position, types.index(kind)])
        by_sign[sign] += 1

    return {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "generated": stamp.generated(),
        "edition": info["edition"],
        "base": {"mushaf": info["base"]["mushaf"], "file": f"data/mushaf/{info['base']['mushaf']}.json",
                 "word_count": len(words), "words_sha256": digest,
                 "words_sha256_of": "the words joined with one line feed (U+000A), UTF-8, no trailing line feed"},
        "provenance": {
            "evidence": [{"path": f"sources/prints/{key}/{n}", "sha256": hashlib.sha256(b).hexdigest()}
                         for n, b in raw.items()],
            "prints": info["prints"],
            "method": info["method"],
            "starting_points": info["starting_points"],
            "open_questions": info["open_questions"],
        },
        "layers": {
            "present": ["pages", "lines", "waqf"],
            "absent": info["absent"],
            "proof_vocabulary": info["proof_vocabulary"],
            "proof": {"lines": dict(sorted(proof.items())), "waqf": dict(sorted(waqf_proof.items()))},
            "waqf_by_sign": dict(sorted(by_sign.items())),
        },
        "page_starts": page_starts,
        "line_starts": line_starts,
        "marks": marks,
        "mark_types": types,
        "unproved": {"waqf": unproved_waqf},
    }


def differences(doc: dict, base: dict) -> dict:
    """What the print does differently from the base muṣḥaf, layer by layer."""
    refs, n = word_keys(base), len(base["words"])

    def units(starts):
        return [bisect_right(starts, i) for i in range(n)]

    pages = [(i, a, b) for i, (a, b) in enumerate(zip(units(base["page_starts"]), units(doc["page_starts"])))
             if a != b]
    ours, theirs = set(doc["line_starts"]), set(base["line_starts"])

    def signs(d):
        out: dict[int, str] = {}
        for p, t in d["marks"]:
            m = d["mark_types"][t]
            if m["kind"] == "waqf" and m["sign"] in WAQF:
                out[p] = out.get(p, "") + m["sign"]
        return out

    held = {x["position"] for x in doc["unproved"]["waqf"]}
    a, b = signs(base), signs(doc)
    waqf = [(i, a.get(i, ""), b.get(i, "")) for i in sorted(set(a) | set(b))
            if a.get(i) != b.get(i) and i not in held]
    return {"refs": refs, "pages": pages,
            "page_starts_shared": len(set(doc["page_starts"]) & set(base["page_starts"])),
            "lines_shared": len(ours & theirs),
            "lines_only_print": sorted(ours - theirs), "lines_only_base": sorted(theirs - ours),
            "waqf": waqf, "waqf_shared": sum(a.get(i) == s for i, s in b.items())}


def write_differences(doc: dict, base: dict) -> dict:
    """``data/reports/<key>-differences.{md,csv}``."""
    d, key = differences(doc, base), doc["edition"]["key"]
    words, refs = base["words"], d["refs"]
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["layer", "position", "word_key", "word", "base", "print"])
    for i, x, y in d["pages"]:
        w.writerow(["page", i, refs[i], words[i], x, y])
    for i in d["lines_only_base"]:
        w.writerow(["line_start", i, refs[i], words[i], "start", ""])
    for i in d["lines_only_print"]:
        w.writerow(["line_start", i, refs[i], words[i], "", "start"])
    for i, x, y in d["waqf"]:
        w.writerow(["waqf", i, refs[i], words[i], x, y])
    (REPORTS / f"{key}-differences.csv").write_text(buf.getvalue(), encoding="utf-8")

    kinds = Counter((x or "none", y or "none") for _, x, y in d["waqf"])
    runs: list[list] = []
    for i, x, y in d["pages"]:
        if runs and runs[-1][1] == i - 1 and runs[-1][2:] == [x, y]:
            runs[-1][1] = i
        else:
            runs.append([i, i, x, y])
    total, proof = len(doc["line_starts"]), doc["layers"]["proof"]
    out = [f"# {doc['edition']['name_en']} against the current Ḥafṣ",
           "",
           f"Generated by `pipeline/build.py` from `data/print/{key}.json` and "
           f"`{doc['base']['file']}`. Every row is in `{key}-differences.csv`.",
           "",
           "| | same | different |", "|---|---|---|",
           f"| words and their order | {len(words):,} | 0 (not a finding: the layers point at the same list) |",
           f"| word on the same page | {len(words) - len(d['pages']):,} | {len(d['pages']):,} |",
           f"| page starts | {d['page_starts_shared']:,} of {len(doc['page_starts']):,} | "
           f"{len(doc['page_starts']) - d['page_starts_shared']:,} |",
           f"| line starts | {d['lines_shared']:,} of {total:,} | {len(d['lines_only_print']):,} |",
           f"| waqf signs | {d['waqf_shared']:,} of {len(doc['marks']):,} in the print | {len(d['waqf']):,} words |",
           "", "## Waqf", "",
           "The signs the two print at the same word. «none» is no waqf sign. The saktah sīn "
           "is in neither count: it was not read from the print.", "",
           "| current Ḥafṣ | this print | words |", "|---|---|---|"]
    out += [f"| {x} | {y} | {c} |" for (x, y), c in sorted(kinds.items(), key=lambda z: (-z[1], z[0]))]
    out += ["", "| word | | current Ḥafṣ | this print |", "|---|---|---|---|"]
    out += [f"| {refs[i]} | {words[i]} | {x or 'none'} | {y or 'none'} |" for i, x, y in d["waqf"]]
    out += ["", "## Words on another page", "", "| words | count | current Ḥafṣ | this print |", "|---|---|---|---|"]
    out += [f"| {refs[i]} to {refs[j]} | {j - i + 1} | {x} | {y} |" for i, j, x, y in runs]
    out += ["", "## How the print was read", "",
            f"Line starts: {', '.join(f'{v:,} {k}' for k, v in proof['lines'].items())}. "
            f"Waqf signs: {', '.join(f'{v:,} {k}' for k, v in proof['waqf'].items())}. "
            f"See `docs/print-1405.md`.", ""]
    (REPORTS / f"{key}-differences.md").write_text("\n".join(out), encoding="utf-8")
    return d


def write_prints(docs: dict[str, dict]) -> dict[str, dict]:
    """Write every printed edition that has evidence under ``sources/prints/``."""
    OUT.mkdir(parents=True, exist_ok=True)
    out = {}
    for folder in sorted(p for p in PRINTS.iterdir() if p.is_dir()):
        base = docs[json.loads((folder / "print.json").read_text(encoding="utf-8"))["base"]["mushaf"]]
        doc = document(folder.name, base)
        if doc["edition"]["key"] != folder.name:
            raise PrintError(f"{folder.name}: print.json is for {doc['edition']['key']}")
        (OUT / f"{folder.name}.json").write_text(
            json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        write_differences(doc, base)
        out[folder.name] = doc
    return out


def check_prints(prints: dict[str, dict], docs: dict[str, dict]) -> list[dict]:
    """The layer documents fit their words, and their schema."""
    from .validate import check_schema_fields
    problems = list(check_schema_fields(prints, SCHEMA))
    for key, doc in prints.items():
        base = docs[doc["base"]["mushaf"]]
        n = len(base["words"])
        for layer in ("page_starts", "line_starts"):
            s = doc[layer]
            if s != sorted(set(s)) or s[0] != 0 or s[-1] >= n:
                problems.append({"check": "print_positions", "riwayah": key, "detail": f"{layer} is not increasing"})
        if not set(doc["page_starts"]) <= set(doc["line_starts"]):
            problems.append({"check": "print_pages", "riwayah": key, "detail": "a page does not start a line"})
        for p, t in doc["marks"]:
            if not (0 <= p < n and 0 <= t < len(doc["mark_types"])):
                problems.append({"check": "print_marks", "riwayah": key, "detail": f"mark [{p}, {t}] out of range"})
                break
        if doc["base"]["words_sha256"] != words_sha256(base["words"]):
            problems.append({"check": "print_words", "riwayah": key, "detail": "words_sha256 does not match"})
    return problems
