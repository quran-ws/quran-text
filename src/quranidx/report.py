"""Generate the human-readable comparison report."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import date
from difflib import SequenceMatcher
from itertools import combinations

from .build import ORDER, OUT, Word, ayah_ends
from .chars import HARAKAT, OPEN_TANWEEN
from .normalize import fold_notation, pointed, rasm, unpositioned
from .output import boundary_events
from .sources import Riwaya
from .suras import names
from .validate import (check_alif_splits, check_ayah_numbers, check_index,
                       check_release_policy, cross_release)
from .align import WRITTEN_JOINED

STATUS_ORDER = ["identical", "diacritic_variant", "dotting_variant",
                "alif_variant", "rasm_variant", "word_boundary", "partial"]

STATUS_BLURB = {
    "identical": "one reading, one spelling, in all seven",
    "diacritic_variant": "same letters and same dots — the vowelling differs",
    "dotting_variant": "one rasm, pointed differently: تَعۡمَلُونَ against يَعۡمَلُونَ",
    "alif_variant": "one skeleton, one ā: on the line in one hand, above it in the other",
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


def _by_rasm(w: Word) -> dict[str, list[str]]:
    """The distinct skeletons of one word, each with the riwāyāt that write it."""
    out: dict[str, list[str]] = defaultdict(list)
    for k in ORDER:
        if k in w.forms:
            out[rasm(w.forms[k])].append(k)
    return dict(out)


def _rasm_rows(ws: list[Word]) -> list[list]:
    return [[w.id, f"{w.sura}:{w.aya.get('hafs', '—')}",
             "  ·  ".join(f"`{r}` {','.join(ks)}"
                          for r, ks in _by_rasm(w).items()),
             _forms_cell(w)] for w in ws]


def _difference_is_length(w: Word) -> bool:
    """True when one side simply writes a letter the other does not.

    ``ٮرٮد``/``ٮرٮدد`` and ``ٮسٮهى``/``ٮسٮهٮه`` are of this kind; ``ولا``/``ڡلا``
    and ``كلمٮ``/``كلمه`` are not, because there a letter is exchanged rather
    than added.  Compared with the final shapes folded away — see
    :func:`normalize.unpositioned` — since a suffix moves the letter before it
    off the end of the word and would otherwise read as a substitution too.
    """
    skeletons = sorted({unpositioned(r) for r in _by_rasm(w)})
    return all(tag != "replace"
               for a, b in combinations(skeletons, 2)
               for tag, *_ in SequenceMatcher(None, a, b).get_opcodes())


def _partition(w: Word) -> frozenset[frozenset[str]]:
    """How a word divides the riwāyāt: the groups that share a skeleton."""
    return frozenset(frozenset(ks) for ks in _by_rasm(w).values())


def _partitions(ws: list[Word]) -> set:
    return {_partition(w) for w in ws}


def _alone(w: Word, key: str) -> bool:
    """True when ``key`` is the only riwāyah on its side of the difference."""
    return any(ks == [key] for ks in _by_rasm(w).values())


def _systematic(ws: list[Word], words: list[Word]) -> int:
    """How many of ``ws`` split the riwāyāt the same way at every occurrence.

    A word whose plene/defective split is the same everywhere it appears is a
    convention each muṣḥaf keeps, not a one-off setting; the count is what the
    report cites for the ā section.  Occurrences are matched on the reading —
    the pointed letters and the vowels — so that عَلَىٰ and عَلِيࣰّا, which share a
    pointed skeleton, are not counted as one word.
    """
    def reading(w: Word) -> str:
        form = w.forms.get("hafs") or next(iter(w.forms.values()))
        marks = "".join(c for c in fold_notation(form)
                        if c in HARAKAT or c in OPEN_TANWEEN)
        return pointed(form) + "|" + marks

    same: dict[str, set] = defaultdict(set)
    for w in words:
        same[reading(w)].add(_partition(w))
    return sum(1 for w in ws if len(same[reading(w)]) == 1)


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


def write_report(words: list[Word], riwayat: list[Riwaya],
                 docs: dict[str, dict] | None = None) -> None:
    """``out/COMPARISON.md`` and companions.  ``docs`` are the muṣḥaf files
    from :func:`quranidx.mushaf.write_mushafs`, for their ``counting`` blocks."""
    keys = [r.key for r in riwayat]
    status = Counter(w.status for w in words)
    pairs = _pairwise(words, keys)
    cross = cross_release(riwayat)
    counting = {k: d["counting"] for k, d in (docs or {}).items()}

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
        ["`uthmani`", "how is it printed?", "`ٱلرَّحۡمَٰنِ`", "—"],
        ["`folded`", "what does it say, ignoring which codepoints the release chose?",
         "`الرَّحْمَٰنِ`", "release notation, attached-alef letters, editorial marks"],
        ["`pointed`", "which letters, dots and all?", "`الرحمان`",
         "vowels, hamza, madd, ṣilah"],
        ["`rasm`", "what is on the line in the codex?", "`الرحماں`",
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
        "word. It also drops the dagger alif, which is by definition an alef the "
        "scribe did *not* write on the line, so `هَٰرُوتَ` and `هَارُوتَ` do **not** "
        "share a rasm: `هروٮ` against `هاروٮ`. That difference is real inside any "
        "one muṣḥaf and is kept, but between these two typesettings it is a house "
        "style rather than a codex — see "
        "[the ā on the line or above it](#the-ā-on-the-line-or-above-it).")
    add("")

    # --- inventory --------------------------------------------------------
    add("## The riwāyāt")
    add("")
    add(_table([[
        r.key, r.name_en, r.name_ar, r.qari_en,
        f"`{counting[r.key]['system']}`" if r.key in counting else "—",
        f"{sum(1 for a in r.ayat if a.aya > 0):,}",
        f"{sum(1 for w in words if r.key in w.forms and r.key not in w.continuation):,}",
    ] for r in riwayat],
        ["key", "riwāyah", "الرواية", "qāriʾ", "counting system", "āyāt", "words"]))
    add("")
    add("The āyah totals are not errors and not deducible from the qāriʾ. Many "
        "fawāṣil are مختلف فيها, so every printed edition chooses, and the "
        "counting system above is **derived** from what this package prints, "
        "not assumed from the riwāyah. That is exactly why the index is flat, "
        "and why the āyah boundaries are read off each muṣḥaf: see "
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
        "rasm, ā, absence, boundary, dotting, vowelling. So a `dotting_variant` "
        "is guaranteed to share one rasm across all seven, an `alif_variant` to "
        "share one skeleton once every ā is spelled out, and an `identical` word "
        "is identical after notation folding — the raw spelling of every riwāyah "
        "is always kept in `forms`, whatever the label.")
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

    # --- the real disagreements -------------------------------------------
    rasm_v = [w for w in words if w.status == "rasm_variant"]
    alif_v = [w for w in words if w.status == "alif_variant"]
    absent = [w for w in words if w.status == "partial"]
    events = boundary_events(words)
    longer = [w for w in rasm_v if _difference_is_length(w)]
    swapped = [w for w in rasm_v if not _difference_is_length(w)]

    add("## Where the riwāyāt genuinely disagree")
    add("")
    add(f"Three things can differ once spelling, vowelling and pointing are set "
        f"aside: the letters, the word boundaries, and whether a word is there "
        f"at all. Together they account for "
        f"{len(rasm_v) + len(absent) + sum(len(e['word_ids']) for e in events):,} "
        f"of {len(words):,} words. A fourth kind is listed with them and counted "
        f"apart: {len(alif_v):,} words where the disagreement is only about "
        f"whether an ā sits on the line or above it.")
    add("")
    add(_table([
        ["letters differ", f"{len(rasm_v):,}", "`rasm_variant`",
         f"a letter one codex has on the line and another does not — "
         f"{len(longer):,} of them one letter more, {len(swapped):,} one letter "
         f"for another"],
        ["the ā is placed differently", f"{len(alif_v):,}", "`alif_variant`",
         "one skeleton once every ā is spelled out; the two hands disagree "
         "about which ā to write on the line"],
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
        f"the line, after dots, hamza, vowelling and the ā have all been set "
        f"aside. These are the differences the sources can be trusted on: they "
        f"split the seven riwāyāt {len(_partitions(rasm_v))} different ways — by "
        f"miṣr, not by publisher — and they are the khilāf the rasm literature "
        f"names. All {len(rasm_v):,} are listed "
        f"below, grouped by what the difference *is*. Machine-readable: "
        f"[`rasm-variants.md`](rasm-variants.md), "
        f"[`conflicts.csv`](conflicts.csv).")
    add("")

    add("#### One skeleton, one letter more")
    add("")
    add(f"{len(longer):,} of the {len(rasm_v):,}. Both sides write the same "
        f"letters in the same order and one side writes a letter the other does "
        f"not: `ٮرٮد`/`ٮرٮدد` — يَرۡتَدَّ against يَرۡتَدِدۡ at 5:54 — or "
        f"`ٮسٮهى`/`ٮسٮهٮه`, تَشۡتَهِي against تَشۡتَهِيهِ at 43:71. Nothing is "
        f"replaced; the skeletons nest.")
    add("")
    add(_table(_rasm_rows(longer),
               ["word id", "sūrah:āyah", "rasm on each side", "as printed"]))
    add("")

    add("#### One letter for another")
    add("")
    add(f"{len(swapped):,} of the {len(rasm_v):,}, where a letter is not added "
        f"but exchanged — `ولا`/`ڡلا` (وَلَا against فَلَا, 91:15), `كلمٮ`/`كلمه` "
        f"(the open against the tied tāʾ, 7:137).")
    add("")
    add(_table(_rasm_rows(swapped),
               ["word id", "sūrah:āyah", "rasm on each side", "as printed"]))
    add("")

    # --- the alif --------------------------------------------------------
    add("### The ā on the line or above it")
    add("")
    add(f"{len(alif_v):,} words whose skeletons agree once every ā is spelled "
        f"out, and differ only because one hand wrote that ā on the line and the "
        f"other wrote it above: the Warsh/Qālūn set prints `هَارُوتَ` and "
        f"`مُبَٰرَك` where the Kūfī set prints `هَٰرُوتَ` and `مُبَارَك`.")
    add("")
    # Stated from the data, not asserted: if a future package ever splits these
    # words more than one way the sentence says so, and `check_alif_splits`
    # flags it in the Checks section above.
    parts = _partitions(alif_v)
    if len(parts) == 1:
        sides = sorted(next(iter(parts)), key=len, reverse=True)
        one_line = ("along exactly one line — "
                    + " against ".join(f"`{','.join(sorted(g))}`" for g in sides)
                    + " — in both directions and without one exception")
    else:
        one_line = f"{len(parts)} different ways"
    add(f"They are not counted as the codices disagreeing, and the reason is in "
        f"the data rather than in a judgement about it. **All "
        f"{len(alif_v):,} split the seven riwāyāt {one_line}.** The "
        f"{len(rasm_v):,} real letter differences split "
        f"them {len(_partitions(rasm_v))} different ways. Ḥadhf and ithbāt "
        f"al-alif do vary between the codices of the amṣār, but they do not put "
        f"Makkah with Madinah {len(alif_v):,} times out of {len(alif_v):,} and "
        f"never once apart; a publisher's house style does. Bazzī goes its own "
        f"way {sum(1 for w in rasm_v if _alone(w, 'bazzi'))} times among the "
        f"{len(rasm_v):,} and not once among these.")
    add("")
    add(f"The distinction is still kept in `rasm`, because inside any one muṣḥaf "
        f"it is that muṣḥaf's own ḥadhf, carried consistently: Ḥafṣ writes قال "
        f"plene 412 times and defective 4, سبحان defective 12 and plene once, "
        f"and {_systematic(alif_v, words)} of these {len(alif_v):,} words show "
        f"the identical split at *every* occurrence of the word in the corpus. "
        f"What the sources cannot answer is which of the two hands is the "
        f"codex's. A sample:")
    add("")
    add(_table(_rasm_rows(alif_v[:15]),
               ["word id", "sūrah:āyah", "rasm on each side", "as printed"]))
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
    add("Each is well attested: Ibn Kathīr's `مِن` at 9:101; Nāfiʿ reading "
        "`فإن الله الغني` at 57:24 where the others read `فإن الله هو الغني`; "
        "and `أَوۡ` at 40:26, where Ḥafṣ and Shuʿbah read *aw* and the other "
        "five read *wa* — a different word, so the number of `أَوۡ` is absent "
        "from them and their `وَأَنْ` takes the number of `أَن`.")
    add("")
    add(_table([[
        w.id, f"{w.sura}:{w.aya.get('hafs') or max(w.aya.values())}", f"`{w.rasm}`",
        ", ".join(w.present), ", ".join(w.missing), _forms_cell(w),
    ] for w in absent],
        ["number", "sūrah:āyah", "rasm", "present in", "absent from", "as printed"]))
    add("")

    # --- written joined ---------------------------------------------------
    joined = [w for w in words if any(v == WRITTEN_JOINED for v in w.boundary.values())]
    add("### Written joined — two words some muṣḥafs print as one")
    add("")
    add("Nothing is added and nothing is dropped: the nūn assimilates into the "
        "letter after it and is not written, so the same two words are printed "
        "as one. The numbering counts the finest division, so both words keep a "
        "number and the joined word *covers* both — recorded in each muṣḥaf's "
        "`numbering.written_joined`, never as a missing word. Declared in "
        "`data/written-joined.json`.")
    add("")
    add(_table([[
        w.id, f"{w.sura}:{w.aya.get('hafs') or max(w.aya.values())}", f"`{w.rasm}`",
        ", ".join(k for k in ORDER if w.boundary.get(k) == WRITTEN_JOINED),
        _forms_cell(w),
    ] for w in joined],
        ["number", "sūrah:āyah", "rasm", "written joined by", "as printed"]))
    add("")

    # --- fawasil ----------------------------------------------------------
    add("## Fawāṣil: where the āyāt end")
    add("")
    add("The āyah boundaries are a layer *over* the word index, not a property "
        "of it, and **the count belongs to the printed edition, not to the "
        "qirāʾah**. An edition follows one of the six classical counting "
        "systems, and at the points where the system's own authorities disagree "
        "it follows one of them: al-Dānī records Al-Mulk 67:9 «قد جاءنا نذير» as "
        "counted by Shayba and not by Abū Jaʿfar inside the First Madinan, and "
        "KFGQPC's own Dūrī printings all state they follow المدني الأول and still "
        "total 6,218 (1429 AH), 6,217 (1436) and 6,214 (1443).")
    add("")
    add("Each edition's system is **derived** by comparing its own āyah ends to "
        "every system's boundaries (from "
        "[qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map), "
        "vendored under `data/counting/`), then the points of khilāf inside the "
        "system are named with the authority the edition follows. Whatever is "
        "left is `unexplained` and is an open finding. Machine-readable: "
        "[`fawasil.json`](fawasil.json).")
    add("")
    add(_table([[
        k, f"`{c['system']}`", c["system_name_ar"], f"{c['ayah_count']:,}",
        "yes" if c["basmalah_counted"] else "no",
        "; ".join(f"{e['kufi']} {'counted' if e['counted'] else 'not counted'} "
                  f"({', '.join(e['follows'])})" for e in c["khilaf"]) or "—",
        "; ".join(f"{e['kufi']} {'counted' if e['counted'] else 'not counted'}"
                  for e in c["unexplained"]) or "—",
    ] for k, c in counting.items()],
        ["muṣḥaf", "system", "", "āyāt", "basmalah counted",
         "khilāf inside the system", "unexplained"]))
    add("")
    ends = {k: set(ayah_ends(words, k)) for k in keys}
    add(_table([[f"`{a}`"] + [
        "—" if a == b else f"{len(ends[a] ^ ends[b]):,}" for b in keys
    ] for a in keys], ["edition"] + [f"`{b}`" for b in keys]))
    add("")
    add("Āyah ends where two editions differ. Dūrī and Sūsī, both First Madinan, "
        "part company at exactly one place — 67:9 — which is the whole of the "
        "6,217/6,218 difference between them: Dūrī follows Abū Jaʿfar there and "
        "Sūsī follows Shayba. Bazzī counts 78:40, which no source yet gives to "
        "the Makkī count; it is reported as an open finding, not corrected.")
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
    problems = (check_index(words, riwayat) + check_ayah_numbers(riwayat)
                + check_release_policy(riwayat) + check_alif_splits(words))
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
                     c["alif_variant"], c["rasm_variant"],
                     c["word_boundary"] + c["partial"],
                     f"{1000 * hard / c['total']:.1f}"])
    add(_table(rows, ["sūrah", "name", "words", "identical", "diacritic",
                      "dotting", "ā", "rasm", "boundary/absent", "per 1000"]))
    add("")

    (OUT / "COMPARISON.md").write_text("\n".join(L), encoding="utf-8")

    # --- full rasm variant listing ---------------------------------------
    V = ["# Rasm disagreements — full listing", "",
         f"Every word where the seven riwāyāt disagree about the letters on the "
         f"line, in order. Dots, hamza and vowelling have all been set aside, "
         f"and so has the dagger alif — a superscript alef is by definition an "
         f"alef the scribe did not write on the line.", "",
         f"The {len(rasm_v):,} `rasm_variant` words come first: a letter one "
         f"riwāyah has and another does not, splitting the seven "
         f"{len(_partitions(rasm_v))} different ways. The {len(alif_v):,} "
         f"`alif_variant` words follow: one skeleton once every ā is spelled "
         f"out, differing only in where the ā was written, and splitting the "
         f"seven exactly one way. See *The ā on the line or above it* in "
         f"`COMPARISON.md` for why that difference is reported apart.", "",
         "Machine-readable: `conflicts.csv`, `conflicts.json`.", ""]
    for title, ws in (("Letters", rasm_v), ("The ā", alif_v)):
        V += [f"## {title} — {len(ws):,}", ""]
        V.append(_table([[w.id, f"{w.sura}:{w.aya.get('hafs', '—')}", w.index,
                          "  ·  ".join(f"`{r}` {','.join(ks)}"
                                       for r, ks in _by_rasm(w).items()),
                          _forms_cell(w)] for w in ws],
                        ["word id", "sūrah:āyah", "word #", "rasm on each side",
                         "as printed"]))
        V.append("")
    (OUT / "rasm-variants.md").write_text("\n".join(V), encoding="utf-8")

    # --- matrix as csv ----------------------------------------------------
    with (OUT / "agreement-matrix.csv").open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["riwaya_a", "riwaya_b", "shared_words", "same_spelling",
                     "same_reading", "same_pointed", "same_rasm"])
        for p in pairs:
            wr.writerow([p["a"], p["b"], p["shared"], p["same_form"],
                         p["same_reading"], p["same_pointed"], p["same_rasm"]])
