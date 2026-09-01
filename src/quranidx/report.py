"""Generate the human-readable comparison report."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import date
from difflib import SequenceMatcher
from itertools import combinations

from .build import ORDER, OUT, Kalimah, fasilahs
from .chars import HARAKAT, OPEN_TANWEEN
from .normalize import fold_notation, pointed, rasm, unpositioned
from .output import boundary_events
from .sources import Riwayah
from .surahs import names
from .validate import (check_alif_splits, check_counting, check_index,
                       check_release_policy, cross_release)

STATUS_ORDER = ["identical", "diacritic_variant", "dotting_variant",
                "alif_variant", "rasm_variant", "kalimah_boundary", "partial"]

STATUS_BLURB = {
    "identical": "one qira'ah, one spelling, in all seven",
    "diacritic_variant": "same harfs and same dots — the vowelling differs",
    "dotting_variant": "one rasm, pointed differently: تَعۡمَلُونَ against يَعۡمَلُونَ",
    "alif_variant": "one skeleton, one ā: on the line in one hand, above it in the other",
    "rasm_variant": "the mushafs disagree about the harfs on the line",
    "kalimah_boundary": "a source prints the kalimah joined to its neighbour",
    "partial": "the kalimah is absent from at least one riwayah",
}


def _table(rows: list[list], header: list[str]) -> str:
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def _groups(w: Kalimah) -> dict[str, list[str]]:
    """The distinct spellings of one kalimah, each with the riwayahs that use it."""
    out: dict[str, list[str]] = defaultdict(list)
    for k in ORDER:
        if k in w.forms:
            out[w.forms[k]].append(k)
    return dict(out)


def _forms_cell(w: Kalimah) -> str:
    return "  ·  ".join(f"**{v}** {','.join(ks)}" for v, ks in _groups(w).items())


def _by_rasm(w: Kalimah) -> dict[str, list[str]]:
    """The distinct skeletons of one kalimah, each with the riwayahs that write it."""
    out: dict[str, list[str]] = defaultdict(list)
    for k in ORDER:
        if k in w.forms:
            out[rasm(w.forms[k])].append(k)
    return dict(out)


def _rasm_rows(ws: list[Kalimah]) -> list[list]:
    return [[w.id, f"{w.surah}:{w.ayah.get('hafs', '—')}",
             "  ·  ".join(f"`{r}` {','.join(ks)}"
                          for r, ks in _by_rasm(w).items()),
             _forms_cell(w)] for w in ws]


def _difference_is_length(w: Kalimah) -> bool:
    """True when one side simply writes a harf the other does not.

    ``ٮرٮد``/``ٮرٮدد`` and ``ٮسٮهى``/``ٮسٮهٮه`` are of this kind; ``ولا``/``ڡلا``
    and ``كلمٮ``/``كلمه`` are not, because there a harf is exchanged rather
    than added.  Compared with the final shapes folded away — see
    :func:`normalize.unpositioned` — since a suffix moves the harf before it
    off the end of the kalimah and would otherwise read as a substitution too.
    """
    skeletons = sorted({unpositioned(r) for r in _by_rasm(w)})
    return all(tag != "replace"
               for a, b in combinations(skeletons, 2)
               for tag, *_ in SequenceMatcher(None, a, b).get_opcodes())


def _partition(w: Kalimah) -> frozenset[frozenset[str]]:
    """How a kalimah divides the riwayahs: the groups that share a skeleton."""
    return frozenset(frozenset(ks) for ks in _by_rasm(w).values())


def _partitions(ws: list[Kalimah]) -> set:
    return {_partition(w) for w in ws}


def _alone(w: Kalimah, key: str) -> bool:
    """True when ``key`` is the only riwayah on its side of the difference."""
    return any(ks == [key] for ks in _by_rasm(w).values())


def _systematic(ws: list[Kalimah], kalimahs: list[Kalimah]) -> int:
    """How many of ``ws`` split the riwayahs the same way at every occurrence.

    A kalimah whose plene/defective split is the same everywhere it appears is a
    convention each mushaf keeps, not a one-off setting; the count is what the
    report cites for the ā section.  Occurrences are matched on the qira'ah —
    the pointed harfs and the vowels — so that عَلَىٰ and عَلِيࣰّا, which share a
    pointed skeleton, are not counted as one kalimah.
    """
    def qiraah(w: Kalimah) -> str:
        form = w.forms.get("hafs") or next(iter(w.forms.values()))
        marks = "".join(c for c in fold_notation(form)
                        if c in HARAKAT or c in OPEN_TANWEEN)
        return pointed(form) + "|" + marks

    same: dict[str, set] = defaultdict(set)
    for w in kalimahs:
        same[qiraah(w)].add(_partition(w))
    return sum(1 for w in ws if len(same[qiraah(w)]) == 1)


def _pairwise(kalimahs: list[Kalimah], keys: list[str]) -> list[dict]:
    stats = []
    for a, b in combinations(keys, 2):
        both = same_form = same_fold = same_point = same_rasm = 0
        for w in kalimahs:
            fa, fb = w.forms.get(a), w.forms.get(b)
            if fa is None or fb is None:
                continue
            both += 1
            same_form += fa == fb
            same_fold += fold_notation(fa) == fold_notation(fb)
            same_point += pointed(fa) == pointed(fb)
            same_rasm += rasm(fa) == rasm(fb)
        stats.append({"a": a, "b": b, "shared": both, "same_form": same_form,
                      "same_qiraah": same_fold, "same_pointed": same_point,
                      "same_rasm": same_rasm})
    return stats


def write_report(kalimahs: list[Kalimah], riwayahs: list[Riwayah]) -> None:
    keys = [r.key for r in riwayahs]
    status = Counter(w.status for w in kalimahs)
    pairs = _pairwise(kalimahs, keys)
    cross = cross_release(riwayahs)
    systems = fasilahs(kalimahs)

    L: list[str] = []
    add = L.append

    add("# Cross-riwayah comparison")
    add("")
    add(f"Generated {date.today().isoformat()} from the KFGQPC packages in `data/`. "
        f"{len(kalimahs):,} canonical kalimahs across {len({w.surah for w in kalimahs})} surahs "
        f"and {len(keys)} riwayahs.")
    add("")
    add("Every kalimah carries one ID that means the same kalimah in every riwayah that "
        "has it. Where the riwayahs disagree, the disagreement is recorded against "
        "that ID rather than hidden by it.")
    add("")

    # --- what is actually being compared ----------------------------------
    add("## What is being compared")
    add("")
    add("A kalimah is never compared as raw text. Four forms are derived from every "
        "spelling, each stripping one more layer of what a scribe added after the "
        "mushafs were written. Two riwayahs are said to agree *at a level* when "
        "their forms at that level are identical.")
    add("")
    add(_table([
        ["`uthmani`", "how is it printed?", "`ٱلرَّحۡمَٰنِ`", "—"],
        ["`folded`", "what does it say, ignoring which codepoints the release chose?",
         "`الرَّحْمَٰنِ`", "release notation, attached-alef harfs, editorial marks"],
        ["`pointed`", "which harfs, dots and all?", "`الرحمان`",
         "vowels, hamza, madd, ṣilah"],
        ["`rasm`", "what is on the line in the mushaf?", "`الرحماں`",
         "the dots"],
    ], ["form", "question it answers", "example", "and what it drops"]))
    add("")
    add("The two skeletons are separate on purpose. `تَعۡمَلُونَ` and `يَعۡمَلُونَ` have "
        "different `pointed` forms but one `rasm` — `ٮعملوں` — because the mushafs "
        "were written undotted and carry both qira'ahs by design. Calling that a "
        "rasm variant would be a category error; calling it vowelling would hide a "
        "real qira'ah. It is named **`dotting_variant`**.")
    add("")
    add("`rasm` drops hamza and every hamza carrier reduces to its seat, because "
        "hamza is post-Uthmani notation: `يَسۡتَهۡزِئُ` and `يَسْتَهْزِۓُ` are one "
        "kalimah. It also drops the dagger alif, which is by definition an alef the "
        "scribe did *not* write on the line, so `هَٰرُوتَ` and `هَارُوتَ` do **not** "
        "share a rasm: `هروٮ` against `هاروٮ`. That difference is real inside any "
        "one mushaf and is kept, but between these two typesettings it is a house "
        "style rather than a mushaf — see "
        "[the ā on the line or above it](#the-ā-on-the-line-or-above-it).")
    add("")

    # --- inventory --------------------------------------------------------
    add("## The riwayahs")
    add("")
    add(_table([[
        r.key, r.name_en, r.name_ar, r.qari_en, r.counting,
        f"{sum(1 for a in r.ayahs if a.ayah > 0):,}",
        f"{sum(1 for w in kalimahs if r.key in w.forms):,}",
    ] for r in riwayahs],
        ["key", "riwayah", "الرواية", "qari", "counting", "ayahs", "kalimahs"]))
    add("")
    add("The ayah totals are not errors and not deducible from the qari. Many "
        "fasilahs are مختلف فيها, so every printed mushaf chooses, and the "
        "`counting` column above is a conventional label rather than a claim "
        "about this package. That is exactly why the index is flat, and why the "
        "ayah boundaries are read off each mushaf rather than assumed: see "
        "[the fasilahs](#fasilahs-where-the-ayahs-end) below.")
    add("")

    # --- status -----------------------------------------------------------
    add("## How the kalimahs compare")
    add("")
    add(_table([[f"`{s}`", f"{status[s]:,}", f"{100 * status[s] / len(kalimahs):.2f}%",
                 STATUS_BLURB[s]] for s in STATUS_ORDER if status[s]],
               ["status", "kalimahs", "share", "meaning"]))
    add("")
    add("Each kalimah gets the *strongest* label that applies, tested in this order: "
        "rasm, ā, absence, boundary, dotting, vowelling. So a `dotting_variant` "
        "is guaranteed to share one rasm across all seven, an `alif_variant` to "
        "share one skeleton once every ā is spelled out, and an `identical` kalimah "
        "is identical after notation folding — the raw spelling of every riwayah "
        "is always kept in `forms`, whatever the label.")
    add("")

    # --- pairwise ---------------------------------------------------------
    add("## Pairwise agreement")
    add("")
    add("Share of the kalimahs two riwayahs both have, where they agree at each level.")
    add("")
    add(_table([[
        f"{p['a']}–{p['b']}", f"{p['shared']:,}",
        f"{100 * p['same_form'] / p['shared']:.1f}%",
        f"{100 * p['same_qiraah'] / p['shared']:.1f}%",
        f"{100 * p['same_pointed'] / p['shared']:.2f}%",
        f"{100 * p['same_rasm'] / p['shared']:.2f}%",
    ] for p in sorted(pairs, key=lambda p: -p["same_rasm"] / p["shared"])],
        ["pair", "shared kalimahs", "same spelling", "same qira'ah", "same harfs",
         "same rasm"]))
    add("")
    add("Rasm agreement never drops below 99.5%: the seven riwayahs are one text. "
        "Spelling agreement is far lower because the packages were typeset in "
        "different years with different conventions — which is what the `folded` "
        "and `pointed` columns strip away.")
    add("")

    # --- the real disagreements -------------------------------------------
    rasm_v = [w for w in kalimahs if w.status == "rasm_variant"]
    alif_v = [w for w in kalimahs if w.status == "alif_variant"]
    absent = [w for w in kalimahs if w.status == "partial"]
    events = boundary_events(kalimahs)
    longer = [w for w in rasm_v if _difference_is_length(w)]
    swapped = [w for w in rasm_v if not _difference_is_length(w)]

    add("## Where the riwayahs genuinely disagree")
    add("")
    add(f"Three things can differ once spelling, vowelling and pointing are set "
        f"aside: the harfs, the kalimah boundaries, and whether a kalimah is there "
        f"at all. Together they account for "
        f"{len(rasm_v) + len(absent) + sum(len(e['kalimah_ids']) for e in events):,} "
        f"of {len(kalimahs):,} kalimahs. A fourth kind is listed with them and counted "
        f"apart: {len(alif_v):,} kalimahs where the disagreement is only about "
        f"whether an ā sits on the line or above it.")
    add("")
    add(_table([
        ["harfs differ", f"{len(rasm_v):,}", "`rasm_variant`",
         f"a harf one mushaf has on the line and another does not — "
         f"{len(longer):,} of them one harf more, {len(swapped):,} one harf "
         f"for another"],
        ["the ā is placed differently", f"{len(alif_v):,}", "`alif_variant`",
         "one skeleton once every ā is spelled out; the two hands disagree "
         "about which ā to write on the line"],
        ["boundaries differ", f"{len(events)} events",
         "`kalimah_boundary`", "one source prints two kalimahs as one"],
        ["kalimah absent", f"{len(absent)}", "`partial`",
         "a riwayah does not have the kalimah at all"],
    ], ["kind", "count", "status", "what it means"]))
    add("")

    # --- rasm variants ----------------------------------------------------
    add("### Harfs — rasm disagreements")
    add("")
    add(f"{len(rasm_v):,} kalimahs where the riwayahs disagree about the harfs on "
        f"the line, after dots, hamza, vowelling and the ā have all been set "
        f"aside. These are the differences the sources can be trusted on: they "
        f"split the seven riwayahs {len(_partitions(rasm_v))} different ways — by "
        f"miṣr, not by publisher — and they are the khilāf the rasm literature "
        f"names. All {len(rasm_v):,} are listed "
        f"below, grouped by what the difference *is*. Machine-readable: "
        f"[`rasm-variants.md`](rasm-variants.md), "
        f"[`conflicts.csv`](conflicts.csv).")
    add("")

    add("#### One skeleton, one harf more")
    add("")
    add(f"{len(longer):,} of the {len(rasm_v):,}. Both sides write the same "
        f"harfs in the same order and one side writes a harf the other does "
        f"not: `ٮرٮد`/`ٮرٮدد` — يَرۡتَدَّ against يَرۡتَدِدۡ at 5:54 — or "
        f"`ٮسٮهى`/`ٮسٮهٮه`, تَشۡتَهِي against تَشۡتَهِيهِ at 43:71. Nothing is "
        f"replaced; the skeletons nest.")
    add("")
    add(_table(_rasm_rows(longer),
               ["kalimah id", "surah:ayah", "rasm on each side", "as printed"]))
    add("")

    add("#### One harf for another")
    add("")
    add(f"{len(swapped):,} of the {len(rasm_v):,}, where a harf is not added "
        f"but exchanged — `ولا`/`ڡلا` (وَلَا against فَلَا, 91:15), `كلمٮ`/`كلمه` "
        f"(the open against the tied tāʾ, 7:137).")
    add("")
    add(_table(_rasm_rows(swapped),
               ["kalimah id", "surah:ayah", "rasm on each side", "as printed"]))
    add("")

    # --- the alif --------------------------------------------------------
    add("### The ā on the line or above it")
    add("")
    add(f"{len(alif_v):,} kalimahs whose skeletons agree once every ā is spelled "
        f"out, and differ only because one hand wrote that ā on the line and the "
        f"other wrote it above: the Warsh/Qālūn set prints `هَارُوتَ` and "
        f"`مُبَٰرَك` where the Kūfī set prints `هَٰرُوتَ` and `مُبَارَك`.")
    add("")
    # Stated from the data, not asserted: if a future package ever splits these
    # kalimahs more than one way the sentence says so, and `check_alif_splits`
    # flags it in the Checks section above.
    parts = _partitions(alif_v)
    if len(parts) == 1:
        sides = sorted(next(iter(parts)), key=len, reverse=True)
        one_line = ("along exactly one line — "
                    + " against ".join(f"`{','.join(sorted(g))}`" for g in sides)
                    + " — in both directions and without one exception")
    else:
        one_line = f"{len(parts)} different ways"
    add(f"They are not counted as the mushafs disagreeing, and the reason is in "
        f"the data rather than in a judgement about it. **All "
        f"{len(alif_v):,} split the seven riwayahs {one_line}.** The "
        f"{len(rasm_v):,} real harf differences split "
        f"them {len(_partitions(rasm_v))} different ways. Ḥadhf and ithbāt "
        f"al-alif do vary between the mushafs of the amṣār, but they do not put "
        f"Makkah with Madinah {len(alif_v):,} times out of {len(alif_v):,} and "
        f"never once apart; a publisher's house style does. Bazzī goes its own "
        f"way {sum(1 for w in rasm_v if _alone(w, 'bazzi'))} times among the "
        f"{len(rasm_v):,} and not once among these.")
    add("")
    add(f"The distinction is still kept in `rasm`, because inside any one mushaf "
        f"it is that mushaf's own ḥadhf, carried consistently: Ḥafṣ writes قال "
        f"plene 412 times and defective 4, سبحان defective 12 and plene once, "
        f"and {_systematic(alif_v, kalimahs)} of these {len(alif_v):,} kalimahs show "
        f"the identical split at *every* occurrence of the kalimah in the corpus. "
        f"What the sources cannot answer is which of the two hands is the "
        f"mushaf's. A sample:")
    add("")
    add(_table(_rasm_rows(alif_v[:15]),
               ["kalimah id", "surah:ayah", "rasm on each side", "as printed"]))
    add("")

    # --- dotting variants -------------------------------------------------
    dotting = [w for w in kalimahs if w.status == "dotting_variant"]
    add("### Pointing — one rasm, two qira'ahs")
    add("")
    add(f"{len(dotting):,} kalimahs share a rasm but are pointed differently. These "
        f"are real differences in qira'ah, not in the mushaf: an undotted skeleton "
        f"carries them all. A sample:")
    add("")
    rows = []
    for w in dotting[:15]:
        by_pt: dict[str, list[str]] = defaultdict(list)
        for k in ORDER:
            if k in w.forms:
                by_pt[pointed(w.forms[k])].append(k)
        rows.append([w.id, f"{w.surah}:{w.ayah.get('hafs', '—')}", f"`{w.rasm}`",
                     "  ·  ".join(f"**{p}** {','.join(ks)}" for p, ks in by_pt.items())])
    add(_table(rows, ["kalimah id", "surah:ayah", "shared rasm", "pointed as"]))
    add("")

    # --- boundaries, in detail --------------------------------------------
    add("### Boundaries — where the space falls")
    add("")
    add("A boundary disagreement is never about one kalimah; it is about the space "
        "between two. Each event below shows the whole run, exactly as each "
        "riwayah prints it. The last column is the one that matters: **agree** "
        "means every riwayah reads the run identically once it is re-segmented, "
        "so the flag is a *source* that lost a space, not a mushaf that really "
        "prints the kalimahs joined.")
    add("")
    for ev in events:
        ids = ", ".join(str(i) for i in ev["kalimah_ids"])
        add(f"**{ev['surah']}:{ev['ayah']}** — kalimah ids {ids} · "
            f"joined in `{'`, `'.join(ev['riwayahs'])}` · "
            + ("**all riwayahs agree** (a dropped space in the source)"
               if ev["agree"] else "**the riwayahs differ** (a real difference)"))
        add("")
        add(_table([[f"`{','.join(ks)}`", t] for t, ks in ev["texts"].items()],
                   ["riwayahs", "as printed"]))
        add("")
    add("Machine-readable: [`boundaries.csv`](boundaries.csv).")
    add("")

    # --- absent -----------------------------------------------------------
    add("### Absence — kalimahs not every riwayah has")
    add("")
    add("Each is well attested: Ibn Kathīr's `مِن` at 9:100, and Nāfiʿ reading "
        "`فإن الله الغني` at 57:24 where the others read `فإن الله هو الغني`. The "
        "rest are kalimahs one riwayah writes joined to its neighbour and another "
        "writes separately, so the count of kalimahs genuinely differs.")
    add("")
    add(_table([[
        w.id, f"{w.surah}:{w.ayah.get('hafs') or max(w.ayah.values())}", f"`{w.rasm}`",
        ", ".join(w.present), ", ".join(w.missing), _forms_cell(w),
    ] for w in absent],
        ["kalimah id", "surah:ayah", "rasm", "present in", "absent from", "as printed"]))
    add("")

    # --- fasilahs ----------------------------------------------------------
    add("## Fasilahs: where the ayahs end")
    add("")
    add("The ayah boundaries are a layer *over* the kalimah index, not a property "
        "of it, and **they belong to the printed mushaf rather than to the "
        "qira'ah**. Many fasilahs are مختلف فيها: al-Dānī records Al-Mulk 67:9 "
        "«قد جاءنا نذير» as counted by المدني الأخير والمكي and by Shayba and "
        "not by the rest, and four of the seven packages here count it. An "
        "edition has to choose, and editions of the same riwayah choose "
        "differently — KFGQPC's own Dūrī printings all state they follow "
        "المدني الأول and still total 6,218 (1429 AH), 6,217 (1436) and 6,214 "
        "(1443).")
    add("")
    add("So the systems below are not counting traditions and are not derived "
        "from any. They are read off the packages, and two riwayahs are grouped "
        "only where their fasilahs are identical. Machine-readable: "
        "[`fasilahs.json`](fasilahs.json).")
    add("")
    add(_table([[
        f"`{name}`", ", ".join(v["mushaf"]), f"{v['ayah_count']:,}",
    ] for name, v in systems.items()],
        ["system", "mushaf", "ayahs"]))
    add("")
    ends = {name: set(v["ends"]) for name, v in systems.items()}
    order = list(systems)
    add(_table([[f"`{a}`"] + [
        "—" if a == b else f"{len(ends[a] ^ ends[b]):,}" for b in order
    ] for a in order], ["system"] + [f"`{b}`" for b in order]))
    add("")
    add("Positions where two systems put a fasilah differently. Dūrī and Sūsī "
        "are both conventionally labelled Baṣrī and part company at exactly one "
        "place — 67:9 — which is the whole of the 6,217/6,218 difference between "
        "them, and is a documented خلافي point rather than a mistake by either.")
    add("")

    # --- source integrity -------------------------------------------------
    add("## Source integrity")
    add("")
    add("Six riwayahs ship two releases. Comparing them is the sharpest available "
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
        k, f"{v['ayahs_compared']:,}", f"{v['identical']:,}",
        f"{v['notation_only']:,}", f"{v['marks_only']:,}", v["rasm_differs"],
    ] for k, v in cross.items()],
        ["riwayah", "ayahs compared", "byte-identical", "notation only",
         "marks/vowels only", "rasm differs"]))
    add("")
    add("`notation only` is dominated by the 2026 files adopting the Arabic "
        "Extended-B alif harfs (`U+0870`–`U+0882`), which fold an alef and its "
        "vowel into one codepoint where the 2022 files used an alef plus combining "
        "marks. The `folded` form decomposes them again, so none of it reaches the "
        "kalimah index.")
    add("")
    problems = (check_index(kalimahs, riwayahs) + check_counting(riwayahs)
                + check_release_policy(riwayahs) + check_alif_splits(kalimahs))
    add("### Checks")
    add("")
    if problems:
        add(_table([[p["check"], p.get("riwayah", "—"), p["detail"]] for p in problems],
                   ["check", "riwayah", "detail"]))
    else:
        add("All checks pass.")
    add("")

    # --- per surah --------------------------------------------------------
    add("## Per surah")
    add("")
    per: dict[int, Counter] = defaultdict(Counter)
    for w in kalimahs:
        per[w.surah][w.status] += 1
        per[w.surah]["total"] += 1
    rows = []
    for s in range(1, 115):
        c = per[s]
        hard = c["rasm_variant"] + c["kalimah_boundary"] + c["partial"]
        rows.append([s, names()[s]["name_en"], f"{c['total']:,}",
                     c["identical"], c["diacritic_variant"], c["dotting_variant"],
                     c["alif_variant"], c["rasm_variant"],
                     c["kalimah_boundary"] + c["partial"],
                     f"{1000 * hard / c['total']:.1f}"])
    add(_table(rows, ["surah", "name", "kalimahs", "identical", "diacritic",
                      "dotting", "ā", "rasm", "boundary/absent", "per 1000"]))
    add("")

    (OUT / "COMPARISON.md").write_text("\n".join(L), encoding="utf-8")

    # --- full rasm variant listing ---------------------------------------
    V = ["# Rasm disagreements — full listing", "",
         f"Every kalimah where the seven riwayahs disagree about the harfs on the "
         f"line, in order. Dots, hamza and vowelling have all been set aside, "
         f"and so has the dagger alif — a superscript alef is by definition an "
         f"alef the scribe did not write on the line.", "",
         f"The {len(rasm_v):,} `rasm_variant` kalimahs come first: a harf one "
         f"riwayah has and another does not, splitting the seven "
         f"{len(_partitions(rasm_v))} different ways. The {len(alif_v):,} "
         f"`alif_variant` kalimahs follow: one skeleton once every ā is spelled "
         f"out, differing only in where the ā was written, and splitting the "
         f"seven exactly one way. See *The ā on the line or above it* in "
         f"`COMPARISON.md` for why that difference is reported apart.", "",
         "Machine-readable: `conflicts.csv`, `conflicts.json`.", ""]
    for title, ws in (("Harfs", rasm_v), ("The ā", alif_v)):
        V += [f"## {title} — {len(ws):,}", ""]
        V.append(_table([[w.id, f"{w.surah}:{w.ayah.get('hafs', '—')}", w.index,
                          "  ·  ".join(f"`{r}` {','.join(ks)}"
                                       for r, ks in _by_rasm(w).items()),
                          _forms_cell(w)] for w in ws],
                        ["kalimah id", "surah:ayah", "kalimah #", "rasm on each side",
                         "as printed"]))
        V.append("")
    (OUT / "rasm-variants.md").write_text("\n".join(V), encoding="utf-8")

    # --- matrix as csv ----------------------------------------------------
    with (OUT / "agreement-matrix.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["riwayah_a", "riwayah_b", "shared_kalimahs", "same_spelling",
                     "same_qiraah", "same_pointed", "same_rasm"])
        for p in pairs:
            wr.writerow([p["a"], p["b"], p["shared"], p["same_form"],
                         p["same_qiraah"], p["same_pointed"], p["same_rasm"]])
