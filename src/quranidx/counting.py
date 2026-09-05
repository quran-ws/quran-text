"""Which counting system each edition follows, and what it does at points of khilāf.

An āyah count is not a property of the qirāʾah.  It is a property of the
**edition**, and there is a level in between:

* a **counting system** — one of the six madhhabs of ʿadd al-āy, as the
  classical sources define it: المدني الأول, المدني الأخير, المكي, البصري,
  الدمشقي, الكوفي;
* a **transmission within the system** — the system reached us through more
  than one authority, and at some points they differ: Abū Jaʿfar and Shayba
  differ at 3:92, 3:97, 37:167, 67:9, 80:24 and 81:26 inside the First Madinan;
* an **edition** — one printing declares a system and, at the points of khilāf
  inside it, follows one authority, a stated rule, or sets them aside.

Three KFGQPC printings of the Dūrī muṣḥaf carry two different āyah divisions
and three different colophons.  None of that is an error; it is the third level
doing its job, and a string cannot hold it.  So ``mushaf.counting`` is a block:
the system, **derived** by comparing the edition's own ``ayah_starts`` to each
system's boundaries; what the edition declares about itself; and every point
where the sources record a disagreement inside that system, with what this
edition does there and whose position that is.  Whatever is left over — an
āyah end where the edition differs from the system and no source records a
khilāf — is ``unexplained``, and the build fails on any that is not already an
acknowledged open finding.

The boundaries come from `qiraat-ayah-map <https://github.com/quranpedia/qiraat-ayah-map>`_,
vendored at a pinned commit under ``data/counting/``; the khilāf inside a
system, which that repository does not yet model, is this repository's overlay
``data/counting/khilaf.json``, cited point by point.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from collections import defaultdict
from datetime import date
from functools import lru_cache
from pathlib import Path

from .build import ORDER, OUT, Word, ayah_ends

COUNTING_DIR = Path("data/counting")
PRIMITIVES = COUNTING_DIR / "book-boundary-primitives.json"
SYSTEMS = COUNTING_DIR / "counting-systems.json"
KHILAF = COUNTING_DIR / "khilaf.json"
OPEN_FINDINGS = COUNTING_DIR / "open-findings.json"
DECLARED = COUNTING_DIR / "declared.json"
UPSTREAM = {
    "repository": "https://github.com/quranpedia/qiraat-ayah-map",
    "commit": "076255281ec6f76241d7e901e27072733d02a18d",
}

#: The upstream build resolves an anchor that occurs twice in its āyah to the
#: first occurrence for an internal point and the last for an end, with this
#: one exception.  Mirrored so the two repositories place the same boundary.
OCCURRENCE_OVERRIDES = {(7, 38, "internal", "النار"): 2}


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------

def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(maxsize=None)
def systems() -> dict[str, dict]:
    raw = _load(SYSTEMS)
    return {k: v for k, v in raw.items() if isinstance(v, dict) and "name_ar" in v}


@lru_cache(maxsize=None)
def system_order() -> list[str]:
    return list(_load(PRIMITIVES)["_counting_system_order"])


def _anchor(rec: dict) -> tuple[int, int, str, str]:
    return rec["sura"], rec["ayah"], rec["kind"], rec["word"]


@lru_cache(maxsize=None)
def points() -> dict[tuple[int, int, str, str], dict]:
    """Every disputed boundary, keyed by anchor, with the vendored ``counted_by``
    and this repository's corrections and khilāf applied."""
    out: dict[tuple, dict] = {}
    prim = _load(PRIMITIVES)
    for sura, ayahs in prim["surahs"].items():
        for ayah, rec in ayahs.items():
            if "end" in rec:
                p = rec["end"]
                out[(int(sura), int(ayah), "end", p["word"])] = {
                    "counted_by": set(p["counted_by"]), "khilaf": {}}
            for p in rec.get("internal", []):
                out[(int(sura), int(ayah), "internal", p["word"])] = {
                    "counted_by": set(p["counted_by"]), "khilaf": {}}

    overlay = _load(KHILAF)
    for c in overlay["system_corrections"]:
        key = _anchor(c)
        if key not in out:
            raise ValueError(f"system_corrections names an unknown point {key}")
        (out[key]["counted_by"].add if c["counted"] else out[key]["counted_by"].discard)(c["system"])
    for k in overlay["khilaf"]:
        key = _anchor(k)
        if key not in out:
            raise ValueError(f"khilaf.json names an unknown point {key}")
        out[key]["khilaf"][k["system"]] = {
            "authorities": dict(k["authorities"]),
            "source": {**{kk: vv for kk, vv in overlay["source_default"].items()},
                       **k.get("source", {})},
        }
    return out


@lru_cache(maxsize=None)
def authorities() -> dict[str, dict]:
    return dict(_load(KHILAF)["authorities"])


@lru_cache(maxsize=None)
def open_findings() -> list[dict]:
    return list(_load(OPEN_FINDINGS)["findings"])


@lru_cache(maxsize=None)
def declared() -> dict[str, dict | None]:
    return dict(_load(DECLARED)["declared"])


def provenance() -> dict:
    return {
        **UPSTREAM,
        "files": {p.name: _sha256(p) for p in (PRIMITIVES, SYSTEMS)},
        "overlay": {p.name: _sha256(p) for p in (KHILAF, OPEN_FINDINGS, DECLARED)},
    }


# --------------------------------------------------------------------------
# anchors -> numbers
# --------------------------------------------------------------------------

_FOLD = {"ٱ": "ا", "أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه",
         "ء": "", "ـ": "", "۞": "", "۩": ""}
_SEATS = ({"ئ": "ي", "ؤ": "و"}, {"ئ": "", "ؤ": ""})
_TABLES = [str.maketrans({**_FOLD, **seat}) for seat in _SEATS]


def fold(text: str) -> set[str]:
    """The comparison keys an anchor word and a muṣḥaf word can both reach.

    Marks and formatting characters are dropped, the hamza in all its seats is
    dropped and the alif forms unified — close to the treatment the upstream
    build applies to its plain text.  A seated hamza is folded both to its
    seat and to nothing (``إسرائيل`` against ``إِسۡرَٰٓءِيلَ``).
    """
    text = unicodedata.normalize("NFC", text)
    text = "".join(c for c in text
                   if not unicodedata.category(c).startswith(("M", "C")))
    return {text.translate(table) for table in _TABLES}


def loose(keys: set[str]) -> set[str]:
    """The same keys without their alifs — a second tier, for ``simple``
    writing a superscript alif out on the line where the anchor does not
    (``موسى``).  Tried only when nothing matches exactly, since it would
    otherwise let ``كثير`` match ``كثيرا``."""
    return {k.replace("ا", "") for k in keys}


def _candidates(w: Word) -> set[str]:
    return fold(w.simple) | fold(w.pointed) | fold(w.uthmani)


def _last_covered(words: list[Word], w: Word) -> int:
    """The boundary follows the printed word, so it follows the *last* number
    that word covers."""
    last = w.id
    for nxt in words[w.id:]:
        if "hafs" in nxt.continuation:
            last = nxt.id
        else:
            break
    return last


_RESOLVED: dict[int, tuple[dict, list]] = {}


def _resolve(words: list[Word]) -> tuple[dict, list]:
    if id(words) in _RESOLVED:
        return _RESOLVED[id(words)]
    by_ayah: dict[tuple[int, int], list[Word]] = defaultdict(list)
    for w in words:
        if "hafs" in w.forms and "hafs" not in w.continuation:
            by_ayah[(w.sura, w.aya["hafs"])].append(w)
    edition_ends = [set(ayah_ends(words, k)) for k in ORDER]

    resolved: dict[tuple, int] = {}
    ambiguous: list[dict] = []
    for key in points():
        sura, ayah, kind, word = key
        target = fold(word)
        ws = by_ayah[(sura, ayah)]
        hits = [w for w in ws if target & _candidates(w)]
        if not hits:
            hits = [w for w in ws if loose(target) & loose(_candidates(w))]
        if not hits:
            raise ValueError(f"anchor {sura}:{ayah} {kind} «{word}» not found in Ḥafṣ")
        # An end point is the Kūfī āyah's last word by definition; an internal
        # point cannot be, so an occurrence there is not a candidate.
        if kind == "end" and ws[-1] in hits:
            hits = [ws[-1]]
        elif kind == "internal" and len(hits) > 1:
            hits = [w for w in hits if w is not ws[-1]]
        numbers = [_last_covered(words, w) for w in hits]
        if len(hits) == 1:
            resolved[key] = numbers[0]
            continue
        # The anchor occurs more than once in its āyah.  qiraat-ayah-map anchors
        # by word text and resolves this in its build by a rule (first for an
        # internal point, last for an end, one override); their issue #11 is to
        # anchor by number instead.  Until then the occurrence is the one the
        # editions actually end at — the seven files are evidence the rule is
        # not — and the rule is the fallback when no edition ends at either.
        votes = [sum(n in ends for ends in edition_ends) for n in numbers]
        if max(votes):
            taken, by = votes.index(max(votes)) + 1, "editions"
        else:
            taken, by = OCCURRENCE_OVERRIDES.get(
                key, len(hits) if kind == "end" else 1), "upstream rule"
        resolved[key] = numbers[taken - 1]
        ambiguous.append({"anchor": f"{sura}:{ayah}:{kind}:{word}",
                          "occurrences": len(hits), "taken": taken,
                          "decided_by": by, "number": resolved[key]})
    _RESOLVED[id(words)] = (resolved, ambiguous)
    return resolved, ambiguous


def resolve_anchors(words: list[Word]) -> tuple[dict[tuple, int], list[dict]]:
    """anchor -> the number the boundary follows, in Ḥafṣ's āyah.

    Returns the map and a report of every anchor that occurred more than once
    in its āyah, with the occurrence taken and what decided it — so an
    ambiguity upstream is visible here rather than silently resolved.
    """
    resolved, ambiguous = _resolve(words)
    return dict(resolved), [dict(a) for a in ambiguous]


# --------------------------------------------------------------------------
# systems and editions
# --------------------------------------------------------------------------

def system_ends(words: list[Word], anchors: dict[tuple, int]) -> dict[str, set[int]]:
    """For every system, the set of numbers after which an āyah ends."""
    kufi = set(ayah_ends(words, "hafs"))
    out: dict[str, set[int]] = {}
    for system in system_order():
        ends = set(kufi)
        for key, p in points().items():
            n = anchors[key]
            if system in p["counted_by"]:
                ends.add(n)
            else:
                ends.discard(n)
        out[system] = ends
    return out


def _edition_ends(words: list[Word], key: str) -> set[int]:
    return set(ayah_ends(words, key))


def _ayah_of(words: list[Word], key: str, n: int) -> tuple[int, int]:
    w = words[n - 1]
    return w.sura, w.aya.get(key, 0)


def _khilaf_entry(words: list[Word], key: str, anchor: tuple, n: int,
                  counted: bool, p: dict, system: str) -> dict:
    auth = p["khilaf"][system]["authorities"]
    sura, ayah = _ayah_of(words, key, n)
    return {
        "sura": sura, "ayah": ayah, "kufi": f"{anchor[0]}:{anchor[1]}",
        "word": n, "anchor": anchor[3],
        "counted": counted,
        "follows": [a for a, v in auth.items() if v == counted],
        "against": [a for a, v in auth.items() if v != counted],
        "source": p["khilaf"][system]["source"],
    }


def derive(doc: dict, words: list[Word]) -> dict:
    """The ``counting`` block of one edition's file, from its own āyah layer."""
    key = doc["mushaf"]["key"]
    anchors, ambiguous = resolve_anchors(words)
    per_system = system_ends(words, anchors)
    mine = _edition_ends(words, key)

    distance = {s: len(mine ^ ends) for s, ends in per_system.items()}
    system = min(system_order(), key=lambda s: (distance[s], system_order().index(s)))
    diff = mine ^ per_system[system]

    khilaf, unexplained = [], []
    for anchor, p in sorted(points().items(), key=lambda kv: anchors[kv[0]]):
        n = anchors[anchor]
        if system in p["khilaf"]:
            khilaf.append(_khilaf_entry(words, key, anchor, n, n in mine, p, system))
            diff.discard(n)
    for n in sorted(diff):
        anchor = next((a for a, m in anchors.items() if m == n), None)
        sura, ayah = _ayah_of(words, key, n)
        unexplained.append({
            "sura": sura, "ayah": ayah,
            "kufi": f"{anchor[0]}:{anchor[1]}" if anchor else None,
            "word": n, "anchor": anchor[3] if anchor else None,
            "counted": n in mine,
        })

    basmalah_counted = not any(w.aya.get(key) == 0 for w in words if w.sura == 1)
    info = systems()[system]
    stated = declared().get(key)
    block = {
        "system": system,
        "system_name_ar": info["name_ar"],
        "system_name_en": info["name_en"],
        "declared_by": stated,
        "ayah_count": len(doc["ayah_starts"]),
        "basmalah_counted": basmalah_counted,
        "khilaf": khilaf,
        "unexplained": unexplained,
        "distance_to_systems": {s: distance[s] for s in system_order()},
        "checked_against": provenance(),
    }
    if stated and stated.get("system") and stated["system"] != system:
        block["declared_disagrees"] = True
    if ambiguous:
        block["resolved_anchors"] = ambiguous
    return block


def reference_total(system: str) -> int:
    """The system's classical total, with the overlay's corrections applied."""
    total = systems()[system]["total_ayahs"]
    for c in _load(KHILAF)["system_corrections"]:
        if c["system"] == system:
            total += 1 if c["counted"] else -1
    return total


def write_fawasil(words: list[Word], docs: dict[str, dict]) -> dict:
    """``out/fawasil.json``: every system's boundaries as numbers, and the
    editions that follow each, with their khilāf resolutions alongside."""
    anchors, ambiguous = resolve_anchors(words)
    per_system = system_ends(words, anchors)
    by_anchor = {n: a for a, n in anchors.items()}

    out_systems = {}
    for system in system_order():
        info = systems()[system]
        editions = [
            {"mushaf": k, "ayah_count": d["counting"]["ayah_count"],
             "basmalah_counted": d["counting"]["basmalah_counted"],
             "khilaf": d["counting"]["khilaf"],
             "unexplained": d["counting"]["unexplained"]}
            for k, d in docs.items() if d["counting"]["system"] == system]
        out_systems[system] = {
            "name_ar": info["name_ar"],
            "name_en": info["name_en"],
            "reference_total": reference_total(system),
            "editions": editions,
            "khilaf_points": [
                {"kufi": f"{a[0]}:{a[1]}", "anchor": a[3], "word": anchors[a],
                 "authorities": p["khilaf"][system]["authorities"],
                 "source": p["khilaf"][system]["source"]}
                for a, p in sorted(points().items(), key=lambda kv: anchors[kv[0]])
                if system in p["khilaf"]],
            "ends": sorted(per_system[system]),
        }

    doc = {
        "format": "quran-fawasil",
        "format_version": "1.0",
        "generated": date.today().isoformat(),
        "model": "Each system lists the shared number after which every one of "
                 "its āyāt ends. The count belongs to the edition, not the "
                 "qirāʾah: an edition is listed under the system its own "
                 "ayah_starts match, with what it does at every point where "
                 "the system's own authorities disagree.",
        "source": provenance(),
        "disputed_points": [
            {"kufi": f"{a[0]}:{a[1]}", "kind": a[2], "anchor": a[3], "word": n,
             "counted_by": sorted(points()[a]["counted_by"], key=system_order().index)}
            for n, a in sorted(by_anchor.items())],
        "systems": out_systems,
        "open_findings": open_findings(),
        "resolved_anchors": ambiguous,
    }
    (OUT / "fawasil.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    return doc


def check_unexplained(docs: dict[str, dict]) -> list[dict]:
    """Every ``unexplained`` point must be an acknowledged open finding, and
    every acknowledged finding must still occur — a stale allowlist fails too."""
    problems = []
    allowed = {(f["mushaf"], f["sura"], f["ayah"]) for f in open_findings()}
    seen = set()
    for key, doc in docs.items():
        for u in doc["counting"]["unexplained"]:
            k = (key, u["sura"], u["ayah"])
            seen.add(k)
            if k not in allowed:
                problems.append({"check": "counting_unexplained", "riwaya": key,
                                 "detail": f"āyah end at {u['sura']}:{u['ayah']} "
                                           f"(after number {u['word']}) differs from "
                                           f"{doc['counting']['system']} and no "
                                           f"source records a khilāf there"})
    for k in allowed - seen:
        problems.append({"check": "counting_open_finding_stale",
                         "riwaya": k[0],
                         "detail": f"open finding {k[1]}:{k[2]} no longer occurs"})
    return problems
