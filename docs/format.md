# The muṣḥaf format

`data/mushaf/<key>.json` publishes one muṣḥaf on its own. `data/word-index.json`
publishes the shared numbering that means the same word in all seven.

This document is the specification. **Only `data/mushaf/<key>.json` and
`data/word-index.json` (with `data/word-index.csv`) are normative.** The nested,
CSV and SQLite forms are generated from them and are labelled views; a consumer
may read them, but a claim about "the format" refers to the files above.
[`files.md`](files.md) lists every file under `data/`, the views of these two
included, and what each answers.

## The shape

**A muṣḥaf is an ordered array of word strings. Everything else is a layer over
that array, addressed by position.**

```json
{
  "format": "quran-mushaf", "format_version": "1.0", "generated": "2026-09-08",

  "mushaf":   { "key": "warsh", "name_en": "Warsh", "name_ar": "ورش",
                "qiraah_en": "Nāfiʿ al-Madanī", "qiraah_ar": "نافع المدني", "word_count": 77431 },
  "counting": { "system": "madani-last", "declared_by": null, "ayah_count": 6214,
                "basmalah_counted": false, "khilaf": [], "unexplained": [] },
  "provenance": { "text": { "package": "UthmanicWarsh-v-3.0.zip", "…": "…" }, "layout": { "…": "…" } },
  "layers":   { "present": ["surahs", "ayahs", "pages", "lines", "marks", "juz"], "absent": { "…": "…" } },

  "words":  ["بِسْمِ", "ࡴ۬للَّهِ", "ࡴ۬لرَّحْمَٰنِ", "ࡴ۬لرَّحِيمِ", "ࡴ۬لْحَمْدُ", "…"],
  "rasm_imlai": null,

  "numbering": { "total": 77434, "missing": [25685, 60522, 69720], "written_joined": [] },

  "surah_starts": [0, 29, 6146, "…"],
  "ayah_starts": [4, 8, 10, "…"],
  "page_starts": [0, 29, 65, "…"],
  "line_starts": [0, 4, 8, "…"],
  "juz_starts":  [0, 2522, "…"],

  "surahs": [ { "number": 1, "name_ar": "الفَاتِحة", "name_en": "Al-Fātiḥah", "revelation": "makki",
               "has_basmalah": true, "ayah_count": 7, "first_ayah": 0 }, "…" ],

  "marks":      [[33, 0], [34, 0], "…"],
  "mark_types": [ { "kind": "waqf", "side": "after", "sign": "ۖ" }, "…" ],
  "mark_signs": { "ۖ": { "cp": "U+06D6", "unicode_name": "…" } },

  "resegmentation":     [ { "positions": [11633, 11634], "surah": 4, "ayah": 91, "kind": "joined_in_source",
                            "source_text": "مَا رُدُّوٓاْ", "emitted": ["مَا", "رُدُّوٓاْ"], "riwayahs_agree": true } ],
  "line_disagreements": [ { "surah": 1, "ayah": 1, "derived": 3, "source": 2 }, "…" ]
}
```

Why the file is shaped this way is in [`design.md`](design.md); the views
generated from it are in [`files.md`](files.md).

## Two kinds of integer, kept apart

| kind | where it appears | meaning |
|---|---|---|
| **position** | every `*_starts` array, `marks[][0]`, `numbering.written_joined[].position`, `resegmentation[].positions` | index into `words` of *this* muṣḥaf |
| **number** | `numbering.total`, `numbering.missing`, `numbering.written_joined[].numbers` | the shared numbering that means the same word in all seven |

No field holds both. A key that ends in `_starts` holds positions. Only the
`numbering` block holds numbers.

## The rules

- **`words[i]` is the *i*-th printed word of this muṣḥaf**, in ʿUthmānī
  spelling exactly as the release prints it, without waqf marks. That is a
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
- **The sūrah an āyah belongs to** is the last `surah_starts` entry at or before
  it. `surahs[k].ayah_count` is the edition's count for that sūrah and
  `surahs[k].first_ayah` the prefix sum, so `(sūrah, n)` → index into
  `ayah_starts` is `first_ayah + n − 1`. `surahs[k].has_basmalah` is false for
  Tawbah alone; whether the basmalah is *counted* is `counting.basmalah_counted`.
- **`page_starts` is read** from the release's explicit page breaks;
  **`line_starts` is reconstructed** and declared under `layers.derived.line`
  with its score. A line is counted within the whole muṣḥaf; the views convert
  it to a line within the page. Bazzī has no v2 release to score against, so its
  file says `"validated": false`; its lines are nonetheless identical, word for
  word, to Ḥafṣ's.
- **`juz_starts`** comes from the v2 CSV and is absent for Bazzī, which has
  none; `layers.absent` says why.
- **`marks`** is a list of `[position, type]` with `mark_types` interned per
  file and `mark_signs` naming every sign's codepoint. See *Marks*.
- **`rasm_imlai`** is an array parallel to `words`, or `null` when the release
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
places are joins is declared in `sources/alignment/written-joined.json`, because the
unwritten nūn changes the rasm and no rule can tell a join from a different
qiraah; the build asserts the list is exactly these.

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
*not* promised across a future KFGQPC release — see `docs/limitations.md`.

## The word index

Under this numbering the master is a division nobody prints, so it has a file
of its own, normative alongside the seven: `data/word-index.json`, and
`data/word-index.csv` with the same columns flattened. One record per number:

```json
{ "number": 73951, "surah": 72, "index": 153, "key": "72:لو#1",
  "rasm": "لو", "pointed": "لو", "rasm_uthmani": "لَّوِ", "plain": "لّو",
  "status": "word_boundary",
  "hafs": { "surah": 72, "ayah": 16, "position": 1 },
  "forms": { "hafs": "وَأَلَّوِ", "shubah": "وَأَلَّوِ", "bazzi": "وَأَلَّوِ",
             "qalun": "لَّوِ", "warsh": "لَّوِ", "duri": "لَّوِ", "susi": "لَّوِ" },
  "ayah":  { "hafs": 16, "shubah": 16, "bazzi": 16, "qalun": 16, "warsh": 16, "duri": 16, "susi": 16 },
  "written_joined": ["hafs", "shubah", "bazzi"] }
```

- `number` is the shared number, `1 … total`, dense.
- `rasm_uthmani`, `pointed`, `rasm`, `plain` describe *this one word*, taken from a
  muṣḥaf that writes it apart.
- `hafs` is the word's `surah`, `ayah` and `position` in the āyah in the Kūfī count,
  present on every number Ḥafṣ covers and `null` where it does not. This is the column that lets
  every existing word-level dataset — corpus.quran.com morphology, quran.com
  word audio segments, word by word translations — attach in one lookup. At
  72:16 two numbers carry the same coordinates, which is the honest statement
  that Ḥafṣ writes them as one word.
- `forms[key]` is absent where that muṣḥaf lacks the number. Where a muṣḥaf
  writes the number joined with its neighbour the form is the joined word,
  repeated on both numbers, and `written_joined` names those muṣḥafs.
- `ayah[key]` is absent in the same places; `0` is the unnumbered basmalah.
- `status` keeps the vocabulary of `docs/files.md`, which also lists the
  optional fields: `groups` (the distinct spellings and who uses each),
  `missing`, `resegmented`, `waqf`, `division`, `sajdah`.

The word index is where a number gets a text. The muṣḥaf files are where a
text gets a position. Neither is derivable from the other alone, so both are
normative. `data/differences.json` is the same records filtered to the words
where the riwāyāt disagree, and `data/ayah-map.json` answers what a Kūfī āyah
reference is in each edition.

## Counting

The āyah count belongs to the printed edition, not to the riwāyah; the three
levels — counting system, transmission within it, edition — are explained in
[`design.md`](design.md). The `counting` block records what this edition does:

```json
"counting": {
  "system": "madani-first", "system_name_ar": "المدني الأول", "system_name_en": "First Madani",
  "declared_by": null,
  "ayah_count": 6217,
  "basmalah_counted": false,
  "khilaf": [
    { "surah": 67, "ayah": 9, "kufi": "67:9", "number": 72557, "anchor": "نذير", "counted": false,
      "follows": ["abu-jafar"], "against": ["shayba"],
      "source": { "work": "البيان في عدّ آي القرآن", "locator": "…" } }
  ],
  "unexplained": []
}
```

| field | meaning |
|---|---|
| `system` | the madhhab this edition follows. **Derived** by comparing the edition's `ayah_starts` to each system's boundaries and taking the one it matches once khilāf points are set aside; the distances are in `distance_to_systems` |
| `declared_by` | what the edition states about itself, and where, or `null` if the source in `sources/` states nothing — which is the case for every KFGQPC `.docx`, since they carry the text without the printed colophon. A declaration that disagreed with the derived system would be kept and flagged `declared_disagrees`, not overwritten |
| `ayah_count` | what the edition prints: `ayah_starts.length` |
| `basmalah_counted` | whether the basmalah of al-Fātiḥah is a numbered āyah |
| `khilaf[]` | **every** point where the sources record a disagreement *inside* this system — not only the ones where this edition departs from the default — with what this edition does there (`counted`) and whose position that is (`follows`, `against`). `number` is the shared number the āyah ends after and `anchor` the word it follows; `surah`/`ayah` are this edition's own numbering; `kufi` is the Kūfī reference |
| `unexplained[]` | āyah ends where the edition differs from the system and no source records a khilāf. The build fails on any that is not listed in `sources/counting/open-findings.json`, and on any listed there that no longer occurs |

The seven editions today:

| edition | system | āyāt | khilāf | unexplained |
|---|---|---|---|---|
| Ḥafṣ, Shuʿbah | Kūfī | 6,236 | — | — |
| Warsh, Qālūn | Last Madani | 6,214 | — | — |
| Dūrī | First Madani | 6,217 | six Abū Jaʿfar/Shayba points; 67:9 not counted, following Abū Jaʿfar | — |
| Sūsī | First Madani | 6,218 | the same six; 67:9 counted, following Shayba | — |
| Bazzī | Makkī | 6,220 | — | 78:40 ﴿قريبًا﴾ counted, until a source is cited |

The boundaries come from
[qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map), vendored at
a pinned commit under `sources/counting/` with its SHA-256 in the manifest and in
`counting.checked_against`. The disagreements *inside* a system, which that
repository does not yet model, are this repository's overlay
`sources/counting/khilaf.json`, cited point by point from al-Dānī's *al-Bayān*.
Where an anchor word occurs twice in its Kūfī āyah (three of the 246 points),
the occurrence the editions actually end at is taken and listed under
`resolved_anchors` in `data/counting.json`.

`data/counting.json` is the same information keyed by system: every system's
boundaries as numbers, the editions that follow each, and their `khilaf`
resolutions alongside.

## Marks

```json
"marks":      [[33, 0], [51, 1]],
"mark_types": [ { "kind": "waqf",   "side": "after",  "sign": "ۖ" },
                { "kind": "division",   "side": "before", "sign": "۞" },
                { "kind": "sajdah", "side": "after",  "sign": "۩" } ]
```

`marks[i]` is `[position, index into mark_types]`. `mark_types` is interned per
file — the whole corpus has 4,491 marks of 8 kinds in Ḥafṣ, so restating
`{kind, side, sign}` on each would be waste. `side` is which side of the word
the sign is printed on. `mark_signs` at the top of every file
maps each sign to its codepoint and Unicode name, so no consumer has to
hard-code a table.

**Waqf marks are not comparable across muṣḥafs.** Warsh and Qālūn print one
general waqf sign where Ḥafṣ, Dūrī and Sūsī print seven distinct ones. This is
a difference of publishing convention, not of qiraah, and nothing here
normalises it.

**`marks` records ink, not divisions.** The ۞ counts disagree between the
releases — 199 in Ḥafṣ, Shuʿbah and Bazzī against 433–437 in the others — and
the symbol is emitted exactly as each release prints it, reconciled to nothing.
Two things follow, and a consumer needs both:

- the 199-releases mark the **240 rubu_al_hizbs** and the others the **480 thumns**, so
  `marks` of the two groups are not counting the same division;
- **a division can be printed in the muṣḥaf and absent from `marks`.** Where a
  sūrah heading occupies the place the inline symbol would take, the printed
  muṣḥaf states the division in a margin medallion instead, and the `.docx`
  releases carry no marginal apparatus at all. Ḥafṣ prints 199 of its 239
  markable rubu_al_hizbs; the other 40 are in the margin.

So `marks` answers "what symbols does this edition print, and where", not "where
are this muṣḥaf's divisions". Only `juz_starts` is a division layer, and
`docs/known-issues.md` §11 records two points where even it disagrees with the
edition's own marks. See §7 for the full reconstruction.

*The kind is named `hizb` for historical reasons; ۞ is the **rubu_al_hizb**
sign, and the ḥizb proper is the marginal label these files do not carry.*

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
- Bazzī has no v2 release, so it is not scored against one, and its file says
  `"validated": false`. That is a statement about the *check*, not about the
  data: mapped through the shared numbering its lines are identical, word for
  word, to Ḥafṣ's, and so carry Ḥafṣ's accuracy. See `docs/known-issues.md` §6.

Treat `line_starts` as an aid to layout, not as a citable fact. Treat
`page_starts` as a fact.

## Departures from the source

A shared numbering is only stable because the alignment sometimes overrides a
package's own spacing — splitting what one source printed joined. A file
claiming to *be* that muṣḥaf has to say where that happened, so every one is
listed, addressed by position:

```json
"resegmentation": [
  { "positions": [11633, 11634], "surah": 4, "ayah": 91,
    "kind": "joined_in_source",
    "source_text": "مَا رُدُّوٓاْ",
    "emitted": ["مَا", "رُدُّوٓاْ"],
    "riwayahs_agree": true }
]
```

`riwayahs_agree` of `true` means every muṣḥaf reads the run identically once
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
is `null`. `layers.derived.rasm_imlai` reports the totals.

## Font

Every muṣḥaf file names the font its text is set in:

```json
"font": { "family": "KFGQPC Warsh Uthmanic Script", "file": "data/fonts/UthmanicWarsh-v-3.0.ttf",
          "package": "UthmanicWarsh-v-3.0.zip", "member": "UthmanicWarsh-v-3.0.ttf",
          "sha256": "…", "publisher": "https://fonts.qurancomplex.gov.sa/" }
```

It is the `.ttf` KFGQPC ships in the same package as the text, and it is
**required, not decorative**: the words use codepoints — the Arabic Extended-B
alefs of Warsh, Qālūn and Sūsī, the open tanwīn marks, the waqf signs — that
only this font is guaranteed to draw. A general Arabic font shows gaps where
those letters should be. `family` is read from the font's own name table so
a stylesheet or a `Typeface` can refer to it exactly; `file` is the copy under
`data/fonts/`, hashed like every other emitted file in `manifest.json`.

The `font` block also says which one to ship with which text, because each
muṣḥaf has its own: seven files, one per riwāyah, not one font for all seven.

## Provenance

Every file names the KFGQPC release it came from, with a SHA-256 — in the file
itself, not only in the manifest, because a muṣḥaf file will be copied and
vendored on its own and a text whose edition cannot be named is not citable.

`data/manifest.json` carries the same hashes for every source package,
for the vendored qiraat-ayah-map data, and for every emitted file, and lists
the normative set.

`generated` is the **edition date of the dataset**, not the day the file
happened to be written. It is declared once in the pipeline and committed
alongside the data it describes, so that rebuilding an unchanged commit — today,
or in ten years — produces the same bytes and therefore the same hashes in the
manifest. A date read from the clock would move every checksum in the dataset on
a build that had changed nothing, which is the opposite of what a manifest is
for. A release pipeline that wants to stamp its own date can export
`SOURCE_DATE_EPOCH`, the reproducible-builds convention; the date is read from
it, in UTC, when it is set.

## What each file declares

`layers.present` and `layers.absent` say what a file carries and why it lacks
whatever it lacks, so a consumer can check before querying instead of
discovering a missing key at runtime. Bazzī:

```json
"absent": { "juz": "no v2 package released for this riwāyah",
            "rasm_imlai": "column not present in this riwāyah's release" }
```

Bazzī still has `page_starts`, because page comes from the `.docx` that every
muṣḥaf has.

## Known issues

Listed in full in [`known-issues.md`](known-issues.md): the reconstructed
lines, the ۞ discrepancy, the incomparable waqf conventions, Bazzī's missing
layers, the imlāʾī residual, and the open counting finding at 78:40.

## The names

Every key here spells its concept the way the [Quran.ws terminology
standard](https://github.com/quranws/guidelines) does, so that a field in this
dataset means what the same field means in another Quranic one.
`.terminology.json` records how this repository is read against that standard —
which trees are vendored, which words are ordinary English here, and which
names belong to somebody else — and `audit_terminology.py --strict` passes with
no finding. Names this repository does not own are quoted, not chosen: the
KFGQPC package, member and font names, the columns of their CSVs (`sura_no`,
`aya_text_emlaey`) and the Unicode character names.
