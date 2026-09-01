# quran-index

A **flat, word-level representation of the Uthmānī Qur'anic text** in which every
word carries one fixed ID that means the same word across all seven riwāyāt
available in `data/`.

```
sūrah  →  [ word, word, word, … ]
```

Not `sūrah → āyah → word`. The āyah number is an *attribute* of a word, not a
level of nesting — because the riwāyāt disagree about where āyāt end far more
than they disagree about words:

| counting tradition | āyāt | riwāyāt |
|---|---|---|
| Kūfī | 6,236 | Ḥafṣ, Shuʿbah |
| Madanī | 6,214 | Warsh, Qālūn |
| Baṣrī (Dūrī) | 6,217 | Dūrī |
| Baṣrī (Sūsī) | 6,218 | Sūsī |
| Makkī | 6,220 | Bazzī |

Nesting words under āyāt would make an ID mean a different word in each
riwāyah. Flattening to the sūrah makes one ID stable across all of them, and
the āyah boundaries become their own layer over the word index:
[`out/fawasil.json`](out/fawasil.json).

## What makes an ID mean one word

Words are identified by their **bare ʿUthmānic rasm** — undotted, unvowelled,
without hamza — because that is what the seven riwāyāt actually share. The
codices were written that way, and a single skeleton carries several readings
on purpose:

```
تَعۡمَلُونَ  ┐
           ├─►  ٮعملوں   one rasm, one ID, two readings
يَعۡمَلُونَ  ┘
```

Everything a scribe added later to fix a reading — dots, hamza, vowels — is
exactly what the riwāyāt are allowed to disagree about, so none of it is part
of a word's identity. Each riwāyah's own spelling is kept in `forms`.

## What is here

| path | what |
|---|---|
| `out/suras/001.json` … `114.json` | the index, one file per sūrah |
| `out/quran-words.json.gz` | the whole corpus in one file |
| `out/words.csv` | one row per canonical word, with each riwāyah's form |
| `out/variants.csv` | one row per riwāyah form that differs from canonical |
| `out/conflicts.csv` / `.json` | only the words that disagree |
| `out/fawasil.json` | where each counting tradition ends its āyāt |
| `out/boundaries.csv` | every word-boundary disagreement, in full |
| `out/COMPARISON.md` | the cross-riwāyah comparison report |
| `out/compare.html` | interactive word-by-word comparison — open it in a browser |
| `out/rasm-variants.md` | all 232 letter-level disagreements, listed |
| `out/agreement-matrix.csv` | pairwise agreement between riwāyāt |

## Headline numbers

**77,434** canonical words · **114** sūrahs · **7** riwāyāt.

| status | words | share | meaning |
|---|---|---|---|
| `identical` | 40,558 | 52.4% | one reading, one spelling, everywhere |
| `diacritic_variant` | 36,458 | 47.1% | same letters and dots — the vowelling differs |
| `dotting_variant` | 169 | 0.22% | one rasm, pointed two ways |
| `rasm_variant` | 232 | 0.30% | the codices disagree about the letters |
| `word_boundary` | 12 | 0.02% | a source joins the word to its neighbour |
| `partial` | 5 | 0.01% | the word is absent from some riwāyah |

So **418 words in 77,434** — one in 185 — are anything more than a difference
of vowelling. Rasm agreement between any two riwāyāt is **99.5 %–100 %**.

## A word

```json
{
 "id": 11, "i": 11, "key": "1:مالك#1",
 "rasm": "مالك", "pointed": "مالك", "uthmani": "مَٰلِكِ", "simple": "مالك",
 "status": "rasm_variant",
 "aya":   { "hafs": 4, "shuba": 4, "warsh": 3, "qaloun": 3,
            "douri": 3, "sousi": 3, "bazzi": 4 },
 "forms": { "hafs": "مَٰلِكِ", "shuba": "مَٰلِكِ", "warsh": "مَلِكِ", "qaloun": "مَلِكِ",
            "douri": "مَلِكِ", "sousi": "مَّلِكِ", "bazzi": "مَلِكِ" }
}
```

One ID, one word. `aya` records that this word is in āyah 4 for the Kūfī and
Makkī counts and āyah 3 for the Madanī and Baṣrī ones. `forms` records that
Ḥafṣ and Shuʿbah read *māliki* where the rest read *maliki* — and because that
ā is written on the line in one and absent in the other, it is a difference in
the codex, not merely in the vowelling.

## Build it

No dependencies beyond the Python standard library (3.11+).

```sh
python3 build.py                            # ~60 s, writes out/
python3 -m unittest discover -s tests        # 24 tests
```

## Read next

- [`docs/METHOD.md`](docs/METHOD.md) — how words are derived and aligned
- [`docs/SCHEMA.md`](docs/SCHEMA.md) — every field of every output
- [`docs/DATA-SOURCES.md`](docs/DATA-SOURCES.md) — what is in `data/`
- [`docs/ISSUES.md`](docs/ISSUES.md) — what the sources contain, and mistakes made building this
- [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) — what this does **not** do

## Provenance

All text is derived from King Fahd Glorious Qur'an Printing Complex (KFGQPC)
releases. Nothing was authored here; the pipeline only re-segments and aligns
what the packages contain. Redistribution of the text remains subject to
KFGQPC's terms.
