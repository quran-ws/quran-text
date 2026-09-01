# Output schema

Everything is written to `out/` by `python3 build.py`. All text is UTF-8, NFC,
with no BOM.

## `out/surahs/NNN.json` — the index

One file per surah, `001.json` … `114.json`.

```json
{
  "surah": 1,
  "name_ar": "الفَاتِحة",
  "name_en": "Al-Fātiḥah",
  "revelation": "makki",
  "kalimah_count": 29,
  "first_kalimah_id": 1,
  "last_kalimah_id": 29,
  "ayah_count": { "hafs": 7, "warsh": 7, "…": 7 },
  "kalimahs": [ … ]
}
```

### A kalimah

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
  "ayah":   { "hafs": 4, "shuba": 4, "warsh": 3, "qaloun": 3, "douri": 3, "sousi": 3, "bazzi": 4 },
  "forms": { "hafs": "مَٰلِكِ", "shuba": "مَٰلِكِ", "warsh": "مَلِكِ", "qaloun": "مَلِكِ",
             "douri": "مَلِكِ", "sousi": "مَّلِكِ", "bazzi": "مَلِكِ" }
}
```

| field | always | meaning |
|---|---|---|
| `id` | ✓ | running integer over the whole corpus, `1 … 77434` |
| `i` | ✓ | 1-based position within the surah |
| `key` | ✓ | `surah:pointed#occurrence` — content-derived, stable across rebuilds |
| `rasm` | ✓ | bare Uthmani skeleton — undotted, unvowelled, no hamza, no dagger alif. The alignment key: every riwayah sharing an `id` shares this exactly, except in the 62 `rasm_variant` and 198 `alif_variant` kalimahs |
| `pointed` | ✓ | the same skeleton with its dots, from the canonical spelling |
| `uthmani` | ✓ | canonical display form — Ḥafṣ's spelling where Ḥafṣ has the kalimah, else the most common |
| `simple` | ✓ | plain spelling for search: no diacritics, superscript alif written out |
| `status` | ✓ | see below |
| `ayah` | ✓ | ayah number **per riwayah**; `0` means printed but unnumbered (the basmalah) |
| `forms` | ✓ | each riwayah's own spelling; a riwayah is absent from this map iff it lacks the kalimah |
| `missing` | — | riwayahs that lack the kalimah |
| `waqf` | — | pause marks that trailed the kalimah, per riwayah |
| `boundary` | — | riwayahs where the kalimah was re-segmented, and why |
| `hizb` | — | riwayahs marking a rub al-hizb `۞` before this kalimah |
| `sajdah` | — | riwayahs marking a sajdah `۩` on this kalimah |

| `groups` | — | the distinct spellings, each with the riwayahs using it; present only when they are not all the same |

Optional fields are omitted when empty, so their presence is itself the signal.

`forms` and `groups` say the same thing two ways. `forms` answers "how does
Warsh spell this?" in one lookup; `groups` answers "who reads what?" without a
scan, and its mere presence means the riwayahs part company here.

> **If Warsh, Qālūn or Sūsī look empty**, that is your font, not the data —
> their v3.0 documents use Arabic Extended-B codepoints (`U+0870`–`U+0882`) that
> few fonts can draw. See `docs/LIMITATIONS.md`.

### `status`

| value | kalimahs | meaning |
|---|---|---|
| `identical` | 40,558 | same qira'ah and spelling in all seven, after notation folding |
| `diacritic_variant` | 36,261 | same harfs *and* dots — the vowelling differs |
| `dotting_variant` | 338 | one rasm, pointed differently: `تَعۡمَلُونَ` against `يَعۡمَلُونَ` |
| `alif_variant` | 198 | one skeleton once every ā is spelled out; the hands disagree about where the ā was written |
| `rasm_variant` | 62 | the riwayahs disagree about the harfs on the line |
| `kalimah_boundary` | 12 | a source prints the kalimah joined to its neighbour |
| `partial` | 5 | the kalimah is absent from at least one riwayah |

Each kalimah gets the *strongest* label that applies, tested in this order: rasm,
ā, absence, boundary, dotting, vowelling. So a `dotting_variant` is guaranteed
to share one rasm across all seven, an `alif_variant` to share one skeleton once
every ā is spelled out, and a `diacritic_variant` shares its dots too.

`alif_variant` is the plene/defective ā: `هَٰرُوتَ` against `هَارُوتَ`, the same
kalimah with the alef on the line in one hand and above it in the other. It is not
counted as the mushafs disagreeing, and the reason is empirical rather than
editorial: **all 198 of these kalimahs divide the seven riwayahs along exactly one
line — `qaloun,warsh` against the other five — in both directions and without an
exception, while the 62 `rasm_variant` kalimahs divide them fourteen different
ways.** Ḥadhf and ithbāt al-alif do vary between the mushafs of the amṣār, but
they do not put Makkah with Madinah 198 times out of 198; a publisher's house
style does. `validate.check_alif_splits` asserts the one-partition fact, so a
future package that broke it would show up in the report's *Checks* section.

The distinction stays in `rasm` all the same, because within any one mushaf it
is that mushaf's own ḥadhf, carried consistently — Ḥafṣ writes قال plene 412
times and defective 4 — and 175 of the 198 show the identical split at every
occurrence of the kalimah. `COMPARISON.md` lists them under *The ā on the line or
above it*.

`rasm_variant` is the residue: a harf one mushaf has on the line and another
does not. 56 of the 62 are one skeleton with one harf more — `ٮرٮد`/`ٮرٮدد`
(يَرۡتَدَّ/يَرۡتَدِدۡ, 5:54), `ٮسٮهى`/`ٮسٮهٮه` (تَشۡتَهِي/تَشۡتَهِيهِ, 43:71) — and 6 are
one harf exchanged for another, `ولا`/`ڡلا` and `كلمٮ`/`كلمه`. The report
tables them separately.

`kalimah_boundary` is deliberately ranked *below* the content comparison. It used
to outrank everything, which meant five of the six boundary events in the corpus
were reported as disagreements when in fact all seven riwayahs read them
identically and one *source* had merely lost a space. The `boundary` field is
still set either way; `out/boundaries.csv` says which is which.

## `out/index.json`

The same surah headers with `kalimahs` omitted, plus corpus metadata and the
riwayah registry (name, qari, counting tradition, ayah count, source file).
Small; read this to discover the corpus without loading it.

## `out/quran-kalimahs.json.gz`

Every surah and every kalimah in one gzipped file (4.3 MB compressed, 36 MB raw).

```python
import gzip, json
data = json.load(gzip.open("out/quran-kalimahs.json.gz", "rt", encoding="utf-8"))
```

## `out/kalimahs.csv`

One row per canonical kalimah — the whole index as a flat table.

```
kalimah_id, surah, kalimah_index, key, rasm, pointed, uthmani, simple, status,
present_count, ayah_hafs … ayah_bazzi, form_hafs … form_bazzi
```

## `out/variants.csv`

One row per riwayah form that differs from the canonical spelling. Narrower
than `kalimahs.csv` when you only care about disagreement.

```
kalimah_id, surah, kalimah_index, riwayah, ayah, canonical_uthmani, riwayah_uthmani,
same_rasm, status
```

## `out/fasilahs.json`

Where each counting tradition ends its ayahs — the ayah boundaries as a layer
over the kalimah index rather than a property of it.

```json
{ "systems": {
    "hafs+shuba":   { "mushaf": ["hafs", "shuba"],   "ayah_count": 6236, "ends": [4, 8, …] },
    "bazzi":        { "mushaf": ["bazzi"],           "ayah_count": 6220, "ends": [ … ] },
    "qaloun+warsh": { "mushaf": ["qaloun", "warsh"], "ayah_count": 6214, "ends": [ … ] },
    "douri":        { "mushaf": ["douri"],           "ayah_count": 6217, "ends": [ … ] },
    "sousi":        { "mushaf": ["sousi"],           "ayah_count": 6218, "ends": [ … ] } } }
```

A system is keyed and named by the mushaf(s) that use it, never by a counting
tradition, and the member list is `mushaf` for the same reason: the fasilahs
belong to the printed mushaf rather than to the qira'ah. See `build.fasilahs`.

`ends[n]` is the `id` of the last kalimah of ayah *n+1*. Five systems, not four:
Dūrī and Sūsī are both Baṣrī but differ at exactly one fasilah.

## `out/boundaries.csv`

One row per kalimah-boundary event — never per kalimah, because a boundary
disagreement is about the space *between* two kalimahs.

```
kalimah_ids, surah, ayah_hafs, kind, riwayahs, riwayahs_agree, forms
```

`riwayahs_agree` is the column that matters: `1` means every riwayah reads the
run identically once re-segmented, so the flag is a source that lost a space
rather than a mushaf that really prints the kalimahs joined.

## `out/conflicts.csv` and `out/conflicts.json`

Only the 277 kalimahs with `status` of `rasm_variant`, `alif_variant`,
`kalimah_boundary` or `partial`. The CSV groups identical spellings so one row shows who reads what:

```
قُلۡ [hafs,shuba,warsh,qaloun,douri,sousi]  ||  قَالَ [bazzi]
```

## `out/agreement-matrix.csv`

Pairwise agreement, one row per pair of riwayahs.

```
riwayah_a, riwayah_b, shared_kalimahs, same_spelling, same_qiraah, same_pointed,
same_rasm
```

## `out/COMPARISON.md` and `out/rasm-variants.md`

The human-readable report. It opens by stating what is being compared at each
level, then gives the inventory, counting traditions, status distribution,
pairwise agreement, every rasm disagreement, every boundary event shown run by
run with each riwayah's own text, every absent kalimah, the fasilahs systems and
how far apart they are, source-integrity cross-checks, and a per-surah density
table. `rasm-variants.md` lists every harf-level disagreement in full:
the 62 `rasm_variant` kalimahs first, then the 198 `alif_variant` ones.

## `out/mushaf/`

Each mushaf on its own, with every kalimah carrying the same global `id` used here.
Specified separately in [`MUSHAF-FORMAT.md`](MUSHAF-FORMAT.md), with a JSON
Schema in `schema/mushaf-2.0.json`.

The files above compare the seven mushafs; those publish one at a time, and add
what only makes sense for a single mushaf: the safhah each kalimah is printed on, the
line it falls on, its juz, and the pause marks in that mushaf's own convention.

## `out/compare.html`

A self-contained page for reading the comparison rather than querying it: pick
a surah, see every kalimah with each riwayah's spelling side by side, filter to
one kind of disagreement, and search. No server and no dependencies — open the
file.
