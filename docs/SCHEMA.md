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
  "key": "1:ملك#1",
  "rasm": "ملك",
  "uthmani": "مَٰلِكِ",
  "simple": "مالك",
  "status": "diacritic_variant",
  "aya":   { "hafs": 4, "shuba": 4, "warsh": 3, "qaloun": 3, "douri": 3, "sousi": 3, "bazzi": 4 },
  "forms": { "hafs": "مَٰلِكِ", "shuba": "مَٰلِكِ", "warsh": "مَلِكِ", "qaloun": "مَلِكِ",
             "douri": "مَلِكِ", "sousi": "مَّلِكِ", "bazzi": "مَلِكِ" }
}
```

| field | always | meaning |
|---|---|---|
| `id` | ✓ | running integer over the whole corpus, `1 … 77434` |
| `i` | ✓ | 1-based position within the sūrah |
| `key` | ✓ | `sūrah:rasm#occurrence` — content-derived, stable across rebuilds |
| `rasm` | ✓ | consonantal skeleton; the alignment key |
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

Optional fields are omitted when empty, so their presence is itself the signal.

### `status`

| value | meaning |
|---|---|
| `identical` | same reading and spelling in all seven, after notation folding |
| `diacritic_variant` | same rasm, different vowelling or marks |
| `rasm_variant` | the riwāyāt disagree about the letters themselves |
| `word_boundary` | at least one source printed the word joined to a neighbour |
| `partial` | the word is absent from at least one riwāyah |

Reported most-specific-first: `word_boundary` outranks `partial`, because a join
*causes* an apparent absence and reporting the effect would hide the cause.

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
word_id, sura, word_index, key, rasm, uthmani, simple, status, present_count,
aya_hafs … aya_bazzi, form_hafs … form_bazzi
```

## `out/variants.csv`

One row per riwāyah form that differs from the canonical spelling. Narrower
than `words.csv` when you only care about disagreement.

```
word_id, sura, word_index, riwaya, aya, canonical_uthmani, riwaya_uthmani,
same_rasm, status
```

## `out/conflicts.csv` and `out/conflicts.json`

Only the 985 words with `status` of `rasm_variant`, `word_boundary` or
`partial`. The CSV groups identical spellings so one row shows who reads what:

```
يَسۡتَهۡزِئُ [hafs,shuba,douri,sousi,bazzi]  ||  يَسْتَهْزِۓُ [warsh,qaloun]
```

## `out/agreement-matrix.csv`

Pairwise agreement, one row per pair of riwāyāt.

```
riwaya_a, riwaya_b, shared_words, same_spelling, same_reading, same_rasm
```

## `out/COMPARISON.md` and `out/rasm-variants.md`

The human-readable report: inventory, counting traditions, status distribution,
pairwise agreement, every boundary and partial word in full, source-integrity
cross-checks, and a per-sūrah variant density table. `rasm-variants.md` lists
all 968 letter-level disagreements.
