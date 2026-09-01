# The mushaf format

`out/mushaf/<key>.json` publishes one mushaf on its own, with every kalimah carrying
the global ID that means the same kalimah in all seven.

This document is the specification. **Only `out/mushaf/<key>.json` is
normative.** The nested, sharded, CSV and SQLite forms are generated from it and
are labelled views; a consumer may read them, but a claim about "the format"
refers to the file above.

## The shape

A mushaf is an **ordered list of kalimahs**. The structures above a kalimah — ayah,
juz, safhah — are lists of boundaries over kalimah IDs, not levels of nesting.

```
kalimahs:  [ w1, w2, w3, w4, w5, w6, w7, w8, … ]
ayahs:   [ ──── 1 ────][──── 2 ────]…
safhahs:  [ ─────────── 1 ───────────]…
```

The reason is the one this project is built on, stated in the README: *the ayah
is an attribute of a kalimah, not a level of nesting.* The mushafs count 6,214 to
6,236 ayahs, so `2:255:3` names a different kalimah in each of them, while `w` names
the same kalimah in all of them. Nesting kalimahs under ayahs would put the unstable
coordinate on the outside and make the seven files incomparable.

Reconstructing a nested view takes three lines, and `out/mushaf/nested/` ships
one already.

## Identity

`w` is the global kalimah ID, `1 … 77434`, the same integer as `kalimah_id` in
`out/kalimahs.csv`. **A mushaf that lacks a kalimah leaves a gap in the sequence**;
IDs are never renumbered per mushaf, because that would defeat the point of
having them.

IDs are stable across rebuilds of the same sources. They are *not* promised
across a future KFGQPC release — see `docs/LIMITATIONS.md`.

## A kalimah

```json
{ "w": 13, "t": "ٱلدِّينِ", "pg": 1, "ln": 5, "e": "الدين",
  "marks": [ { "k": "waqf", "at": "after", "sign": "ۖ" } ] }
```

| field | always | meaning |
|---|---|---|
| `w` | ✓ | global kalimah ID — the join key |
| `t` | ✓ | Uthmani text exactly as this mushaf prints it |
| `pg` | — | printed safhah, **read** from the release |
| `ln` | — | printed line, **reconstructed** — see below |
| `e` | — | imlāʾī, only where a release supplies it |
| `marks` | — | signs printed against the kalimah |
| `resegmented` | — | this build changed the source's spacing here |

Optional fields are omitted when empty, so their presence is itself the signal.

### Marks

```json
{ "k": "hizb",   "at": "before", "sign": "۞" }
{ "k": "waqf",   "at": "after",  "sign": "ۖ" }
{ "k": "sajdah", "at": "after",  "sign": "۩" }
```

`mark_signs` at the top of every file maps each sign to its codepoint and
Unicode name, so no consumer has to hard-code a table.

**Waqf marks are not comparable across mushafs.** Warsh and Qālūn print one
general pause sign 9,948 times where Ḥafṣ, Dūrī and Sūsī print seven distinct
ones. This is a difference of publishing convention, not of qira'ah, and nothing
here normalises it.

**The ۞ counts disagree between the releases** — 199 in Ḥafṣ, Shuʿbah and Bazzī
against 433–437 in the others. The symbol is emitted exactly as each release
prints it. It is *not* reconciled to the 240 arbāʿ, because that number is not in
any package and this project does not add data its sources do not carry.

## Layers

```json
"ayahs":  [ { "surah": 1, "n": 1, "kalimahs": [1, 4] } ],
"safhahs": [ { "n": 1, "kalimahs": [1, 29] } ],
"juz":   [ { "n": 1, "kalimahs": [1, 2522] } ]
```

`kalimahs` is `[first_kalimah_id, last_kalimah_id]`, inclusive.

`ayahs[].n` of **`0`** means *printed but not numbered* — Al-Fātiḥah's basmalah in
Warsh, Qālūn, Dūrī and Sūsī, which print the kalimahs without counting them as an
ayah. Ḥafṣ, Shuʿbah and Bazzī number them `1`.

## Safhah is read; line is reconstructed

These are not equally sound, and the format keeps them apart.

**Safhah** is read from the release. Every `.docx` marks its safhah turns
explicitly — 603 `<w:br w:type="page"/>` elements, giving 604 safhahs. Checked
against the v2 CSVs, the safhah of every ayah agrees: 6,236/6,236 for Ḥafṣ and
Shuʿbah, 6,214/6,214 for Warsh and Qālūn, 6,217/6,217 for Dūrī, 6,210/6,212 for
Sūsī. It is available for **all seven mushafs, Bazzī included**, which has no
CSV at all.

**Line is not encoded anywhere.** It is inferred from the document's line
breaks, paragraph boundaries and headings:

| method | ayahs whose line matches the CSV |
|---|---|
| line breaks alone | 5,079 / 6,236 |
| + paragraph boundaries | 6,131 / 6,236 ← shipped |

Roughly 98.3%. The residual overshoots by one or two on safhahs the publisher sets
specially — Al-Fātiḥah above all, whose frame the document flow does not
describe. So:

- every file declares the line layer under `layers.derived`, with its score;
- `line_disagreements` lists **every ayah** where the reconstruction differs
  from the release that states it, so a consumer can exclude them rather than
  discover them;
- Bazzī has no v2 release, so its lines **cannot be checked at all**, and its
  file says `"validated": false` rather than implying the same confidence.

Treat `ln` as an aid to layout, not as a citable fact. Treat `pg` as a fact.

## Departures from the source

A global kalimah ID is only stable because the alignment sometimes overrides a
package's own spacing — splitting what one mushaf prints joined. A file claiming
to *be* that mushaf has to say where that happened, so every one is listed:

```json
"resegmentation": [
  { "kalimahs": [11634, 11635], "surah": 4, "ayah": 91,
    "kind": "joined_in_source",
    "source_text": "مَا رُدُّوٓاْ",
    "emitted": ["مَا", "رُدُّوٓاْ"],
    "riwayahs_agree": true }
]
```

`riwayahs_agree` of `true` means every mushaf reads the run identically once
re-segmented — a source that lost a space, not a mushaf that really prints the
kalimahs joined.

The list is present even when empty, so silence is never ambiguous. In the
current sources: **Dūrī 5, Bazzī 3, Qālūn 1**, and none for Ḥafṣ, Shuʿbah, Warsh
or Sūsī. Affected kalimahs also carry `"resegmented": true`.

## Imlāʾī

Published for **Ḥafṣ only**, because the Ḥafṣ v2 release is the only package with
an `aya_text_emlaey` column. It is **never generated**: deriving it by rule for
the other six would be this project asserting a spelling no source states.

The column is per ayah, so it is brought down to the kalimah. 6,175 of 6,236 ayahs
hold exactly as many imlāʾī tokens as Uthmani ones and map across directly. In
the other 61 the imlāʾī side always has *more* — it writes `أو لا` where the
Uthmani line writes `أَوَلَا` — never fewer; those are matched on the skeleton
and joined, so `e` is always one string. A kalimah the chain cannot resolve gets no
`e` at all. `layers.derived.imlaei` reports the totals.

## Provenance

Every file names the KFGQPC release it came from, with a SHA-256 — in the file
itself, not only in the manifest, because a mushaf file will be copied and
vendored on its own and a text whose edition cannot be named is not citable.

`out/mushaf/manifest.json` carries the same hashes for every source package and
every emitted file.

## What each file declares

`layers.present` and `layers.absent` say what a file carries and why it lacks
whatever it lacks, so a consumer can check before querying instead of
discovering a missing key at runtime. Bazzī:

```json
"absent": { "juz": "no v2 package released for this riwayah",
            "imlaei": "column not present in this riwayah's release" }
```

Bazzī still has `pg`, because safhah comes from the `.docx` that every mushaf has.

## The minimal variant

`out/mushaf/<key>.min.json` is the text and the IDs and nothing else — no marks,
no layout, no imlāʾī. `resegmentation` stays, because it is a disclosure about
the text itself and dropping it would make the small file quietly less honest
than the large one.

## Views

| path | shape |
|---|---|
| `out/mushaf/nested/<key>.json` | surah → ayah → kalimahs |
| `out/mushaf/surahs/<key>/NNN.json` | the canonical shape, one surah per file |
| `out/mushaf/<key>.csv` | one row per kalimah |
| `out/quran.sqlite` | all seven plus the spine, queryable |

Comparing two mushafs in SQL:

```sql
SELECT a.kalimah_id, a.uthmani, b.uthmani
FROM kalimah a JOIN kalimah b USING (kalimah_id)
WHERE a.mushaf = 'hafs' AND b.mushaf = 'warsh' AND a.uthmani <> b.uthmani;
```

## Known issues

Listed in full in `docs/ISSUES.md`: the reconstructed lines, the ۞ discrepancy,
the incomparable waqf conventions, Bazzī's missing layers, and the imlāʾī
residual.
