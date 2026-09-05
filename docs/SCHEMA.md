# Output schema

Everything is written to `out/` by `python3 build.py`. All text is UTF-8, NFC,
with no BOM.

Two files are **normative**: `out/mushaf/<key>.json` and `out/spine.json`
(with `out/spine.csv`), both specified in
[`MUSHAF-FORMAT.md`](MUSHAF-FORMAT.md) and checkable against
`schema/mushaf-1.0.json` and `schema/spine-1.0.json`. Everything below is the
cross-riwāyah index and its reports, generated from the same build.

## `out/spine.json` and `out/spine.csv` — the numbering

Every number of the shared numbering, `1 … 77434`, with a text, its Ḥafṣ
coordinates, and each riwāyah's form. The CSV has the same content flattened:

```
number, sura, rasm, pointed, uthmani, simple, status, hafs_sura, hafs_ayah, hafs_pos,
written_joined, ayah_hafs … ayah_bazzi, form_hafs … form_bazzi
```

See *The spine* in `MUSHAF-FORMAT.md` for the fields.

## `out/suras/NNN.json` — the index

One file per sūrah, `001.json` … `114.json`.

```json
{
  "sura": 1,
  "name_ar": "الفَاتِحة",
  "name_en": "Al-Fātiḥah",
  "revelation": "makki",
  "word_count": 29,
  "first_number": 1,
  "last_number": 29,
  "ayah_count": { "hafs": 7, "warsh": 7, "…": 7 },
  "words": [ … ]
}
```

### A word

```json
{
  "number": 11,
  "index": 11,
  "key": "1:مالك#1",
  "rasm": "مالك",
  "pointed": "مالك",
  "uthmani": "مَٰلِكِ",
  "simple": "مالك",
  "status": "dotting_variant",
  "ayah":  { "hafs": 4, "shuba": 4, "warsh": 3, "qaloun": 3, "douri": 3, "sousi": 3, "bazzi": 4 },
  "forms": { "hafs": "مَٰلِكِ", "shuba": "مَٰلِكِ", "warsh": "مَلِكِ", "qaloun": "مَلِكِ",
             "douri": "مَلِكِ", "sousi": "مَّلِكِ", "bazzi": "مَلِكِ" }
}
```

| field | always | meaning |
|---|---|---|
| `number` | ✓ | the shared number, `1 … 77434` — the same integer as `number` in `out/spine.json` and in every muṣḥaf view |
| `index` | ✓ | 1-based position within the sūrah |
| `key` | ✓ | `sūrah:pointed#occurrence` — content-derived, stable across rebuilds |
| `rasm` | ✓ | bare ʿUthmānic skeleton — undotted, unvowelled, no hamza, no dagger alif. The alignment key: every riwāyah sharing a number shares this exactly, except in the 60 `rasm_variant` and 198 `alif_variant` words |
| `pointed` | ✓ | the same skeleton with its dots, from the canonical spelling |
| `uthmani` | ✓ | canonical display form — Ḥafṣ's spelling where Ḥafṣ writes the word apart, else the most common |
| `simple` | ✓ | plain spelling for search: no diacritics, superscript alif written out |
| `status` | ✓ | see below |
| `ayah` | ✓ | āyah number **per riwāyah**; `0` means printed but unnumbered (the basmalah) |
| `forms` | ✓ | each riwāyah's own spelling; a riwāyah is absent from this map iff it lacks the word. Where a riwāyah writes the word joined with its neighbour, this is the joined word |
| `missing` | — | riwāyāt that do not read the word |
| `written_joined` | — | riwāyāt whose printed word here also covers the previous number: they write the two as one |
| `waqf` | — | pause marks that trailed the word, per riwāyah |
| `boundary` | — | riwāyāt where the word was re-segmented (`joined_in_source`, `split_in_source`, `unresolved_boundary`) or is really printed joined (`written_joined`) |
| `hizb` | — | riwāyāt marking a rub-el-ḥizb `۞` before this word |
| `sajdah` | — | riwāyāt marking a sajdah `۩` on this word |
| `groups` | — | the distinct spellings, each with the riwāyāt using it; present only when they are not all the same |

Optional fields are omitted when empty, so their presence is itself the signal.

`forms` and `groups` say the same thing two ways. `forms` answers "how does
Warsh spell this?" in one lookup; `groups` answers "who reads what?" without a
scan, and its mere presence means the riwāyāt part company here.

> **If Warsh, Qālūn or Sūsī look empty**, that is your font, not the data —
> their v3.0 documents use Arabic Extended-B codepoints (`U+0870`–`U+0882`) that
> few fonts can draw. See `docs/LIMITATIONS.md`.

### `status`

| value | words | meaning |
|---|---|---|
| `identical` | 40,558 | same reading and spelling in all seven, after notation folding |
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
line — `qaloun,warsh` against the other five — in both directions and without an
exception, while the 60 `rasm_variant` words divide them fourteen different
ways.** Ḥadhf and ithbāt al-alif do vary between the codices of the amṣār, but
they do not put Makkah with Madinah 198 times out of 198; a publisher's house
style does. `validate.check_alif_splits` asserts the one-partition fact, so a
future package that broke it would show up in the report's *Checks* section.

The distinction stays in `rasm` all the same, because within any one muṣḥaf it
is that muṣḥaf's own ḥadhf, carried consistently — Ḥafṣ writes قال plene 412
times and defective 4 — and 175 of the 198 show the identical split at every
occurrence of the word. `COMPARISON.md` lists them under *The ā on the line or
above it*.

`rasm_variant` is the residue: a letter one codex has on the line and another
does not. 56 of the 60 are one skeleton with one letter more — `ٮرٮد`/`ٮرٮدد`
(يَرۡتَدَّ/يَرۡتَدِدۡ, 5:54), `ٮسٮهى`/`ٮسٮهٮه` (تَشۡتَهِي/تَشۡتَهِيهِ, 43:71) — and 4 are
one letter exchanged for another, `ولا`/`ڡلا` and `كلمٮ`/`كلمه`. The report
tables them separately.

`word_boundary` is deliberately ranked *below* the content comparison. It used
to outrank everything, which meant five of the six boundary events in the corpus
were reported as disagreements when in fact all seven riwāyāt read them
identically and one *source* had merely lost a space. The `boundary` field is
still set either way; `out/boundaries.csv` says which is which, and the two
really-joined words are listed apart in `COMPARISON.md` under *Written joined*.

## `out/index.json`

The same sūrah headers with `words` omitted, plus corpus metadata and the
riwāyah registry (name, qāriʾ, āyah count, source file). Small; read this to
discover the corpus without loading it. The counting system is not here: it
belongs to the edition and is in each muṣḥaf file's `counting` block.

## `out/quran-words.json.gz`

Every sūrah and every word in one gzipped file (about 5 MB compressed, 36 MB raw).

```python
import gzip, json
data = json.load(gzip.open("out/quran-words.json.gz", "rt", encoding="utf-8"))
```

## `out/variants.csv`

One row per riwāyah form that differs from the canonical spelling.

```
number, sura, index, riwaya, ayah, canonical_uthmani, riwaya_uthmani,
same_rasm, status
```

## `out/fawasil.json`

The six classical counting systems, each with its āyah boundaries as shared
numbers, and the editions that follow each with their choices at the points of
khilāf inside the system.

```json
{ "format": "quran-fawasil", "format_version": "1.0",
  "source": { "repository": "https://github.com/quranpedia/qiraat-ayah-map", "commit": "…", "files": { "…": "sha256" } },
  "disputed_points": [ { "kufi": "1:1", "kind": "end", "anchor": "الرحيم", "number": 4, "counted_by": ["makki", "kufi"] }, "…" ],
  "systems": {
    "madani-first": { "name_ar": "المدني الأول", "name_en": "First Madinan", "reference_total": 6217,
                      "editions": [ { "mushaf": "douri", "ayah_count": 6217, "khilaf": [ "…" ], "unexplained": [] },
                                    { "mushaf": "sousi", "ayah_count": 6218, "khilaf": [ "…" ], "unexplained": [] } ],
                      "khilaf_points": [ { "kufi": "67:9", "anchor": "نذير", "number": 72557,
                                           "authorities": { "abu-jafar": false, "shayba": true }, "source": { "…": "…" } }, "…" ],
                      "ayah_ends": [8, 10, "…"] },
    "basri": { "…": "…", "editions": [] } },
  "open_findings": [ { "mushaf": "bazzi", "sura": 78, "ayah": 40, "…": "…" } ] }
```

The count belongs to the printed edition rather than to the qirāʾah, so an
edition is listed under the system its own `ayah_starts` match, not under the
system its riwāyah is conventionally associated with; Baṣrī and Damascene have
no edition here. `ayah_ends[i]` is the number after which an āyah ends. Rationale
and the derivation are in `MUSHAF-FORMAT.md`, *Counting*.

## `out/boundaries.csv`

One row per word-boundary event — never per word, because a boundary
disagreement is about the space *between* two words.

```
numbers, sura, ayah_hafs, kind, riwayat, riwayat_agree, forms
```

`riwayat_agree` is the column that matters: `1` means every riwāyah reads the
run identically once re-segmented, so the flag is a source that lost a space
rather than a muṣḥaf that really prints the words joined. The two places a
muṣḥaf really prints two words as one are not events here; they are
`written_joined` in the numbering.

## `out/conflicts.csv` and `out/conflicts.json`

Only the 277 words with `status` of `rasm_variant`, `alif_variant`,
`word_boundary` or `partial`. The CSV groups identical spellings so one row shows who reads what:

```
قُلۡ [hafs,shuba,warsh,qaloun,douri,sousi]  ||  قَالَ [bazzi]
```

## `out/agreement-matrix.csv`

Pairwise agreement, one row per pair of riwāyāt.

```
riwaya_a, riwaya_b, shared_words, same_spelling, same_reading, same_pointed,
same_rasm
```

## `out/COMPARISON.md` and `out/rasm-variants.md`

The human-readable report. It opens by stating what is being compared at each
level, then gives the inventory with each edition's derived counting system,
status distribution, pairwise agreement, every rasm disagreement, every
boundary event shown run by run with each riwāyah's own text, every absent
word, the two written-joined words, the fawāṣil with each edition's khilāf
choices and how far apart the editions are, source-integrity cross-checks, and
a per-sūrah density table. `rasm-variants.md` lists every letter-level
disagreement in full: the 60 `rasm_variant` words first, then the 198
`alif_variant` ones.

## `out/mushaf/`

Each muṣḥaf on its own, as words by position with every other fact a layer
over them, and the `numbering` block that maps positions onto the same shared
numbers used here. Specified separately in
[`MUSHAF-FORMAT.md`](MUSHAF-FORMAT.md), with a JSON Schema in
`schema/mushaf-1.0.json`; the views beside it (per-sūrah shards, nested,
CSV, SQLite) are described there too.

The files above compare the seven muṣḥafs; those publish one at a time, and add
what only makes sense for a single muṣḥaf: the page each word is printed on, the
line it falls on, its juz, the pause marks in that muṣḥaf's own convention, and
the counting system its āyah division follows.

## `out/compare.html`

A self-contained page for reading the comparison rather than querying it: pick
a sūrah, see every word with each riwāyah's spelling side by side, filter to
one kind of disagreement, and search. No server and no dependencies — open the
file.
