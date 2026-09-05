# quran-text

**The Qurʾān as text, in seven riwāyāt, as the printed muṣḥafs have it — with
one word numbering that means the same word in all seven.**

Every word of Ḥafṣ, Shuʿbah, Warsh, Qālūn, Dūrī, Sūsī and Bazzī, taken from the
King Fahd Complex's own digital releases, published as plain JSON with its
page, its line, its āyah, its pause marks, and a number shared across the
seven — so a translation, a grammar entry or an audio segment attached to a
word once can be read off any riwāyah.

## Just want the text?

Take **[`out/mushaf/hafs.json`](out/mushaf/hafs.json)** — Ḥafṣ, the riwāyah
nearly every app uses, as the King Fahd Complex prints it. `words` is the text,
`ayah_starts` says where each āyah begins, and that is all you need:

```python
import json
m = json.load(open("out/mushaf/hafs.json", encoding="utf-8"))
a = m["ayah_starts"]
k = m["suras"][2 - 1]["first_ayah"] + 255 - 1          # sūrah 2, āyah 255
print(" ".join(m["words"][a[k]:a[k + 1]]))
```

Pages, lines, juz and pause marks are in the same file; `.nested.json.gz`
beside it is the same text as sūrah → āyah → words. Agents: see
[`skills/quran-text/SKILL.md`](skills/quran-text/SKILL.md).

## Why this exists

Most Qurʾān datasets give you one riwāyah, Ḥafṣ, as āyāt. That is enough for a
reader and not enough for anything that has to *reason* about the text:

- **Seven riwāyāt, not one.** The others are not variants of Ḥafṣ; each is a
  printed muṣḥaf of its own, and here each is published on its own terms —
  its words, its spelling, its āyah division, its typesetting.
- **Words, not āyāt, are the unit.** The riwāyāt agree on the words almost
  everywhere and disagree on where āyāt end far more often, so the āyah is an
  attribute of a word here, not a container. That is what lets one number
  mean one word in all seven, and what lets data cross between them.
- **The āyah count belongs to the edition.** Dūrī and Sūsī are both First
  Madinan and differ at exactly one documented point; Bazzī counts one āyah
  no source yet explains. Each edition's counting system is *derived* from
  what it prints and checked against the classical systems, not assumed from
  the riwāyah, and every disagreement is named with the authority it follows.
- **Nothing is invented, and every departure is disclosed.** The text is the
  KFGQPC release's, hash for hash. Where this build re-spaces a word, where a
  line is reconstructed rather than read, where a count is unexplained — it
  is in the file, not in a footnote.

## What you get

Start with [`out/catalog.json`](out/catalog.json): the riwāyāt, the sūrahs,
and every file with the question it answers.

| you want to… | read |
|---|---|
| render one muṣḥaf — Warsh, on its own, with its pages, lines, āyāt and pause marks | [`out/mushaf/warsh.json`](out/mushaf/warsh.json), or its views `warsh.nested.json.gz` (sūrah → āyah → words) and `warsh.csv.gz` (one row per word) |
| use the same word across riwāyāt, attach a Ḥafṣ-keyed dataset, search by plain spelling | [`out/word-index.json`](out/word-index.json), `.csv` — every number with its text, its Ḥafṣ `{sura, ayah, pos}`, and each riwāyah's form |
| see only where the riwāyāt actually differ | [`out/differences.json`](out/differences.json), `.csv` — 277 words |
| convert an āyah reference: what is 2:255 in Warsh? | [`out/ayah-map.json`](out/ayah-map.json), `.csv` |
| know which counting system each edition follows, and the boundaries of all six | [`out/counting.json`](out/counting.json) |
| query it in SQL | `out/quran.sqlite.gz` — all seven plus the word index |
| verify what you downloaded | [`out/manifest.json`](out/manifest.json) — SHA-256 of every source and every file |
| read the findings | [`out/reports/`](out/reports/) — the comparison report, every letter-level variant, an interactive comparison page |

## Three lines of use

Print āyat al-Kursī as Warsh prints it — where it is āyāt 253–254 of sūrah 2:

```python
import json
m = json.load(open("out/mushaf/warsh.json", encoding="utf-8"))
a = m["ayah_starts"]; k = m["suras"][1]["first_ayah"] + 253 - 1   # sūrah 2, āyah 253 in Warsh's own count
print(" ".join(m["words"][a[k]:a[k + 2]]))
```

Find the same word in every riwāyah:

```python
idx = json.load(open("out/word-index.json", encoding="utf-8"))["words"]
w = idx[10]                      # number 11
print(w["hafs"], w["forms"])     # {'sura': 1, 'ayah': 4, 'pos': 1}  {'hafs': 'مَٰلِكِ', 'warsh': 'مَلِكِ', …}
```

Keep a reader on the same āyah when switching riwāyah:

```python
rows = json.load(open("out/ayah-map.json", encoding="utf-8"))["ayat"]
print(next(r for r in rows if (r["sura"], r["ayah"]) == (2, 255))["warsh"])
# {'sura': 2, 'ayah': 253, 'ayah_last': 254, 'relation': 'split'}
```

## The seven

| edition | qāriʾ | counting system | āyāt | words |
|---|---|---|---|---|
| Ḥafṣ, Shuʿbah | ʿĀṣim al-Kūfī | Kūfī | 6,236 | 77,432 |
| Warsh, Qālūn | Nāfiʿ al-Madanī | Last Madinan | 6,214 | 77,431 |
| Dūrī | Abū ʿAmr al-Baṣrī | First Madinan, following Abū Jaʿfar at 67:9 | 6,217 | 77,431 |
| Sūsī | Abū ʿAmr al-Baṣrī | First Madinan, following Shayba at 67:9 | 6,218 | 77,431 |
| Bazzī | Ibn Kathīr al-Makkī | Makkī, plus 78:40 ([open](docs/known-issues.md)) | 6,220 | 77,432 |

77,434 numbers in all. The seven agree on the letters of 99.5 % or more of
them; where they differ, [`out/differences.json`](out/differences.json) says
who reads what.

## Sources

All text is from King Fahd Glorious Qur'an Printing Complex (KFGQPC) releases,
listed with hashes in [`docs/sources.md`](docs/sources.md) and in
every file's `provenance`. Nothing was authored here; the pipeline only
re-segments and aligns what the packages contain. Redistribution of the text
remains subject to KFGQPC's terms. The counting-system boundaries under
`data/counting/` are from
[quranpedia/qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map),
MIT, at a pinned commit.

## Build it

No dependencies beyond the Python standard library (3.11+); the build is
reproducible offline.

```sh
python3 build.py                            # ~3 min, writes out/
python3 -m unittest discover -s tests        # 71 tests
```

## Documentation

| | |
|---|---|
| [`docs/design.md`](docs/design.md) | **why** — the text is flat, what a number means, the count belongs to the edition |
| [`docs/format.md`](docs/format.md) | **the spec** — the two normative files, shapes and rules |
| [`docs/files.md`](docs/files.md) | **the map of `out/`** — every file, its shape, what it answers |
| [`docs/method.md`](docs/method.md) | **how it is built** — parse, tokenise, normalise, align, verify |
| [`docs/sources.md`](docs/sources.md) | **what is in `data/`** |
| [`docs/known-issues.md`](docs/known-issues.md) | **what the sources contain**, and the open findings |
| [`docs/limitations.md`](docs/limitations.md) | **what this does not do** |
| [`docs/lessons.md`](docs/lessons.md) | **mistakes made building this** |
