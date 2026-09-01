"""Generate the human-readable comparison report."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import date
from itertools import combinations

from .build import ORDER, OUT, Word, fawasil
from .normalize import fold_notation, pointed, rasm
from .output import boundary_events
from .sources import Riwaya
from .suras import names
from .validate import (check_counting, check_index, check_release_policy,
                       cross_release)

STATUS_ORDER = ["identical", "diacritic_variant", "dotting_variant",
                "rasm_variant", "word_boundary", "partial"]

STATUS_BLURB = {
    "identical": "one reading, one spelling, in all seven",
    "diacritic_variant": "same letters and same dots — the vowelling differs",
    "dotting_variant": "one rasm, pointed differently: تَعۡمَلُونَ against يَعۡمَلُونَ",
    "rasm_variant": "the codices disagree about the letters on the line",
    "word_boundary": "a source prints the word joined to its neighbour",
    "partial": "the word is absent from at least one riwāyah",
}


def _table(rows: list[list], header: list[str]) -> str:
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def _groups(w: Word) -> dict[str, list[str]]:
    """The distinct spellings of one word, each with the riwāyāt that use it."""
    out: dict[str, list[str]] = defaultdict(list)
    for k in ORDER:
        if k in w.forms:
            out[w.forms[k]].append(k)
    return dict(out)


def _forms_cell(w: Word) -> str:
    return "  ·  ".join(f"**{v}** {','.join(ks)}" for v, ks in _groups(w).items())


def _pairwise(words: list[Word], keys: list[str]) -> list[dict]:
    stats = []
    for a, b in combinations(keys, 2):
        both = same_form = same_fold = same_point = same_rasm = 0
        for w in words:
            fa, fb = w.forms.get(a), w.forms.get(b)
            if fa is None or fb is None:
                continue
            both += 1
            same_form += fa == fb
            same_fold += fold_notation(fa) == fold_notation(fb)
            same_point += pointed(fa) == pointed(fb)
            same_rasm += rasm(fa) == rasm(fb)
        stats.append({"a": a, "b": b, "shared": both, "same_form": same_form,
                      "same_reading": same_fold, "same_pointed": same_point,
                      "same_rasm": same_rasm})
    return stats


def write_report(words: list[Word], riwayat: list[Riwaya]) -> None:
    keys = [r.key for r in riwayat]
    status = Counter(w.status for w in words)
    pairs = _pairwise(words, keys)
    cross = cross_release(riwayat)
    systems = fawasil(words)

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

    # --- what is actually being compared ----------------------------------
    add("## What is being compared")
    add("")
    add("A word is never compared as raw text. Four forms are derived from every "
        "spelling, each stripping one more layer of what a scribe added after the "
        "codices were written. Two riwāyāt are said to agree *at a level* when "
        "their forms at that level are identical.")
    add("")
    add(_table([
        ["`uthmani`", "how is it printed?", "`مَٰلِكِ`", "—"],
        ["`folded`", "what does it say, ignoring which codepoints the release chose?",
         "`مَٰلِكِ`", "release notation, attached-alef letters, editorial marks"],
        ["`pointed`", "which letters, dots and all?", "`مالك`",
         "vowels, hamza, madd, ṣilah"],
        ["`rasm`", "what is on the line in the codex?", "`مالك`",
         "the dots"],
    ], ["form", "question it answers", "example", "and what it drops"]))
    add("")
    add("The two skeletons are separate on purpose. `تَعۡمَلُونَ` and `يَعۡمَلُونَ` have "
        "different `pointed` forms but one `rasm` — `ٮعملوں` — because the codices "
        "were written undotted and carry both readings by design. Calling that a "
        "rasm variant would be a category error; calling it vowelling would hide a "
        "real reading. It is named **`dotting_variant`**.")
    add("")
    add("`rasm` drops hamza and every hamza carrier reduces to its seat, because "
        "hamza is post-ʿUthmānic notation: `يَسۡتَهۡزِئُ` and `يَسْتَهْزِۓُ` are one "
        "word. Dagger alif and written alef are also one ā — `هَٰرُوتَ` and "
        "`هَارُوتَ` — since the packages differ only in where the publisher put it.")
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
    add("The āyah totals are not errors and not deducible from the qāriʾ. Many "
        "fawāṣil are مختلف فيها, so every printed muṣḥaf chooses, and the "
        "`counting` column above is a conventional label rather than a claim "
        "about this package. That is exactly why the index is flat, and why the "
        "āyah boundaries are read off each muṣḥaf rather than assumed: see "
        "[the fawāṣil](#fawāṣil-where-the-āyāt-end) below.")
    add("")

    # --- status -----------------------------------------------------------
    add("## How the words compare")
    add("")
    add(_table([[f"`{s}`", f"{status[s]:,}", f"{100 * status[s] / len(words):.2f}%",
                 STATUS_BLURB[s]] for s in STATUS_ORDER if status[s]],
               ["status", "words", "share", "meaning"]))
    add("")
    add("Each word gets the *strongest* label that applies, tested in this order: "
        "rasm, absence, boundary, dotting, vowelling. So a `dotting_variant` is "
        "guaranteed to share one rasm across all seven, and an `identical` word is "
        "identical after notation folding — the raw spelling of every riwāyah is "
        "always kept in `forms`, whatever the label.")
    add("")

    # --- pairwise ---------------------------------------------------------
    add("## Pairwise agreement")
    add("")
    add("Share of the words two riwāyāt both have, where they agree at each level.")
    add("")
    add(_table([[
        f"{p['a']}–{p['b']}", f"{p['shared']:,}",
        f"{100 * p['same_form'] / p['shared']:.1f}%",
        f"{100 * p['same_reading'] / p['shared']:.1f}%",
        f"{100 * p['same_pointed'] / p['shared']:.2f}%",
        f"{100 * p['same_rasm'] / p['shared']:.2f}%",
    ] for p in sorted(pairs, key=lambda p: -p["same_rasm"] / p["shared"])],
        ["pair", "shared words", "same spelling", "same reading", "same letters",
         "same rasm"]))
    add("")
    add("Rasm agreement never drops below 99.5%: the seven riwāyāt are one text. "
        "Spelling agreement is far lower because the packages were typeset in "
        "different years with different conventions — which is what the `folded` "
        "and `pointed` columns strip away.")
    add("")

    # --- the three real disagreements -------------------------------------
    rasm_v = [w for w in words if w.status == "rasm_variant"]
    absent = [w for w in words if w.status == "partial"]
    events = boundary_events(words)

    add("## Where the riwāyāt genuinely disagree")
    add("")
    add(f"Three things can differ once spelling, vowelling and pointing are set "
        f"aside: the letters, the word boundaries, and whether a word is there at "
        f"all. Together they account for "
        f"{len(rasm_v) + len(absent) + sum(len(e['word_ids']) for e in events):,} "
        f"of {len(words):,} words.")
    add("")
    add(_table([
        ["letters differ", f"{len(rasm_v):,}", "`rasm_variant`",
         "the codices are pointed from different exemplars"],
        ["boundaries differ", f"{len(events)} events",
         "`word_boundary`", "one source prints two words as one"],
        ["word absent", f"{len(absent)}", "`partial`",
         "a riwāyah does not have the word at all"],
    ], ["kind", "count", "status", "what it means"]))
    add("")

    # --- rasm variants ----------------------------------------------------
    add("### Letters — rasm disagreements")
    add("")
    add(f"{len(rasm_v):,} words where the riwāyāt disagree about the letters on "
        f"the line, after dots, hamza and vowelling have been set aside. The full "
        f"list is in [`rasm-variants.md`](rasm-variants.md) and "
        f"[`conflicts.csv`](conflicts.csv); the first 25 follow.")
    add("")
    rows = []
    for w in rasm_v[:25]:
        by_rasm: dict[str, list[str]] = defaultdict(list)
        for k in ORDER:
            if k in w.forms:
                by_rasm[rasm(w.forms[k])].append(k)
        rows.append([w.id, f"{w.sura}:{w.aya.get('hafs', '—')}",
                     "  ·  ".join(f"`{r}` {','.join(ks)}" for r, ks in by_rasm.items()),
                     _forms_cell(w)])
    add(_table(rows, ["word id", "sūrah:āyah", "rasm on each side", "as printed"]))
    add("")

    # --- dotting variants -------------------------------------------------
    dotting = [w for w in words if w.status == "dotting_variant"]
    add("### Pointing — one rasm, two readings")
    add("")
    add(f"{len(dotting):,} words share a rasm but are pointed differently. These "
        f"are real differences in reading, not in the codex: an undotted skeleton "
        f"carries them all. A sample:")
    add("")
    rows = []
    for w in dotting[:15]:
        by_pt: dict[str, list[str]] = defaultdict(list)
        for k in ORDER:
            if k in w.forms:
                by_pt[pointed(w.forms[k])].append(k)
        rows.append([w.id, f"{w.sura}:{w.aya.get('hafs', '—')}", f"`{w.rasm}`",
                     "  ·  ".join(f"**{p}** {','.join(ks)}" for p, ks in by_pt.items())])
    add(_table(rows, ["word id", "sūrah:āyah", "shared rasm", "pointed as"]))
    add("")

    # --- boundaries, in detail --------------------------------------------
    add("### Boundaries — where the space falls")
    add("")
    add("A boundary disagreement is never about one word; it is about the space "
        "between two. Each event below shows the whole run, exactly as each "
        "riwāyah prints it. The last column is the one that matters: **agree** "
        "means every riwāyah reads the run identically once it is re-segmented, "
        "so the flag is a *source* that lost a space, not a muṣḥaf that really "
        "prints the words joined.")
    add("")
    for ev in events:
        ids = ", ".join(str(i) for i in ev["word_ids"])
        add(f"**{ev['sura']}:{ev['aya']}** — word ids {ids} · "
            f"joined in `{'`, `'.join(ev['riwayat'])}` · "
            + ("**all riwāyāt agree** (a dropped space in the source)"
               if ev["agree"] else "**the riwāyāt differ** (a real difference)"))
        add("")
        add(_table([[f"`{','.join(ks)}`", t] for t, ks in ev["texts"].items()],
                   ["riwāyāt", "as printed"]))
        add("")
    add("Machine-readable: [`boundaries.csv`](boundaries.csv).")
    add("")

    # --- absent -----------------------------------------------------------
    add("### Absence — words not every riwāyah has")
    add("")
    add("Each is well attested: Ibn Kathīr's `مِن` at 9:100, and Nāfiʿ reading "
        "`فإن الله الغني` at 57:24 where the others read `فإن الله هو الغني`. The "
        "rest are words one riwāyah writes joined to its neighbour and another "
        "writes separately, so the count of words genuinely differs.")
    add("")
    add(_table([[
        w.id, f"{w.sura}:{w.aya.get('hafs') or max(w.aya.values())}", f"`{w.rasm}`",
        ", ".join(w.present), ", ".join(w.missing), _forms_cell(w),
    ] for w in absent],
        ["word id", "sūrah:āyah", "rasm", "present in", "absent from", "as printed"]))
    add("")

    # --- fawasil ----------------------------------------------------------
    add("## Fawāṣil: where the āyāt end")
    add("")
    add("The āyah boundaries are a layer *over* the word index, not a property "
        "of it, and **they belong to the printed muṣḥaf rather than to the "
        "qirāʾah**. Many fawāṣil are مختلف فيها: al-Dānī records Al-Mulk 67:9 "
        "«قد جاءنا نذير» as counted by المدني الأخير والمكي and by Shayba and "
        "not by the rest, and four of the seven packages here count it. An "
        "edition has to choose, and editions of the same riwāyah choose "
        "differently — KFGQPC's own Dūrī printings all state they follow "
        "المدني الأول and still total 6,218 (1429 AH), 6,217 (1436) and 6,214 "
        "(1443).")
    add("")
    add("So the systems below are not counting traditions and are not derived "
        "from any. They are read off the packages, and two riwāyāt are grouped "
        "only where their fawāṣil are identical. Machine-readable: "
        "[`fawasil.json`](fawasil.json).")
    add("")
    add(_table([[
        f"`{name}`", ", ".join(v["mushaf"]), f"{v['ayah_count']:,}",
    ] for name, v in systems.items()],
        ["system", "muṣḥaf", "āyāt"]))
    add("")
    ends = {name: set(v["ends"]) for name, v in systems.items()}
    order = list(systems)
    add(_table([[f"`{a}`"] + [
        "—" if a == b else f"{len(ends[a] ^ ends[b]):,}" for b in order
    ] for a in order], ["system"] + [f"`{b}`" for b in order]))
    add("")
    add("Positions where two systems put a fāṣilah differently. Dūrī and Sūsī "
        "are both conventionally labelled Baṣrī and part company at exactly one "
        "place — 67:9 — which is the whole of the 6,217/6,218 difference between "
        "them, and is a documented خلافي point rather than a mistake by either.")
    add("")

    # --- source integrity -------------------------------------------------
    add("## Source integrity")
    add("")
    add("Six riwāyāt ship two releases. Comparing them is the sharpest available "
        "check on each, since the publisher is the same.")
    add("")
    add("**Where the two releases disagree, the later one is the text.** KFGQPC "
        "revises these documents deliberately: the 2026 Ḥafṣ separates `مَا لِيَ` "
        "where Ḥafṣ's own 2022 CSV joins it as `مَالِيَ`. That is a change of "
        "convention, not a defect, and the newer convention is the one published "
        "here. The earlier release is never merged into the text — it is only "
        "compared against it, below. The rule cannot discriminate for Dūrī, whose "
        "two packages are both from 2022; its three dropped spaces are recorded "
        "as boundary events instead.")
    add("")
    add(_table([[
        k, f"{v['ayat_compared']:,}", f"{v['identical']:,}",
        f"{v['notation_only']:,}", f"{v['marks_only']:,}", v["rasm_differs"],
    ] for k, v in cross.items()],
        ["riwāyah", "āyāt compared", "byte-identical", "notation only",
         "marks/vowels only", "rasm differs"]))
    add("")
    add("`notation only` is dominated by the 2026 files adopting the Arabic "
        "Extended-B alif letters (`U+0870`–`U+0882`), which fold an alef and its "
        "vowel into one codepoint where the 2022 files used an alef plus combining "
        "marks. The `folded` form decomposes them again, so none of it reaches the "
        "word index.")
    add("")
    problems = (check_index(words, riwayat) + check_counting(riwayat)
                + check_release_policy(riwayat))
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
        hard = c["rasm_variant"] + c["word_boundary"] + c["partial"]
        rows.append([s, names()[s]["name_en"], f"{c['total']:,}",
                     c["identical"], c["diacritic_variant"], c["dotting_variant"],
                     c["rasm_variant"], c["word_boundary"] + c["partial"],
                     f"{1000 * hard / c['total']:.1f}"])
    add(_table(rows, ["sūrah", "name", "words", "identical", "diacritic",
                      "dotting", "rasm", "boundary/absent", "per 1000"]))
    add("")

    (OUT / "COMPARISON.md").write_text("\n".join(L), encoding="utf-8")

    # --- full rasm variant listing ---------------------------------------
    V = ["# Rasm disagreements — full listing", "",
         f"All {len(rasm_v):,} words where the seven riwāyāt disagree about the "
         "letters on the line, in order. Dots, hamza, vowelling and the dagger "
         "alif have already been set aside, so every row here is a difference "
         "between the codices rather than between the typesettings.", "",
         "Known residual: 34 rows are the `أَرَءَيۡتَ` / `ࡰرَٰٓيْتَ` family, where Warsh "
         "writes the tashīl'd hamza as a dagger alif and Ḥafṣ writes it as a "
         "hamza. The rasm is the same in both; see `docs/ISSUES.md`.", "",
         "Machine-readable: `conflicts.csv`, `conflicts.json`.", ""]
    rows = []
    for w in rasm_v:
        by_rasm = defaultdict(list)
        for k in ORDER:
            if k in w.forms:
                by_rasm[rasm(w.forms[k])].append(k)
        rows.append([w.id, f"{w.sura}:{w.aya.get('hafs', '—')}", w.index,
                     "  ·  ".join(f"`{r}` {','.join(ks)}" for r, ks in by_rasm.items()),
                     _forms_cell(w)])
    V.append(_table(rows, ["word id", "sūrah:āyah", "word #", "rasm on each side",
                           "as printed"]))
    (OUT / "rasm-variants.md").write_text("\n".join(V), encoding="utf-8")

    # --- matrix as csv ----------------------------------------------------
    with (OUT / "agreement-matrix.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["riwaya_a", "riwaya_b", "shared_words", "same_spelling",
                     "same_reading", "same_pointed", "same_rasm"])
        for p in pairs:
            wr.writerow([p["a"], p["b"], p["shared"], p["same_form"],
                         p["same_reading"], p["same_pointed"], p["same_rasm"]])
