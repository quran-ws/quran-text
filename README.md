# quran-kalimah-index

A **flat, kalimah-level representation of the Uthmani Quranic text** in which every
kalimah carries one fixed ID that means the same kalimah across all seven riwayahs
available in `data/`.

```
surah  →  [ kalimah, kalimah, kalimah, … ]
```

Not `surah → ayah → kalimah`. The ayah number is an *attribute* of a kalimah, not a
level of nesting — because the riwayahs disagree about where ayahs end far more
than they disagree about kalimahs:

| counting tradition | ayahs | riwayahs |
|---|---|---|
| Kūfī | 6,236 | Ḥafṣ, Shuʿbah |
| Madanī | 6,214 | Warsh, Qālūn |
| Baṣrī (Dūrī) | 6,217 | Dūrī |
| Baṣrī (Sūsī) | 6,218 | Sūsī |
| Makkī | 6,220 | Bazzī |

Nesting kalimahs under ayahs would make an ID mean a different kalimah in each
riwayah. Flattening to the surah makes one ID stable across all of them, and
the ayah boundaries become their own layer over the kalimah index:
[`out/fasilahs.json`](out/fasilahs.json).

## What makes an ID mean one kalimah

Kalimahs are identified by their **bare Uthmani rasm** — undotted, unvowelled,
without hamza — because that is what the seven riwayahs actually share. The
mushafs were written that way, and a single skeleton carries several qira'ahs
on purpose:

```
تَعۡمَلُونَ  ┐
           ├─►  ٮعملوں   one rasm, one ID, two qira'ahs
يَعۡمَلُونَ  ┘
```

Everything a scribe added later to fix a qira'ah — dots, hamza, vowels — is
exactly what the riwayahs are allowed to disagree about, so none of it is part
of a kalimah's identity. Each riwayah's own spelling is kept in `forms`.

## What is here

| path | what |
|---|---|
| `out/surahs/001.json` … `114.json` | the index, one file per surah |
| `out/quran-kalimahs.json.gz` | the whole corpus in one file |
| `out/kalimahs.csv` | one row per canonical kalimah, with each riwayah's form |
| `out/variants.csv` | one row per riwayah form that differs from canonical |
| `out/conflicts.csv` / `.json` | only the kalimahs that disagree |
| `out/fasilahs.json` | where each counting tradition ends its ayahs |
| `out/boundaries.csv` | every kalimah-boundary disagreement, in full |
| `out/COMPARISON.md` | the cross-riwayah comparison report |
| `out/compare.html` | interactive kalimah-by-kalimah comparison — open it in a browser |

### One mushaf at a time

The tables above compare the seven. To take just one — Warsh, on its own, with
its own safhahs and pause marks — read `out/mushaf/`:

| path | what |
|---|---|
| `out/mushaf/warsh.json` | the whole mushaf, every kalimah carrying its global ID |
| `out/mushaf/warsh.min.json` | the same text and IDs, nothing else |
| `out/mushaf/surahs/warsh/002.json` | one surah, for a page that fetches what it shows |
| `out/mushaf/nested/warsh.json.gz` | surah → ayah → kalimah, for ayah-level consumers |
| `out/mushaf/warsh.csv.gz` | one row per kalimah |
| `out/quran.sqlite.gz` | all seven plus the spine, queryable in SQL |
| `out/mushaf/manifest.json` | every file and every source package, with SHA-256 |

Each file names the KFGQPC release it came from, says which layers it carries
and why it lacks the rest, and lists every place this build changed the source's
own kalimah spacing. Only `out/mushaf/<key>.json` is normative — the rest are
generated views of it. The format is specified in
[`docs/MUSHAF-FORMAT.md`](docs/MUSHAF-FORMAT.md) and checkable against
[`schema/mushaf-2.0.json`](schema/mushaf-2.0.json).
| `out/rasm-variants.md` | every harf-level disagreement, listed |
| `out/agreement-matrix.csv` | pairwise agreement between riwayahs |

## Headline numbers

**77,434** canonical kalimahs · **114** surahs · **7** riwayahs.

| status | kalimahs | share | meaning |
|---|---|---|---|
| `identical` | 40,558 | 52.4% | one qira'ah, one spelling, everywhere |
| `diacritic_variant` | 36,261 | 46.8% | same harfs and dots — the vowelling differs |
| `dotting_variant` | 338 | 0.44% | one rasm, pointed two ways |
| `alif_variant` | 198 | 0.26% | one ā, on the line in one hand and above it in the other |
| `rasm_variant` | 62 | 0.08% | the riwayahs disagree about the harfs |
| `kalimah_boundary` | 12 | 0.02% | a source joins the kalimah to its neighbour |
| `partial` | 5 | 0.01% | the kalimah is absent from some riwayah |

So **615 kalimahs in 77,434** — one in 126 — are anything more than a difference
of vowelling, and only **62** of those are a harf one mushaf has and another
does not. The other 198 harf-level differences are an ā the two typesettings
place differently, on the line in one hand and above it in the other. They are
counted apart because the corpus says they belong apart: all 198 divide the
seven riwayahs along one line, Warsh+Qālūn against the rest, in both directions
and without an exception, while the 62 divide them fourteen different ways.
Ḥadhf/ithbāt al-alif does vary between the mushafs of the amṣār — but not by
publisher. Rasm agreement between any two riwayahs is **99.5 %–100 %**.

## A kalimah

```json
{
 "id": 11, "i": 11, "key": "1:مالك#1",
 "rasm": "ملك", "pointed": "مالك", "uthmani": "مَٰلِكِ", "simple": "مالك",
 "status": "dotting_variant",
 "ayah":  { "hafs": 4, "shuba": 4, "warsh": 3, "qaloun": 3,
            "douri": 3, "sousi": 3, "bazzi": 4 },
 "forms": { "hafs": "مَٰلِكِ", "shuba": "مَٰلِكِ", "warsh": "مَلِكِ", "qaloun": "مَلِكِ",
            "douri": "مَلِكِ", "sousi": "مَّلِكِ", "bazzi": "مَلِكِ" }
}
```

One ID, one kalimah. `ayah` records that this kalimah is in ayah 4 for the Kūfī and
Makkī counts and ayah 3 for the Madanī and Baṣrī ones. `forms` records that
Ḥafṣ and Shuʿbah read *māliki* where the rest read *maliki* — and `rasm` records
that the mushaf writes `ملك` either way. Ḥafṣ's ā is printed as a superscript
alef, which is precisely the scribal cue that it is *not* on the line: one
skeleton, deliberately written to carry both qira'ahs.

## Build it

No dependencies beyond the Python standard library (3.11+).

```sh
python3 build.py                            # ~60 s, writes out/
python3 -m unittest discover -s tests        # 24 tests
```

## Read next

- [`docs/METHOD.md`](docs/METHOD.md) — how kalimahs are derived and aligned
- [`docs/SCHEMA.md`](docs/SCHEMA.md) — every field of every output
- [`docs/DATA-SOURCES.md`](docs/DATA-SOURCES.md) — what is in `data/`
- [`docs/ISSUES.md`](docs/ISSUES.md) — what the sources contain, and mistakes made building this
- [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) — what this does **not** do

## Provenance

All text is derived from King Fahd Glorious Qur'an Printing Complex (KFGQPC)
releases. Nothing was authored here; the pipeline only re-segments and aligns
what the packages contain. Redistribution of the text remains subject to
KFGQPC's terms.
