# quran-word-index

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

### One muṣḥaf at a time

The tables above compare the seven. To take just one — Warsh, on its own, with
its own pages and pause marks — read `out/mushaf/`:

| path | what |
|---|---|
| `out/mushaf/warsh.json` | the whole muṣḥaf, every word carrying its global ID |
| `out/mushaf/warsh.min.json` | the same text and IDs, nothing else |
| `out/mushaf/suras/warsh/002.json` | one sūrah, for a page that fetches what it shows |
| `out/mushaf/nested/warsh.json.gz` | sūrah → āyah → word, for verse-level consumers |
| `out/mushaf/warsh.csv.gz` | one row per word |
| `out/quran.sqlite.gz` | all seven plus the spine, queryable in SQL |
| `out/mushaf/manifest.json` | every file and every source package, with SHA-256 |

Each file names the KFGQPC release it came from, says which layers it carries
and why it lacks the rest, and lists every place this build changed the source's
own word spacing. Only `out/mushaf/<key>.json` is normative — the rest are
generated views of it. The format is specified in
[`docs/MUSHAF-FORMAT.md`](docs/MUSHAF-FORMAT.md) and checkable against
[`schema/mushaf-1.0.json`](schema/mushaf-1.0.json).
| `out/rasm-variants.md` | every letter-level disagreement, listed |
| `out/agreement-matrix.csv` | pairwise agreement between riwāyāt |

## Headline numbers

**77,434** canonical words · **114** sūrahs · **7** riwāyāt.

| status | words | share | meaning |
|---|---|---|---|
| `identical` | 40,558 | 52.4% | one reading, one spelling, everywhere |
| `diacritic_variant` | 36,261 | 46.8% | same letters and dots — the vowelling differs |
| `dotting_variant` | 338 | 0.44% | one rasm, pointed two ways |
| `alif_variant` | 198 | 0.26% | one ā, on the line in one hand and above it in the other |
| `rasm_variant` | 62 | 0.08% | the riwāyāt disagree about the letters |
| `word_boundary` | 12 | 0.02% | a source joins the word to its neighbour |
| `partial` | 5 | 0.01% | the word is absent from some riwāyah |

So **615 words in 77,434** — one in 126 — are anything more than a difference
of vowelling, and only **62** of those are a letter one codex has and another
does not. The other 198 letter-level differences are an ā the two typesettings
place differently, on the line in one hand and above it in the other. They are
counted apart because the corpus says they belong apart: all 198 divide the
seven riwāyāt along one line, Warsh+Qālūn against the rest, in both directions
and without an exception, while the 62 divide them fourteen different ways.
Ḥadhf/ithbāt al-alif does vary between the codices of the amṣār — but not by
publisher. Rasm agreement between any two riwāyāt is **99.5 %–100 %**.

## A word

```json
{
 "id": 11, "i": 11, "key": "1:مالك#1",
 "rasm": "ملك", "pointed": "مالك", "uthmani": "مَٰلِكِ", "simple": "مالك",
 "status": "dotting_variant",
 "aya":   { "hafs": 4, "shuba": 4, "warsh": 3, "qaloun": 3,
            "douri": 3, "sousi": 3, "bazzi": 4 },
 "forms": { "hafs": "مَٰلِكِ", "shuba": "مَٰلِكِ", "warsh": "مَلِكِ", "qaloun": "مَلِكِ",
            "douri": "مَلِكِ", "sousi": "مَّلِكِ", "bazzi": "مَلِكِ" }
}
```

One ID, one word. `aya` records that this word is in āyah 4 for the Kūfī and
Makkī counts and āyah 3 for the Madanī and Baṣrī ones. `forms` records that
Ḥafṣ and Shuʿbah read *māliki* where the rest read *maliki* — and `rasm` records
that the codex writes `ملك` either way. Ḥafṣ's ā is printed as a superscript
alef, which is precisely the scribal cue that it is *not* on the line: one
skeleton, deliberately written to carry both readings.

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

## Two HTML pages

They answer different questions and are built from the same data.

| page | question it answers |
|---|---|
| `out/compare.html` | *What does this word look like across the riwāyāt?* — the whole corpus, every word, searchable by sūrah |
| `out/review.html` | *Should I trust this index?* — the disagreements only, plus the evidence for judging them |

`out/review.html` is a self-contained review apparatus: the 615 words that are
more than a vowelling difference, each with every riwāyah's own spelling **and
its codepoints** (several 2026 KFGQPC codepoints are new enough that fonts may
have no glyph yet); the pairwise agreement matrix at rasm, reading and spelling
level; complete sample sūrahs showing the flat word model; the three source
defects with before/after text; and variant density across all 114 sūrahs.

```sh
python3 build_review.py      # writes out/review.html
```
