"""Generate the human-readable comparison report."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import date
from itertools import combinations

from .build import ORDER, OUT, Word
from .normalize import fold_notation, rasm
from .sources import Riwaya
from .suras import names
from .validate import check_counting, check_index, cross_release

STATUS_ORDER = ["identical", "diacritic_variant", "rasm_variant",
                "word_boundary", "partial"]

STATUS_BLURB = {
    "identical": "same reading and same spelling in all seven",
    "diacritic_variant": "same consonantal skeleton, different vowelling or marks",
    "rasm_variant": "the riwāyāt disagree about the letters themselves",
    "word_boundary": "at least one source prints the word joined to its neighbour",
    "partial": "the word is absent from at least one riwāyah",
}


def _table(rows: list[list], header: list[str]) -> str:
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def _pairwise(words: list[Word], keys: list[str]) -> list[dict]:
    stats = []
    for a, b in combinations(keys, 2):
        both = same_form = same_fold = same_rasm = 0
        for w in words:
            fa, fb = w.forms.get(a), w.forms.get(b)
            if fa is None or fb is None:
                continue
            both += 1
            if fa == fb:
                same_form += 1
            if fold_notation(fa) == fold_notation(fb):
                same_fold += 1
            if rasm(fa) == rasm(fb):
                same_rasm += 1
        stats.append({"a": a, "b": b, "shared": both, "same_form": same_form,
                      "same_reading": same_fold, "same_rasm": same_rasm})
    return stats


def write_report(words: list[Word], riwayat: list[Riwaya]) -> None:
    keys = [r.key for r in riwayat]
    by_key = {r.key: r for r in riwayat}
    status = Counter(w.status for w in words)
    pairs = _pairwise(words, keys)
    cross = cross_release(riwayat)

    L: list[str] = []
    add = L.append

    add("# Cross-riwāyah comparison")
    add("")
    add(f"Generated {date.today().isoformat()} from the KFGQPC packages in `data/`. "
        f"{len(words):,} canonical words across {len({w.sura for w in words})} sūrahs "
        f"and {len(keys)} riwāyāt.")
    add("")
    add("Every word carries one ID that means the same word in every riwāyah that "
        "has it. Where the riwāyāt disagree, the disagreement is recorded against "
        "that ID rather than hidden by it.")
    add("")

    # --- inventory --------------------------------------------------------
    add("## The riwāyāt")
    add("")
    add(_table([[
        r.key, r.name_en, r.name_ar, r.qari_en, r.counting,
        f"{sum(1 for a in r.ayat if a.aya > 0):,}",
        f"{sum(1 for w in words if r.key in w.forms):,}",
    ] for r in riwayat],
        ["key", "riwāyah", "الرواية", "qāriʾ", "counting", "āyāt", "words"]))
    add("")
    add("The āyah totals are not errors: the riwāyāt follow different counting "
        "traditions (Kūfī 6236, Madanī 6214, Baṣrī 6217, and the Makkī count "
        "KFGQPC uses for Bazzī, 6220). This is exactly why the index is flat — "
        "the riwāyāt disagree about where āyāt end far more than about words.")
    add("")

    # --- status -----------------------------------------------------------
    add("## What the words look like across riwāyāt")
    add("")
    add(_table([[s, f"{status[s]:,}", f"{100 * status[s] / len(words):.2f}%",
                 STATUS_BLURB[s]] for s in STATUS_ORDER if status[s]],
               ["status", "words", "share", "meaning"]))
    add("")
    add("`identical` compares after folding release notation — the 2022 and 2026 "
        "packages spell the same sukūn and tanwīn with different codepoints "
        "(`U+06E1`/`U+0652`, `U+0657`/`U+08F1`), which is a typographic difference, "
        "not a textual one. The raw spelling of each riwāyah is always kept in "
        "`forms`.")
    add("")

    # --- pairwise ---------------------------------------------------------
    add("## Pairwise agreement")
    add("")
    add("Share of shared words where two riwāyāt agree, at three levels: exact "
        "stored spelling, the same reading once notation is folded, and the "
        "consonantal skeleton.")
    add("")
    add(_table([[
        f"{p['a']}–{p['b']}", f"{p['shared']:,}",
        f"{100 * p['same_form'] / p['shared']:.1f}%",
        f"{100 * p['same_reading'] / p['shared']:.1f}%",
        f"{100 * p['same_rasm'] / p['shared']:.2f}%",
    ] for p in sorted(pairs, key=lambda p: -p["same_rasm"] / p["shared"])],
        ["pair", "shared words", "same spelling", "same reading", "same rasm"]))
    add("")
    add("Rasm agreement never drops below 98%: the seven riwāyāt are one text. "
        "Spelling agreement is far lower because the packages were typeset in "
        "different years with different conventions.")
    add("")

    # --- rasm variants ----------------------------------------------------
    rasm_v = [w for w in words if w.status == "rasm_variant"]
    add("## Rasm variants")
    add("")
    add(f"{len(rasm_v):,} words where the riwāyāt disagree about the letters. "
        f"The full list is in [`rasm-variants.md`](rasm-variants.md) and "
        f"[`conflicts.csv`](conflicts.csv); a sample follows.")
    add("")
    rows = []
    for w in rasm_v[:25]:
        groups = defaultdict(list)
        for k, v in w.forms.items():
            groups[v].append(k)
        rows.append([w.id, f"{w.sura}:{w.aya.get('hafs', '—')}", w.rasm,
                     "  ·  ".join(f"**{v}** {','.join(ks)}" for v, ks in groups.items())])
    add(_table(rows, ["word id", "sūrah:āyah", "rasm", "forms"]))
    add("")

    # --- boundary + partial ----------------------------------------------
    for st, title, blurb in [
        ("word_boundary", "Word-boundary disagreements",
         "One source prints as a single word what the others print as two. Some "
         "are the source's own orthography (Bazzī's `لَأُاْقۡسِمُ`, the traditional "
         "`مَالِ`), and some are dropped spaces — Dūrī's `كَانُواْيَعۡمَلُونَ` at 11:77 "
         "is written with the space in that riwāyah's own 2022 release. Both are "
         "re-segmented so the index keeps one column per word, and both are "
         "recorded here rather than judged."),
        ("partial", "Words absent from some riwāyāt",
         "Genuine textual differences, each well attested."),
    ]:
        items = [w for w in words if w.status == st]
        add(f"## {title}")
        add("")
        add(blurb)
        add("")
        rows = []
        for w in items:
            groups = defaultdict(list)
            for k, v in w.forms.items():
                groups[v].append(k)
            rows.append([
                w.id, f"{w.sura}:{w.aya.get('hafs') or max(w.aya.values())}",
                w.rasm,
                ", ".join(w.missing) or "—",
                "  ·  ".join(f"**{v}** {','.join(ks)}" for v, ks in groups.items()),
            ])
        add(_table(rows, ["word id", "sūrah:āyah", "rasm", "absent from", "forms"]))
        add("")

    # --- source integrity -------------------------------------------------
    add("## Source integrity")
    add("")
    add("Six riwāyāt ship two releases. Comparing them is the sharpest available "
        "check on each, since the publisher is the same.")
    add("")
    add(_table([[
        k, f"{v['ayat_compared']:,}", f"{v['identical']:,}",
        f"{v['notation_only']:,}", f"{v['marks_only']:,}", v["rasm_differs"],
    ] for k, v in cross.items()],
        ["riwāyah", "āyāt compared", "byte-identical", "notation only",
         "marks/vowels only", "rasm differs"]))
    add("")
    add("The `marks/vowels only` column is dominated by the 2026 files adopting "
        "the Arabic Extended-B alif letters (`U+0870`–`U+0879`), which fold an "
        "alif and its vowel into one codepoint where the 2022 files used an alif "
        "plus combining marks. The rasm is untouched, so none of it reaches the "
        "word index.")
    add("")
    problems = check_index(words, riwayat) + check_counting(riwayat)
    add("### Checks")
    add("")
    if problems:
        add(_table([[p["check"], p.get("riwaya", "—"), p["detail"]] for p in problems],
                   ["check", "riwāyah", "detail"]))
    else:
        add("All checks pass.")
    add("")

    # --- per sūrah --------------------------------------------------------
    add("## Per sūrah")
    add("")
    per: dict[int, Counter] = defaultdict(Counter)
    for w in words:
        per[w.sura][w.status] += 1
        per[w.sura]["total"] += 1
    rows = []
    for s in range(1, 115):
        c = per[s]
        variants = c["rasm_variant"] + c["word_boundary"] + c["partial"]
        rows.append([s, names()[s]["name_en"], f"{c['total']:,}",
                     c["identical"], c["diacritic_variant"], c["rasm_variant"],
                     c["word_boundary"] + c["partial"],
                     f"{1000 * variants / c['total']:.1f}"])
    add(_table(rows, ["sūrah", "name", "words", "identical", "diacritic",
                      "rasm", "boundary/absent", "variants per 1000"]))
    add("")

    (OUT / "COMPARISON.md").write_text("\n".join(L), encoding="utf-8")

    # --- full rasm variant listing ---------------------------------------
    V = ["# Rasm variants — full listing", "",
         f"All {len(rasm_v):,} words where the seven riwāyāt disagree about the "
         "letters, in order. Machine-readable equivalents: `conflicts.csv`, "
         "`conflicts.json`.", ""]
    rows = []
    for w in rasm_v:
        groups = defaultdict(list)
        for k, v in w.forms.items():
            groups[v].append(k)
        rows.append([w.id, f"{w.sura}:{w.aya.get('hafs', '—')}", w.index, w.rasm,
                     "  ·  ".join(f"**{v}** {','.join(ks)}" for v, ks in groups.items())])
    V.append(_table(rows, ["word id", "sūrah:āyah", "word #", "rasm", "forms"]))
    (OUT / "rasm-variants.md").write_text("\n".join(V), encoding="utf-8")

    # --- matrix as csv ----------------------------------------------------
    with (OUT / "agreement-matrix.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["riwaya_a", "riwaya_b", "shared_words", "same_spelling",
                     "same_reading", "same_rasm"])
        for p in pairs:
            wr.writerow([p["a"], p["b"], p["shared"], p["same_form"],
                         p["same_reading"], p["same_rasm"]])
