# The muṣḥaf format

`out/mushaf/<key>.json` publishes one muṣḥaf on its own. `out/word-index.json`
publishes the shared numbering that means the same word in all seven.

This document is the specification. **Only `out/mushaf/<key>.json` and
`out/word-index.json` (with `out/word-index.csv`) are normative.** The nested,
CSV and SQLite forms are generated from them and are labelled views; a consumer
may read them, but a claim about "the format" refers to the files above.
`docs/SCHEMA.md` lists every file under `out/` and what it answers.

## The shape

**A muṣḥaf is an ordered array of word strings. Everything else is a layer over
that array, addressed by position.**

```json
{
  "format": "quran-mushaf", "format_version": "1.0", "generated": "2026-09-05",

  "mushaf":   { "key": "warsh", "name_en": "Warsh", "name_ar": "ورش",
                "qari_en": "Nāfiʿ al-Madanī", "qari_ar": "نافع المدني", "word_count": 77431 },
  "counting": { "system": "madani-last", "declared_by": null, "ayah_count": 6214,
                "basmalah_counted": false, "khilaf": [], "unexplained": [] },
  "provenance": { "text": { "package": "UthmanicWarsh-v-3.0.zip", "…": "…" }, "layout": { "…": "…" } },
  "layers":   { "present": ["suras", "ayat", "pages", "lines", "marks", "juz"], "absent": { "…": "…" } },

  "words":  ["بِسْمِ", "ࡴ۬للَّهِ", "ࡴ۬لرَّحْمَٰنِ", "ࡴ۬لرَّحِيمِ", "ࡴ۬لْحَمْدُ", "…"],
  "imlaei": null,

  "numbering": { "total": 77434, "missing": [25685, 60522, 69720], "written_joined": [] },

  "sura_starts": [0, 29, 6146, "…"],
  "ayah_starts": [4, 8, 10, "…"],
  "page_starts": [0, 29, 65, "…"],
  "line_starts": [0, 4, 8, "…"],
  "juz_starts":  [0, 2522, "…"],

  "suras": [ { "number": 1, "name_ar": "الفَاتِحة", "name_en": "Al-Fātiḥah", "revelation": "makki",
               "has_basmalah": true, "ayah_count": 7, "first_ayah": 0 }, "…" ],

  "marks":      [[33, 0], [34, 0], "…"],
  "mark_types": [ { "kind": "waqf", "side": "after", "sign": "ۖ" }, "…" ],
  "mark_signs": { "ۖ": { "cp": "U+06D6", "unicode_name": "…" } },

  "resegmentation":     [ { "positions": [11633, 11634], "sura": 4, "ayah": 91, "kind": "joined_in_source",
                            "source_text": "مَا رُدُّوٓاْ", "emitted": ["مَا", "رُدُّوٓاْ"], "riwayat_agree": true } ],
  "line_disagreements": [ { "sura": 1, "ayah": 1, "derived": 3, "source": 2 }, "…" ]
}
```

The reason is the one this project is built on: *the āyah is an attribute of a
word, not a level of nesting.* The editions count 6,214 to 6,236 āyāt, so
`2:255:3` names a different word in each of them. Nesting words under āyāt
would put the unstable coordinate on the outside and make the seven files
incomparable. Reconstructing a nested view takes three lines, and
`out/mushaf/<key>.nested.json.gz` ships one already.

## Two kinds of integer, kept apart

| kind | where it appears | meaning |
|---|---|---|
| **position** | every `*_starts` array, `marks[][0]`, `numbering.written_joined[].position`, `resegmentation[].positions` | index into `words` of *this* muṣḥaf |
| **number** | `numbering.total`, `numbering.missing`, `numbering.written_joined[].numbers` | the shared numbering that means the same word in all seven |

No field holds both. A key that ends in `_starts` holds positions. Only the
`numbering` block holds numbers.

## The rules

- **`words[i]` is the *i*-th printed word of this muṣḥaf**, in ʿUthmānī
  spelling exactly as the release prints it, without pause marks. That is a
  word's address inside its own file, and it does not depend on the numbering.
- **Every `*_starts` array is a sorted list of positions**, one per unit, and
  unit *k* is `words.slice(starts[k], starts[k+1] ?? words.length)`. Slicing
  is correct in all seven files; there is nothing to filter.
- **`ayah_starts` is what this edition prints**, one entry per numbered āyah
  and nothing else. The basmalah of al-Fātiḥah is in it only where the edition
  counts it: Ḥafṣ, Shuʿbah and Bazzī number it `1:1` and their `ayah_starts[0]`
  is `0`; Warsh, Qālūn, Dūrī and Sūsī print the same four words unnumbered, so
  their `ayah_starts[0]` is `4` and positions `0…3` belong to no āyah.
  `counting.basmalah_counted` states this once instead of an āyah numbered 0.
- **The sūrah an āyah belongs to** is the last `sura_starts` entry at or before
  it. `suras[k].ayah_count` is the edition's count for that sūrah and
  `suras[k].first_ayah` the prefix sum, so `(sūrah, n)` → index into
  `ayah_starts` is `first_ayah + n − 1`. `suras[k].has_basmalah` is false for
  at-Tawbah alone; whether the basmalah is *counted* is `counting.basmalah_counted`.
- **`page_starts` is read** from the release's explicit page breaks;
  **`line_starts` is reconstructed** and declared under `layers.derived.line`
  with its score. A line is counted within the whole muṣḥaf; the views convert
  it to a line within the page. Bazzī's lines cannot be validated and its file
  says so.
- **`juz_starts`** comes from the v2 CSV and is absent for Bazzī, which has
  none; `layers.absent` says why.
- **`marks`** is a list of `[position, type]` with `mark_types` interned per
  file and `mark_signs` naming every sign's codepoint. See *Marks*.
- **`imlaei`** is an array parallel to `words`, or `null` when the release
  carries no imlāʾī column. A `null` entry is a word the chain could not
  resolve. Ḥafṣ only, as before.
- **`resegmentation` and `line_disagreements`** are disclosures and are present
  even when empty.
- **The word count is `words.length`**; `mushaf.word_count` restates it so a
  consumer can check a truncated download.

## Numbering

The shared numbering counts the **finest division** of the text that any of
the seven muṣḥafs prints: every word anyone writes has a number, and where one
muṣḥaf writes two words as one, the two words are numbered separately. The
numbers run `1 … total` with no gap.

Every word in `words` covers a **contiguous run** of those numbers. Runs are in
order and do not overlap. A run has length one except where the muṣḥaf writes
joined what others write apart.

`numbering` is the complete description of how this muṣḥaf's positions map
onto the numbers:

```json
"numbering": {
  "total":          77434,
  "missing":        [25685],
  "written_joined": [ { "position": 73948, "numbers": [73950, 73951] } ]
}
```

| key | holds | means |
|---|---|---|
| `total` | a count | the size of the shared numbering, the same in all seven files |
| `missing` | numbers | this muṣḥaf **does not read** these words. A number appears here if and only if no word in `words` covers it |
| `written_joined[].position` | a position | the word in `words` that covers more than one number |
| `written_joined[].numbers` | numbers, `[first, last]` | the inclusive run it covers, always of length ≥ 2 |

The invariants, which the build checks on every file:

1. runs are strictly increasing and contiguous, so every number in
   `1 … total` is covered by exactly one word or listed in `missing`, never
   both, never neither;
2. `len(words) + Σ(len(run) − 1 for run in written_joined) + len(missing) == total`;
3. `total` is identical across the seven files;
4. every `written_joined` run is length ≥ 2, and every `missing` number is
   covered by at least one *other* muṣḥaf — otherwise it would not be in the
   numbering at all.

A word's number can be recovered from its position in one pass: walk `words`,
advance the counter by one per word, skip over `missing`, and advance by the
run length at a `written_joined` position. A consumer who never compares
recitations never needs to.

In the current sources the whole of it is five āyāt. Three words are read by
some muṣḥafs and not others — `مِن` at 9:101 (Bazzī alone), `أَوۡ` at 40:26
(Ḥafṣ and Shuʿbah, where the other five read `وَ`), `هُوَ` at 57:24 (all but
Warsh and Qālūn) — and two pairs of words are written joined: `وَأَلَّوِ` at
72:16 by Ḥafṣ, Shuʿbah and Bazzī, and `أَلَّن` at 73:20 by Dūrī and Sūsī. Which
places are joins is declared in `data/written-joined.json`, because the
unwritten nūn changes the rasm and no rule can tell a join from a different
reading; the build asserts the list is exactly these.

**`missing` says "does not read this word", nothing finer.** At 40:26 Warsh's
`وَأَنْ` covers the number of `أَن` and `أَوۡ` is `missing`. That is true, but the
fuller truth is that Warsh reads `وَ` where Ḥafṣ reads `أَوۡ`. `numbering` does
not record substitutions; the word text does, and so does the word index.

**`written_joined` is not `resegmentation`.** `written_joined` records a
muṣḥaf that *really* prints two words as one — an orthographic fact about that
muṣḥaf. `resegmentation` records a source package that *lost a space* and was
split back by the build — a defect in the file, not a feature of the muṣḥaf.
They are separate keys.

The scheme is a property of the format, bound by `format_version`, not a field
a file may set. Numbers are stable across rebuilds of the same sources and are
*not* promised across a future KFGQPC release — see `docs/LIMITATIONS.md`.

## The word index

Under this numbering the master is a division nobody prints, so it has a file
of its own, normative alongside the seven: `out/word-index.json`, and
`out/word-index.csv` with the same columns flattened. One record per number:

```json
{ "number": 73951, "sura": 72, "index": 153, "key": "72:لو#1",
  "rasm": "لو", "pointed": "لو", "uthmani": "لَّوِ", "simple": "لّو",
  "status": "word_boundary",
  "hafs": { "sura": 72, "ayah": 16, "pos": 1 },
  "forms": { "hafs": "وَأَلَّوِ", "shuba": "وَأَلَّوِ", "bazzi": "وَأَلَّوِ",
             "qaloun": "لَّوِ", "warsh": "لَّوِ", "douri": "لَّوِ", "sousi": "لَّوِ" },
  "ayah":  { "hafs": 16, "shuba": 16, "bazzi": 16, "qaloun": 16, "warsh": 16, "douri": 16, "sousi": 16 },
  "written_joined": ["hafs", "shuba", "bazzi"] }
```

- `number` is the shared number, `1 … total`, dense.
- `uthmani`, `pointed`, `rasm`, `simple` describe *this one word*, taken from a
  muṣḥaf that writes it apart.
- `hafs` is the word's `sura`, `ayah` and `pos` in the āyah in the Kūfī count,
  present on every number Ḥafṣ covers and `null` where it does not. This is the column that lets
  every existing word-level dataset — corpus.quran.com morphology, quran.com
  word audio segments, word-by-word translations — attach in one lookup. At
  72:16 two numbers carry the same coordinates, which is the honest statement
  that Ḥafṣ writes them as one word.
- `forms[key]` is absent where that muṣḥaf lacks the number. Where a muṣḥaf
  writes the number joined with its neighbour the form is the joined word,
  repeated on both numbers, and `written_joined` names those muṣḥafs.
- `ayah[key]` is absent in the same places; `0` is the unnumbered basmalah.
- `status` keeps the vocabulary of `docs/SCHEMA.md`, which also lists the
  optional fields: `groups` (the distinct spellings and who uses each),
  `missing`, `resegmented`, `waqf`, `hizb`, `sajdah`.

The word index is where a number gets a text. The muṣḥaf files are where a
text gets a position. Neither is derivable from the other alone, so both are
normative. `out/differences.json` is the same records filtered to the words
where the riwāyāt disagree, and `out/ayah-map.json` answers what a Kūfī āyah
reference is in each edition.

## Counting: system, transmission, edition

An āyah count is not a property of the qirāʾah. It belongs to the **edition**,
and there is a level in between:

| level | what it is | example |
|---|---|---|
| **counting system** | one of the six madhhabs of ʿadd al-āy, as the classical sources define it | المدني الأول |
| **transmission within the system** | the system reached us through more than one authority, and at some points they differ | Abū Jaʿfar and Shayba differ at 3:92, 3:97, 37:167, 67:9, 80:24, 81:26 |
| **edition** | one printing declares a system and, at the points of khilāf inside it, follows one authority, a stated rule, or sets them aside | the 1429 KFGQPC Dūrī: «(٦٢١٤) … ما عدا الآيات المختلف فيها بين أبي جعفر وشيبة» |

Three KFGQPC printings of the Dūrī muṣḥaf carry two different āyah divisions
and three different colophons. None of that is an error; it is the third level
doing its job, and a string cannot hold it. So the `counting` block:

```json
"counting": {
  "system": "madani-first", "system_name_ar": "المدني الأول", "system_name_en": "First Madinan",
  "declared_by": null,
  "ayah_count": 6217,
  "basmalah_counted": false,
  "khilaf": [
    { "sura": 67, "ayah": 9, "kufi": "67:9", "number": 72557, "anchor": "نذير", "counted": false,
      "follows": ["abu-jafar"], "against": ["shayba"],
      "source": { "work": "البيان في عدّ آي القرآن", "locator": "…" } }
  ],
  "unexplained": []
}
```

| field | meaning |
|---|---|
| `system` | the madhhab this edition follows. **Derived** by comparing the edition's `ayah_starts` to each system's boundaries and taking the one it matches once khilāf points are set aside; the distances are in `distance_to_systems` |
| `declared_by` | what the edition states about itself, and where, or `null` if the source in `data/` states nothing — which is the case for every KFGQPC `.docx`, since they carry the text without the printed colophon. A declaration that disagreed with the derived system would be kept and flagged `declared_disagrees`, not overwritten |
| `ayah_count` | what the edition prints: `ayah_starts.length` |
| `basmalah_counted` | whether the basmalah of al-Fātiḥah is a numbered āyah |
| `khilaf[]` | **every** point where the sources record a disagreement *inside* this system — not only the ones where this edition departs from the default — with what this edition does there (`counted`) and whose position that is (`follows`, `against`). `number` is the shared number the āyah ends after and `anchor` the word it follows; `sura`/`ayah` are this edition's own numbering; `kufi` is the Kūfī reference |
| `unexplained[]` | āyah ends where the edition differs from the system and no source records a khilāf. The build fails on any that is not listed in `data/counting/open-findings.json`, and on any listed there that no longer occurs |

The seven editions today:

| edition | system | āyāt | khilāf | unexplained |
|---|---|---|---|---|
| Ḥafṣ, Shuʿbah | Kūfī | 6,236 | — | — |
| Warsh, Qālūn | Last Madinan | 6,214 | — | — |
| Dūrī | First Madinan | 6,217 | six Abū Jaʿfar/Shayba points; 67:9 not counted, following Abū Jaʿfar | — |
| Sūsī | First Madinan | 6,218 | the same six; 67:9 counted, following Shayba | — |
| Bazzī | Makkī | 6,220 | — | 78:40 ﴿قريبًا﴾ counted, until a source is cited |

The boundaries come from
[qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map), vendored at
a pinned commit under `data/counting/` with its SHA-256 in the manifest and in
`counting.checked_against`. The disagreements *inside* a system, which that
repository does not yet model, are this repository's overlay
`data/counting/khilaf.json`, cited point by point from al-Dānī's *al-Bayān*.
Where an anchor word occurs twice in its Kūfī āyah (three of the 246 points),
the occurrence the editions actually end at is taken and listed under
`resolved_anchors` in `out/counting.json`.

`out/counting.json` is the same information keyed by system: every system's
boundaries as numbers, the editions that follow each, and their `khilaf`
resolutions alongside.

## Marks

```json
"marks":      [[33, 0], [51, 1]],
"mark_types": [ { "kind": "waqf",   "side": "after",  "sign": "ۖ" },
                { "kind": "hizb",   "side": "before", "sign": "۞" },
                { "kind": "sajdah", "side": "after",  "sign": "۩" } ]
```

`marks[i]` is `[position, index into mark_types]`. `mark_types` is interned per
file — the whole corpus has 4,491 marks of 8 kinds in Ḥafṣ, so restating
`{kind, side, sign}` on each would be waste. `side` is which side of the word
the sign is printed on. `mark_signs` at the top of every file
maps each sign to its codepoint and Unicode name, so no consumer has to
hard-code a table.

**Waqf marks are not comparable across muṣḥafs.** Warsh and Qālūn print one
general pause sign where Ḥafṣ, Dūrī and Sūsī print seven distinct ones. This is
a difference of publishing convention, not of reading, and nothing here
normalises it.

**The ۞ counts disagree between the releases** — 199 in Ḥafṣ, Shuʿbah and Bazzī
against 433–437 in the others. The symbol is emitted exactly as each release
prints it. It is *not* reconciled to the 240 arbāʿ, because that number is not in
any package and this project does not add data its sources do not carry.

## Page is read; line is reconstructed

These are not equally sound, and the format keeps them apart.

**Page** is read from the release. Every `.docx` marks its page turns
explicitly — 603 `<w:br w:type="page"/>` elements, giving 604 pages. Checked
against the v2 CSVs, the page of every āyah agrees. It is available for **all
seven muṣḥafs, Bazzī included**, which has no CSV at all.

**Line is not encoded anywhere.** It is inferred from the document's line
breaks, paragraph boundaries and headings. Ḥafṣ scores 6,131 of 6,236 āyāt
against the CSV that states the line, roughly 98.3%; the residual overshoots
by one or two on pages the publisher sets specially, al-Fātiḥah above all. So:

- every file declares the line layer under `layers.derived.line`, with its score;
- `line_disagreements` lists **every āyah** where the reconstruction differs
  from the release that states it, so a consumer can exclude them rather than
  discover them;
- Bazzī has no v2 release, so its lines **cannot be checked at all**, and its
  file says `"validated": false` rather than implying the same confidence.

Treat `line_starts` as an aid to layout, not as a citable fact. Treat
`page_starts` as a fact.

## Departures from the source

A shared numbering is only stable because the alignment sometimes overrides a
package's own spacing — splitting what one source printed joined. A file
claiming to *be* that muṣḥaf has to say where that happened, so every one is
listed, addressed by position:

```json
"resegmentation": [
  { "positions": [11633, 11634], "sura": 4, "ayah": 91,
    "kind": "joined_in_source",
    "source_text": "مَا رُدُّوٓاْ",
    "emitted": ["مَا", "رُدُّوٓاْ"],
    "riwayat_agree": true }
]
```

`riwayat_agree` of `true` means every muṣḥaf reads the run identically once
re-segmented — a source that lost a space, not a muṣḥaf that really prints the
words joined. The list is present even when empty, so silence is never
ambiguous. In the current sources: **Dūrī 5, Bazzī 3, Qālūn 1**, and none for
Ḥafṣ, Shuʿbah, Warsh or Sūsī.

## Imlāʾī

Published for **Ḥafṣ only**, because the Ḥafṣ v2 release is the only package with
an `aya_text_emlaey` column. It is **never generated**: deriving it by rule for
the other six would be this project asserting a spelling no source states.

The column is per āyah, so it is brought down to the word. 6,175 of 6,236 āyāt
hold exactly as many imlāʾī tokens as ʿUthmānī ones and map across directly. In
the other 61 the imlāʾī side always has *more* — it writes `أو لا` where the
ʿUthmānī line writes `أَوَلَا` — never fewer; those are matched on the skeleton
and joined, so an entry is always one string. A word the chain cannot resolve
is `null`. `layers.derived.imlaei` reports the totals.

## Provenance

Every file names the KFGQPC release it came from, with a SHA-256 — in the file
itself, not only in the manifest, because a muṣḥaf file will be copied and
vendored on its own and a text whose edition cannot be named is not citable.

`out/manifest.json` carries the same hashes for every source package,
for the vendored qiraat-ayah-map data, and for every emitted file, and lists
the normative set.

## What each file declares

`layers.present` and `layers.absent` say what a file carries and why it lacks
whatever it lacks, so a consumer can check before querying instead of
discovering a missing key at runtime. Bazzī:

```json
"absent": { "juz": "no v2 package released for this riwāyah",
            "imlaei": "column not present in this riwāyah's release" }
```

Bazzī still has `page_starts`, because page comes from the `.docx` that every
muṣḥaf has.

## Views

| path | shape |
|---|---|
| `out/mushaf/<key>.nested.json.gz` | sūrah → āyah → words, with every layer's value repeated on the word; the unnumbered basmalah under `"basmalah"` |
| `out/mushaf/<key>.csv.gz` | one row per word: `pos, sura, ayah, pos_in_ayah, page, line, juz, number, number_last, text, imlaei, marks, resegmented` |
| `out/quran.sqlite.gz` | all seven plus the word index; `word(mushaf, pos, …, number, number_last, …)` and `word_index(number, …)` |
| `out/ayah-map.json` | what a Kūfī āyah reference is in every edition |
| `out/counting.json` | the counting systems, their boundaries as numbers, and the editions under each |

There is no per-sūrah file: a whole muṣḥaf is about half a megabyte gzipped,
and a sūrah, a page or a juz is one slice of it.

`ayah` in the CSV and SQLite views is `0` for the unnumbered basmalah. Where a
word covers a run of numbers, `number` is the first and `number_last` the
last; elsewhere they are equal, so the table stays one row per word.

Comparing two muṣḥafs in SQL:

```sql
SELECT a.number, a.uthmani, b.uthmani
FROM word a LEFT JOIN word b
  ON b.number = a.number AND b.mushaf = 'warsh'
WHERE a.mushaf = 'hafs' AND (b.uthmani IS NULL OR b.uthmani <> a.uthmani);
```

`LEFT JOIN` rather than `JOIN` because the answer is sometimes *no row*: Warsh
does not recite `هُوَ` at 57:24, and a word-level dataset projected from Ḥafṣ
has to see that rather than skip silently past it.

## Known issues

Listed in full in `docs/ISSUES.md`: the reconstructed lines, the ۞ discrepancy,
the incomparable waqf conventions, Bazzī's missing layers, the imlāʾī residual,
and the open counting finding at 78:40.
