# Output schema

Everything is written to `out/` by `python3 build.py`. All text is UTF-8, NFC,
with no BOM.

## `out/suras/NNN.json` — the index

One file per sūrah, `001.json` … `114.json`.

```json
{
  "sura": 1,
  "name_ar": "الفَاتِحة",
  "name_en": "Al-Fātiḥah",
  "revelation": "makki",
  "word_count": 29,
  "first_word_id": 1,
  "last_word_id": 29,
  "ayah_count": { "hafs": 7, "warsh": 7, "…": 7 },
  "words": [ … ]
}
```

### A word

```json
{
  "id": 11,
  "i": 11,
  "key": "1:مالك#1",
  "rasm": "مالك",
  "pointed": "مالك",
  "uthmani": "مَٰلِكِ",
  "simple": "مالك",
  "status": "rasm_variant",
  "aya":   { "hafs": 4, "shuba": 4, "warsh": 3, "qaloun": 3, "douri": 3, "sousi": 3, "bazzi": 4 },
  "forms": { "hafs": "مَٰلِكِ", "shuba": "مَٰلِكِ", "warsh": "مَلِكِ", "qaloun": "مَلِكِ",
             "douri": "مَلِكِ", "sousi": "مَّلِكِ", "bazzi": "مَلِكِ" }
}
```

| field | always | meaning |
|---|---|---|
| `id` | ✓ | running integer over the whole corpus, `1 … 77434` |
| `i` | ✓ | 1-based position within the sūrah |
| `key` | ✓ | `sūrah:pointed#occurrence` — content-derived, stable across rebuilds |
| `rasm` | ✓ | bare ʿUthmānic skeleton — undotted, unvowelled, no hamza, no dagger alif. The alignment key: every riwāyah sharing an `id` shares this exactly, except in the 62 `rasm_variant` and 198 `alif_variant` words |
| `pointed` | ✓ | the same skeleton with its dots, from the canonical spelling |
| `uthmani` | ✓ | canonical display form — Ḥafṣ's spelling where Ḥafṣ has the word, else the most common |
| `simple` | ✓ | plain spelling for search: no diacritics, superscript alif written out |
| `status` | ✓ | see below |
| `aya` | ✓ | āyah number **per riwāyah**; `0` means printed but unnumbered (the basmalah) |
| `forms` | ✓ | each riwāyah's own spelling; a riwāyah is absent from this map iff it lacks the word |
| `missing` | — | riwāyāt that lack the word |
| `waqf` | — | pause marks that trailed the word, per riwāyah |
| `boundary` | — | riwāyāt where the word was re-segmented, and why |
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
| `rasm_variant` | 62 | the riwāyāt disagree about the letters on the line |
| `word_boundary` | 12 | a source prints the word joined to its neighbour |
| `partial` | 5 | the word is absent from at least one riwāyah |

Each word gets the *strongest* label that applies, tested in this order: rasm,
ā, absence, boundary, dotting, vowelling. So a `dotting_variant` is guaranteed
to share one rasm across all seven, an `alif_variant` to share one skeleton once
every ā is spelled out, and a `diacritic_variant` shares its dots too.

`alif_variant` is the plene/defective ā: `هَٰرُوتَ` against `هَارُوتَ`, the same
word with the alef on the line in one hand and above it in the other. It is not
counted as the codices disagreeing, and the reason is empirical rather than
editorial: **all 198 of these words divide the seven riwāyāt along exactly one
line — `qaloun,warsh` against the other five — in both directions and without an
exception, while the 62 `rasm_variant` words divide them fourteen different
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
does not. 56 of the 62 are one skeleton with one letter more — `ٮرٮد`/`ٮرٮدد`
(يَرۡتَدَّ/يَرۡتَدِدۡ, 5:54), `ٮسٮهى`/`ٮسٮهٮه` (تَشۡتَهِي/تَشۡتَهِيهِ, 43:71) — and 6 are
one letter exchanged for another, `ولا`/`ڡلا` and `كلمٮ`/`كلمه`. The report
tables them separately.

`word_boundary` is deliberately ranked *below* the content comparison. It used
to outrank everything, which meant five of the six boundary events in the corpus
were reported as disagreements when in fact all seven riwāyāt read them
identically and one *source* had merely lost a space. The `boundary` field is
still set either way; `out/boundaries.csv` says which is which.

## `out/index.json`

The same sūrah headers with `words` omitted, plus corpus metadata and the
riwāyah registry (name, qāriʾ, counting tradition, āyah count, source file).
Small; read this to discover the corpus without loading it.

## `out/quran-words.json.gz`

Every sūrah and every word in one gzipped file (4.3 MB compressed, 36 MB raw).

```python
import gzip, json
data = json.load(gzip.open("out/quran-words.json.gz", "rt", encoding="utf-8"))
```

## `out/words.csv`

One row per canonical word — the whole index as a flat table.

```
word_id, sura, word_index, key, rasm, pointed, uthmani, simple, status,
present_count, aya_hafs … aya_bazzi, form_hafs … form_bazzi
```

## `out/variants.csv`

One row per riwāyah form that differs from the canonical spelling. Narrower
than `words.csv` when you only care about disagreement.

```
word_id, sura, word_index, riwaya, aya, canonical_uthmani, riwaya_uthmani,
same_rasm, status
```

## `out/fawasil.json`

Where each counting tradition ends its āyāt — the āyah boundaries as a layer
over the word index rather than a property of it.

```json
{ "systems": {
    "kufi":        { "riwayat": ["hafs", "shuba"],  "ayah_count": 6236, "ends": [7, 25, …] },
    "madani":      { "riwayat": ["warsh", "qaloun"], "ayah_count": 6214, "ends": [ … ] },
    "basri_douri": { "riwayat": ["douri"],           "ayah_count": 6217, "ends": [ … ] },
    "basri_sousi": { "riwayat": ["sousi"],           "ayah_count": 6218, "ends": [ … ] },
    "makki":       { "riwayat": ["bazzi"],           "ayah_count": 6220, "ends": [ … ] } } }
```

`ends[n]` is the `id` of the last word of āyah *n+1*. Five systems, not four:
Dūrī and Sūsī are both Baṣrī but differ at exactly one fāṣilah.

## `out/boundaries.csv`

One row per word-boundary event — never per word, because a boundary
disagreement is about the space *between* two words.

```
word_ids, sura, aya_hafs, kind, riwayat, riwayat_agree, forms
```

`riwayat_agree` is the column that matters: `1` means every riwāyah reads the
run identically once re-segmented, so the flag is a source that lost a space
rather than a muṣḥaf that really prints the words joined.

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
level, then gives the inventory, counting traditions, status distribution,
pairwise agreement, every rasm disagreement, every boundary event shown run by
run with each riwāyah's own text, every absent word, the fawāṣil systems and
how far apart they are, source-integrity cross-checks, and a per-sūrah density
table. `rasm-variants.md` lists every letter-level disagreement in full:
the 62 `rasm_variant` words first, then the 198 `alif_variant` ones.

## `out/compare.html`

A self-contained page for reading the comparison rather than querying it: pick
a sūrah, see every word with each riwāyah's spelling side by side, filter to
one kind of disagreement, and search. No server and no dependencies — open the
file.
