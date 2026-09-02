# The muṣḥaf format

`out/mushaf/<key>.json` publishes one muṣḥaf on its own, with every word carrying
the global ID that means the same word in all seven.

This document is the specification. **Only `out/mushaf/<key>.json` is
normative.** The nested, sharded, CSV and SQLite forms are generated from it and
are labelled views; a consumer may read them, but a claim about "the format"
refers to the file above.

## The shape

A muṣḥaf is an **ordered list of words**. The structures above a word — āyah,
juz, page — are lists of boundaries over word IDs, not levels of nesting.

```
words:  [ w1, w2, w3, w4, w5, w6, w7, w8, … ]
ayat:   [ ──── 1 ────][──── 2 ────]…
pages:  [ ─────────── 1 ───────────]…
```

The reason is the one this project is built on, stated in the README: *the āyah
is an attribute of a word, not a level of nesting.* The muṣḥafs count 6,214 to
6,236 āyāt, so `2:255:3` names a different word in each of them, while `w` names
the same word in all of them. Nesting words under āyāt would put the unstable
coordinate on the outside and make the seven files incomparable.

Reconstructing a nested view takes three lines, and `out/mushaf/nested/` ships
one already.

## Identity

`w` is the global word ID, `1 … 77432`, the same integer as `word_id` in
`out/words.csv`. IDs are never renumbered per muṣḥaf, because that would defeat
the point of having them — so **a muṣḥaf that lacks a word leaves a gap in the
sequence**, and one that has an extra word carries it on a sub-index rather than
shifting everything after it.

IDs are stable across rebuilds of the same sources. They are *not* promised
across a future KFGQPC release — see `docs/LIMITATIONS.md`.

### The spine is Ḥafṣ, and everything else is said relative to it

**`w` counts Ḥafṣ's words.** ID *n* is the *n*-th word of Ḥafṣ, so
`out/mushaf/hafs.json` runs `1 … 77432` with no repeat, no gap and no `x` field
at all. Shuʿbah comes out the same way.

Every other muṣḥaf is then described by how it differs from that sequence, and
there are only two ways it can:

**It lacks a word Ḥafṣ has.** The ID is absent from that muṣḥaf — Warsh has no
`هُوَ` at 57:23 — so its sequence skips. A gap means that and nothing else.

**It has a word Ḥafṣ does not.** Then there is no ID for it, so it hangs off the
**previous** word with a sub-index `x`:

```json
{ "w": 25684, "t": "تَجۡرِي" },
{ "w": 25684, "x": 1, "t": "مِن" },     ← Bazzī alone, 9:101
{ "w": 25685, "t": "تَحۡتِهَا" }
```

`x` is omitted when zero, so its presence is the signal. Five words in the whole
corpus are involved — two added, three lacking:

| | word | | |
|---|---|---|---|
| 9:101 | `مِن` | added by | Bazzī |
| 72:16 | `لَّوِ` | added by | Warsh, Qālūn, Dūrī, Sūsī |
| 40:26 | `أَوْ` | lacked by | Warsh, Qālūn, Dūrī, Sūsī, Bazzī |
| 57:23 | `هُوَ` | lacked by | Warsh, Qālūn |
| 73:20 | `أَن` | lacked by | Dūrī, Sūsī |

*Added* and *lacked* are said **with respect to Ḥafṣ**, which is a declared
frame of reference and not a claim that Ḥafṣ reads correctly. At 72:16 four
muṣḥafs write `لَّوِ` and three do not; it is still an "addition" here, because
Ḥafṣ is where the counting starts. Without naming a frame, `هُوَ` has no answer
to *was it added by five or dropped by two?*

So: **`w` alone addresses a word in Ḥafṣ and Shuʿbah. Everywhere else read
`(w, x)`.** One muṣḥaf in five carries a single repeated `w`, and a lookup on
`w` alone would silently return only the first of the two.

### How an ID is written

```
25684      a word Ḥafṣ has
25684.1    a word hanging off it
```

That is the one canonical way to write the pair, and it is what every report,
table and message in this project prints. It is **notation, not storage**: the
data keeps two integers, because `ayat`, `pages` and `juz` compare their ranges
numerically and a string could not be — and because `25684.1` as a JSON *number*
is a float, which round-trips as `25684.099999999999` and is no kind of
identifier.

### Two things that follow

**A muṣḥaf's own word number is the list index, not `w`.** `words` is dense and
in order, so the *n*-th word is the *n*-th entry. For Ḥafṣ the two coincide; for
the rest they do not. The number is not stored — a file that lists its words in
order already says it — and the tabular views carry `pos`, the āyah-relative
word number, which is what word audio timings and highlighting address.

**Every range — `ayat`, `suras`, `pages`, `juz` — is in ID coordinates**, so a
range may name IDs this muṣḥaf has no word for. Select by value, never by
slicing:

```js
words.filter(x => x.w >= first && x.w <= last)   // right
words.slice(first - 1, last)                     // wrong wherever there is a gap
```

## A word

```json
{ "w": 13, "t": "ٱلدِّينِ", "pg": 1, "ln": 5, "e": "الدين",
  "marks": [ { "k": "waqf", "at": "after", "sign": "ۖ" } ] }
```

| field | always | meaning |
|---|---|---|
| `w` | ✓ | global word ID — the join key |
| `x` | — | sub-index: this muṣḥaf has a word Ḥafṣ does not. Read `(w, x)` together |
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
"ayat":  [ { "sura": 1, "n": 1, "words": [1, 4] } ],
"pages": [ { "n": 1, "words": [1, 29] } ],
"juz":   [ { "n": 1, "words": [1, 2522] } ]
```

`words` is `[first_word_id, last_word_id]`, inclusive.

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
  { "words": [11634, 11635], "sura": 4, "ayah": 91,
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

`out/mushaf/<key>.min.json` is the text and the IDs and nothing else — no marks,
no layout, no imlāʾī. `resegmentation` stays, because it is a disclosure about
the text itself and dropping it would make the small file quietly less honest
than the large one.

## Views

| path | shape |
|---|---|
| `out/mushaf/nested/<key>.json` | sūrah → āyah → words |
| `out/mushaf/suras/<key>/NNN.json` | the canonical shape, one sūrah per file |
| `out/mushaf/<key>.csv` | one row per word |
| `out/quran.sqlite` | all seven plus the spine, queryable |

Comparing two muṣḥafs in SQL:

```sql
SELECT a.word_id, a.sub, a.uthmani, b.uthmani
FROM word a LEFT JOIN word b
  ON b.word_id = a.word_id AND b.sub = a.sub AND b.mushaf = 'warsh'
WHERE a.mushaf = 'hafs'
  AND (b.uthmani IS NULL OR b.uthmani <> a.uthmani);
```

`LEFT JOIN` rather than `JOIN`, and on `(word_id, sub)` rather than `word_id`
alone. Both matter: the honest answer is sometimes *no row*. Projecting a
word-level dataset from Ḥafṣ onto Warsh — a translation, morphology, an audio
segment — loses exactly two words, and a consumer needs to see that rather than
slide silently past it:

| | | |
|---|---|---|
| `60520.1` | `أَوۡ` | Ḥafṣ adds it; Warsh has no such word |
| `69718` | `هُوَ` | the spine has it; Warsh does not recite it |

Playing one word across all seven is the same table read the other way:

```sql
SELECT mushaf, sura, ayah, pos FROM word
WHERE word_id = ? AND sub = ? ORDER BY mushaf;
```

`pos` is the āyah-relative word number, which is what word-level audio timings
(`{word_position, start_ms, end_ms}`) address.

## Known issues

Listed in full in `docs/ISSUES.md`: the reconstructed lines, the ۞ discrepancy,
the incomparable waqf conventions, Bazzī's missing layers, and the imlāʾī
residual.
