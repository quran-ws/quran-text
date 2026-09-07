# quran-text

**The Qurʾān as words.** Seven riwāyāt, exactly as the King Fahd Complex prints
them — and one number that means the same word in all seven.

**العربية** — سبع روايات من مصاحف مجمع الملك فهد، مقسَّمة كلمةً كلمة، ولكل كلمة
رقمٌ واحد يدل عليها في الروايات السبع جميعًا. النص نصُّ المجمع بحرفه، وكل ملف
يذكر إصداره وبصمته. ابدأ من `lib/` إن كنت تبني تطبيقًا، ومن `out/` إن كنت تعمل
على البيانات مباشرة.

---

### Word 425 — sūrah 2, āyah 28, sixth word

| | |
|---|---|
| Ḥafṣ · Shuʿbah · Dūrī · Sūsī | فَأَحۡيَٰكُمۡ |
| Bazzī | فَأَحۡيَٰكُمُۥ |
| Qālūn | فَأَحْيَاكُمْ |
| Warsh | فَأَحْيٜاكُمْ |

One number, four spellings. There are **77,434 numbers**; **277** read like
this and the rest are the same word everywhere. Attach a translation, a grammar
entry or an audio segment to a number once, and it is attached in all seven.

None of the KFGQPC packages contain word-level data — every one of them is
āyah-level ([`docs/sources.md`](docs/sources.md)). The words, and the number
that ties them together, are what this repository derives.

## Quick start

Ḥafṣ is bundled with every library; nothing to download, nothing to know about
riwāyāt.

```python
from quran_text import Mushaf

m = Mushaf.hafs()
m.ayah(2, 255).render(marks=True, ayah_marks=True)  # ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ ٱلۡحَيُّ ٱلۡقَيُّومُۚ …
m.page(3).lines                                     # a printed page, line by line
m.juz(30).ayahs
m.search("مالك يوم الدين")                          # → [Span(10, 13)]
```

The same six lines in Python, JavaScript, PHP, Dart, Swift and Kotlin — one
package each, no dependencies, tested against the same facts. Nothing is
published to PyPI or npm yet; install from the directory
(`pip install ./lib/python`) or copy it in. [`lib/`](lib/) has the full API.

Āyah numbers are the edition's own, and the libraries convert:

```python
warsh = Mushaf.load("out/mushaf/warsh.json")

m.ayah(2, 255).to(warsh)      # AyahMatch(2:253-254, split)
m.word(2, 255, 3).to(warsh)   # Word(5176, 'إِلَٰهَ')
```

## The seven

| riwāyah | qāriʾ | counting | āyāt | words |
|---|---|---|---|---|
| Ḥafṣ | ʿĀṣim al-Kūfī | Kūfī | 6,236 | 77,432 |
| Shuʿbah | ʿĀṣim al-Kūfī | Kūfī | 6,236 | 77,432 |
| Warsh | Nāfiʿ al-Madanī | Madanī (last) | 6,214 | 77,431 |
| Qālūn | Nāfiʿ al-Madanī | Madanī (last) | 6,214 | 77,431 |
| Dūrī | Abū ʿAmr al-Baṣrī | Madanī (first) | 6,217 | 77,431 |
| Sūsī | Abū ʿAmr al-Baṣrī | Madanī (first) | 6,218 | 77,431 |
| Bazzī | Ibn Kathīr al-Makkī | Makkī | 6,220 | 77,432 |

Each is a printed muṣḥaf on its own terms: 604 pages, 8,820 lines, its own
spelling, waqf marks and āyah count — not a font trick over Ḥafṣ. Juz is
recorded for all but Bazzī, whose source carries none.

Every file names the KFGQPC package it came from and its SHA-256, and lists in
the file itself each place the build departed from it:

```json
"hafs": { "text": { "package": "UthmanicHafs-v-3.0.zip",
                    "sha256": "cdec7341b7c684e7b8dd469c4b68988914d2784e924c7e6cbb9cb4b57c24f013" } }
```

## Where to go

| you are… | go to |
|---|---|
| building an app | [`lib/`](lib/) — Python, JS, PHP, Dart, Swift, Kotlin |
| after a file in a particular shape | [`service/`](service/) — a download page and HTTP API producing text, JSON, CSV, XML or SQL for any selection |
| working with the data | [`out/`](out/) — start at [`catalog.json`](out/catalog.json); [`docs/files.md`](docs/files.md) maps every file |
| an agent | [`skills/quran-text/SKILL.md`](skills/quran-text/SKILL.md) |

## Build

Python 3.11, no dependencies, reproducible offline:

```sh
python3 build.py                          # ~3 min, writes out/
python3 -m unittest discover -s tests
```

## Licence

**[CC BY 4.0](LICENSE)** — anywhere, commercially, no permission needed. One
condition: keep the link.

> quran-text by quran-ws — https://github.com/quran-ws/quran-text — CC BY 4.0

That covers the work done here: the word index and its numbering, the
alignment, the counting analysis, the code and the docs. It does **not** cover
the Qurʾānic text or the KFGQPC packages and fonts in `data/kfgqpc/` and
`out/fonts/`, which remain KFGQPC's under KFGQPC's terms.
[`NOTICE.md`](NOTICE.md) draws the line precisely.

## Documentation

[`design.md`](docs/design.md) why the format is shaped this way ·
[`format.md`](docs/format.md) the spec ·
[`files.md`](docs/files.md) every file in `out/` ·
[`method.md`](docs/method.md) how it is built ·
[`sources.md`](docs/sources.md) what it is built from ·
[`known-issues.md`](docs/known-issues.md) and
[`limitations.md`](docs/limitations.md) what to be careful with ·
[`verify-in-print.md`](docs/verify-in-print.md) what is still unknown, and where
in a printed muṣḥaf to look ·
[`launch.md`](docs/launch.md) what stands between this and a public release
