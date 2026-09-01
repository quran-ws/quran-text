# The muṣḥaf format

`out/mushaf/<key>.json` publishes one muṣḥaf on its own. Format **1.1** gives
every token both its shared slot ID and its dense position in this muṣḥaf.
It is an additive successor to 1.0: all 1.0 identifiers and ranges remain.

This document is the specification. **Only `out/mushaf/<key>.json` is
normative.** The nested, sharded, CSV and SQLite forms are generated from it and
are labelled views; a consumer may read them, but a claim about "the format"
refers to the file above.

## The shape

A muṣḥaf is an **ordered list of tokens**. The structures above a token — āyah,
juz, page — are lists of boundaries over shared slot IDs, not levels of nesting.

```
words:  [ w1, w2, w3, w4, w5, w6, w7, w8, … ]
ayat:   [ ──── 1 ────][──── 2 ────]…
pages:  [ ─────────── 1 ───────────]…
```

The reason is the one this project is built on, stated in the README: *the āyah
is an attribute of a word, not a level of nesting.* The muṣḥafs count 6,214 to
6,236 āyāt, so `2:255:3` names a different word in each of them, while `s` names
the same slot in all of them. Nesting words under āyāt would put the unstable
coordinate on the outside and make the seven files incomparable.

Reconstructing a nested view takes three lines, and `out/mushaf/nested/` ships
one already.

## Identity

`s` is the shared `slot_id`, `1 … 77434`. `w` is its 1.0 compatibility alias,
and both equal `word_id` in CSV and SQLite views. **A muṣḥaf that lacks a word
leaves a gap in `s`/`w`**; slots are never renumbered per muṣḥaf.

`p` is the dense global position of an actual token inside this muṣḥaf. It is
exactly `1 … word_count`, so a missing slot does not create a position gap.

IDs are stable across rebuilds of the same sources. They are *not* promised
across a future KFGQPC release — see `docs/LIMITATIONS.md`.

## A word

```json
{ "w": 13, "s": 13, "p": 13, "t": "ٱلدِّينِ", "pg": 1, "ln": 5, "e": "الدين",
  "marks": [ { "k": "waqf", "at": "after", "sign": "ۖ" } ] }
```

| field | always | meaning |
|---|---|---|
| `w` | ✓ | legacy 1.0 alias of `s` |
| `s` | ✓ | shared slot ID — the cross-muṣḥaf join key |
| `p` | ✓ | dense global token position inside this muṣḥaf |
| `t` | ✓ | ʿUthmānī text exactly as this muṣḥaf prints it |
| `pg` | — | printed page, **read** from the release |
| `ln` | — | printed line, **reconstructed** — see below |
| `e` | — | imlāʾī, only where a release supplies it |
| `marks` | — | signs printed against the word |
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

**Waqf marks are not comparable across muṣḥafs.** Warsh and Qālūn print one
general pause sign 9,948 times where Ḥafṣ, Dūrī and Sūsī print seven distinct
ones. This is a difference of publishing convention, not of reading, and nothing
here normalises it.

**The ۞ counts disagree between the releases** — 199 in Ḥafṣ, Shuʿbah and Bazzī
against 433–437 in the others. The symbol is emitted exactly as each release
prints it. It is *not* reconciled to the 240 arbāʿ, because that number is not in
any package and this project does not add data its sources do not carry.

## Layers

```json
"ayat":  [ { "sura": 1, "n": 1, "words": [1, 4], "slots": [1, 4] } ],
"pages": [ { "n": 1, "words": [1, 29], "slots": [1, 29] } ],
"juz":   [ { "n": 1, "words": [1, 2522], "slots": [1, 2522] } ]
```

`slots` is `[first_slot_id, last_slot_id]`, inclusive. `words` is retained and
must contain the exact same pair. The same alias policy applies to sūrah and
resegmentation ranges. At the document level, `spine.slot_id_range` equals the
legacy `spine.word_id_range`.

`ayat[].n` of **`0`** means *printed but not numbered* — Al-Fātiḥah's basmalah in
Warsh, Qālūn, Dūrī and Sūsī, which print the words without counting them as an
āyah. Ḥafṣ, Shuʿbah and Bazzī number them `1`.

## Page is read; line is reconstructed

These are not equally sound, and the format keeps them apart.

**Page** is read from the release. Every `.docx` marks its page turns
explicitly — 603 `<w:br w:type="page"/>` elements, giving 604 pages. Checked
against the v2 CSVs, the page of every āyah agrees: 6,236/6,236 for Ḥafṣ and
Shuʿbah, 6,214/6,214 for Warsh and Qālūn, 6,217/6,217 for Dūrī, 6,210/6,212 for
Sūsī. It is available for **all seven muṣḥafs, Bazzī included**, which has no
CSV at all.

**Line is not encoded anywhere.** It is inferred from the document's line
breaks, paragraph boundaries and headings:

| method | āyāt whose line matches the CSV |
|---|---|
| line breaks alone | 5,079 / 6,236 |
| + paragraph boundaries | 6,131 / 6,236 ← shipped |

Roughly 98.3%. The residual overshoots by one or two on pages the publisher sets
specially — Al-Fātiḥah above all, whose frame the document flow does not
describe. So:

- every file declares the line layer under `layers.derived`, with its score;
- `line_disagreements` lists **every āyah** where the reconstruction differs
  from the release that states it, so a consumer can exclude them rather than
  discover them;
- Bazzī has no v2 release, so its lines **cannot be checked at all**, and its
  file says `"validated": false` rather than implying the same confidence.

Treat `ln` as an aid to layout, not as a citable fact. Treat `pg` as a fact.

## Departures from the source

A global word ID is only stable because the alignment sometimes overrides a
package's own spacing — splitting what one muṣḥaf prints joined. A file claiming
to *be* that muṣḥaf has to say where that happened, so every one is listed:

```json
"resegmentation": [
  { "words": [11634, 11635], "slots": [11634, 11635],
    "sura": 4, "ayah": 91,
    "kind": "joined_in_source",
    "source_text": "مَا رُدُّوٓاْ",
    "emitted": ["مَا", "رُدُّوٓاْ"],
    "riwayat_agree": true }
]
```

`riwayat_agree` of `true` means every muṣḥaf reads the run identically once
re-segmented — a source that lost a space, not a muṣḥaf that really prints the
words joined.

The list is present even when empty, so silence is never ambiguous. In the
current sources: **Dūrī 5, Bazzī 3, Qālūn 1**, and none for Ḥafṣ, Shuʿbah, Warsh
or Sūsī. Affected words also carry `"resegmented": true`.

## Imlāʾī

Published for **Ḥafṣ only**, because the Ḥafṣ v2 release is the only package with
an `aya_text_emlaey` column. It is **never generated**: deriving it by rule for
the other six would be this project asserting a spelling no source states.

The column is per āyah, so it is brought down to the word. 6,175 of 6,236 āyāt
hold exactly as many imlāʾī tokens as ʿUthmānī ones and map across directly. In
the other 61 the imlāʾī side always has *more* — it writes `أو لا` where the
ʿUthmānī line writes `أَوَلَا` — never fewer; those are matched on the skeleton
and joined, so `e` is always one string. A word the chain cannot resolve gets no
`e` at all. `layers.derived.imlaei` reports the totals.

## Provenance

Every file names the KFGQPC release it came from, with a SHA-256 — in the file
itself, not only in the manifest, because a muṣḥaf file will be copied and
vendored on its own and a text whose edition cannot be named is not citable.

`out/mushaf/manifest.json` carries the same hashes for every source package and
every emitted file.

## What each file declares

`layers.present` and `layers.absent` say what a file carries and why it lacks
whatever it lacks, so a consumer can check before querying instead of
discovering a missing key at runtime. Bazzī:

```json
"absent": { "juz": "no v2 package released for this riwāyah",
            "imlaei": "column not present in this riwāyah's release" }
```

Bazzī still has `pg`, because page comes from the `.docx` that every muṣḥaf has.

## The minimal variant

`out/mushaf/<key>.min.json` is the text, slot IDs, and dense positions and
nothing else — no marks, no layout, no imlāʾī. `resegmentation` stays, because it is a disclosure about
the text itself and dropping it would make the small file quietly less honest
than the large one.

## Views

| path | shape |
|---|---|
| `out/mushaf/nested/<key>.json` | sūrah → āyah → words |
| `out/mushaf/suras/<key>/NNN.json` | the canonical shape, one sūrah per file |
| `out/mushaf/<key>.csv` | one row per word |
| `out/quran.sqlite.gz` | all seven plus the spine, queryable after decompression |

Comparing two muṣḥafs in SQL:

```sql
SELECT a.word_id, a.uthmani, b.uthmani
FROM word a JOIN word b USING (word_id)
WHERE a.mushaf = 'hafs' AND b.mushaf = 'warsh' AND a.uthmani <> b.uthmani;
```

The CSV and SQLite word views retain `word_id` and add `slot_id` plus the dense
global `position`. Their `pos` column is different: it is the dense ordinal
inside one āyah, counting only tokens present in that muṣḥaf. SQLite enforces
`UNIQUE (mushaf, position)` in addition to its legacy primary key.

The 1.1 format is checkable against `schema/mushaf-1.1.json`; the retained 1.0
schema documents the previous version.

## Known issues

Listed in full in `docs/ISSUES.md`: the reconstructed lines, the ۞ discrepancy,
the incomparable waqf conventions, Bazzī's missing layers, and the imlāʾī
residual.
