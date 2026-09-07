# What is in `out/`

Everything is written by `python3 build.py`. All text is UTF-8, NFC, with no
BOM. Start with `out/catalog.json`: it lists the riwāyāt, the sūrahs, and every
file below with the question it answers.

Two files are **normative**, specified in [`format.md`](format.md)
and checkable against `schema/`: `out/mushaf/<key>.json` (one muṣḥaf) and
`out/word-index.json` (the shared numbering). Everything else is generated
from them.

| you want to… | read |
|---|---|
| render one muṣḥaf | `mushaf/<key>.json`, or `.nested.json.gz` / `.csv.gz` views of it |
| use the same word across riwāyāt, attach a Ḥafṣ-keyed dataset, search | `word-index.json` / `.csv` |
| see only where the riwāyāt differ | `differences.json` / `.csv` |
| convert an āyah reference between editions | `ayah-map.json` / `.csv` |
| know which counting system an edition follows, and the boundaries of all six | `counting.json` |
| query in SQL | `quran.sqlite.gz` |
| verify what you downloaded | `manifest.json` |
| read the findings and how this was built | `reports/` |

## `out/catalog.json`

```json
{ "format": "quran-catalog", "word_count": 77434, "surah_count": 114,
  "riwayahs": [ { "key": "duri", "name_en": "Dūrī", "name_ar": "الدوري", "qiraah_en": "…", "qiraah_ar": "…",
                 "counting_system": "madani-first", "ayah_count": 6217, "word_count": 77431,
                 "source": "UthmanicDouri_V20.zip :: UthmanicDouri V20.docx", "crosscheck_source": "…",
                 "file": "out/mushaf/duri.json" }, "…" ],
  "surahs":   [ { "number": 1, "name_ar": "الفَاتِحة", "name_en": "Al-Fātiḥah", "revelation": "makki",
                 "word_count": 29, "first_number": 1, "last_number": 29,
                 "ayah_count": { "hafs": 7, "warsh": 7, "…": 7 } }, "…" ],
  "files":   [ { "path": "out/mushaf/<key>.json", "format": "quran-mushaf", "normative": true, "answers": "…" }, "…" ] }
```

## `out/mushaf/<key>.json` and its views

One muṣḥaf: `words` by position, with `ayah_starts`, `page_starts`,
`line_starts`, `juz_starts`, `marks`, and the `numbering` block that maps
positions onto the shared numbers. Specified in
[`format.md`](format.md), schema `schema/mushaf-1.0.json`.

| view | shape |
|---|---|
| `mushaf/<key>.nested.json.gz` | `surahs → ayahs → words[]`, every layer's value repeated on the word; the unnumbered basmalah under `"basmalah"` |
| `mushaf/<key>.csv.gz` | one row per word: `position, surah, ayah, position_in_ayah, page, line, juz, number, number_last, text, rasm_imlai, marks, resegmented`; `ayah` is `0` for the unnumbered basmalah |

A sūrah, a page or a juz is one slice of `words`, so there is no per-sūrah file.

## `out/fonts/`

The KFGQPC font each muṣḥaf's text is set in, one `.ttf` per riwāyah, copied
from the same package as the text. Each muṣḥaf file's `font` block names its
own (`family`, `file`, `sha256`); ship that font with that text, because the
words use codepoints only it is guaranteed to draw. See `format.md`, *Font*.

## `out/word-index.json` and `out/word-index.csv` — the numbering

Every number of the shared numbering, `1 … 77434`, one record per line, with
a text, its Ḥafṣ coordinates, and each riwāyah's form. Schema
`schema/word-index-1.0.json`.

```json
{ "number": 11, "surah": 1, "index": 11, "key": "1:مالك#1",
  "rasm": "ملك", "pointed": "مالك", "rasm_uthmani": "مَٰلِكِ", "plain": "مالك",
  "status": "dotting_variant",
  "hafs":  { "surah": 1, "ayah": 4, "position": 1 },
  "ayah":  { "hafs": 4, "shubah": 4, "bazzi": 4, "qalun": 3, "warsh": 3, "duri": 3, "susi": 3 },
  "forms": { "hafs": "مَٰلِكِ", "shubah": "مَٰلِكِ", "bazzi": "مَلِكِ", "qalun": "مَلِكِ",
             "warsh": "مَلِكِ", "duri": "مَلِكِ", "susi": "مَّلِكِ" },
  "groups": [ { "text": "مَٰلِكِ", "riwayahs": ["hafs", "shubah"] },
              { "text": "مَلِكِ", "riwayahs": ["bazzi", "qalun", "warsh", "duri"] },
              { "text": "مَّلِكِ", "riwayahs": ["susi"] } ] }
```

| field | always | meaning |
|---|---|---|
| `number` | ✓ | the shared number — the same integer every muṣḥaf file maps its positions onto, and the same key in every view and in SQLite |
| `surah` | ✓ | the sūrah |
| `index` | ✓ | 1-based position within the sūrah |
| `key` | ✓ | `sūrah:pointed#occurrence` — content-derived, stable across rebuilds |
| `rasm` | ✓ | bare ʿUthmānic skeleton — undotted, unvowelled, no hamzah, no dagger alif. The alignment key: every riwāyah sharing a number shares this exactly, except in the 60 `rasm_variant` and 198 `alif_variant` words |
| `pointed` | ✓ | the same skeleton with its dots, from the canonical spelling |
| `rasm_uthmani` | ✓ | canonical display form of this one word — Ḥafṣ's spelling where Ḥafṣ writes the word apart, else the most common |
| `plain` | ✓ | plain spelling for search: no harakah, superscript alif written out |
| `status` | ✓ | see below |
| `hafs` | ✓ | `{surah, ayah, position}` in the Kūfī count, `null` where Ḥafṣ does not read the word; two numbers Ḥafṣ writes as one word share the same coordinates |
| `ayah` | ✓ | āyah number **per riwāyah**; `0` means printed but unnumbered (the basmalah) |
| `forms` | ✓ | each riwāyah's own spelling; a riwāyah is absent from this map iff it lacks the word. Where a riwāyah writes the word joined with its neighbour, this is the joined word |
| `groups` | — | the distinct spellings, each with the riwāyāt using it; present only when they are not all the same |
| `missing` | — | riwāyāt that do not read the word |
| `written_joined` | — | riwāyāt whose printed word here also covers the previous number: they write the two as one |
| `resegmented` | — | riwāyāt where this build changed the source's spacing, and how (`joined_in_source`, `split_in_source`, `unresolved_boundary`) |
| `waqf` | — | waqf marks that trailed the word, per riwāyah |
| `division` | — | riwāyāt printing `۞` before this word |
| `sajdah` | — | riwāyāt marking a sajdah `۩` on this word |

Optional fields are omitted when empty, so their presence is itself the signal.
`forms` and `groups` say the same thing two ways: `forms` answers "how does
Warsh spell this?" in one lookup; `groups` answers "who reads what?" without a
scan.

The CSV has one row per number with the same content flattened:

```
number, surah, index, key, rasm, pointed, rasm_uthmani, plain, status,
hafs_surah, hafs_ayah, hafs_position, missing, written_joined,
ayah_hafs … ayah_susi, form_hafs … form_susi
```

> **If Warsh, Qālūn or Sūsī look empty**, that is your font, not the data —
> their v3.0 documents use Arabic Extended-B codepoints (`U+0870`–`U+0882`) that
> few fonts can draw. Use the font named in each muṣḥaf's `font` block, under
> `out/fonts/`. See `docs/limitations.md`.

### `status`

| value | words | meaning |
|---|---|---|
| `identical` | 40,558 | same qiraah and spelling in all seven, after notation folding |
| `diacritic_variant` | 36,261 | same letters *and* dots — the vowelling differs |
| `dotting_variant` | 338 | one rasm, pointed differently: `تَعۡمَلُونَ` against `يَعۡمَلُونَ` |
| `alif_variant` | 198 | one skeleton once every ā is spelled out; the hands disagree about where the ā was written |
| `rasm_variant` | 60 | the riwāyāt disagree about the letters on the line |
| `word_boundary` | 16 | a source prints the word joined to its neighbour (12), or a muṣḥaf really writes it joined (4: 72:16, 73:20) |
| `partial` | 3 | the word is absent from at least one riwāyah: 9:101 `مِن`, 40:26 `أَوۡ`, 57:24 `هُوَ` |

Each word gets the *strongest* label that applies, tested in this order: rasm,
ā, absence, boundary, dotting, vowelling. So a `dotting_variant` is guaranteed
to share one rasm across all seven, an `alif_variant` to share one skeleton once
every ā is spelled out, and a `diacritic_variant` shares its dots too. A
riwāyah that writes the word joined to its neighbour is compared on nothing —
its form is of two words — and counted as present.

`alif_variant` is the plene/defective ā: `هَٰرُوتَ` against `هَارُوتَ`, the same
word with the alef on the line in one hand and above it in the other. It is not
counted as the codices disagreeing, and the reason is empirical rather than
editorial: **all 198 of these words divide the seven riwāyāt along exactly one
line — `qalun,warsh` against the other five — in both directions and without an
exception, while the 60 `rasm_variant` words divide them fourteen different
ways.** Ḥadhf and ithbāt al-alif do vary between the codices of the amṣār, but
they do not put Makkah with Madinah 198 times out of 198; a publisher's house
style does. `validate.check_alif_splits` asserts the one-partition fact, so a
future package that broke it would show up in the report's *Checks* section.

The distinction stays in `rasm` all the same, because within any one muṣḥaf it
is that muṣḥaf's own ḥadhf, carried consistently — Ḥafṣ writes قال plene 412
times and defective 4 — and 175 of the 198 show the identical split at every
occurrence of the word. `reports/COMPARISON.md` lists them under *The ā on the
line or above it*.

`rasm_variant` is the residue: a letter one codex has on the line and another
does not. 56 of the 60 are one skeleton with one letter more — `ٮرٮد`/`ٮرٮدد`
(يَرۡتَدَّ/يَرۡتَدِدۡ, 5:54), `ٮسٮهى`/`ٮسٮهٮه` (تَشۡتَهِي/تَشۡتَهِيهِ, 43:71) — and 4 are
one letter exchanged for another, `ولا`/`ڡلا` and `كلمٮ`/`كلمه`. The report
tables them separately.

`word_boundary` is deliberately ranked *below* the content comparison. It used
to outrank everything, which meant five of the six boundary events in the corpus
were reported as disagreements when in fact all seven riwāyāt read them
identically and one *source* had merely lost a space. `resegmented` is still
set either way; `reports/resegmentation.csv` says which is which, and the two
really-joined words are listed apart in `reports/COMPARISON.md` under *Written
joined*.

## `out/differences.json` and `out/differences.csv`

The word-index records whose `status` is `rasm_variant`, `alif_variant`,
`word_boundary` or `partial` — 277 words — with `count` and `by_status` at the
top. The CSV groups identical spellings so one row shows who reads what:

```
number, surah, index, ayah_hafs, status, rasm, missing_in, written_joined_by,
resegmented_in, distinct_forms, forms
قُلۡ [hafs,shubah,warsh,qalun,duri,susi]  ||  قَالَ [bazzi]
```

## `out/ayah-map.json` and `out/ayah-map.csv`

What a Kūfī āyah reference is in every edition. The table is derived from the
shared word numbering — an āyah is a run of numbers, and the editions' āyāt
holding those numbers are its counterparts — so the libraries' `ayah.to(other)`
computes the same answer between any two editions without this file; it is
published for readers who load one file rather than two. One entry per āyah of the
Kūfī count as Ḥafṣ prints it; for each edition, the āyah its words fall in and
how the two relate. Schema `schema/ayah-map-1.0.json`.

```json
{ "surah": 2, "ayah": 255,
  "hafs":  { "surah": 2, "ayah": 255, "relation": "same" },
  "warsh": { "surah": 2, "ayah": 253, "ayah_last": 254, "relation": "split" },
  "duri": { "surah": 2, "ayah": 253, "relation": "same" }, "…": "…" }
```

| relation | meaning |
|---|---|
| `same` | the edition's āyah has exactly these words |
| `merged` | the edition's āyah also contains words of a neighbouring Kūfī āyah |
| `split` | the Kūfī āyah's words fall in more than one edition āyah — `ayah_last` is present |
| `shifted` | the boundaries cross: neither āyah contains the other |
| `unnumbered` | the words are printed but not numbered — the basmalah of Al-Fātiḥah, `ayah: 0` |

The CSV has one row per Kūfī āyah with a `2:253-254` style cell per edition
and a `<key>_relation` column each.

## `out/counting.json`

The six classical counting systems, each with its āyah boundaries as shared
numbers, and the editions that follow each with their choices at the points of
khilāf inside the system. Schema `schema/counting-1.0.json`.

```json
{ "format": "quran-counting",
  "source": { "repository": "https://github.com/quranpedia/qiraat-ayah-map", "commit": "…", "files": { "…": "sha256" } },
  "disputed_points": [ { "kufi": "1:1", "kind": "end", "anchor": "الرحيم", "number": 4, "counted_by": ["makki", "kufi"] }, "…" ],
  "systems": {
    "madani-first": { "name_ar": "المدني الأول", "name_en": "First Madani", "reference_total": 6217,
                      "editions": [ { "mushaf": "duri", "ayah_count": 6217, "khilaf": [ "…" ], "unexplained": [] },
                                    { "mushaf": "susi", "ayah_count": 6218, "khilaf": [ "…" ], "unexplained": [] } ],
                      "khilaf_points": [ { "kufi": "67:9", "anchor": "نذير", "number": 72557,
                                           "authorities": { "abu-jafar": false, "shayba": true }, "source": { "…": "…" } }, "…" ],
                      "ayah_ends": [8, 10, "…"] },
    "basri": { "…": "…", "editions": [] } },
  "open_findings": [ { "mushaf": "bazzi", "surah": 78, "ayah": 40, "…": "…" } ],
  "resolved_anchors": [ "…" ] }
```

The count belongs to the printed edition rather than to the riwāyah, so an
edition is listed under the system its own `ayah_starts` match, not under the
system its riwāyah is conventionally associated with; Baṣrī and Dimashqī have
no edition here. `ayah_ends[i]` is the number after which an āyah ends.
Rationale and the derivation are in `format.md`, *Counting*.

## `out/quran.sqlite.gz`

All seven muṣḥafs and the word index in one file. Tables: `mushaf`, `surah`,
`word` (one row per printed word, keyed `(mushaf, position)`, with `number` and
`number_last`), `word_index` (one row per number), `mark`, `resegmentation`,
`line_disagreement`. `ayah` is `0` for the unnumbered basmalah. Where a word
covers a run of numbers, `number` is the first and `number_last` the last;
elsewhere they are equal, so the table stays one row per word.

Comparing two muṣḥafs:

```sql
SELECT a.number, a.rasm_uthmani, b.rasm_uthmani
FROM word a LEFT JOIN word b
  ON b.number = a.number AND b.mushaf = 'warsh'
WHERE a.mushaf = 'hafs' AND (b.rasm_uthmani IS NULL OR b.rasm_uthmani <> a.rasm_uthmani);
```

`LEFT JOIN` rather than `JOIN` because the answer is sometimes *no row*: Warsh
does not recite `هُوَ` at 57:24, and a word-level dataset projected from Ḥafṣ
has to see that rather than skip silently past it.

## `out/manifest.json`

The SHA-256 of every source package, of the vendored counting data, and of
every file under `out/`, and the list of normative files.

## `out/reports/`

For people to read, not to load.

| file | what |
|---|---|
| `COMPARISON.md` | the cross-riwāyah report: what is compared at each level, each edition's derived counting system, the status distribution, pairwise agreement, every rasm disagreement, every boundary event with each riwāyah's own text, the absent and written-joined words, the fawāṣil and how far apart the editions are, source-integrity cross-checks, a per-sūrah density table |
| `rasm-variants.md` | every letter-level disagreement in full: the 60 `rasm_variant` words, then the 198 `alif_variant` ones |
| `compare.html` | a self-contained page: pick a sūrah, see every word with each riwāyah's spelling side by side, filter to one kind of disagreement, search |
| `agreement-matrix.csv` | `riwayah_a, riwayah_b, shared_words, same_spelling, same_qiraah, same_pointed, same_rasm` |
| `variants.csv` | one row per riwāyah form that differs from the canonical spelling: `number, surah, index, riwayah, ayah, canonical_rasm_rasm_uthmani, riwayah_rasm_uthmani, same_rasm, status` |
| `resegmentation.csv` | one row per place this build re-spaced a source: `numbers, surah, ayah_hafs, kind, riwayahs, riwayahs_agree, forms`; `riwayahs_agree` = 1 means every riwāyah reads the run identically once re-segmented, so the source merely lost a space |
