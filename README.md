# quran-word-index

A **flat, word-level representation of the Uthmānī Qur'anic text** in which every
word carries one fixed number that means the same word across all seven riwāyāt
available in `data/`.

```
sūrah  →  [ word, word, word, … ]
```

Not `sūrah → āyah → word`. The āyah number is an *attribute* of a word, not a
level of nesting — because the editions disagree about where āyāt end far more
than they disagree about words, and **the count belongs to the printed edition,
not to the qirāʾah**:

| edition | counting system | āyāt | at the points of khilāf inside the system |
|---|---|---|---|
| Ḥafṣ, Shuʿbah | Kūfī | 6,236 | — |
| Warsh, Qālūn | Last Madinan | 6,214 | — |
| Dūrī | First Madinan | 6,217 | 67:9 not counted, following Abū Jaʿfar |
| Sūsī | First Madinan | 6,218 | 67:9 counted, following Shayba |
| Bazzī | Makkī | 6,220 | 78:40 counted, [not yet cited](docs/ISSUES.md) |

Each system is derived from what the edition prints, not assumed from the
riwāyah — the two Abū ʿAmr editions are First Madinan, not Baṣrī, and they
differ from each other at exactly one documented point. Nesting words under
āyāt would make a number mean a different word in each edition. Flattening to
the sūrah makes one number stable across all of them, and the āyah boundaries
become their own layer over the word index: [`out/counting.json`](out/counting.json).

## What makes a number mean one word

Words are identified by their **bare ʿUthmānic rasm** — undotted, unvowelled,
without hamza — because that is what the seven riwāyāt actually share. The
codices were written that way, and a single skeleton carries several readings
on purpose:

```
تَعۡمَلُونَ  ┐
           ├─►  ٮعملوں   one rasm, one number, two readings
يَعۡمَلُونَ  ┘
```

Everything a scribe added later to fix a reading — dots, hamza, vowels — is
exactly what the riwāyāt are allowed to disagree about, so none of it is part
of a word's identity. Each riwāyah's own spelling is kept in `forms`.

The numbering counts the **finest division** any muṣḥaf prints. Where one
muṣḥaf writes two words as one — `وَأَلَّوِ` at 72:16, `أَلَّن` at 73:20 — both
words keep a number and the joined word covers both; where a muṣḥaf does not
read a word — Bazzī's `مِن` at 9:101, Nāfiʿ's absent `هُوَ` at 57:24, `أَوۡ` at
40:26 — the number is simply missing from it. Nothing false is ever stated,
and each concept means one thing. Specified in
[`docs/MUSHAF-FORMAT.md`](docs/MUSHAF-FORMAT.md).

## What is here

Start with [`out/catalog.json`](out/catalog.json): it lists the riwāyāt, the
sūrahs, and every file below with the question it answers.

| you want to… | read |
|---|---|
| render one muṣḥaf — Warsh, on its own, with its pages, lines, āyāt and pause marks | `out/mushaf/warsh.json` (**normative**), or its views `warsh.nested.json.gz` (sūrah → āyah → words) and `warsh.csv.gz` (one row per word) |
| use the same word across riwāyāt, attach a Ḥafṣ-keyed dataset, search by plain spelling | `out/word-index.json`, `.csv` (**normative**) — every number with its text, its Ḥafṣ `{sura, ayah, pos}`, and each riwāyah's form |
| see only where the riwāyāt actually differ | `out/differences.json`, `.csv` |
| convert an āyah reference: what is 2:255 in Warsh? | `out/ayah-map.json`, `.csv` |
| know which counting system each edition follows, and the boundaries of all six | `out/counting.json` |
| query it in SQL | `out/quran.sqlite.gz` — all seven plus the word index |
| verify what you downloaded | `out/manifest.json` — SHA-256 of every source and every file |
| read the findings and how this was built | `out/reports/` — `COMPARISON.md`, `rasm-variants.md`, `compare.html`, `agreement-matrix.csv`, `variants.csv`, `resegmentation.csv` |

A muṣḥaf file is about half a megabyte gzipped, and a sūrah, a page or a juz
is one slice of its `words`, so there are no per-sūrah files. Each muṣḥaf
file names the KFGQPC release it came from, says which layers it carries and
why it lacks the rest, names the counting system its āyah division follows and
what it does at every point of khilāf, and lists every place this build
changed the source's own word spacing. The format is specified in
[`docs/MUSHAF-FORMAT.md`](docs/MUSHAF-FORMAT.md), every file in
[`docs/SCHEMA.md`](docs/SCHEMA.md), and the JSON Schemas are in
[`schema/`](schema/).

## Headline numbers

**77,434** numbers · **114** sūrahs · **7** riwāyāt.

| status | words | share | meaning |
|---|---|---|---|
| `identical` | 40,558 | 52.4% | one reading, one spelling, everywhere |
| `diacritic_variant` | 36,261 | 46.8% | same letters and dots — the vowelling differs |
| `dotting_variant` | 338 | 0.44% | one rasm, pointed two ways |
| `alif_variant` | 198 | 0.26% | one ā, on the line in one hand and above it in the other |
| `rasm_variant` | 60 | 0.08% | the riwāyāt disagree about the letters |
| `word_boundary` | 16 | 0.02% | a source joins the word to its neighbour, or a muṣḥaf really prints it joined |
| `partial` | 3 | 0.004% | the word is absent from some riwāyah |

So **615 words in 77,434** — one in 126 — are anything more than a difference
of vowelling, and only **60** of those are a letter one codex has and another
does not. The other 198 letter-level differences are an ā the two typesettings
place differently, on the line in one hand and above it in the other. They are
counted apart because the corpus says they belong apart: all 198 divide the
seven riwāyāt along one line, Warsh+Qālūn against the rest, in both directions
and without an exception, while the 60 divide them fourteen different ways.
Ḥadhf/ithbāt al-alif does vary between the codices of the amṣār — but not by
publisher. Rasm agreement between any two riwāyāt is **99.5 %–100 %**.

## A word

```json
{
 "number": 11, "sura": 1, "index": 11, "key": "1:مالك#1",
 "rasm": "ملك", "pointed": "مالك", "uthmani": "مَٰلِكِ", "simple": "مالك",
 "status": "dotting_variant",
 "hafs":  { "sura": 1, "ayah": 4, "pos": 1 },
 "ayah":  { "hafs": 4, "shuba": 4, "warsh": 3, "qaloun": 3,
            "douri": 3, "sousi": 3, "bazzi": 4 },
 "forms": { "hafs": "مَٰلِكِ", "shuba": "مَٰلِكِ", "warsh": "مَلِكِ", "qaloun": "مَلِكِ",
            "douri": "مَلِكِ", "sousi": "مَّلِكِ", "bazzi": "مَلِكِ" }
}
```

One number, one word. `ayah` records that this word is in āyah 4 for the Kūfī
and Makkī counts and āyah 3 for the Madanī ones. `forms` records that Ḥafṣ and
Shuʿbah read *māliki* where the rest read *maliki* — and `rasm` records that
the codex writes `ملك` either way. Ḥafṣ's ā is printed as a superscript alef,
which is precisely the scribal cue that it is *not* on the line: one skeleton,
deliberately written to carry both readings.

## Build it

No dependencies beyond the Python standard library (3.11+). The counting-system
boundaries are vendored under `data/counting/` from
[qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map) at a pinned
commit, so the build is reproducible offline.

```sh
python3 build.py                            # ~3 min, writes out/
python3 -m unittest discover -s tests        # 71 tests
```

## Read next

- [`docs/MUSHAF-FORMAT.md`](docs/MUSHAF-FORMAT.md) — the normative format: words by position, the numbering, the counting block
- [`docs/METHOD.md`](docs/METHOD.md) — how words are derived and aligned
- [`docs/SCHEMA.md`](docs/SCHEMA.md) — every file under `out/`, and every field
- [`docs/DATA-SOURCES.md`](docs/DATA-SOURCES.md) — what is in `data/`
- [`docs/ISSUES.md`](docs/ISSUES.md) — what the sources contain, and mistakes made building this
- [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) — what this does **not** do

## Provenance

All text is derived from King Fahd Glorious Qur'an Printing Complex (KFGQPC)
releases. Nothing was authored here; the pipeline only re-segments and aligns
what the packages contain. Redistribution of the text remains subject to
KFGQPC's terms. The counting-system data under `data/counting/` is from
quranpedia/qiraat-ayah-map, MIT.
