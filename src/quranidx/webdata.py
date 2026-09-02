"""Assemble the payload embedded in the HTML review page.

Only what a reviewer actually needs is included: every disagreement in full,
summary statistics, and a few complete sūrahs so the flat word model can be
seen rather than described.  The whole corpus stays in ``out/`` — the review
page is for judging the result, not for holding it.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations

from .build import OUT, Word
from .normalize import fold_notation, rasm
from .sources import Riwaya
from .suras import names
from .validate import cross_release

#: Sūrahs shipped complete, to show the word model end to end.
SAMPLE_SURAS = [1, 108, 112]


def _groups(w: Word) -> list[dict]:
    """Riwāyāt collapsed by shared spelling — one row per distinct reading."""
    by_form: dict[str, list[str]] = defaultdict(list)
    for key, form in w.forms.items():
        by_form[form].append(key)
    return [{"form": f, "riwayat": ks} for f, ks in by_form.items()]


def _word(w: Word, full: bool = False) -> dict:
    rec = {
        "id": w.id, "s": w.sura, "i": w.index, "rasm": w.rasm,
        "uthmani": w.uthmani, "status": w.status,
        "aya": w.aya.get("hafs") or (max(w.aya.values()) if w.aya else 0),
        "groups": _groups(w),
    }
    if w.missing:
        rec["missing"] = w.missing
    if w.boundary:
        rec["boundary"] = w.boundary
    if full:
        rec["ayaAll"] = w.aya
        rec["simple"] = w.simple
        rec["key"] = w.key
    return rec


def payload(words: list[Word], riwayat: list[Riwaya]) -> dict:
    keys = [r.key for r in riwayat]
    status = Counter(w.status for w in words)

    pairs = []
    for a, b in combinations(keys, 2):
        both = form = read = skeleton = 0
        for w in words:
            fa, fb = w.forms.get(a), w.forms.get(b)
            if fa is None or fb is None:
                continue
            both += 1
            form += fa == fb
            read += fold_notation(fa) == fold_notation(fb)
            skeleton += rasm(fa) == rasm(fb)
        pairs.append({"a": a, "b": b, "n": both, "form": form,
                      "read": read, "rasm": skeleton})

    per_sura = []
    grouped: dict[int, list[Word]] = defaultdict(list)
    for w in words:
        grouped[w.sura].append(w)
    for s in range(1, 115):
        ws = grouped[s]
        c = Counter(w.status for w in ws)
        per_sura.append({
            "s": s, **{k: names()[s][k] for k in ("name_en", "name_ar", "revelation")},
            "n": len(ws),
            "identical": c["identical"], "diacritic": c["diacritic_variant"],
            "rasm": c["rasm_variant"], "boundary": c["word_boundary"],
            "partial": c["partial"],
            "ayat": {r.key: max((w.aya.get(r.key, 0) for w in ws), default=0)
                     for r in riwayat},
        })

    flagged = [w for w in words
               if w.status in ("rasm_variant", "word_boundary", "partial")]

    return {
        "wordCount": len(words),
        "riwayat": [{
            "key": r.key, "en": r.name_en, "ar": r.name_ar,
            "qari": r.qari_en, "qariAr": r.qari_ar, "counting": r.counting,
            "ayat": sum(1 for a in r.ayat if a.aya > 0),
            "words": sum(1 for w in words if r.key in w.forms),
            "source": r.source.split(":: ")[-1],
        } for r in riwayat],
        "status": dict(status),
        "pairs": pairs,
        "perSura": per_sura,
        "conflicts": [_word(w) for w in flagged],
        "samples": {str(s): {"name_en": names()[s]["name_en"],
                             "name_ar": names()[s]["name_ar"],
                             "words": [_word(w, full=True) for w in grouped[s]]}
                    for s in SAMPLE_SURAS},
        "crossRelease": cross_release(riwayat),
    }


def write_payload(words: list[Word], riwayat: list[Riwaya]) -> int:
    data = payload(words, riwayat)
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    (OUT / "review-data.json").write_text(text, encoding="utf-8")
    return len(text)
