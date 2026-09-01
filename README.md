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
| Baṣrī | 6,217 | Dūrī, Sūsī |
| Makkī | 6,220 | Bazzī |

Nesting words under āyāt would make an ID mean a different word in each
riwāyah. Flattening to the sūrah makes one ID stable across all of them.

## What is here

| path | what |
|---|---|
| `out/suras/001.json` … `114.json` | the index, one file per sūrah |
| `out/quran-words.json.gz` | the whole corpus in one file |
| `out/words.csv` | one row per canonical word, with each riwāyah's form |
| `out/variants.csv` | one row per riwāyah form that differs from canonical |
| `out/conflicts.csv` / `.json` | only the words that disagree |
| `out/COMPARISON.md` | the cross-riwāyah comparison report |
| `out/rasm-variants.md` | all 968 letter-level disagreements, listed |
| `out/agreement-matrix.csv` | pairwise agreement between riwāyāt |

## Headline numbers

**77,434** canonical words · **114** sūrahs · **7** riwāyāt.

| status | words | share | meaning |
|---|---|---|---|
| `identical` | 32,704 | 42.2% | same reading and spelling everywhere |
| `diacritic_variant` | 43,745 | 56.5% | same letters, different vowelling |
| `rasm_variant` | 968 | 1.25% | the riwāyāt disagree about the letters |
| `word_boundary` | 12 | 0.02% | a source joins the word to its neighbour |
| `partial` | 5 | 0.01% | the word is absent from some riwāyah |

Rasm agreement between any two riwāyāt is **99.0 %–99.99 %**. The two pairs
that share a qāriʾ — Dūrī–Sūsī and Ḥafṣ–Shuʿbah — sit at the top of that range,
which is the result you would want to see if the pipeline is measuring
something real.

## A word

```json
{
 "id": 11, "i": 11, "key": "1:ملك#1",
 "rasm": "ملك", "uthmani": "مَٰلِكِ", "simple": "مالك",
 "status": "diacritic_variant",
 "aya":   { "hafs": 4, "shuba": 4, "warsh": 3, "qaloun": 3,
            "douri": 3, "sousi": 3, "bazzi": 4 },
 "forms": { "hafs": "مَٰلِكِ", "shuba": "مَٰلِكِ", "warsh": "مَلِكِ", "qaloun": "مَلِكِ",
            "douri": "مَلِكِ", "sousi": "مَّلِكِ", "bazzi": "مَلِكِ" }
}
```

One ID, one word. `aya` records that this word is in āyah 4 for the Kūfī and
Makkī counts and āyah 3 for the Madanī and Baṣrī ones. `forms` records that
Ḥafṣ and Shuʿbah read *māliki* where the rest read *maliki*.

## Build it

No dependencies beyond the Python standard library (3.11+).

```sh
python3 build.py                            # ~75 s, writes out/
python3 -m unittest discover -s tests        # 16 tests
```

## Read next

- [`docs/METHOD.md`](docs/METHOD.md) — how words are derived and aligned
- [`docs/SCHEMA.md`](docs/SCHEMA.md) — every field of every output
- [`docs/DATA-SOURCES.md`](docs/DATA-SOURCES.md) — what is in `data/`
- [`docs/ISSUES.md`](docs/ISSUES.md) — defects found in the sources, and in the first attempts
- [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) — what this does **not** do

## Provenance

All text is derived from King Fahd Glorious Qur'an Printing Complex (KFGQPC)
releases. Nothing was authored here; the pipeline only re-segments and aligns
what the packages contain. Redistribution of the text remains subject to
KFGQPC's terms.
