# quran-text

**The Qurʾān as text, in seven riwāyāt, exactly as the King Fahd Complex prints
them — with one word numbering that means the same word in all seven.**

Ḥafṣ, Shuʿbah, Warsh, Qālūn, Dūrī, Sūsī and Bazzī: every word with its page,
line, āyah, juz and waqf marks, published as plain JSON, and a number shared
across the seven so a translation, a grammar entry or an audio segment attached
to a word once can be read off any riwāyah.

## Why

Every Qurʾān database in use today has three gaps.

- **Nobody says which text it is.** Here every file names its KFGQPC release
  and SHA-256, and lists in the file itself every place the build departed
  from it. The text is the source's, hash for hash.
- **Nobody agrees on what a word is.** Split one āyah in three apps and you
  get three word counts. Here the word is defined once, reviewed against the
  classical sources, and numbered so the same number is the same word in
  all seven riwāyāt.
- **The riwāyāt are missing.** Outside Ḥafṣ they exist in software as a font
  trick or a scanned page. Here each riwāyah is text on its own terms: its own
  words, spelling, āyah count, pages and marks, aligned word by word with the
  others.

## Start here

| you are… | go to |
|---|---|
| building an app (Flutter, iOS, Android, web, PHP, Python) | [`lib/`](lib/) — one small library per platform, Ḥafṣ bundled: `Mushaf.hafs().ayah(2, 255).render(marks: true, ayahMarks: true)`, pages, lines, juz, search |
| after a file: one riwāyah, with the marks and format you want | [`service/`](service/) — the download service, an interactive page and an HTTP API that produce text, JSON, CSV, XML or SQL for any selection |
| working with the data directly | [`out/`](out/) — start with [`out/catalog.json`](out/catalog.json); [`docs/files.md`](docs/files.md) maps every file, [`docs/format.md`](docs/format.md) is the spec |
| an agent | [`skills/quran-text/SKILL.md`](skills/quran-text/SKILL.md) |

The one-minute version, in Python:

```python
import json
m = json.load(open("out/mushaf/hafs.json", encoding="utf-8"))
a = m["ayah_starts"]
k = m["surahs"][2 - 1]["first_ayah"] + 255 - 1          # sūrah 2, āyah 255
print(" ".join(m["words"][a[k]:a[k + 1]]))
```

## Sources and build

All text is from King Fahd Glorious Qur'an Printing Complex releases, listed
with hashes in [`docs/sources.md`](docs/sources.md); redistribution stays
subject to KFGQPC's terms. Nothing was authored here. The build needs only
Python 3.11 and is reproducible offline:

```sh
python3 build.py                              # ~3 min, writes out/
python3 -m unittest discover -s tests         # the build's tests
```

## Documentation

[`docs/design.md`](docs/design.md) why the format is shaped as it is ·
[`docs/format.md`](docs/format.md) the spec ·
[`docs/files.md`](docs/files.md) every file in `out/` ·
[`docs/method.md`](docs/method.md) how it is built ·
[`docs/known-issues.md`](docs/known-issues.md) and
[`docs/limitations.md`](docs/limitations.md) what to be careful with.
